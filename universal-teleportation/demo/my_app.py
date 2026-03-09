#!/usr/bin/env python3
"""
Demo Application - A Simple Web Server
This app will be teleported across different platforms
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import platform
import os

class DemoAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Generate platform-specific response
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "current_dir": os.getcwd(),
        }
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Demo App - Running on {system_info['platform']}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .platform {{
                    text-align: center;
                    font-size: 1.5em;
                    color: #ffd700;
                    margin-bottom: 30px;
                }}
                .info {{
                    background: rgba(0, 0, 0, 0.3);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                }}
                .label {{
                    font-weight: bold;
                    color: #ffd700;
                }}
                .status {{
                    text-align: center;
                    padding: 20px;
                    background: rgba(76, 175, 80, 0.3);
                    border-radius: 10px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 My Demo Application</h1>
                <div class="platform">Running on: {system_info['platform']}</div>
                
                <div class="info">
                    <div><span class="label">Platform:</span> {system_info['platform']} {system_info['platform_release']}</div>
                    <div><span class="label">Architecture:</span> {system_info['architecture']}</div>
                    <div><span class="label">Hostname:</span> {system_info['hostname']}</div>
                    <div><span class="label">Python Version:</span> {system_info['python_version']}</div>
                    <div><span class="label">Processor:</span> {system_info['processor'] or 'N/A'}</div>
                    <div><span class="label">Working Directory:</span> {system_info['current_dir']}</div>
                </div>
                
                <div class="status">
                    ✅ Application is running successfully!<br>
                    This app was teleported using WekezaOmniOS UAT Engine
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[Demo App] {self.address_string()} - {format % args}")

def run_server(port=8080):
    """Start the demo app server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DemoAppHandler)
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║     🚀 Demo Application Started                          ║
    ║     Platform: {platform.system():<45}║
    ║     URL: http://localhost:{port:<38}║
    ║     Press Ctrl+C to stop                                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Demo App] Shutting down...")
        httpd.shutdown()

if __name__ == '__main__':
    run_server(port=8080)
