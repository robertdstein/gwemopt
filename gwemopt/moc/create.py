import json
from pathlib import Path

from tqdm import tqdm

from gwemopt.moc.fov import Fov2Moc


def create_moc(telescope, params, output_path: Path):
    nside = params["nside"]

    print(
        f"No cached MOC found for {telescope} and niside={nside}. "
        f"Creating MOC and saving to {output_path}"
    )

    config_struct = params["config"][telescope]
    tesselation = config_struct["tesselation"]
    moc_struct = {}

    for ii, tess in tqdm(enumerate(tesselation), total=len(tesselation)):
        index, ra, dec = tess[0], tess[1], tess[2]
        if (telescope == "ZTF") and params["doUsePrimary"] and (index > 880):
            continue
        if (telescope == "ZTF") and params["doUseSecondary"] and (index < 1000):
            continue
        moc_struct[int(index)] = Fov2Moc(
            params, config_struct, telescope, ra, dec, nside
        )

    with open(output_path, "w") as f:
        json.dump(moc_struct, f)


# def create_moc(params, map_struct=None):
#
#     nside = params["nside"]
#
#     if params["doMinimalTiling"]:
#         prob = map_struct["prob"]
#
#         n, cl, dist_exp = (
#             params["powerlaw_n"],
#             params["powerlaw_cl"],
#             params["powerlaw_dist_exp"],
#         )
#         prob_scaled = copy.deepcopy(prob)
#         prob_sorted = np.sort(prob_scaled)[::-1]
#         prob_indexes = np.argsort(prob_scaled)[::-1]
#         prob_cumsum = np.cumsum(prob_sorted)
#         index = np.argmin(np.abs(prob_cumsum - cl)) + 1
#         prob_indexes = prob_indexes[: index + 1]
#
#     moc_structs = {}
#     for telescope in params["telescopes"]:
#         config_struct = params["config"][telescope]
#         tesselation = config_struct["tesselation"]
#         moc_struct = {}
#
#         if params["doMinimalTiling"] and (config_struct["FOV"] < 1.0):
#             idxs = hp.pixelfunc.ang2pix(
#                 map_struct["nside"], tesselation[:, 1], tesselation[:, 2], lonlat=True
#             )
#             isin = np.isin(idxs, prob_indexes)
#
#             idxs = [i for i, x in enumerate(isin) if x]
#             print("Keeping %d/%d tiles" % (len(idxs), len(tesselation)))
#             tesselation = tesselation[idxs, :]
#
#         if params["doParallel"]:
#             moclists = Parallel(n_jobs=params["Ncores"])(
#                 delayed(Fov2Moc)(
#                     params, config_struct, telescope, tess[1], tess[2], nside
#                 )
#                 for tess in tesselation
#             )
#             for ii, tess in enumerate(tesselation):
#                 index, ra, dec = tess[0], tess[1], tess[2]
#                 if (telescope == "ZTF") and params["doUsePrimary"] and (index > 880):
#                     continue
#                 if (telescope == "ZTF") and params["doUseSecondary"] and (index < 1000):
#                     continue
#                 moc_struct[index] = moclists[ii]
#         else:
#             for ii, tess in enumerate(tesselation):
#                 index, ra, dec = tess[0], tess[1], tess[2]
#                 if (telescope == "ZTF") and params["doUsePrimary"] and (index > 880):
#                     continue
#                 if (telescope == "ZTF") and params["doUseSecondary"] and (index < 1000):
#                     continue
#                 index = index.astype(int)
#                 moc_struct[index] = Fov2Moc(
#                     params, config_struct, telescope, ra, dec, nside
#                 )
#
#         if map_struct is not None:
#             ipix_keep = map_struct["ipix_keep"]
#         else:
#             ipix_keep = []
#         if params["doMinimalTiling"]:
#             moc_struct_new = copy.copy(moc_struct)
#             if params["tilesType"] == "galaxy":
#                 tile_probs = gwemopt.tiles.compute_tiles_map(
#                     params, moc_struct_new, prob, func="center", ipix_keep=ipix_keep
#                 )
#             else:
#                 tile_probs = gwemopt.tiles.compute_tiles_map(
#                     params, moc_struct_new, prob, func="np.sum(x)", ipix_keep=ipix_keep
#                 )
#
#             keys = moc_struct.keys()
#
#             sort_idx = np.argsort(tile_probs)[::-1]
#             csm = np.empty(len(tile_probs))
#             csm[sort_idx] = np.cumsum(tile_probs[sort_idx])
#             ipix_keep = np.where(csm <= cl)[0]
#
#             moc_struct = {}
#             cnt = 0
#             for ii, key in enumerate(keys):
#                 if ii in ipix_keep:
#                     moc_struct[key] = moc_struct_new[key]
#                     cnt = cnt + 1
#
#         moc_structs[telescope] = moc_struct
#
#         print(moc_struct.keys(), type(moc_struct), len(moc_struct.keys()))
#         raise
#
#     return moc_structs
