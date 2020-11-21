from flask import Flask, request, jsonify
from flask_cors import CORS
from face import Face

app = Flask(__name__)
CORS(app)

@app.route("/v2/face_existence", methods=["GET"])
def face_existence_view():
    base_string = request.args.get("frame")
    is_face = Face.face_existence(base_string)
    if is_face:
        return "", 200
    return "", 500

@app.route("/v2/evaluate", methods=["POST"])
def evaluate_view():
    video = request.files['file']
    doc_string_front_side = request.form.get("frame_front")
    doc_string_back_side = request.form.get("frame_back")
    results = Face.evaluate(doc_string_front_side, doc_string_back_side, video)

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5010, threaded=True)