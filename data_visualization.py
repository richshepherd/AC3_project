import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import glob
import pandas as pd

# Define directories
HADCRUT5_DIR = "./HadCRUT5"
ERA5_DIR = "./ERA5"

def create_monthly_gif(input_files, var_name, output_gif, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    ims = []

    for file in input_files:
        try:
            ds = xr.open_dataset(file)
        except Exception as e:
            print(f"Error opening file {file}: {e}")
            continue
        
        time = ds['time']
        temp = ds[var_name]

        for t in range(temp.shape[0]):
            temp_data = temp.isel(time=t).values.squeeze()
            if temp_data.ndim == 3:
                temp_data = temp_data[0]
            im = ax.imshow(temp_data, animated=True, cmap='coolwarm')
            timestamp = pd.to_datetime(time.values[t]).strftime('%Y-%m')
            ims.append([im, ax.text(0.5, 1.05, timestamp, ha="center", va="bottom", transform=ax.transAxes)])

    ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True)
    ani.save(output_gif, writer='imagemagick')
    plt.close()

def compute_winter_mean(input_files, var_name):
    winter_means = []
    years = []

    for file in input_files:
        try:
            ds = xr.open_dataset(file)
        except Exception as e:
            print(f"Error opening file {file}: {e}")
            continue

        time = ds['time']
        temp = ds[var_name]

        # Convert time to pandas datetime
        time = pd.to_datetime(time.values)
        temp['time'] = ('time', time)

        # Select winter months (December, January, February)
        winter_months = temp.sel(time=(time.month == 12) | (time.month == 1) | (time.month == 2))
        
        # Ensure there are winter months in the dataset
        if not winter_months.time.size:
            continue

        # Compute mean temperature for each winter season (DJF)
        winter_mean = winter_months.groupby('time.year').mean(dim='time')
        
        # Convert to 2D arrays
        for year in winter_mean['year'].values:
            mean_temp = winter_mean.sel(year=year).values.squeeze()
            if mean_temp.ndim == 3:
                mean_temp = mean_temp[0]
            winter_means.append(mean_temp)
            years.append(year)

    return years, winter_means

def create_winter_gif(years, winter_means, output_gif, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    ims = []

    for year, mean_temp in zip(years, winter_means):
        im = ax.imshow(mean_temp, animated=True, cmap='coolwarm')
        ims.append([im, ax.text(0.5, 1.05, str(year), ha="center", va="bottom", transform=ax.transAxes)])

    ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True)
    ani.save(output_gif, writer='imagemagick')
    plt.close()

# Collect the regridded HadCRUT5 files
hadcrut5_files = sorted(glob.glob(f"{HADCRUT5_DIR}/*_regrid.nc"))

# Create monthly evolution GIF for HadCRUT5
if hadcrut5_files:
    print("Creating monthly evolution GIF for HadCRUT5...")
    create_monthly_gif(hadcrut5_files, "tas_mean", "hadcrut5_monthly_evolution.gif", "HadCRUT5 Monthly Evolution")

# Compute and create winter mean temperatures GIF for HadCRUT5
if hadcrut5_files:
    print("Computing winter mean temperatures for HadCRUT5...")
    years, winter_means = compute_winter_mean(hadcrut5_files, "tas_mean")
    if years and winter_means:
        print("Creating winter mean temperatures GIF for HadCRUT5...")
        create_winter_gif(years, winter_means, "hadcrut5_winter_mean.gif", "HadCRUT5 Winter Mean Temperature")

# Collect the regridded ERA5 files
era5_files = sorted(glob.glob(f"{ERA5_DIR}/*_regrid.nc"))

# Create monthly evolution GIF for ERA5
if era5_files:
    print("Creating monthly evolution GIF for ERA5...")
    create_monthly_gif(era5_files, "t2m", "era5_monthly_evolution.gif", "ERA5 Monthly Evolution")

# Compute and create winter mean temperatures GIF for ERA5
if era5_files:
    print("Computing winter mean temperatures for ERA5...")
    years, winter_means = compute_winter_mean(era5_files, "t2m")
    if years and winter_means:
        print("Creating winter mean temperatures GIF for ERA5...")
        create_winter_gif(years, winter_means, "era5_winter_mean.gif", "ERA5 Winter Mean Temperature")

print("GIF creation complete.")
