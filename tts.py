from scipy.io import wavfile

from style_bert_vits2.constants import BASE_DIR, Languages
from style_bert_vits2.tts_model import TTSModelHolder

from datetime import datetime

def synthesize(device: str = "cpu", style: str = "Neutral", text: str = ""):

    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S")

    # 音声合成モデルが配置されていれば、音声合2成を実行
    model_holder = TTSModelHolder(BASE_DIR / "model_assets", device)
    model = model_holder.get_model("jvnv-M1-jp", "C:/Users/TWRT/Desktop/dual/Style-Bert-VITS2/model_assets/jvnv-M1-jp/jvnv-M1-jp_e158_s14000.safetensors")
    model.load()
    sample_rate, audio_data = model.infer(
        text,
        # 言語 (JP, EN, ZH / JP-Extra モデルの場合は JP のみ)
        language=Languages.JP,
        # 話者 ID (音声合成モデルに複数の話者が含まれる場合のみ必須、単一話者のみの場合は 0)
        speaker_id=0,
        # 感情表現の強さ (0.0 〜 1.0)
        sdp_ratio=0.4,
        # スタイル (Neutral, Happy など)
        style=style,
        # スタイルの強さ (0.0 〜 100.0)
        style_weight=6.0,
    )

    # 音声データを保存
    (BASE_DIR / "audio").mkdir(exist_ok=True, parents=True)
    wav_file_path = BASE_DIR / f"outAudio/{filename}.wav"
    with open(wav_file_path, "wb") as f:
        wavfile.write(f, sample_rate, audio_data)

    return f"/outAudio/{filename}.wav"
# synthesize(device="cuda",style="Fear")
