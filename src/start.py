#!/usr/bin/env python3

import boto3
import json
import os
import time
import base64

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

from image_extension.core import start_process
from image_extension.utils import image_to_base64
from data import ImageProgress, to_dict, Status

script_directory = os.path.dirname(os.path.abspath(__file__))
firebase_key_path = os.path.join(script_directory, "../firebase-service-key.json")

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET')
})

db = firestore.client()
bucket = storage.bucket()


def handle_message(message_body):
    @firestore.transactional
    def send_status_in_transaction(transaction, doc_ref):
        snapshot = doc_ref.get(transaction=transaction)
        status = snapshot.get('status')
        if status != Status.SEND.value:
            raise Exception()
        transaction.update(doc_ref, {"status": Status.LOADING.value})

    payload = json.loads(message_body)
    _id = payload.pop('id')
    doc_ref = db.collection("imageProgress").document(_id)

    try:
        transaction = db.transaction()
        send_status_in_transaction(transaction, doc_ref)
    except:
        return

    base64img = start_process(
        base_image = image_to_base64(payload['base_image']),
        roop_image = image_to_base64(payload['roop_image']),
        face_index = payload['face_index']
    )
    image_data = base64.b64decode(base64img)
    blob = bucket.blob(f'/upload/{_id}.png')
    blob.upload_from_file(image_data)
    blob.make_public()

    doc_ref.update(to_dict(ImageProgress(_id=_id, status=Status.SUCCESS.value, imageUrl=f'{_id}.png', worker=os.environ.get('WORKER_INSTANCE'))))


def main():
    sqs = boto3.client('sqs')
    QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

    print("Message Listening...")
    while True:
        messages = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                print("Get message")
                print(message)

                try:
                    handle_message(message['Body'])
                except Exception as e:
                    print(e)
                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
        
        time.sleep(1)


if __name__ == "__main__":
    main()
