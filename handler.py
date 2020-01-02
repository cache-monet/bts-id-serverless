import json
import logging
import os
import sys
# Set logging level
logging.basicConfig(level=logging.INFO)
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
  s3.download_file(Bucket='bts-identifier-source', Key=key, Filename=key)
  logging.info('{} downloaded'.format(key))
  identified = identify(key, processed_key, 'encodings.pickle')
  s3.upload_file(Bucket='bts-identifier-target', Key=processed_key, Filename=processed_key)
  logging.info('{} uploaded'.format(processed_key))
  os.remove(key)
  os.remove(processed_key)
  return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
  }

if __name__ == '__main__':
  process({'object': {'key': 'test.png'}}, '')
