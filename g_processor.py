#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import struct
import xarray as xr
import os

# In[2]:


grids = {}

for i in ['lon','lat']:

    grid = np.array(pd.read_csv(f'grids/{i}grid.dat',header=None, delim_whitespace=True))
    flat_grid = grid.ravel()
    shaped_grid = flat_grid.reshape(360,120)
    grids[i] = shaped_grid


# In[3]:

h_cats=[0,0.26,0.71,1.46,2.61,4.23,6.39,9.10,12.39,16.24,20.62,25.49]

def process_piomas(year,variable):
    
    binary_dir = f'binaries/{variable}.H{year}'
    
    ############################################################
    
    # Read File
    
    with open(binary_dir, mode='rb') as file:
    
        fileContent = file.read()
        data = struct.unpack("f" * (len(fileContent)// 4), fileContent)
        
    ############################################################
    
    # Put it in a 3D array
        
        native_data = np.full((12,12,360,120),np.nan)

        for month in range(1,13):
            
            start = (month-1)*(360*120*12)
            end = month*(360*120*12)
            thickness_list = np.array(data[start:end])
            
            gridded = thickness_list.reshape(12,360,120)
            native_data[month-1,:,:,:] = gridded
            
          
    ############################################################
        
    # Output to NetCDF4
    
        time  = year + np.linspace(.5,11.5,12)
        ds = xr.Dataset( data_vars={variable:(['time','h','x','y'],native_data)},

                         coords =  {'lon':(['x','y'],grids['lon']),
                                    'lat':(['x','y'],grids['lat']),
                                    'thick':(['h'],h_cats),
                                    'year':(['time'],time) } )
        output_dir = f'output/'

        outputname = f'{output_dir}{variable}.{year}.nc'

        ds.to_netcdf(outputname+'.temp','w')
        
        return outputname
        

# In[4]:
variables=['gice']
for v in variables:
    for year in range(2016,2021):
        outputname=process_piomas(year,v)
        os.system(f'cdo -O -setgrid,piomas_static_scalar.nc {outputname}.temp {outputname}')
#    os.system('cdo mul -selvar,OceanMask piomas_static_scalar.nc -setgrid,piomas_static_scalar.nc -mergetime output/'+v+'*.nc' ' piomas.'+v+'.nc')
