from __future__ import annotations

import io
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

import clip
import torch
from PIL import Image


ROOT = Path(__file__).resolve().parent
PUBLIC_DIR = ROOT / "public"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

CAT_THRESHOLD = 0.42

CATEGORIES = [
    {"key": "laranja", "label": "gato laranja", "prompt": "a photo of an orange cat"},
    {"key": "preto", "label": "gato preto", "prompt": "a photo of a black cat"},
    {"key": "frajola", "label": "gato frajola", "prompt": "a photo of a black and white tuxedo cat"},
    {"key": "malhado", "label": "gato malhado", "prompt": "a photo of a striped tabby cat"},
    {"key": "cinza", "label": "gato cinza", "prompt": "a photo of a gray cat"},
    {"key": "branco", "label": "gato branco", "prompt": "a photo of a white cat"},
    {"key": "siames", "label": "gato siamês", "prompt": "a photo of a siamese cat"},
    {"key": "tricolor", "label": "gato tricolor", "prompt": "a photo of a calico cat"},
]

GENERAL_PROMPTS = [
    ("cat", "a photo of a cat"),
    ("dog", "a photo of a dog"),
    ("person", "a photo of a person"),
    ("landscape", "a photo of a landscape"),
    ("food", "a photo of food"),
    ("car", "a photo of a car"),
]

device = "cuda" if torch.cuda.is_available() else "cpu"
model = None
preprocess = None
category_tokens = None
general_tokens = None


def load_model():
    global model, preprocess, category_tokens, general_tokens
    if model is not None:
        return

    model, preprocess = clip.load("ViT-B/32", device=device)
    model.eval()
    category_tokens = clip.tokenize([item["prompt"] for item in CATEGORIES]).to(device)
    general_tokens = clip.tokenize([prompt for _, prompt in GENERAL_PROMPTS]).to(device)


def rank_probabilities(image_tensor, tokens):
    with torch.no_grad():
        logits_per_image, _ = model(image_tensor, tokens)
        return logits_per_image.softmax(dim=-1).cpu().numpy()[0]


def meme_path_for(key: str) -> str:
    for extension in (".png", ".jpg", ".jpeg"):
        candidate = PUBLIC_DIR / "memes" / f"{key}{extension}"
        if candidate.exists():
            return f"/memes/{key}{extension}"
    return ""


def classify_image(image_bytes: bytes) -> dict:
    load_model()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    general_probs = rank_probabilities(image_tensor, general_tokens)
    general_ranking = sorted(
        [
            {"key": key, "prompt": prompt, "probability": float(probability)}
            for (key, prompt), probability in zip(GENERAL_PROMPTS, general_probs)
        ],
        key=lambda item: item["probability"],
        reverse=True,
    )

    best_general = general_ranking[0]
    if best_general["key"] != "cat" or best_general["probability"] < CAT_THRESHOLD:
        return {
            "isCat": False,
            "message": "Oops! Isso não é gato!",
            "generalRanking": general_ranking[:3],
        }

    category_probs = rank_probabilities(image_tensor, category_tokens)
    category_ranking = sorted(
        [
            {
                "key": category["key"],
                "label": category["label"],
                "prompt": category["prompt"],
                "probability": float(probability),
            }
            for category, probability in zip(CATEGORIES, category_probs)
        ],
        key=lambda item: item["probability"],
        reverse=True,
    )

    winner = category_ranking[0]
    return {
        "isCat": True,
        "label": winner["label"],
        "key": winner["key"],
        "confidence": winner["probability"],
        "meme": meme_path_for(winner["key"]),
        "ranking": category_ranking[:3],
        "generalRanking": general_ranking[:3],
    }


def parse_multipart_image(body: bytes, content_type: str) -> bytes | None:
    marker = "boundary="
    if marker not in content_type:
        return None

    boundary = content_type.split(marker, 1)[1].split(";", 1)[0].strip().strip('"')
    delimiter = f"--{boundary}".encode("utf-8")

    for part in body.split(delimiter):
        if b'name="image"' not in part:
            continue
        if b"\r\n\r\n" not in part:
            continue

        _, payload = part.split(b"\r\n\r\n", 1)
        payload = payload.rsplit(b"\r\n", 1)[0]
        if payload:
            return payload
    return None


class CatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/":
            path = "/index.html"

        file_path = (PUBLIC_DIR / path.lstrip("/")).resolve()
        if not file_path.is_relative_to(PUBLIC_DIR.resolve()) or not file_path.exists() or not file_path.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != "/api/classify":
            self.send_error(404)
            return

        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_json({"error": "Envie uma imagem usando multipart/form-data."}, status=400)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        image_bytes = parse_multipart_image(body, content_type)
        if not image_bytes:
            self.send_json({"error": "Campo image não encontrado."}, status=400)
            return

        try:
            result = classify_image(image_bytes)
        except Exception as error:
            self.send_json({"error": str(error)}, status=500)
            return

        self.send_json(result)

    def send_json(self, payload: dict, status: int = 200):
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    server = ThreadingHTTPServer((HOST, PORT), CatHandler)
    print(f"Servidor rodando em http://{HOST}:{PORT}")
    print("Pressione Ctrl+C para parar.")
    server.serve_forever()


if __name__ == "__main__":
    main()
