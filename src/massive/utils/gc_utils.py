import glob
import os
import shutil
from pathlib import Path

from google.cloud import storage
from loguru import logger

logger.add("logs.log") 


PATH_TO_KEY_JSON_FILE = "./gc_creds.json"
PROJECT_ID = "massive_ks"
TMP_DIR = "./temp"
BUCKET = "massive_ks"

client = storage.Client.from_service_account_json(PATH_TO_KEY_JSON_FILE, project=PROJECT_ID)

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)


def upload_checkpoint_gcp(output_dir, gcs_path):
    """
    Create zip and upload to gcp
    """

    try:
        local_path = max(glob.glob(os.path.join(output_dir, "*/")), key=os.path.getmtime)
        logger.info(f"Found latest checkpoint {local_path=}")

        assert os.path.isdir(local_path)

        local_path = Path(local_path)

        zip_file_name = local_path.stem
        zip_path = os.path.join(TMP_DIR, zip_file_name)

        logger.info(f"Create zip from {local_path=} to {zip_path=}")
        zip_path = shutil.make_archive(zip_path, "zip", local_path)
        logger.info(f"Created zip {zip_path=}")

        bucket = client.get_bucket(BUCKET)
        blob_name = os.path.join(gcs_path, zip_file_name + ".zip")
        logger.info(f"Upload zip to {blob_name=}")
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(zip_path)

        os.remove(zip_path)
    except Exception as error:
        logger.exception(error)
