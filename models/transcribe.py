import pandas as pd
import json
import random
import time
import boto3
from decouple import config
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Accessing the environment variables stored in .env file
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

MY_REGION = config('MY_REGION')
BUCKET_NAME = config('BUCKET_NAME')

LANG_CODE = 'en-AU'

# For each transcription call, create a random job name
def random_job_name():
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
    LOWERCASE_CHAR = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
    UPPERCASE_CHAR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','Z']

    COMBINED_LIST = DIGITS + UPPERCASE_CHAR + LOWERCASE_CHAR
    temp_name = ""

    for x in range(10):
        temp_name += random.choice(COMBINED_LIST)

    return str(temp_name)

def get_text(file_path , file_name):
    # Create a resource service client by name using the default session. AWS Transcribe will transcribe files from S3 Storage
    s3 = boto3.resource(service_name = "s3" , region_name = MY_REGION , aws_access_key_id = AWS_ACCESS_KEY_ID , 
                    aws_secret_access_key = AWS_SECRET_KEY)

    try:
        s3.Bucket(f"{BUCKET_NAME}").upload_file(Filename = f"{file_path}" , Key = file_name)
    except Exception as e:
        print("Could not fetch data")


    transcribe = boto3.Session(region_name = MY_REGION , 
                        aws_access_key_id = AWS_ACCESS_KEY_ID , 
                        aws_secret_access_key = AWS_SECRET_KEY).client("transcribe")  

    file_format = "webm"
    job_uri = f"s3://{BUCKET_NAME}/"+file_name
    job_name =  random_job_name()             

    # starts an asynchronous job to transcribe speech to text
    transcribe.start_transcription_job(TranscriptionJobName = job_name , 
                                    Media = {'MediaFileUri': job_uri} , 
                                    MediaFormat = file_format , 
                                    LanguageCode = LANG_CODE)

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        time.sleep(20)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    if status['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
        data = pd.read_json(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])

    elif status['TranscriptionJob']['TranscriptionJobStatus'] == "FAILED":
        print("Failed to extract text from audio.....Try again!!")

    # get the text from json response object
    text = data['results'][1][0]['transcript']

    s3.Bucket(BUCKET_NAME).objects.all().delete()
    s3.Bucket(BUCKET_NAME).object_versions.delete()

    return text
