import firebase_admin
import os, itertools
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

import argparse
from typing import Optional


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./pythondbtest-a8bdf-firebase-adminsdk-daafs-7052e44485.json"
# Use a service account
cred = credentials.Certificate('./pythondbtest-a8bdf-firebase-adminsdk-daafs-7052e44485.json')
app = firebase_admin.initialize_app(cred,{
    'storageBucket':'pythondbtest-a8bdf.appspot.com'
    })

if __name__ == "__main__":
    print(app)
