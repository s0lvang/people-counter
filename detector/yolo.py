import time

import pydarknet
from pydarknet import Detector, Image
import cv2
import firebase_admin
from firebase_admin import credentials, db
import json
if __name__ == "__main__":
    # Optional statement to configure preferred GPU. Available only in GPU version.
    # pydarknet.set_cuda_device(0)

    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://people-counter-4f7dc.firebaseio.com/"})

    net = Detector(bytes("cfg/yolo-tiny.cfg", encoding="utf-8"), bytes("weights/yolov3-tiny.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    cap = cv2.VideoCapture(-1)

    while True:
        r, frame = cap.read()
        if r:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            # Frames per second can be calculated as 1 frame divided by time required to process 1 frame
            fps = 1 / (end_time - start_time)

            print("FPS: ", fps)
            print("Elapsed Time:",end_time-start_time)

            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
            persons = list(filter(lambda result: result[0].decode("utf-8") == "person", results))
            print(len(persons))
            ref = db.reference("/")
            ref.set(json.dumps({"persons": len(persons)}))
            cv2.imshow("preview", frame)

        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break
