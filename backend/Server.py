from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from flask_ngrok import run_with_ngrok
from flask import Flask, request

from VQA import PythiaModel

VQA = PythiaModel()

app = Flask(__name__)
run_with_ngrok(app)

speech_to_text = SpeechToTextV1(authenticator=IAMAuthenticator('KlSualKWykb2Cs8HlpcZKHdPnj0JKFhSJgQ8qF3fcs64'))
speech_to_text.set_service_url(
    'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/870f0a1c-85f1-40a1-bfca-b949bf63683a')

@app.route("/speech2text", methods=['POST'])
def speech2text():
    audio_filename = './audio.flac'
    request.files['audio_file'].save(audio_filename)

    with open(audio_filename, 'rb') as audio_file:
        re = speech_to_text.recognize(audio=audio_file).get_result()
    print(re)
    return re['results'][0]['alternatives'][0]['transcript']


@app.route("/getanswer", methods=['POST'])
def get_answer():
    audio_filename = './audio.flac'
    request.files['audio_file'].save(audio_filename)

    image_filename = './image.png'
    request.files['image_file'].save(image_filename)

    with open(audio_filename, 'rb') as audio_file:
        re = speech_to_text.recognize(audio=audio_file).get_result()
    question = re['results'][0]['alternatives'][0]['transcript']

app.run()