import boto3
import cv2
from image import identify

s3 = boto3.client('s3')

def process(event, context):
  image = event['image']
  [filename, extension] = image.split('.')
  processed = '{}_identified.{}'.format(filename, extension)
  s3.download_file('bts-identifier-source', image, image)
  identify(image, 'encodings.pickle')
  s3.upload_file(processed, 'bts-identifier-source', processed)
