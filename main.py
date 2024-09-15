import os
from flask import Flask, request, jsonify
import requests
import json

from tts import synthesize

from analyze_emotion import analyze_image

from bucket_operations import image_downloader, audio_downloader, audio_uploader

from db_operations import get_latest_emotion_data

from gpt import get_gpt_message

from mysql.connector import Error

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.makedirs("./inAudio", exist_ok=True)
os.makedirs("./outAudio", exist_ok=True)
os.makedirs("./images", exist_ok=True)


@app.route('/', methods=['GET','POST'])
def test():
    data = request.data.decode('utf-8')
    image_path = json.loads(data)["image"]

    try:
        save_image_path = image_downloader("media", image_path)
        emotions = analyze_image(save_image_path)
    except Exception as e:
        print(f"画像取得または分析エラー: {e}")
        # データベースから最新の感情データを取得
        #db_emotions = get_latest_emotion_data()
        #if db_emotions:
        #    emotions = {k: v for k, v in db_emotions.items() if k != 'dominant_emotion'}
        #    dominant_emotion = db_emotions['dominant_emotion']
        emotions = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 60, 'sad': 40, 'surprise': 0, 'neutral': 1}
        dominant_emotion = 'neutral'
    else:
        # データベースからも取得できない場合のデフォルト値
        emotions = {'angry': 20, 'disgust': 0, 'fear': 40, 'happy': 0, 'sad': 40, 'surprise': 0, 'neutral': 1}
        dominant_emotion = 'neutral'

    with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()

    emotion_data = f"感情データ、angry:{str(emotions['angry'])}、disgust:{str(emotions['disgust'])}、fear:{str(emotions['fear'])}、happy:{str(emotions['happy'])}、sad:{str(emotions['sad'])}、surprise:{str(emotions['surprise'])}、neutral:{str(emotions['neutral'])}"
    prompt += emotion_data
    script = get_gpt_message(prompt)
    
    if 'dominant_emotion' not in locals():
        dominant_emotion = max(emotions, key=emotions.get)
    print(script)

    emotion_list = {
        "angry": "Angry",
        "disgust": "Disgust",
        "fear": "Fear",
        "happy": "Happy",
        "sad": "Sad",
        "surprise": "Surprise",
        "neutral": "Neutral"
    }

    audio_file_path = synthesize(device="cuda",style=emotion_list[dominant_emotion],text=script)
    audio_uploader("media", audio_file_path)

    post_data = {"audioData" : audio_file_path,"kokoronokoe":script}

    return jsonify(post_data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5555)