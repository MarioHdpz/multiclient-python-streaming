"""Streaming server"""
import cv2
import imagezmq
import numpy as np

imageHub = imagezmq.ImageHub(open_port="tcp://127.0.0.1:5555", REQ_REP=False)

while True:
    dispositivo, jpg_buffer = imageHub.recv_jpg()
    imagen = cv2.imdecode(np.frombuffer(jpg_buffer, dtype="uint8"), -1)
    cv2.imshow(dispositivo, imagen)
    cv2.waitKey(1)
