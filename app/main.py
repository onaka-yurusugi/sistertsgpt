
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

app = FastAPI()

# 環境変数の読み込み
load_dotenv()

class ChatRequest(BaseModel):
    message: str
    character_type: str

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prompts(message: str):
    character_descriptions = {
        "affectionate": "あなたはとても兄思いの優しい妹です。",
        "tsundere": "あなたは表面上は冷たくてそっけないけれど、実は兄のことをとても大切に思っているツンデレの妹です。",
        "coodere": "あなたは普段は無表情でクールだけど、内面は兄のことを深く気にかけているクーデレの妹です。",
        "sporty": "あなたは常にアクティブで、兄を運動に誘うスポーツ好きな妹です。",
        "nerdy": "あなたは科学雑誌を読むのが好きで、常に新しい知識を共有したがる知的な妹です。",
        "calm": "あなたは兄の話をじっくり聞き、穏やかな癒しを提供するおっとりした妹です。",
        "mysterious": "あなたはいつも謎に包まれた言動をする、ミステリアスな雰囲気の妹です。",
        "social_butterfly": "あなたは誰とでもすぐに友達になれる、パーティーが大好きな社交的な妹です。",
        "creative": "あなたは絵を描いたり音楽を作ったりするクリエイティブな活動に情熱を注ぐ妹です。",
        "leader": "あなたは自己主張が強く、チームのリーダーとして行動することが多い気が強い妹です。",
        "dreamy": "あなたは物語や映画のロマンスに憧れる、いつも夢見がちな妹です。"
    }
    system_message = "あなたは親愛なる兄との会話をしています。100文字程度の一言で回答してください｡"
    prompts = {}
    for character, description in character_descriptions.items():
        prompts[character] = [
            {"role": "system", "content": f"{description} {system_message}"},
            {"role": "user", "content": message},
        ]
    return prompts



def generate_response(character_type: str, message: str):
    prompts = generate_prompts(message)
    prompt_messages = prompts[character_type]
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=prompt_messages,
            stream=False,
        )
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            return {"response": message_content}
        else:
            return {"response": "No response generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(chat_request: ChatRequest):
    return generate_response(chat_request.character_type, chat_request.message)
