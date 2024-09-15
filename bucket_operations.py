from supabase import create_client, Client
from io import BytesIO
from PIL import Image, ImageOps
from scipy.io import wavfile

url: str = "https://hoymimtuzezshkuqcejv.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhveW1pbXR1emV6c2hrdXFjZWp2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMDgwMTksImV4cCI6MjA0MTg4NDAxOX0.yX8rrQx8QHA009vOy8JsIoFIj4eyoL2H7j5PVOxj8_Y"

supabase: Client = create_client(url, key)

def image_downloader(bucket_name, file_path):

    data = supabase.storage.from_(bucket_name).download(file_path)

    #画像の保存
    img_file_path = f".{file_path}"
    img = Image.open(BytesIO(data))
    img.save(img_file_path)

    return img_file_path

def audio_downloader(bucket_name, file_path):

    data = supabase.storage.from_(bucket_name).download(file_path)

    #オーディオの保存
    wav_file_path = f".{file_path}"
    with open(wav_file_path, 'wb') as f:
        f.write(data)

    return wav_file_path


# image_downloader("media","media")
def audio_uploader(bucket_name, file_path):  

    with open(f".{file_path}", 'rb') as f:
        supabase.storage.from_("media").upload(file=f,path=file_path, file_options={"content-type": "audio/mpeg"})
    
    wav_file_path = str(file_path)

    return wav_file_path