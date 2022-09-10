import os
from google.cloud import storage

def change_mode(mode, bucketname):
    upload_file("version.txt", "version_config/{}.txt".format(mode), bucketname)

def upload_file(file_stream, filename, bucketname):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """


    # [START bookshelf_cloud_storage_client]
    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(filename)

    blob.upload_from_filename(file_stream)
    # Ensure the file is publicly readable.
    blob.make_public()