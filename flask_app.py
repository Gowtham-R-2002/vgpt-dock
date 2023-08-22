
import audioop
import time
from flask import Flask, render_template, request, jsonify

import openai
import os
import time
from deep_translator import GoogleTranslator
from gtts import gTTS


import io
import speech_recognition as sr

app = Flask(__name__)

# Set your AssemblyAI and OpenAI API keys
openai_api_key = "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"

# Configure OpenAI API key
openai.api_key = openai_api_key

tts_base_url = "https://texttospeech.googleapis.com/v1/text:synthesize"

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/record', methods=['POST']) # type: ignore
def record():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        silence_threshold = 700  # Adjust silence threshold as needed
        audio_data = []

        while True:
            audio_chunk = recognizer.listen(source, timeout=2)
            rms = audioop.rms(audio_chunk.frame_data, 2)
            audio_data.append(audio_chunk)

            if rms < silence_threshold:
                break

    audio = sr.AudioData(b''.join(chunk.frame_data for chunk in audio_data), audio_chunk.sample_rate, 2)

    try:
        text = recognizer.recognize_google(audio)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': 'Error with the request to Google API: ' + str(e)})
    except sr.WaitTimeoutError:
        print("Timeout: No audio detected within the specified timeout.")


@app.route('/record_tamil', methods=['POST']) # type: ignore
def record_tamil():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        silence_threshold = 700  # Adjust silence threshold as needed
        audio_data = []

        while True:
            audio_chunk = recognizer.listen(source, timeout=1)
            rms = audioop.rms(audio_chunk.frame_data, 2)
            audio_data.append(audio_chunk)

            if rms < silence_threshold:
                break

    audio = sr.AudioData(b''.join(chunk.frame_data for chunk in audio_data), audio_chunk.sample_rate, 2)

    try:
        text = recognizer.recognize_google(audio,language="ta")

        to_translate = text
        translated = GoogleTranslator(source='auto', target='en').translate(to_translate) # type: ignore


        return jsonify({'text': translated})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': 'Error with the request to Google API: ' + str(e)})
    except sr.WaitTimeoutError:
        print("Timeout: No audio detected within the specified timeout.")







@app.route('/get_gpt3_response', methods=['POST'])
def get_gpt3_response():
    data = request.get_json()
    prompt_text = data.get('prompt_text', '')

        # Call the GPT-3 API
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_text,
            max_tokens=150
        )

    gpt3_response = response['choices'][0]['text'] # type: ignore
    return jsonify(gpt3_response=gpt3_response)


@app.route('/get_gpt3_response_tamil', methods=['POST'])
def get_gpt3_response_tamil():
    data = request.get_json()
    prompt_text = data.get('prompt_text', '')

        # Call the GPT-3 API
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_text,
            max_tokens=150
        )

    x = response['choices'][0]['text'] # type: ignore

    to_translate = x
    gpt3_response = GoogleTranslator(source='en', target='ta').translate(to_translate)
    tts = gTTS(text=gpt3_response, lang='ta')
    audio_filename = f'output_{time.time()}.mp3'
    audio_path = os.path.join('static', audio_filename)
    tts.save(audio_path)

    return jsonify(gpt3_response=gpt3_response, audio_url=audio_path)










if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
