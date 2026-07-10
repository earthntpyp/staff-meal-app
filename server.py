# เซิร์ฟเวอร์เมนูพนักงาน — ใช้ Python มาตรฐาน ไม่ต้องติดตั้งอะไรเพิ่ม
# รัน: python3 server.py  แล้วให้ทีมเข้า http://<ไอพีเครื่องนี้>:3939
import json
import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DATA_FILE = os.path.join(BASE_DIR, "data", "community.json")
PORT = int(os.environ.get("PORT", 3939))


def read_community():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []


def write_community(recipes):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        # ให้ browser เช็คเวอร์ชันไฟล์ใหม่ทุกครั้ง — กันผู้ใช้ค้างสูตรเก่าหลัง deploy
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/recipes":
            self._send_json(200, read_community())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/recipes":
            self.send_error(404)
            return
        try:
            length = min(int(self.headers.get("Content-Length", 0)), 100_000)
            raw = json.loads(self.rfile.read(length).decode("utf-8"))
            if not raw.get("name") or not isinstance(raw.get("ingredients"), list) \
                    or not isinstance(raw.get("steps"), list):
                raise ValueError("invalid recipe")
            recipe = {
                "id": str(raw.get("id") or f"c{int(time.time() * 1000)}"),
                "name": str(raw["name"])[:200],
                "region": str(raw.get("region", "กลาง"))[:50],
                "protein": str(raw.get("protein", "อื่นๆ"))[:50],
                "difficulty": str(raw.get("difficulty", "ปานกลาง"))[:20],
                "time": raw.get("time") if isinstance(raw.get("time"), (int, float)) else None,
                "author": str(raw.get("author", ""))[:100],
                "ingredients": [str(i)[:300] for i in raw["ingredients"][:50]],
                "steps": [str(s)[:500] for s in raw["steps"][:30]],
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            recipes = read_community()
            recipes.append(recipe)
            write_community(recipes)
            self._send_json(201, recipe)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "รูปแบบสูตรไม่ถูกต้อง"})

    def log_message(self, fmt, *args):
        print(f"[staff-meal] {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    print(f"🍳 เมนูพนักงานวันนี้ รันอยู่ที่ http://localhost:{PORT}")
    print(f"   ให้ทีมในร้านเข้าผ่าน http://<ไอพีเครื่องนี้>:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
