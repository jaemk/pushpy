#!/usr/bin/python
# ^ if you install opencv with apt-get
# else if you compile from source, update to the virtualenv you installed it in

import os 
import sys
import time
time1 = time.time()
try:
    import cv2
except:
    cv2 = None


def capture():
    name = sys.argv[0]
    cam = sys.argv[-1]

    if cam == '1':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(1)

    cap.set(3,640)
    cap.set(4,480)
    ret, frame = cap.read()

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    picdump = os.path.join(cur_dir, 'picdump')
    if not os.path.exists(picdump):
        os.mkdir(picdump)

    cv2.imwrite(os.join(picdump, 'picout.png', frame)
    cap.release()
    elap = time.time() - time1

    with open(os.path.join(cur_dir, '/picdump/captimes.log'),'a') as logfile:
        logfile.write('{}\n'.format(elap))


def main():
    if cv2:
        capture()


if __name__ == '__main__':
    main()
