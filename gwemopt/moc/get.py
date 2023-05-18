from gwemopt.moc.create import create_moc
from gwemopt.moc.load import load_moc
from gwemopt.paths import MOC_DEFAULT_CACHE, MOC_LOCAL_CACHE

DEFAULT_NSIDE = 256


def get_cache_path(telescope, params):
    """
    Get the path to the cached MOC file.

    Stores the MOC in a local cache if the nside is the default value,
    or otherwise in the data directory.

    :param telescope: telescope name
    :param params: parameters

    """

    name = f"{telescope}_{params['nside']}.json"

    if MOC_DEFAULT_CACHE.joinpath(name).exists():
        return MOC_DEFAULT_CACHE.joinpath(name)
    else:
        return MOC_LOCAL_CACHE.joinpath(name)


def get_moc(params, map_struct=None):
    """
    Function to get the MOC for each telescope.

    :param params: parameters
    :param map_struct: map structure
    :return: MOC dict
    """

    moc_structs = {}

    for telescope in params["telescopes"]:
        output_path = get_cache_path(telescope, params)

        if not output_path.exists():
            create_moc(telescope, params, output_path)

        moc_structs[telescope] = load_moc(output_path)

    return moc_structs
