# import os
from hydropandas import observation as obs
from hydropandas import obs_collection as oc
import numpy as np
import pytest

# import sys
# sys.path.insert(1, "..")

# TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
# sys.path.insert(0, PROJECT_DIR)
# os.chdir(TEST_DIR)

# %% DINO

dinozip = r'./tests/data/2019-Dino-test/dino.zip'


def test_observation_gwq():
    # single observation
    fname = r'./tests/data/2019-Dino-test/Grondwatersamenstellingen_Put/B52C0057.txt'
    ogq = obs.GroundwaterQualityObs.from_dino(fname, verbose=True)
    return ogq


def test_observation_wl():
    fname = r'./tests/data/2019-Dino-test/Peilschaal/P58A0001.csv'
    wl = obs.WaterlvlObs.from_dino(fname, verbose=True)
    return wl


def test_observation_gw():
    fname = r'./tests/data/2019-Dino-test/Grondwaterstanden_Put/B33F0080001_1.csv'
    gw = obs.GroundwaterObs.from_dino(fname=fname, verbose=True)
    return gw


def test_observation_dino_download():
    # download dino
    location = "B57F0077"
    filternr = 4.
    gw2 = obs.GroundwaterObs.from_dino(location=location,
                                       filternr=filternr,
                                       tmin="2000-01-01",
                                       tmax="2010-01-01", unit="NAP")
    return gw2


def test_observation_dino_download2():
    # download dino
    gw2 = obs.GroundwaterObs.from_dino(location="B57B0069", filternr=1.,
                                       tmin="2000-01-01",
                                       tmax="2030-01-01", unit="NAP")
    return gw2


def test_observation_dino_download3():
    # download dino data from pb without extra metadata. For this pb
    # io_dino.get_dino_piezometer_metadata() returns an empty list
    location = "B45G1147"
    filternr = 1.

    gw3 = obs.GroundwaterObs.from_dino(location=location,
                                       filternr=filternr,
                                       tmin="1900-01-01",
                                       tmax="1901-01-01", unit="NAP")
    return gw3


def test_obscollection_fieldlogger():
    # collection of observations
    fl = oc.ObsCollection.from_fieldlogger(
        r'./tests/data/2019-Dino-test/fieldlogger/locations.csv')
    return fl


def test_obscollection_from_list():
    dino_gw = oc.ObsCollection.from_dino(
        dirname=dinozip,
        ObsClass=obs.GroundwaterObs,
        subdir='Grondwaterstanden_Put',
        suffix='1.csv',
        keep_all_obs=True,
        verbose=False)
    obs_list = [o for o in dino_gw.obs.values]
    oc_list = oc.ObsCollection.from_list(obs_list)
    return oc_list


# read dino directories
def test_obscollection_dinozip_gw():
    # groundwater quantity
    dino_gw = oc.ObsCollection.from_dino(
        dirname=dinozip,
        ObsClass=obs.GroundwaterObs,
        subdir='Grondwaterstanden_Put',
        suffix='1.csv',
        keep_all_obs=False,
        verbose=False)
    return dino_gw


def test_obscollection_dinozip_gw_keep_all_obs():
    # do not delete empty dataframes
    dino_gw = oc.ObsCollection.from_dino(
        dirname=dinozip,
        ObsClass=obs.GroundwaterObs,
        subdir='Grondwaterstanden_Put',
        suffix='1.csv',
        keep_all_obs=True,
        verbose=False)
    return dino_gw


def test_obscollection_dinozip_wl():
    # surface water
    dino_ps = oc.ObsCollection.from_dino(
        dirname=dinozip,
        ObsClass=obs.WaterlvlObs,
        subdir='Peilschaal',
        suffix='.csv',
        verbose=True)
    return dino_ps


def test_obscollection_dinozip_gwq():
    # groundwater quality
    dino_gwq = oc.ObsCollection.from_dino(
        dirname=dinozip,
        ObsClass=obs.GroundwaterQualityObs,
        subdir='Grondwatersamenstellingen_Put',
        suffix='.txt',
        verbose=True)
    return dino_gwq


def test_obscollection_dino_download_extent():
    # download DINO from extent
    extent = [117850, 117980, 439550, 439700]  # Schoonhoven zoomed
    dino_gw_extent = oc.ObsCollection.from_dino(
        extent=extent, ObsClass=obs.GroundwaterObs, verbose=True)
    return dino_gw_extent

def test_obscollection_dino_download_extent_cache():
    # download DINO from extent
    extent = [117850, 117980, 439550, 439700]  # Schoonhoven zoomed
    dino_gw_extent = oc.ObsCollection.from_dino(
        extent=extent, ObsClass=obs.GroundwaterObs, cache=True, verbose=True)
    return dino_gw_extent


def test_obscollection_dino_download_bbox():
    # download DINO from bbox
    bbox = [117850, 439550, 117980, 439700]  # Schoonhoven zoomed
    bbox = np.array([191608.334, 409880.402, 193072.317, 411477.894])
    dino_gw_bbox = oc.ObsCollection.from_dino(
        bbox=bbox, ObsClass=obs.GroundwaterObs, verbose=True)
    return dino_gw_bbox


def test_obscollection_dino_download_bbox_only_metadata():
    # check if the keep_all_obs argument works
    bbox = [120110.8948323, 389471.92587313, 121213.23597266, 390551.29918915]
    dino_gw_bbox = oc.ObsCollection.from_dino(bbox=bbox, verbose=True)

    dino_gw_bbox_empty = oc.ObsCollection.from_dino(bbox=bbox,
                                                    keep_all_obs=False,
                                                    verbose=True)
    assert dino_gw_bbox_empty.empty

    return dino_gw_bbox


def test_obscollection_dino_download_bbox_empty():
    # download DINO from bbox
    bbox = [88596.63500000164, 407224.8449999988,
            89623.4149999991, 407804.27800000086]
    dino_gw_bbox = oc.ObsCollection.from_dino(
        bbox=bbox, ObsClass=obs.GroundwaterObs, verbose=True)
    return dino_gw_bbox


def test_obscollection_dino_download_bbox_do_not_keep_all_obs():
    bbox = [120110.8948323, 389471.92587313, 121213.23597266, 390551.29918915]
    dino_gw_bbox = oc.ObsCollection.from_dino(bbox=bbox, verbose=True)
    return dino_gw_bbox


# collection methods
def test_obscollection_to_fieldlogger():
    dino_gw = test_obscollection_dinozip_gw()
    fdf = dino_gw.to_fieldlogger(
        r'./tests/data/2019-Dino-test/fieldlogger/locations.csv', verbose=True)
    return fdf


# %% FEWS
def test_obscollection_fews_highmemory():
    fews_gw_prod = oc.ObsCollection.from_fews(
        r'./tests/data/2019-FEWS-test/WaalenBurg_201810-20190215_prod.zip',
        translate_dic={'locationId': 'locatie'},
        verbose=True,
        to_mnap=False,
        remove_nan=False,
        low_memory=False)
    return fews_gw_prod


def test_obscollection_fews_lowmemory():
    fews_gw_prod = oc.ObsCollection.from_fews(
        r'./tests/data/2019-FEWS-test/WaalenBurg_201810-20190215_prod.zip',
        verbose=True,
        locations=None,
        low_memory=True)
    return fews_gw_prod


def test_obscollection_fews_selection():
    fews_gw_prod = oc.ObsCollection.from_fews(
        r'./tests/data/2019-FEWS-test/WaalenBurg_201810-20190215_prod.zip',
        verbose=True,
        locations=("MPN-N-2",)
    )
    return fews_gw_prod


# %% WISKI
@pytest.mark.slow
def test_observation_wiskicsv_gw():
    wiski_gw = obs.GroundwaterObs.from_wiski(
        r"./tests/data/2019-WISKI-test/1016_PBF.csv",
        sep=r'\s+',
        header_sep=':',
        header_identifier=':',
        parse_dates={"datetime": [0, 1]},
        index_col=["datetime"],
        translate_dic={
            'name': 'Station Number',
            'x': 'GlobalX',
            'y': 'GlobalY'},
        verbose=True)

    return wiski_gw

@pytest.mark.slow
def test_obscollection_wiskizip_gw():
    wiski_col = oc.ObsCollection.from_wiski(
        r"./tests/data/2019-WISKI-test/1016_PBF.zip",
        translate_dic={
            'name': 'Station Number',
            'x': 'GlobalX',
            'y': 'GlobalY'},
        sep=r'\s+',
        header_sep=':',
        dayfirst=True,
        header_identifier=':',
        parse_dates={"datetime": [0, 1]},
        index_col=["datetime"],
        verbose=True)

    return wiski_col


# %% PASTAS PROJECTS AND PASTASTORE
@pytest.mark.skip(reason="needs installation pastastore")
def test_to_pastas_project():

    dino_gw = test_obscollection_dinozip_gw()
    pr = dino_gw.to_pastas_project(verbose=True)

    return pr

@pytest.mark.skip(reason="needs installation pastastore")
def test_to_pastastore():

    dino_gw = test_obscollection_dinozip_gw()
    pstore = dino_gw.to_pastastore(verbose=True)

    return pstore

@pytest.mark.skip(reason="needs installation pastastore")
def test_from_pastas_project():

    pr = test_to_pastas_project()
    pr_oc = oc.ObsCollection.from_pastas_project(pr)

    return pr_oc


# %% PYSTORE

def test_obscollection_to_pystore():
    obsc = test_obscollection_fews_lowmemory()
    obsc.to_pystore("test_pystore", "./tests/data/2019-Pystore-test",
                    groupby="locatie", overwrite=True)


def test_obscollection_from_pystore():
    obsc = oc.ObsCollection.from_pystore(
        "test_pystore", "./tests/data/2019-Pystore-test")
    return obsc


def test_obscollection_pystore_only_metadata():
    obsc = oc.ObsCollection.from_pystore("test_pystore",
                                         "./tests/data/2019-Pystore-test",
                                         read_series=False)
    return obsc


def test_obscollection_pystore_extent():
    obsc = oc.ObsCollection.from_pystore("test_pystore",
                                         "./tests/data/2019-Pystore-test",
                                         extent=[115534, 115539, 0, 10000000]
                                         )
    return obsc


def test_obscollection_pystore_item_names():
    obsc = oc.ObsCollection.from_pystore("test_pystore",
                                         "./tests/data/2019-Pystore-test",
                                         item_names=['MPN-N-2']
                                         )
    return obsc


def test_obs_from_pystore_item():
    import pystore
    pystore.set_path("./tests/data/2019-Pystore-test")
    store = pystore.store("test_pystore")
    coll = store.collection(store.collections[0])
    item = coll.item(list(coll.list_items())[0])
    o = obs.GroundwaterObs.from_pystore_item(item)
    return o


# %% KNMI
def test_knmi_obs_from_stn():
    return obs.KnmiObs.from_knmi(233, "RD", verbose=True)

def test_knmi_obs_from_stn_without_data_in_time_period():
    return obs.KnmiObs.from_knmi(441, "RD", startdate='2010-1-2')

def test_knmi_obs_from_xy():
    return obs.KnmiObs.from_nearest_xy(100000, 350000, "RD")


def test_knmi_obs_from_obs():
    pb = test_observation_gw()
    return obs.KnmiObs.from_obs(pb, "EV24", fill_missing_obs=False)

def test_knmi_collection_from_locations():
    obsc = test_obscollection_dino_download_extent_cache()
    oc_knmi = oc.ObsCollection.from_knmi(locations=obsc, 
                                         meteo_vars=["EV24", "RD"], 
                                         start=['2010', '2010'],
                                         end=['2015', '2015'],
                                         verbose=True, cache=True)
    return oc_knmi

def test_knmi_collection_from_stns():
    stns = [344, 260] #Rotterdam en de Bilt
    oc_knmi = oc.ObsCollection.from_knmi(stns=stns, 
                                         meteo_vars=["EV24", "RH"], 
                                         start=['2010', '2010'],
                                         end=['2015', '2015'],
                                         verbose=True)
    return oc_knmi


def test_knmi_collection_from_grid():
    #somewhere in Noord-Holland (near Castricum)
    xmid = np.array([104150., 104550.])
    ymid = np.array([510150., 510550.])
    oc_knmi = oc.ObsCollection.from_knmi(xmid=xmid, ymid=ymid, 
                                         meteo_vars=["RD"], 
                                         start=['2010', '2010'],
                                         end=['2015', '2015'],
                                         verbose=True)
    return oc_knmi

# %% WATERINFO

def test_waterinfo_from_dir():
    path = "./tests/data/waterinfo-test"
    wi = oc.ObsCollection.from_waterinfo(path)
    return wi


# %% MENYANTHES (still need a small menyanthes file to do the test)

# def test_obscollection_menyanthes():
#
#    fname = r'export_from_ADI.men'
#    obsc = oc.ObsCollection.from_menyanthes(fname, verbose=True)
#
#    return obsc



