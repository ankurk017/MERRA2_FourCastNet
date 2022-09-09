# Documentation: https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf

from pydap.client import open_url
from pydap.cas.urs import setup_session
import xarray as xr
import numpy as np
from datetime import datetime


username = "ankurk017"
password = "Jelly0311"


def get_dataset(opendap_url):
    session = setup_session(username, password, check_url=opendap_url)
    opendap_data = open_url(opendap_url, session=session)
    dataset = xr.open_dataset(xr.backends.PydapDataStore(opendap_data))
    return dataset


fourcastnet_lon = np.linspace(-90, 90, 720)
fourcastnet_lat = np.linspace(-180, 180, 1440)

timestamp = "2021082900"  # YYYYMMDDHH


dtime = datetime.strptime(timestamp, "%Y%m%d%H")


url_prefix1 = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/"
url_prefix2 = "https://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/"

surface_url = f"{url_prefix1}M2I1NXASM.5.12.4/{dtime.strftime('%Y/%m/')}MERRA2_401.inst1_2d_asm_Nx.{dtime.strftime('%Y%m%d')}.nc4"
UV_url =      f"{url_prefix2}M2I3NPASM.5.12.4/{dtime.strftime('%Y/%m/')}MERRA2_401.inst3_3d_asm_Np.{dtime.strftime('%Y%m%d')}.nc4"
H_url =       f"{url_prefix2}M2I6NPANA.5.12.4/{dtime.strftime('%Y/%m/')}MERRA2_401.inst6_3d_ana_Np.{dtime.strftime('%Y%m%d')}.nc4"
TCWV_url =    f"{url_prefix1}M2T1NXINT.5.12.4/{dtime.strftime('%Y/%m/')}MERRA2_401.tavg1_2d_int_Nx.{dtime.strftime('%Y%m%d')}.nc4"


# Surface | U10, V10, T2m, sp, mslp
sfc_dataset = get_dataset(surface_url).isel(time=0)
u10m = sfc_dataset["U10M"].interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
v10m = sfc_dataset["V10M"].interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
t2m = sfc_dataset["T2M"].interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
slp = sfc_dataset["SLP"].interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
### MSLP


# 1000 hPa, 850, 500 | U, V
UVTRH_dataset = get_dataset(UV_url).isel(time=0)
U = (
    UVTRH_dataset["U"]
    .interp(lev=[1000, 850, 500])
    .interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
)
V = (
    UVTRH_dataset["V"]
    .interp(lev=[1000, 850, 500])
    .interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
)

#  850 hPa, 500 hPa | T, RH
T = (
    UVTRH_dataset["T"]
    .interp(lev=[1000, 850])
    .interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
)
RH = (
    UVTRH_dataset["RH"]
    .interp(lev=[1000, 850])
    .interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
)

# 1000 hPa, 850 hPa, 500 hPa,  50 hPa | Z
H_dataset = get_dataset(H_url).isel(time=0)
H = (
    H_dataset["H"]
    .interp(lev=[1000, 850, 500])
    .interp(lon=fourcastnet_lon, lat=fourcastnet_lat)
)

# Integrated | TCWV (Total Column Water Vapor)
TCWV_dataset = get_dataset(TCWV_url).isel(time=0)
ITCWV = (
    TCWV_dataset["DQVDT_ANA"]
    + TCWV_dataset["DQVDT_CHM"]
    + TCWV_dataset["DQVDT_DYN"]
    + TCWV_dataset["DQVDT_MST"]
    + TCWV_dataset["DQVDT_PHY"]
    + TCWV_dataset["DQVDT_TRB"]
).interp(lon=fourcastnet_lon, lat=fourcastnet_lat)





