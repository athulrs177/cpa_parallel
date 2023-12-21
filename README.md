# Python package to parallel compute CPA avoiding 4D nested loops
1) ```vectorized_cpa()```
   An extension to vectorize the ```cpa()``` part of ```uroc``` package defined for 1D numpy arrays (based on Gneiting and Walz (2022)).
   ```uroc``` can be installed from: https://github.com/evwalz/urocc

   Parameters:
   - response (xarray.DataArray): An xarray DataArray representing the response variable (e.g., rainfall).
   - predictor (xarray.DataArray): An xarray DataArray representing the predictor variable.

   Returns:
   - result (xarray.DataArray): A new dataArray containing the computed rainfall CPA values.

   Note:
   Use this function when you are building parallel processing architectures not using Dask. 
   If you just want to apply ```cpa()``` in your domain of analysis, just use ```cpa_multi()```.

2) ```cpa_multi()```
   Compute Coefficient of Predictive Ability (CPA) for 3D xarray data-arrays of the form ```('time', lat, lon)``` used 
   in Rasheeda Satheesh et al. (2023).
   Uses parallel processing from Dask avoiding slow 4D nested for-loops.

   Note:
   This is an extension of ```cpa()``` defined for 1D numpy arrays (based on Gneiting and Walz (2022)) which is part of 
   the the ```uroc``` package. ```uroc``` can be installed from: https://github.com/evwalz/urocc 
    
   Parameters:
   - response (xarray.DataArray): The response dataset.
   - predictor (xarray.DataArray): The predictor dataset.
   - res_LatLon_chunks (tuple): Chunk sizes for latitude and longitude in the response dataset.
   - pre_LatLon_chunks (tuple): Chunk sizes for latitude and longitude in the predictor dataset.
   - scheduler (str, optional): Dask scheduler to use for parallel computation. Default is 'processes'.

   Returns:
   - result (xarray.DataArray): Resulting CPA array with dimensions ('lon_tar', 'lat_tar', 'lon_pre', 'lat_pre'). 



