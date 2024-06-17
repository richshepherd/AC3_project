import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Define directories for the input data
HADCRUT5_DIR = "./HadCRUT5"
ERA5_DIR = "./ERA5"

def create_monthly_gif(input_files, var_name, output_gif, title):
    """
    Creates a GIF showing the monthly evolution of temperature data.

    Parameters:
        input_files (list): List of input NetCDF files.
        var_name (str): Variable name of the temperature data in the NetCDF files.
        output_gif (str): Path to save the output GIF.
        title (str): Title for the GIF.
    """
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.Robinson()})
    ims = []

    for file in input_files:
        print(f"Processing file: {file}")
        ds = xr.open_dataset(file)
        time = ds['time']
        temp = ds[var_name]

        # Check if the units attribute exists
        if 'units' in temp.attrs:
            units = temp.attrs['units']
        else:
            units = '°C'

        print(f"Temperature units: {units}")
        print(f"Temperature range: {temp.min().item()} to {temp.max().item()}")

        for t in range(temp.shape[0]):
            temp_data = temp.isel(time=t).values
            print(f"temp_data shape: {temp_data.shape}")  # Debug print

            if temp_data.ndim == 3:
                temp_data = temp_data[0, :, :]  # Ensure temp_data is 2D if it's 3D

            im = ax.imshow(temp_data, animated=True, cmap='coolwarm', vmin=temp.min().item(), vmax=temp.max().item(), transform=ccrs.PlateCarree())
            timestamp = pd.to_datetime(time.values[t]).strftime('%Y-%m')
            ims.append([im, ax.text(0.5, 1.05, timestamp, ha="center", va="bottom", transform=ax.transAxes)])

    # Add map features
    ax.coastlines(resolution='110m')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='none')
    ax.add_feature(cfeature.OCEAN)

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.05)
    cbar.set_label(f'Temperature ({units})')

    # Create and save the animation
    ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True)
    ani.save(output_gif, writer='imagemagick')
    plt.close()

def compute_winter_mean(input_files, var_name):
    """
    Computes the mean temperature for winter months (DJF) from the input files.

    Parameters:
        input_files (list): List of input NetCDF files.
        var_name (str): Variable name of the temperature data in the NetCDF files.

    Returns:
        years (list): List of years for which the winter mean is computed.
        winter_means (list): List of 2D arrays containing the mean winter temperatures.
        units (str): Units of the temperature data.
    """
    winter_means = []
    years = []

    for file in input_files:
        print(f"Processing file: {file}")
        ds = xr.open_dataset(file)
        time = ds['time']
        temp = ds[var_name]

        # Check if the units attribute exists
        if 'units' in temp.attrs:
            units = temp.attrs['units']
        else:
            units = '°C'

        print(f"Temperature units before conversion: {units}")
        print(f"Temperature range before conversion: {temp.min().item()} to {temp.max().item()}")

        # Convert time to pandas datetime
        time = pd.to_datetime(time.values)
        temp['time'] = ('time', time)

        # Select winter months (December, January, February)
        winter_months = temp.sel(time=(time.month == 12) | (time.month == 1) | (time.month == 2))
        
        # Ensure there are winter months in the dataset
        if not winter_months.time.size:
            continue

        # Compute mean temperature for each winter season (DJF)
        winter_mean = winter_months.groupby('time.year').mean(dim='time', skipna=True)
        
        # Convert to 2D arrays
        for year in winter_mean['year'].values:
            mean_temp = winter_mean.sel(year=year).values
            print(f"mean_temp shape: {mean_temp.shape}")  # Debug print
            print(f"mean_temp range: {np.nanmin(mean_temp)} to {np.nanmax(mean_temp)}")

            if mean_temp.ndim == 3:
                mean_temp = mean_temp[0, :, :]  # Ensure mean_temp is 2D if it's 3D

            winter_means.append(mean_temp)
            years.append(year)

    return years, winter_means, units

def create_winter_gif(years, winter_means, output_gif, title, units):
    """
    Creates a GIF showing the mean winter temperature for each year.

    Parameters:
        years (list): List of years for which the winter mean is computed.
        winter_means (list): List of 2D arrays containing the mean winter temperatures.
        output_gif (str): Path to save the output GIF.
        title (str): Title for the GIF.
        units (str): Units of the temperature data.
    """
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.Robinson()})
    ims = []

    # Determine the global min and max temperature for the color scale
    vmin = np.nanmin(winter_means)
    vmax = np.nanmax(winter_means)
    print(f"Winter mean temperature range for GIF: {vmin} to {vmax}")

    for year, mean_temp in zip(years, winter_means):
        im = ax.imshow(mean_temp, animated=True, cmap='coolwarm', vmin=vmin, vmax=vmax, transform=ccrs.PlateCarree())
        ims.append([im, ax.text(0.5, 1.05, str(year), ha="center", va="bottom", transform=ax.transAxes)])
    
    # Add map features
    ax.coastlines(resolution='110m')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='none')
    ax.add_feature(cfeature.OCEAN)

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.05)
    cbar.set_label(f'Temperature ({units})')

    # Create and save the animation
    ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True)
    ani.save(output_gif, writer='imagemagick')
    plt.close()

# Collect the regridded HadCRUT5 files
hadcrut5_files = sorted(glob.glob(f"{HADCRUT5_DIR}/*_regrid_kelvin.nc"))

# Create monthly evolution GIF for HadCRUT5
if hadcrut5_files:
    create_monthly_gif(hadcrut5_files, "tas_mean", "hadcrut5_monthly_evolution.gif", "HadCRUT5 Monthly Evolution")

# Compute and create winter mean temperatures GIF for HadCRUT5
if hadcrut5_files:
    years, winter_means, units = compute_winter_mean(hadcrut5_files, "tas_mean")
    if years and winter_means:
        create_winter_gif(years, winter_means, "hadcrut5_winter_mean.gif", "HadCRUT5 Winter Mean Temperature", units)

# Collect the regridded ERA5 files
era5_files = sorted(glob.glob(f"{ERA5_DIR}/*_regrid.nc"))

# Create monthly evolution GIF for ERA5
if era5_files:
    create_monthly_gif(era5_files, "t2m", "era5_monthly_evolution.gif", "ERA5 Monthly Evolution")

# Compute and create winter mean temperatures GIF for ERA5
if era5_files:
    years, winter_means, units = compute_winter_mean(era5_files, "t2m")
    if years and winter_means:
        create_winter_gif(years, winter_means, "era5_winter_mean.gif", "ERA5 Winter Mean Temperature", units)

print("GIF creation complete.")