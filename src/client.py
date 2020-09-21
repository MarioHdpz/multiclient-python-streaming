"""Streaming client"""
import os
import socket
import time

import cv2
import imagezmq
import imutils
from imutils.video import WebcamVideoStream
from sshtunnel import open_tunnel

with open_tunnel(
    os.getenv("SERVER_HOST"),
    ssh_username=os.getenv("SERVER_USER"),
    ssh_password=os.getenv("SERVER_PASSWORD"),
    remote_bind_address=("127.0.0.1", 5555),
) as server:
    port = server.local_bind_port
    sender = imagezmq.ImageSender(connect_to=f"tcp://127.0.0.1:{port}", REQ_REP=False)

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
