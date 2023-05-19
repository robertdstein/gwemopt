import copy

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

from gwemopt.moc.pixels import get_patch
from gwemopt.plotting.style import CBAR_BOOL, UNIT, add_edges, add_sun_moon, cmap


def make_tile_plots(params, map_struct, tiles_structs, plot_sun_moon=True):
    """
    Function to plot the tiles
    """

    plot_name = params["outputDir"].joinpath("tiles.pdf")
    plt.figure()
    hp.mollview(map_struct["prob"], title="", unit=UNIT, cbar=CBAR_BOOL, cmap=cmap)
    ax = plt.gca()
    for telescope in tiles_structs:
        tiles_struct = tiles_structs[telescope]
        config_struct = params["config"][telescope]

        for i, index in enumerate(tiles_struct.keys()):
            patch = get_patch(
                fov_type=config_struct["FOV_type"],
                fov_deg=config_struct["FOV"],
                ra_deg=tiles_struct[index]["ra"],
                dec_deg=tiles_struct[index]["dec"],
            )

            if patch is not None:
                hp.projaxes.HpxMollweideAxes.add_patch(ax, patch)

    if plot_sun_moon:
        add_sun_moon(params)

    add_edges()
    print(f"Saving to {plot_name}")
    plt.savefig(plot_name, dpi=200)
    plt.close()
    # if params["doReferences"]:
    #     rot = (90, 0, 0)
    #     plot_name = params["outputDir"].joinpath("tiles_ref.pdf")
    #     plt.figure()
    #     hp.mollview(
    #         np.zeros(map_struct["prob"].shape),
    #         title="",
    #         unit=UNIT,
    #         cbar=CBAR_BOOL,
    #         cmap=cmap,
    #     )
    #     ax = plt.gca()
    #     for telescope in tiles_structs:
    #         config_struct = params["config"][telescope]
    #         tiles_struct = tiles_structs[telescope]
    #         if "reference_images" not in config_struct:
    #             continue
    #         for index in tiles_struct.keys():
    #             if index not in config_struct["reference_images"]:
    #                 continue
    #             if len(params["filters"]) == 1:
    #                 if (
    #                     not params["filters"][0]
    #                     in config_struct["reference_images"][index]
    #                 ):
    #                     continue
    #
    #             ipix, corners, patch = (
    #                 tiles_struct[index]["ipix"],
    #                 tiles_struct[index]["corners"],
    #                 tiles_struct[index]["patch"],
    #             )
    #             # hp.visufunc.projplot(corners[:,0], corners[:,1], 'k', lonlat = True)
    #             if not patch:
    #                 continue
    #             patch_cpy = copy.copy(patch)
    #             patch_cpy.axes = None
    #             patch_cpy.figure = None
    #             patch_cpy.set_transform(ax.transData)
    #             hp.projaxes.HpxMollweideAxes.add_patch(ax, patch_cpy)
    #             # tiles.plot()
    #     add_edges()
    #
    #     print(f"Saving to {plot_name}")
    #
    #     plt.savefig(plot_name, dpi=200)
    #     plt.close()
