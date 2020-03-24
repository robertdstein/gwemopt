import os, sys
import numpy as np
import warnings

warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 48})
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt
plt.rcParams['xtick.labelsize']=48
plt.rcParams['ytick.labelsize']=48
from matplotlib.pyplot import cm

configDirectory = "/home/michael.coughlin/gwemopt/config"

events = ["S200105ae","S200213t","S200115j"]
gpstimes = [1262276684.0572,1265602259.327981,1263122607.742047]
skymaps = ["/home/michael.coughlin/gwemopt/data/S200105ae/LALInference.fits.gz","/home/michael.coughlin/gwemopt/data/S200213t/LALInference.fits.gz","/home/michael.coughlin/gwemopt/data/S200115j/LALInference.fits.gz"]

lightcurveFiles = ["/home/michael.coughlin/gwemopt/lightcurves/Bulla_mejdyn0.005_mejwind0.110_phi45_45.6.dat","/home/michael.coughlin/gwemopt/lightcurves/Bulla_mejdyn0.005_mejwind0.010_phi45_45.6.dat","Tophat","Tophat"]
modelTypes = ["file","file","Tophat","Tophat"]
mags = [-16.0,-16.0,-16.0,-16.0]
dmags = [0.0,0.0,0.0,0.5]
exposuretimes = np.arange(60,3660,60)

baseplotDir = "/home/michael.coughlin/gwemopt/output/efficiency"
condorDir = "/home/michael.coughlin/gwemopt/condor"

logDir = os.path.join(condorDir,'logs')
if not os.path.isdir(logDir):
    os.makedirs(logDir)

job_number = 0

fid = open(os.path.join(condorDir,'condor.dag'),'w')
for event,skymap,gpstime in zip(events,skymaps,gpstimes):
    for modelType,lightcurveFile,mag,dmag in zip(modelTypes,lightcurveFiles,mags,dmags):
        for exposuretime in exposuretimes:
            if modelType == "Tophat":
                lcurve = "%.1f_%.1f"%(mag,dmag)
            else:
                lcurve = lightcurveFile.split("/")[-1].replace(".dat","")
            outputDir = os.path.join(baseplotDir,event,lcurve,"%d"%(exposuretime))
            efficiency_file = os.path.join(outputDir,'efficiency.txt')
            if not os.path.isfile(efficiency_file):
                fid.write('JOB %d condor.sub\n'%(job_number))
                fid.write('RETRY %d 3\n'%(job_number))
                #fid.write('VARS %d jobNumber="%d" skymap="%s" gpstime="%.2f" lightcurveFile="%s" outputDir="%s" modelType="%s" mag="%.1f" dmag="%.1f" exposuretimes="%d,%d"\n'%(job_number,job_number,skymap,gpstime,lightcurveFile,outputDir,modelType,mag,dmag,exposuretime,exposuretime))
                fid.write('VARS %d jobNumber="%d" skymap="%s" gpstime="%.2f" lightcurveFile="%s" outputDir="%s" modelType="%s" mag="%.1f" dmag="%.1f" exposuretimes="%d"\n'%(job_number,job_number,skymap,gpstime,lightcurveFile,outputDir,modelType,mag,dmag,exposuretime))
                fid.write('\n\n')
                job_number = job_number + 1
fid.close()

fid = open(os.path.join(condorDir,'condor.sub'),'w')
fid.write('executable = /home/michael.coughlin/gwemopt/bin/gwemopt_run\n')
fid.write('output = logs/out.$(jobNumber)\n');
fid.write('error = logs/err.$(jobNumber)\n');
fid.write('arguments = --telescope ZTF --doSchedule --doSkymap --doPlots --skymap $(skymap) --gpstime $(gpstime) --doBalanceExposure --doTiles --doSingleExposure --filters g,r --powerlaw_cl 0.9 --doAlternatingFilters --doEfficiency --do3D --modelType $(modelType) --mag $(mag) --dmag $(dmag) --lightcurveFiles $(lightcurveFile) -o $(outputDir) --exposuretimes $(exposuretimes) --doUsePrimary -c %s\n' % (configDirectory)) 
#fid.write('arguments = --telescope ZTF --doSchedule --doSkymap --doPlots --skymap $(skymap) --gpstime $(gpstime) --doTiles --doSingleExposure --filters g --powerlaw_cl 0.9 --doAlternatingFilters --doEfficiency --do3D --modelType $(modelType) --mag $(mag) --dmag $(dmag) --lightcurveFiles $(lightcurveFile) -o $(outputDir) --exposuretimes $(exposuretimes) --doUsePrimary -c %s\n' % (configDirectory)) 
fid.write('requirements = OpSys == "LINUX"\n');
fid.write('request_memory = 4000\n');
fid.write('request_cpus = 1\n');
fid.write('accounting_group = ligo.dev.o2.burst.allsky.stamp\n');
fid.write('notification = never\n');
fid.write('getenv = true\n');
fid.write('log = /usr1/mcoughlin/gwemopt_efficiency.log\n')
fid.write('+MaxHours = 24\n');
fid.write('universe = vanilla\n');
fid.write('queue 1\n');
fid.close()

