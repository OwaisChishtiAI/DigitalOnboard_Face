import cv2
import face_lib
from PIL import Image
import numpy as np
import time
import base64
import io
from imageio import imread
import math

class Face:
    def _base64_to_image(self, base_string):
        base_string = base64.b64decode(base_string)   # im_bytes is a binary image
        base_string = io.BytesIO(base_string)  # convert image to file-like object
        base_string = Image.open(base_string)   # img is now PIL Image object
        base_string = np.array(base_string) 
        base_string = base_string[:, :, ::-1].copy()        
        return base_string

    @staticmethod
    def face_existence(self, base_string):
        img = self._base64_to_image(base_string)
        locs = face_lib.face_locations(img)
        if locs:
            return True
        return False

    def _face_extractor(self, base_string):
        img = self._base64_to_image(base_string)
        landmarks = face_lib.face_encodings(img, num_jitters=50, model="large")[0]
        return landmarks
        
    def _compare_faces(self, reference, unknown):
        return face_lib.face_distance([reference], unknown)[0]

    def _comparison_to_percentage(self, face_distance, face_match_threshold=0.6):
        if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range * 2.0)
            return linear_val
        else:
            range = face_match_threshold
            linear_val = 1.0 - (face_distance / (range * 2.0))
            return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
        
    @staticmethod
    def evaluate(self, doc_string_front_side, doc_string_back_side, video):
        results = {"img-img" : None, "img-video" : []}
        img_front_side = self._base64_to_image(doc_string_front_side)
        img_back_side = self._base64_to_image(doc_string_back_side)
        results["img-img"] = self._compare_faces(img_front_side, img_back_side)
        cap = cv2.VideoCapture(video)
        frames = 0
        while cap.isOpened():
            try:
                _,frame = cap.read()
                _ = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                try:
                    if frames % 4 == 0:
                        temp = face_lib.face_encodings(frame, num_jitters=50, model="large")[0]
                        thresh = self._compare_faces(img_front_side, temp)
                        results["img-video"].append(thresh)
                except Exception as e:
                    pass
                
            except Exception as e:
                pass
                
            frames += 1
            
                
        cap.release()
        cv2.destroyAllWindows()
        results["img-video"] = sum(results["img-video"]) / len(results["img-video"])
        results = {(key, self._comparison_to_percentage(value) * 100) for key, value in results.items() if key is not None}

        return results
