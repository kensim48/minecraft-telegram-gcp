import os
from google.cloud import storage

def change_mode(mode, bucketname):
    upload_file("version_config/{}.txt".format(mode),"version.txt", bucketname)

def upload_file(file_stream, filename, bucketname):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """


    # [START bookshelf_cloud_storage_client]
    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(filename)
    blob.delete()
    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(filename)
    print(blob.download_as_string())
    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(filename)
    blob.upload_from_filename(file_stream)
    blob1 = bucket.blob(filename)
    print(blob1.download_as_string())
    # Ensure the file is publicly readable.