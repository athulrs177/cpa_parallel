import xarray as xr
import numpy as np
from urocc import cpa
import dask
from dask import delayed 

def vectorized_cpa(response, predictor):
    """
    This is an extension to vectorize the cpa() defined for 1D numpy arrays (based on Gneiting and Walz (2022)).
    urocc() can be installed from: https://github.com/evwalz/urocc

    Parameters:
    - response (xarray.DataArray): An xarray DataArray representing the response variable (e.g., rainfall).
    - predictor (xarray.DataArray): An xarray DataArray representing the predictor variable.

    Returns:
    - result (xarray.DataArray): A new dataArray containing the computed rainfall CPA values.

    Note:
    Use this only in cases when parallel processing using packages other than Dask is preferred. 
    Otheriwse use cpa_multi().

    """
    # Create a custom ufunc
    def cpa_wrapper(response, predictor):
        # Call the custom function cpa
        return cpa(response, predictor)

    # Apply the custom ufunc using xarray's apply_ufunc
    result = xr.apply_ufunc(cpa_wrapper, response, predictor,
                            input_core_dims=[['time'], ['time']],
                            dask='parallelized', vectorize=True,
                            output_dtypes=[float])

    # Set the name of the result DataArray
    result.name = 'rainfall_cpa'

    return result
    
def cpa_multi(response, predictor, res_LatLon_chunks, pre_LatLon_chunks, scheduler='processes'):
    """
    Compute Coefficient of Predictive Ability (CPA) for 3D xarray data-arrays of the form ('time', lat, lon) used 
    in Rasheeda Satheesh et al. (2023).
    Uses parallel processing from Dask avoiding slow 4D nested for-loops.

    Note:
    This is an extension of cpa() defined for 1D numpy arrays (based on Gneiting and Walz (2022)) which is part of 
    the the urocc package. urocc can be installed from: https://github.com/evwalz/urocc 
    
    Parameters:
    - response (xarray.DataArray): The response dataset.
    - predictor (xarray.DataArray): The predictor dataset.
    - res_LatLon_chunks (tuple): Chunk sizes for latitude and longitude in the response dataset.
    - pre_LatLon_chunks (tuple): Chunk sizes for latitude and longitude in the predictor dataset.
    - scheduler (str, optional): Dask scheduler to use for parallel computation. Default is 'processes'.

    Returns:
    - result (xarray.DataArray): Resulting CPA array with dimensions ('lon_tar', 'lat_tar', 'lon_pre', 'lat_pre').
    """

    # Get dimensions of the input datasets
    res_dims = response.shape
    pre_dims = predictor.shape

    # Chunk the datasets based on the provided chunk sizes
    response = response.chunk({'lat': res_LatLon_chunks[0], 'lon': res_LatLon_chunks[1]})
    predictor = predictor.chunk({'lat': pre_LatLon_chunks[0], 'lon': pre_LatLon_chunks[1]})

    # Make timestamps identical to avoid xarray issues
    response['time'] = predictor['time']

    # Initialize an empty array for the result
    result = np.empty((res_dims[2], res_dims[1], pre_dims[2], pre_dims[1]), dtype=float)

    # Create an xarray DataArray for the result
    result = xr.DataArray(name='rainfall_cpa',
                         data=result,
                         dims=('lon_tar', 'lat_tar', 'lon_pre', 'lat_pre'),
                         coords={'lon_tar': response.lon.values, 'lat_tar': response.lat.values,
                                 'lon_pre': predictor.lon.values, 'lat_pre': predictor.lat.values}
                         )

    # Create index arrays for efficient assignment
    j = xr.DataArray(range(res_dims[1]), dims=['lat_tar'])
    i = xr.DataArray(range(res_dims[2]), dims=['lon_tar'])
    y = xr.DataArray(range(pre_dims[1]), dims=['lat_pre'])
    x = xr.DataArray(range(pre_dims[2]), dims=['lon_pre'])

    # Perform vectorized CPA computation and assign the result to the output array
    result[i, j, x, y] = vectorized_cpa(response[:, i, j], predictor[:, x, y]).compute(scheduler=scheduler)

    return result

