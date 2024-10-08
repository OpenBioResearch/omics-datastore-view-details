# Omics-datastore-view-details

## Overview

This project includes scripts that retrieve and consolidate details of AWS HealthOmics data stores, including sequence, annotation, and variant stores from apllicable AWS regions. They also offer visualizations, displaying the distribution of data stores across regions, types, and over time.

Note: An AWS account needs to be established prior to utilizing the script and notebook in this repository. Ensure that you have the necessary AWS credentials and permissions to access HealthOmics data stores.

## Installation and Usage

**Clone the repository:**

```bash
git clone https://github.com/OpenBioResearch/omics-datastore-view-details.git
cd omics-datastore-view-details
```

**Create a virtual environment (optional but recommended):**

```bash 
python -m venv .venv
source .venv/bin/activate  
```

**Install the Python dependencies:**

```bash
pip install -r requirements.txt
```

**Run the python script and jupyter notebook:**

```bash
python omics_store_summary.py
```
Open `omics_visualization.ipynb` notebook 

## License
This project is licensed under the BSD 3-Clause
