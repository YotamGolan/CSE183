from nqgcs import NQGCS
import os
import json
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials


APP_FOLDER = os.path.dirname(__file__)
GCS_KEY_PATH = os.path.join(APP_FOLDER, 'private/gcs_keys.json')
with open(GCS_KEY_PATH) as gcs_key_f:
    GCS_KEY = json.load(gcs_key_f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(GCS_KEY)

client = storage.Client(credentials=credentials, project='collabcanvas')
bucket = client.get_bucket('checkpointing')
blob = bucket.blob('duck.png')
#blob.upload_from_filename('duck.png')

blob.download_to_filename('duck.png')