#!/usr/bin/python3
import requests
from envyaml import EnvYAML
from enum import Enum
from datetime import datetime, timedelta
import sys
import json
from unicodedata import name
import rfc3339

# This script will create an annotation 
# in the SLO based on current time plus 5 min.

# find all the things
env = EnvYAML('config.yaml')

# init all the things
URL = env['n9Config']['url']
ORGANIZATION = env['n9Config']['org']
CLIENT_ID = env['n9Config']['clientId']
CLIENT_SECRET = env['n9Config']['clientSecret']
PROJECT = env['n9Config']['project']
SLO_NAME = env['n9Config']['sloName']
ANNOTATION_NAME = env['n9Config']['annotationName']
ANNOTATION_DATA = env['n9Config']['annotationData']

# Format the things for the stuff
SLO_ANNOTATION = {
    'slo' : SLO_NAME, 
    'project' : PROJECT, 
    'name' : ANNOTATION_NAME, 
    'description' : ANNOTATION_DATA, 
    'startTime' : TO, 
    'endTime' : FROM
    }

# Get the stuff
def get_token():
    TOKEN = requests.post(
            f'{URL}/api/accessToken',
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={'organization': ORGANIZATION},
        )
    if TOKEN.status_code == 200:
        return('Token acquired!')
    else:
        print('Something went wrong. Unable to retrieve token.')
        return(TOKEN.text)
        exit(1)

# put the stuff where the stuff goes
def annotate(TOKEN):
    TOKEN = TOKEN.json()['access_token']

    # Set Annotation time period. Default duration is 5m. 
    now = datetime.utcnow()
    since = now + timedelta(minutes=5)

    # submit the annotation
    print('Submitting annotation...')

    r = requests.post(
        f'{URL}/api/annotations',
        data=json.dumps(SLO_ANNOTATION),
        headers={
            'authorization': f'Bearer {TOKEN}',
            'organization': ORGANIZATION,
        },
    )
    if r.status_code == 200:
        print(f'Annotation created on {SLO_NAME} at {now}')
    else:
        print('Something went wrong. Your annotation was not accepted. Try again.')
        print(r.text)
        exit(1)

# make the stuff do the things
TOKEN = get_token()
annotate(TOKEN)