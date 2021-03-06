# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:15:42 2018

@author: Artesia
"""

import pandas as pd
import pastastore as pst
import pastas as ps


def _get_metadata_from_obs(o, verbose=False):
    """internal method to get metadata in the right format for a pastas series.
    A pastas timeseries cannot handle the same metadata format as an observation
    object.

    Parameters
    ----------
    o : observations.Obs
        observation time series with metadata
    verbose : boolean, optional
        Print additional information to the screen (default is False).

    Returns
    -------
    meta : dictionary
        meta dictionary.

    """
    meta = dict()
    for attr_key in o._metadata:
        val = getattr(o, attr_key)
        if isinstance(val, (int, float, str, bool)):
            meta[attr_key] = val
        elif isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, (int, float, str, bool)):
                    meta[k] = v
                else:
                    if verbose:
                        print(
                            f'did not add {k} to metadata because datatype is {type(v)}')
        else:
            if verbose:
                print(
                    f'did not add {attr_key} to metadata because datatype is {type(val)}')
    return meta


def create_pastastore(oc, pstore, pstore_name='',
                      conn=pst.DictConnector("my_conn"),
                      add_metadata=True,
                      obs_column='stand_m_tov_nap',
                      kind='oseries',
                      verbose=False
                      ):
    """add observations to a new or existing pastastore

    Parameters
    ----------
    oc : observation.ObsCollection
        collection of observations
    pstore : pastastore.PastasProject, optional
        Existing pastastore, if None a new project is created
    pstore_name : str, optional
        Name of the pastastore only used if pstore is None
    conn : pastastore.connectors
        connector for database
    obs_column : str, optional
        Name of the column in the Obs dataframe to be used
    kind : str, optional
        The kind of series that is added to the pastas project
    add_metadata : boolean, optional
        If True metadata from the observations added to the project.
    verbose : boolean, optional
        Print additional information to the screen (default is False).

    Returns
    -------
    pstore : pastastore.PastasProject
        the pastas project with the series from the ObsCollection
    """
    if pstore is None:
        pstore = pst.PastaStore(pstore_name, connector=conn)

    for o in oc.obs.values:
        if verbose:
            print('add to pastastore -> {}'.format(o.name))

        if add_metadata:
            meta = _get_metadata_from_obs(o, verbose=verbose)
        else:
            meta = dict()

        if kind == 'oseries':
            pstore.conn.add_oseries(o[obs_column], o.name,
                                    metadata=meta)
        else:
            pstore.conn.add_stress(o[obs_column], o.name,
                                   kind, metadata=meta)

    return pstore


def create_pastas_project(oc, pr=None, project_name='',
                          obs_column='stand_m_tov_nap',
                          kind='oseries', add_metadata=True,
                          verbose=False):
    """add observations to a new or existing pastas project

    Parameters
    ----------
    oc : observation.ObsCollection
        collection of observations
    pr : pastas.project, optional
        Existing pastas project, if None a new project is created
    project_name : str, optional
        Name of the pastas project only used if pr is None
    obs_column : str, optional
        Name of the column in the Obs dataframe to be used
    kind : str, optional
        The kind of series that is added to the pastas project
    add_metadata : boolean, optional
        If True metadata from the observations added to the project.
    verbose : boolean, optional
        Print additional information to the screen (default is False).

    Returns
    -------
    pr : pastas.project
        the pastas project with the series from the ObsCollection
    """

    if pr is None:
        pr = ps.Project(project_name)

    for o in oc.obs.values:
        if verbose:
            print('add to pastas project -> {}'.format(o.name))

        if add_metadata:
            meta = _get_metadata_from_obs(o, verbose=verbose)
        else:
            meta = dict()

        series = ps.TimeSeries(o[obs_column], name=o.name, metadata=meta)
        pr.add_series(series, kind=kind)

    return pr


def read_project(pr, ObsClass, rename_dic={}):
    """Read pastas.Project into ObsCollection.

    Parameters
    ----------
    pr : pastas.Project
        Project to read
    ObsClass : Obs
        ObsClass to read data as, usually GroundwaterObs
    rename_dic : dict, optional
        rename columns in Project oseries dictionary, by default empty dict

    Returns
    -------
    list : list of Obs
        list of Obs containing oseries data

    """
    obs_list = []
    for index, row in pr.oseries.iterrows():
        metadata = row.to_dict()
        for key in rename_dic.keys():
            if key in metadata.keys():
                metadata[rename_dic[key]] = metadata.pop(key)

        s = pd.DataFrame(metadata.pop('series').series_original)
        s.rename(columns={index: 'stand_m_tov_nap'}, inplace=True)

        keys_o = ['name', 'x', 'y', 'locatie', 'filternr',
                  'metadata_available', 'maaiveld', 'meetpunt',
                  'bovenkant_filter', 'onderkant_filter']
        meta_o = {k: metadata[k] for k in keys_o if k in metadata}

        o = ObsClass(s, meta=metadata, **meta_o)
        obs_list.append(o)
    return obs_list
