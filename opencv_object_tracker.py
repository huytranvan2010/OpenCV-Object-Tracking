from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf", help="OpenCV object tracker type")
args = vars(ap.parse_args())

# tạo dictionary mao strings to OpenCV object tracker
OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}
# lấy tracker truyền vào
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# khởi tạo tọa độ bounding box của object mà chúng ta sẽ theo dõi
initBB = None

# nếu ko cho video sẽ lấy webcam
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.)
else:
    vs = cv2.VideoCapture(args["video"])

# khởi tạo bộ đánh giá FPS
fps = None

while True:
    ret, frame = vs.read()

    if ret == False:
        break
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    if initBB is not None:
        # lấy new bounding box
        (success, box) = tracker.update(frame)

        # kiểm tra nếu tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # update the FPS counter
        fps.update()
        fps.stop()

        # khởi tạo một số thông tin hiển thị trên frame
