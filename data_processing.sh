#!/bin/bash

# Define directories
HADCRUT5_DIR="./HadCRUT5"
ERA5_DIR="./ERA5"
GRID_FILE="grid_2.5x2.5.txt"

# Create directories if they don't exist
mkdir -p $HADCRUT5_DIR
mkdir -p $ERA5_DIR

# Create grid file for 2.5x2.5 degree resolution
cat <<EOL > $GRID_FILE
gridtype = lonlat
xsize = 144
ysize = 73
xfirst = -180
xinc = 2.5
yfirst = -90
yinc = 2.5
EOL

# Download and unzip HadCRUT5 data
cd $HADCRUT5_DIR
if [ -f "HadCRUT5_data.nc" ]; then
    echo "HadCRUT5_data.nc already exists. Skipping download."
else
    wget -O HadCRUT5_data.nc "https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.5.0.2.0/non-infilled/HadCRUT.5.0.2.0.anomalies.ensemble_mean.nc"
fi
cd ..

# Download ERA5 data using Python
cd $ERA5_DIR
if [ -f "ERA5_data.nc" ]; then
    echo "ERA5_data.nc already exists. Skipping download."
else
    cat <<EOL > download_era5.py
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': '2m_temperature',
        'year': ['1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', 
        '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961',
        '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
        '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983',
        '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994',
        '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005',
        '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
        '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        'time': '00:00',
        'format': 'netcdf'
    },
    'ERA5_data.nc')
EOL

    python download_era5.py
fi
cd ..

# Split HadCRUT5 data into individual monthly files
if [ -f "$HADCRUT5_DIR/HadCRUT5_202001.nc" ]; then
    echo "HadCRUT5 data already split into individual monthly files. Skipping split."
else
    cdo splityearmon $HADCRUT5_DIR/HadCRUT5_data.nc $HADCRUT5_DIR/HadCRUT5_
fi

# Regrid and convert HadCRUT5 data to Kelvin
for file in ${HADCRUT5_DIR}/*.nc; do
    if [[ $file != *_regrid_kelvin.nc ]]; then
        echo "Processing $file"
        # Regrid to 2.5x2.5 degree resolution
        cdo remapbil,$GRID_FILE $file ${file%.nc}_regrid.nc
        # Convert temperature to Kelvin
        cdo addc,273.15 ${file%.nc}_regrid.nc ${file%.nc}_regrid_kelvin.nc
        rm ${file%.nc}_regrid.nc
    fi
done

# Remove the unnecessary variable 'expver' from ERA5 data if present
ERA5_TEMP_FILE="$ERA5_DIR/ERA5_temp.nc"
if cdo showname $ERA5_DIR/ERA5_data.nc | grep -q expver; then
    cdo selvar,t2m $ERA5_DIR/ERA5_data.nc $ERA5_TEMP_FILE
else
    cp $ERA5_DIR/ERA5_data.nc $ERA5_TEMP_FILE
fi

# Split ERA5 data into individual monthly files
if [ -f "$ERA5_DIR/ERA5_202001.nc" ]; then
    echo "ERA5 data already split into individual monthly files. Skipping split."
else
    cdo splityearmon $ERA5_TEMP_FILE $ERA5_DIR/ERA5_
fi

# Regrid and convert ERA5 data to Kelvin
for file in ${ERA5_DIR}/*.nc; do
    if [[ $file != *_regrid_kelvin.nc ]]; then
        echo "Processing $file"
        # Regrid to 2.5x2.5 degree resolution
        cdo remapbil,$GRID_FILE $file ${file%.nc}_regrid.nc
        # Convert temperature to Celsius
        # cdo subc,273.15 ${file%.nc}_regrid.nc ${file%.nc}_regrid_kelvin.nc
        # rm ${file%.nc}_regrid.nc
    fi
done

# Clean up intermediate files
rm $ERA5_TEMP_FILE


# Clean up intermediate HadCRUT5 files
for file in ${HADCRUT5_DIR}/*.nc; do
    if [[ $file != *_regrid_kelvin.nc ]]; then
        rm $file
    fi
done