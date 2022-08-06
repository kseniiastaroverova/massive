import glob
import os
import shutil

from google.cloud import storage

PATH_TO_KEY_JSON_FILE = "./gc_creds.json"
PROJECT_ID = "massive_ks"
TMP_DIR = "./temp"
BUCKET = "massive_ks"

client = storage.Client.from_service_account_json(PATH_TO_KEY_JSON_FILE, project=PROJECT_ID)

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)


def upload_checkpoint_gcp(local_path, gcs_path):
    """
    Create zip and upload to gcp
    """
    assert os.path.isdir(local_path)

    dir_name = os.path.dirname(local_path)
    zip_path = os.path.join(TMP_DIR, dir_name)
    zip_path = shutil.make_archive(zip_path, "zip", local_path)

    bucket = client.get_bucket(BUCKET)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(zip_path)

    os.remove(zip_path)
