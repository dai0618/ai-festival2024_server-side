import openai

def get_gpt_message(text):
  #APIキーを設定
  openai.api_key = ""
  #推論を実行
  response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
          {"role": "assistant", "content": text}
      ]
  )

  #ChatGPTの回答を出力
  gpt_result = response["choices"][0]["message"]["content"]

  return gpt_result