# AC3_project
AC³ project - coding activities

# Climate Data Analysis

This repository contains scripts to download, preprocess, and analyze climate data from HadCRUT5 and ERA5 datasets. The scripts will generate GIFs showing monthly evolution and winter mean temperature anomalies.

## Contents

- `HadCRUT5/`: Directory for HadCRUT5 data files.
- `ERA5/`: Directory for ERA5 data files.
- `scripts/`: Directory for all scripts used in this analysis.
  - `data_processing.sh`: Bash script to download and preprocess the data.
  - `data_visualization.py`: Python script to create GIFs from the processed data.
- `README.md`: This file, containing instructions and explanations.

## Prerequisites

To run these scripts, you need the following software installed:

- **Git**: Version control system to clone the repository.
- **Conda**: Package manager to create and manage environments (recommended).
- **CDO**: Climate data operators for data processing.
- **Imagemagick**: To create GIFs from the images.

### Install Git

Follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install Git. Github on the web is also sufficient and can be assessed [here](https://github.com/login).

### Install Conda

Follow the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to install Conda. You can choose `Miniconda` for a lightweight installation or `Anaconda` for a more comprehensive suite of data analysis tools.

### Create a new environment with the required packages
Open a terminal and run the following command to create a new environment and install all needed packages

```bash
conda create --yes --name climate_analysis python=3.9 matplotlib pandas glob pillow numpy netCDF4 pip
```
### Install CDO

Follow the instructions [here](https://code.mpimet.mpg.de/projects/cdo/wiki) to install CDO.

### Install ImageMagick

Follow the instructions [here](https://imagemagick.org/script/download.php) to install ImageMagick. As an alternative to ImageMagick, Pillow has also been included in the list of packages that should be installed along with conda.

## Cloning the Repository
Firstly, fork the repository to your GitHub account.

![Climate Analysis](screenshot.png)

Next, open a terminal and run the following command to clone the repository:

```git clone git clone git@github.com:yourusername/AC3_project.git```

Replace `yourusername` with your actual GitHub username.

## Usage Instructions
### Activate the Conda Environment
Activate the environment you created:

```bash
conda activate climate_analysis
```

## Navigate to the Repository Directory
Change to the directory of the cloned repository:
```bash 
cd AC3_project
```

## Download and Preprocess the Data
Run the provided bash script to download and preprocess the data:

```bash
./data_processing.sh
```
## Create GIFs
Run the Python script to generate the GIFs:

```bash
python data_visualization.py
```

## Summary
1. Install Git, Conda, CDO, and ImageMagick.
2. Create a Conda environment with the required packages.
3. Clone the repository.
4. Install Python dependencies.
5. Download and preprocess the data.
6. Run the script to generate GIFs.

By following these steps, you should be able to reproduce the analysis and GIFs on your own computer.

