# AC3_project
AC³ project - coding activities

# Climate Data Analysis

This repository contains scripts to download, preprocess, and analyze climate data from HadCRUT5 and ERA5 datasets. The scripts will generate GIFs showing monthly evolution and winter mean temperature anomalies.

## Contents

- `HadCRUT5/`: Directory for HadCRUT5 data files.
- `ERA5/`: Directory for ERA5 data files.
- `scripts/`: Directory for all scripts used in this analysis.
  - `download_and_preprocess.sh`: Bash script to download and preprocess the data.
  - `create_gifs.py`: Python script to create GIFs from the processed data.
- `README.md`: This file, containing instructions and explanations.
- `requirements.txt`: List of Python dependencies.

## Prerequisites

To run these scripts, you need the following software installed:

- **Git**: Version control system to clone the repository.
- **Conda**: Package manager to create and manage environments (recommended).
- **CDO**: Climate data operators for data processing.
- **Imagemagick**: To create GIFs from the images.

### Install Git

Follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install Git.

### Install Conda

Follow the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to install Conda.

### Install CDO

Follow the instructions [here](https://code.mpimet.mpg.de/projects/cdo/wiki) to install CDO.

### Install ImageMagick

Follow the instructions [here](https://imagemagick.org/script/download.php) to install ImageMagick.

## Cloning the Repository

Open a terminal and run the following command to clone the repository:

```sh
git clone https://github.com/yourusername/ClimateDataAnalysis.git
cd ClimateDataAnalysis
