"""
    Calculate intensity statistics (mean, median, std) for all DICOM files in the specified S3 bucket.
    """

import json
import boto3
import pydicom
import numpy as np
import io
import argparse
import csv

def calculate_statistics(bucket_name):
    s3 = boto3.client('s3')
    results = []

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            return {'error': 'No objects found in the bucket'}

        # Iterate through .dcm files
        for obj in response['Contents']:
            if obj['Key'].endswith('.dcm'):
                dicom_key = obj['Key']

                response = s3.get_object(Bucket=bucket_name, Key=dicom_key)
                dicom_file = io.BytesIO(response['Body'].read())

                dataset = pydicom.dcmread(dicom_file)
                image = dataset.pixel_array

                stats = {
                    'file': dicom_key,
                    'mean': round(np.mean(image), 2),
                    'median': round(np.median(image), 2),
                    'std': round(np.std(image), 2)
                }
                results.append(stats)

    except Exception as e:
        return {'error': str(e)}

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate DICOM image intensity statistics from an S3 bucket.")
    parser.add_argument('bucket', type=str, help="The name of the S3 bucket containing the DICOM files.")
    args = parser.parse_args()

    results = calculate_statistics(args.bucket)
    if 'error' in results:
        print("Error:", results['error'])
    else:
        output_file = 'intensity_statistics.csv'

        with open(output_file, mode='w', newline='') as csvfile:
            fieldnames = ['file', 'mean', 'median', 'std']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow(row)

        print(f"Results written to {output_file}")
