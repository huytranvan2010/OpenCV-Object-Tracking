import cv2
import sys
import argparse
import imutils
import time
from imutils.video import FPS

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="KCF", help="OpenCV object tracker type")
args = vars(ap.parse_args())

# tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = args["tracker"]

if int(minor_ver) < 3:
    tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()

# Khởi tạo tọa độ bounding box của obejct muốn theo dõi, nếu điền vào ở dưới sẽ xử lý 
initBB = None

if not args.get("video", False):
    print("[INFO] starting video stream...")
    video = cv2.VideoCapture(0)     # lấy webcam
    time.sleep(1.)      # warm up
else:
    video = cv2.VideoCapture(args["video"])     # lấy video truyền vào

# khởi tạo bộ đếm fps
fps = None

while True:
    ok, frame = video.read()    # đọc video

    # Nếu ko đọc đọc được frame
    if not ok:
        break
    
    # Nếu đọc đến cuối video
    if frame is None:
        break
    
    # resize lại để có tốc độ tốt hơn
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    # kiểm tra nếu chúng ta đang theo dõi vật thể, ban đầu khởi tạo ininBB
    if initBB is not None:
        # lấy new bounding box của vật thể đó - update tracker
        # chú ý xem bên dưới mình mới khởi tạo tracker
        (success, box) = tracker.update(frame)

        # nếu sự theo dõi thành công thì vẽ rectangle
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # update the FPS counter
        fps.update()
        fps.stop()
        # initialize the set of information we'll be displaying on the frame
        info = [
            ("Tracker", tracker_type),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 's' key is selected, we are going to "select" a bounding box to track
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        """ Đây chính là khởi tạo tracker cho bounding boxes đó """
        tracker.init(frame, initBB)
        fps = FPS().start()

    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break
# if we are using a webcam, release the pointer
if not args.get("video", False):
    video.stop()
# otherwise, release the file pointer
else:
    video.release()
# close all windows
cv2.destroyAllWindows()

        