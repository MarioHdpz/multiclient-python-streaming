"""Streaming client"""
import socket
import time

import cv2
import imagezmq
import imutils
from imutils.video import WebcamVideoStream

sender = imagezmq.ImageSender(connect_to="tcp://*:5555", REQ_REP=False)

dispositivo = socket.gethostname()
capture = WebcamVideoStream(src=0).start()
time.sleep(2.0)
jpeg_quality = 95

while True:

    frame = capture.read()
    frame = imutils.resize(frame, width=220)
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    )
    sender.send_jpg(dispositivo, jpg_buffer)
