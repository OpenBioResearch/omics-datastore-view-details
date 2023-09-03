import boto3
from boto3.session import Session
from datetime import date


def get_omics_regions():
    """
    Returns a list of AWS regions which offer the omics (HealthOmics) service
    """
    s = Session()
    omics_regions = s.get_available_regions("omics")
    return omics_regions


def get_stores(client, store_type):
    """
    Returns a list of stores of the specified type for the given client.
    """
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

    # Check if the key is in the response
    if key in response:
        stores = response[key]
        # Add the store type to each store
        for store in stores:
            store["type"] = store_type
        return stores
    else:
        return []


if __name__ == "__main__":
    omics_regions = get_omics_regions()

    # Get the current date and format it as YYYY-MM-DD
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Create the output file name
    output_file_name = f"omics_data_stores_{date_str}.txt"

    # Open the output file for writing
    with open(output_file_name, "w") as f:
        for region in omics_regions:
            # Create a client for AWS HealthOmics
            client = boto3.client("omics", region_name=region)

            # Get the stores for each type
            sequence_stores = get_stores(client, "sequence")
            annotation_stores = get_stores(client, "annotation")
            variant_stores = get_stores(client, "variant")

            # Combine all stores into a single list
            all_stores = sequence_stores + annotation_stores + variant_stores

            # Print the details for each store
            for store in all_stores:
                line = f"Type: {store['type']}, Date: {today}, Name: {store['name']}, Region: {region}, Store ID: {store['id']}\n"
                print(line, end="")
                f.write(line)
