from deepface import DeepFace
from PIL import Image
import os
from db_operations import insert_emotion_data

def analyze_image(image_path):
    try:
        # 画像の存在確認
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"画像が見つかりません: {image_path}")

        # 画像の形式確認と変換
        with Image.open(image_path) as img:
            if img.format not in ['JPEG', 'PNG']:
                new_path = image_path.rsplit('.', 1)[0] + '.jpg'
                img.convert('RGB').save(new_path, 'JPEG')
                image_path = new_path

        # DeepFaceで感情分析
        result = DeepFace.analyze(image_path, actions=['emotion'], enforce_detection=False)
        emotions = {k: round(float(v), 2) for k, v in result[0]['emotion'].items()}
        dominant_emotion = max(emotions, key=emotions.get)

        # データベースに結果を保存
        #insert_emotion_data(os.path.basename(image_path), emotions, dominant_emotion)

        # 結果をコンソールに出力
        print(f"画像: {image_path}")
        print(f"感情分析結果:")
        for emotion, score in emotions.items():
            print(f"  {emotion}: {score:.2f}%")
        print(f"主要な感情: {dominant_emotion}")

        return emotions

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    # テスト用の画像パス
    image_path = "./images/test_image.jpg"
    
    # 画像が存在しない場合のエラーメッセージ
    if not os.path.exists(image_path):
        print(f"エラー: テスト画像が見つかりません。'{image_path}' を 'images' フォルダに配置してください。")
    else:
        analyze_image(image_path)