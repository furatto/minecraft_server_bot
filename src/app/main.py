import os
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)

@app.route("/", methods=['POST'])
async def interactions():
    #httpリクエストを出力する(デバッグ用)
    print(f"Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)

#jsonリクエストを処理する関数
@verify_key_decorator(os.getenv("DISCORD_PUBKEY"))
def interact(raw_request):
    #type == 1: Discordヘルスチェック サーバーのPINGのようなもの
    if raw_request["type"] == 1:
        response_data = {"type": 1}
    else:
        #data == ユーザが入力したパラメータ
        data = raw_request["data"]
        command_name = data["name"]
        
        if command_name == "hello":
            message_context = "しね"
        elif command_name == "echo":
            original_message = data["options"][0]["value"]
            message_context = f"Echoing: {original_message}"
            
        response_data = {
            #Discordインタラクション: ユーザにメッセージ表示
            "type": 4,
            "data": {"content": message_context}
        }
        
        #Discordが正しく認識するためにjsonfyが必要
        return jsonify{response_data}