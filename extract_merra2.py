# Documentation of the variables: https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf

from pydap.client import open_url
from pydap.cas.urs import setup_session
import xarray as xr
import numpy as np
from datetime import datetime
import os
from src_utils.merra2 import (
    get_dataset,
    update_levels,
    get_merra_urls,
    extract_vars_from_url,
    interp_variables,
    var_to_h5,
)

username = "ankurk017"
password = os.environ["EDPSWD"]

fourcastnet_lat = np.linspace(-90, 90, 720)
fourcastnet_lon = np.linspace(-180, 180, 1440)

timestamp = "2021082900"  # YYYYMMDDHH
dtime = datetime.strptime(timestamp, "%Y%m%d%H")

surface_url, UV_url, H_url, TCWV_url = get_merra_urls(dtime)
session = setup_session(username, password, check_url=surface_url)

sfc_dataset, UVTRH_dataset, H_dataset, TCWV_dataset = extract_vars_from_url(
    session, surface_url, UV_url, H_url, TCWV_url
)
variables = interp_variables(
    fourcastnet_lon,
    fourcastnet_lat,
    sfc_dataset,
    UVTRH_dataset,
    H_dataset,
    TCWV_dataset,
)
var_to_h5(variables, output_filename="test.nc")


