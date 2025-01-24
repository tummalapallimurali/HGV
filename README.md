# HGV
- This repo is coding assignment and contains two files dataprep and datapreprocessing.
- A workflow file is created to run for 5000 files and can be passed as arguments.

# To view current report: 
  - Click on following link : https://github.com/tummalapallimurali/HGV/commit/9ef5fb10ccbfbf71d4e0cd3d38c8dc1122a907c7
  - Scroll down you will see model metrics , something like this:

    ![image](https://github.com/user-attachments/assets/bb8586b5-c197-4a8f-a24b-aa9bb6657c00)

# If you wish to modify any arguments: 
  - Go to: https://github.com/tummalapallimurali/HGV/blob/main/.github/workflows/main.yml
  - Change line number 28 as per your requirement and sample input arguments looks like :
  - python 01_dataprep.py --cities_pool NewYork LosAngeles Chicago Houston Phoenix Philadelphia SanAntonio --dirty_records_prob 0.5 --num_files 5000 --num_records_range 50 100

