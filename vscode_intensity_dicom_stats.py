import json
import boto3
import pydicom
import numpy as np
import io

def local_handler(event):
    s3 = boto3.client('s3')
    bucket = event['bucket']

    try:
        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket)
        if 'Contents' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No objects found in the bucket'})
            }

        # Find the first .dcm file
        dicom_key = None
        for obj in response['Contents']:
            if obj['Key'].endswith('.dcm'):
                dicom_key = obj['Key']
                break

        if not dicom_key:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No .dcm files found in the bucket'})
            }

        # Retrieve the DICOM file from S3
        response = s3.get_object(Bucket=bucket, Key=dicom_key)
        dicom_file = io.BytesIO(response['Body'].read())

        # Load the DICOM file using pydicom
        dataset = pydicom.dcmread(dicom_file)
        image = dataset.pixel_array

        # Calculate intensity statistics
        stats = {
            'mean': np.mean(image),
            'median': np.median(image),
            'std': np.std(image)
        }

        return {
            'statusCode': 200,
            'body': json.dumps(stats)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Example event for testing
test_event = {
    "bucket": "dicom-healthimaging-tcia"
}

# Run the local handler with the test event
if __name__ == "__main__":
    result = local_handler(test_event)
    print(json.dumps(result, indent=4))
