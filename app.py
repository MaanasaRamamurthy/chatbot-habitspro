from flask import Flask, render_template, request, jsonify
import os
import openai
import traceback
from datetime import datetime
from chat import get_response

api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)

@app.get("/audio")
def audio():
    return render_template("audio.html")


@app.route("/record_audio", methods=["POST"])
def record_audio():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        upload_folder = 'D:/Maanasa/Projects/PycharmProjects/chatbot-habitspro/audio-files'
        os.makedirs(upload_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"audio_{timestamp}.wav"
        file_path = os.path.join(upload_folder, file_name)


        file.save(file_path)

        with open(file_path, 'rb') as f:
            audio_data = f.read()

        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript['text'])


    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error during audio data processing: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
