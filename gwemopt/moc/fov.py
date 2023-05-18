from gwemopt.chipgaps import get_decam_quadrant_ipix, get_ztf_quadrant_ipix
from gwemopt.moc.pixels import getCirclePixels, getSquarePixels


def Fov2Moc(params, config_struct, telescope, ra_pointing, dec_pointing, nside):
    """Return a MOC in fits file of a fov footprint.
    The MOC fov is displayed in real time in an Aladin plan.

    Input:
        ra--> right ascention of fov center [deg]
        dec --> declination of fov center [deg]
        fov_width --> fov width [deg]
        fov_height --> fov height [deg]
        nside --> healpix resolution; by default
    """

    moc_struct = {}

    if "rotation" in params:
        rotation = params["rotation"]
    else:
        rotation = None

    if config_struct["FOV_type"] == "square":
        ipix, ra, decs, area = getSquarePixels(
            ra_pointing, dec_pointing, config_struct["FOV"], nside, rotation=rotation
        )
    elif config_struct["FOV_type"] == "circle":
        ipix, ra, decs, area = getCirclePixels(
            ra_pointing, dec_pointing, config_struct["FOV"], nside, rotation=rotation
        )
    else:
        raise ValueError("FOV type not recognized")

    if params["doChipGaps"]:
        if telescope == "ZTF":
            ipixs = get_ztf_quadrant_ipix(nside, ra_pointing, dec_pointing)
            ipix = list({int(y) for x in ipixs for y in x})
        elif telescope == "DECam":
            ipixs = get_decam_quadrant_ipix(nside, ra_pointing, dec_pointing)
            ipix = list({int(y) for x in ipixs for y in x})
        else:
            raise ValueError("Chip gaps only available for DECam and ZTF")

    moc_struct["ra"] = float(ra_pointing)
    moc_struct["dec"] = float(dec_pointing)
    moc_struct["ipix"] = ipix
    # moc_struct["corners"] = radecs
    moc_struct["area"] = area

    moc_struct["moc"] = []

    # for x in moc_struct:
    #     print(x, type(moc_struct[x]))
    #
    # raise

    return moc_struct
