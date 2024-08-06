from datetime import date
import boto3
import pandas as pd
import botocore.exceptions  # Import botocore exceptions here

def get_omics_regions():
    """
    Returns a list of AWS regions offering the omics (HealthOmics) service
    """
    session = boto3.session.Session()
    omics_regions = session.get_available_regions("omics")
    return omics_regions

def get_stores(client, store_type):
    """
    Returns a list of stores of the specified type for the given client, with improved error handling.
    """
    try:
        if store_type == "sequence":
            response = client.list_sequence_stores()
            key = "sequenceStores"
        elif store_type == "annotation":
            response = client.list_annotation_stores()
            key = "annotationStores"
        elif store_type == "variant":
            response = client.list_variant_stores()
            key = "variantStores"
        else:
            raise ValueError(f"Invalid store type: {store_type}")

        # Check and print the response
        print(f"Response for {store_type} stores in {client.meta.region_name}: {response}")

        if key in response:
            stores = response[key]
            for store in stores:
                store["type"] = store_type
            return stores
        else:
            return []  # Return an empty list if the key is not found
    except botocore.exceptions.ClientError as error:
        error_code = error.response['Error']['Code']
        if error_code == 'UnrecognizedClientException':
            print(f"ERROR: UnrecognizedClientException for {store_type} stores in {client.meta.region_name}. Check your AWS credentials and configuration.")
        else:
            print(f"ERROR: Unexpected error retrieving {store_type} stores in {client.meta.region_name}: {error}")
        return []  # Return empty list to handle errors gracefully

if __name__ == "__main__":
    omics_regions = get_omics_regions()
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    output_file_name = f"omics_data_stores_{date_str}.csv"
    final_df = None

    for region in omics_regions:
        # Create a client for AWS HealthOmics
        client = boto3.client("omics", region_name=region)

        # Get the stores for each type
        sequence_stores = get_stores(client, "sequence")
        annotation_stores = get_stores(client, "annotation")
        variant_stores = get_stores(client, "variant")

        all_stores = sequence_stores + annotation_stores + variant_stores
        stores_df = pd.DataFrame(
            {
                "type": [x["type"] for x in all_stores],
                "date": [today] * len(all_stores),
                "name": [x["name"] for x in all_stores],
                "region": [region] * len(all_stores),
                "store_id": [x["id"] for x in all_stores],
            }
        )

        if final_df is None:
            final_df = stores_df
        else:
            final_df = pd.concat([final_df, stores_df])

    final_df = final_df.reset_index().drop(columns=["index"])
    final_df.to_csv(output_file_name, index=False)
    print(final_df)
