import json
import logging
import os
import sys
# Set logging level and env vars
logging.basicConfig(level=logging.INFO)
SOURCE = os.environ['SOURCE']
TARGET = os.environ['TARGET']
# Unzip packaged dependencies
try: 
  import unzip_requirements
except ImportError:
  logging.error('Failed unzip requirements')
  sys.exit(1)

import boto3
from image import identify

s3 = boto3.client('s3')

def process(event, context):
  key = event['object']['key']
  [filename, extension] = key.split('.')
  processed_key = '{}_identified.{}'.format(filename, extension)
  s3.download_file(Bucket=SOURCE, Key=key, Filename=key)
  logging.info('{} downloaded'.format(key))
  identified = identify(key, processed_key, 'encodings.pickle')
  s3.upload_file(Bucket=TARGET, Key=processed_key, Filename=processed_key)
  logging.info('{} uploaded'.format(processed_key))
  os.remove(key)
  os.remove(processed_key)
  return {
    'statusCode': 200,
    'body': json.dumps('completed')
  }

if __name__ == '__main__':
  process({'object': {'key': 'example.png'}}, '')
