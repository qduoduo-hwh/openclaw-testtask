#!/usr/bin/env python3
"""
自定义 HTTP 服务器 - 日历应用
在每次请求时记录访问量
"""

import http.server
import socketserver
import subprocess
import os
from datetime import datetime

PORT = 80

class CalendarHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""

    def log_message(self, format, *args):
        """禁用默认日志"""
        pass

    def do_GET(self):
        """处理 GET 请求"""
        # 记录访问
        try:
            subprocess.run(
                ['python3', '/root/.openclaw/workspace/monitor_calendar.py', 'log'],
                capture_output=True,
                timeout=5
            )
        except Exception as e:
            print(f"记录访问失败: {e}")

        # 调用父类方法
        super().do_GET()

    def end_headers(self):
        """添加 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server():
    """启动服务器"""
    print(f"🚀 日历应用服务器启动...")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 监听端口: {PORT}")
    print(f"📝 访问日志已启用")

    # 确保在正确的工作目录
    os.chdir('/root/.openclaw/workspace')

    # 使用 socketserver 允许端口复用
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), CalendarHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == "__main__":
    run_server()
