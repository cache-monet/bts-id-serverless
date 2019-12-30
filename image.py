import cv2
from recognize import process, recognize, draw, show

def identify(image, encodings, detection='hog', tolerance=0.45):
  [filename, extension] = image.split('.')
  identified = './{}_identified.{}'.format(filename, extension)
  names = []
  encodings, image = process(image, encodings)
  boxes = recognize(image, names, encodings, detection, tolerance)
  draw(image, boxes, names)
  cv2.imwrite(identified, image)