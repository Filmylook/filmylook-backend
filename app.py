import replicate
from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        file.save(temp_file.name)

        output = replicate.run(
            "stability-ai/sdxl:latest",
            input={
                "image": open(temp_file.name, "rb"),
                "prompt": "Convert this person into a 90s Bollywood movie hero portrait. Retro hairstyle, cinematic lighting.",
            }
        )

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)