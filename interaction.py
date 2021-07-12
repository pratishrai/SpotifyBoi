import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from spotify import search_song

load_dotenv()

app = Flask(__name__)


def verify_signature(request):
    PUBLIC_KEY = os.getenv("PUBLIC_KEY")

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")

    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, "invalid request signature")


@app.route("/", methods=["POST"])
def ping():
    verify_signature(request)
    if request.json["type"] == 1:
        return jsonify({"type": 1})
    else:
        song = request.json["data"]["options"][0]["value"]
        search_str = f"{song}"
        if len(request.json["data"]["options"]) > 1:
            artist = request.json["data"]["options"][1]["value"]
            search_str += f" {artist}"
        _song, _artist, link = search_song(search_str)
        if link is not None:
            msg = f"{_song} {link}"
        else:
            msg = "Song not found"
        return jsonify(
            {
                "type": 4,
                "data": {
                    "tts": False,
                    "content": msg,
                },
            }
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
