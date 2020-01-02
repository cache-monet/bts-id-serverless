from recognize import process, recognize, draw, show
import cv2
import logging

def identify(source, destination, encodings, detection='hog', tolerance=0.45):
  names = []
  encodings, image = process(source, encodings)
  boxes = recognize(image, names, encodings, detection, tolerance)
  draw(image, boxes, names)
  cv2.imwrite(destination, image)