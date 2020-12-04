from flask import Flask, request, jsonify
from flask_cors import CORS
from face import Face
import uuid
import os

app = Flask(__name__)
CORS(app)

APP_DEBUG = True
FRAMES_SKIPPED = 4

if not os.path.exists('videos'):
    os.makedirs('videos')

@app.route("/v2/face_existence", methods=["POST"])
def face_existence_view():
    base_string = request.form.get("frame")
    is_face = Face().face_existence(base_string)
    if is_face:
        return "", 200
    return "", 403

@app.route("/v2/evaluate", methods=["POST"])
def evaluate_view():
    video = request.files['video']
    unique_video_id = str(uuid.uuid4())
    video.save(f"videos/{unique_video_id}.mp4")
    doc_string_front_side = request.form.get("frame_front")
    doc_string_back_side = request.form.get("frame_back")
    test_frames_skipped = request.form.get("frames_skipped")
    results = Face().evaluate(doc_string_front_side, doc_string_back_side, unique_video_id, int(test_frames_skipped) if test_frames_skipped else FRAMES_SKIPPED)
    return jsonify( {"data" : results} )

if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=APP_DEBUG)