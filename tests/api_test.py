import cv2
from imutils import paths
from api_base import APIBase
import base64
import os

data_dir = "sample_data"
CNIC_FRONT = "front_cnic.jpg"
CNIC_BACK = "back_cnic.jpg"
VIDEO_FILE = "video.webm"
WITHOUT_FACE_IMAGE = "no_face.jpg"

api = APIBase()


"""Testing Face Existing endpoint with images that contain faces"""
face_images = list(paths.list_images(data_dir))

for each in face_images:
    image_file = open(each, "rb")
    base_string = base64.b64encode(image_file.read())
    image_file.close()
    if each.split(os.sep)[1] == WITHOUT_FACE_IMAGE:
        expected_response = 403
    else:
        expected_response = 200  
    api.post(api.face_check_endpoint, {"frame" : base_string}, expected_response=expected_response)
    print("[INFO] {expected_response} OK ImageFile: {each}".format(expected_response=expected_response, each=each))


"""Testing overall Evaluation function"""
frame_front = os.path.join(data_dir, CNIC_FRONT)
frame_back = os.path.join(data_dir, CNIC_BACK)
video = os.path.join(data_dir, VIDEO_FILE)
files = {'video': open(video,'rb')}
data = {"frame_front" : base64.b64encode(open(frame_front, "rb").read()), "frame_back" : base64.b64encode(open(frame_back, "rb").read()),\
     "frames_skipped" : 40}

r = api.post(api.evaluation_endpoint, files=files, data=data)
print(r.json()["data"])