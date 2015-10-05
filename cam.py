#!/usr/bin/python

# change ownership, permissions
# sudo chown root:root /home/james/projects/pushy2/app/cam.py
# sudo chmod 700 cam.py

# sudo visudo
# under %sudo ALL=(ALL:ALL) ALL
# james ALL=(ALL) NOPASSWD: /home/james/projects/pushy2/app/cam.py


import os, sys, time
time1 = time.time()
import cv2

name = sys.argv[0]
cam = sys.argv[-1]

if cam == '1':
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(1)

cap.set(3,640)
cap.set(4,480)
ret, frame = cap.read()
cur_dir = '/home/james/projects/pushy2/app'
cv2.imwrite(cur_dir + '/picdump/picout.png', frame)
cap.release()
elap = time.time()-time1

logfile = open(cur_dir + '/picdump/captimes.log','a')
logfile.write(str(elap) + '\n')
logfile.close()
