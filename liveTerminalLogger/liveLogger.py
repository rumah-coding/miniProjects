# live_logger.py
import http.server
import socketserver
import datetime
from threading import Thread
import time
import os

logs = []
print ("🛠️  Initializing Live Terminal Logger...")
def weblog(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    logs.append(full_msg)
    print(f"📝 {full_msg}")

class LiveLogHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Live Terminal Logger</title>
                <meta http-equiv="refresh" content="2">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    * {
                        box-sizing: border-box;
                    }
                    body {
                        background: #0a0a0a;
                        color: #4ade80; /* hijau neon lembut */
                        font-family: 'SF Mono', 'Courier New', monospace;
                        margin: 0;
                        padding: 16px;
                        line-height: 1.5;
                    }
                    .container {
                        max-width: 900px;
                        margin: 0 auto;
                    }
                    header {
                        text-align: center;
                        margin-bottom: 24px;
                        padding-bottom: 12px;
                        border-bottom: 1px solid #333;
                    }
                    h1 {
                        font-size: 1.8em;
                        margin: 0;
                        color: #00f7ff;
                        letter-spacing: -0.5px;
                    }
                    .subtitle {
                        color: #666;
                        font-size: 0.95em;
                        margin-top: 6px;
                    }
                    .logs {
                        background: #111;
                        border-radius: 10px;
                        padding: 16px;
                        font-size: 1.1em;
                        min-height: 300px;
                        max-height: 70vh;
                        overflow-y: auto;
                    }
                    .log-entry {
                        padding: 8px 0;
                        border-bottom: 1px solid #222;
                    }
                    .log-entry:last-child {
                        border-bottom: none;
                    }
                    .empty {
                        color: #555;
                        text-align: center;
                        padding: 40px 0;
                        font-style: italic;
                    }
                    footer {
                        text-align: center;
                        margin-top: 20px;
                        color: #555;
                        font-size: 0.85em;
                    }
                    @media (max-width: 600px) {
                        body { padding: 12px; }
                        h1 { font-size: 1.5em; }
                        .logs { font-size: 1em; }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1> Live Terminal Logger</h1>
                        <div class="subtitle">Real-time logs from Python → Browser</div>
                    </header>

                    <div class="logs" id="logs">
            """
            if logs:
                for msg in logs:  # tampilkan urut (bukan reversed) — lebih alami seperti terminal
                    html += f'<div class="log-entry">{msg}</div>'
            else:
                html += '<div class="empty">No logs yet... start typing in the terminal!</div>'

            html += """
                    </div>

                    <footer>
                        Auto-refresh every 2s • Built with Python's <code>http.server</code>
                    </footer>
                </div>

                <!-- Auto-scroll ke bawah tiap load -->
                <script>
                    window.scrollTo(0, document.body.scrollHeight);
                </script>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # Sembunyikan log HTTP — jaga terminal tetap bersih
        pass

# Jalankan server di background
def start_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), LiveLogHandler) as httpd:
        httpd.serve_forever()

print("🚀 Starting Live Terminal Logger...")
server_thread = Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(0.3)

print(f"🌐 Open: http://localhost:8000")
print("💡 Type messages below — they'll appear live in your browser!\n")

try:
    while True:
        msg = input(">>> ")
        if msg.strip():
            weblog(msg)
except KeyboardInterrupt:
    print("\n👋 Server stopped.")