import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from services.llm_service import get_chatbot_response

class ChatHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(200, {"ok": True})

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_json(404, {"error": "Endpoint not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 10000:
                self.send_json(413, {"error": "Message is too large"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            message = payload.get("message", "")
            if not isinstance(message, str):
                self.send_json(400, {"error": "Message must be text"})
                return
            reply = get_chatbot_response(message)
            self.send_json(200, {"reply": reply})
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid request"})
        except Exception:
            self.send_json(500, {"error": "Sorry, something went wrong."})

    def log_message(self, fmt, *args):
        print("[BuildWise API] " + (fmt % args))

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), ChatHandler)
    print("BuildWise chatbot API running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping BuildWise chatbot API.")
        server.server_close()
