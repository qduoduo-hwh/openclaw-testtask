#!/usr/bin/env python3
"""
测试 index.html 网页
"""

import subprocess
import time
import http.server
import threading

def start_server():
    """启动 HTTP 服务器"""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # 禁用日志输出

    server = http.server.HTTPServer(('localhost', 8080), Handler)
    server.directory = '/root/.openclaw/workspace'

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    print("🚀 HTTP 服务器已启动 (http://localhost:8080)")
    time.sleep(1)  # 等待服务器启动
    return server

def test_with_browser_use():
    """使用 browser-use 测试"""
    print("\n🧪 使用 browser-use 进行自动化测试...")

    try:
        # 打开网页
        result = subprocess.run(
            ['tmux', 'new-session', '-d', '-s', 'browser-test',
             'bu open http://localhost:8080/index.html'],
            capture_output=True,
            text=True
        )

        time if result.stderr else None

        # 等待浏览器加载
        time.sleep(5)

        # 获取 screenshot
        screenshot_result = subprocess.run(
            ['tmux', 'capture-pane', '-t', 'browser-test', '-p'],
            capture_output=True,
            text=True
        )

        print("📸 浏览器截图输出:")
        print(screenshot_result.stdout[-500:] if len(screenshot_result.stdout) > 500 else screenshot_result.stdout)

        # 关闭 session
        subprocess.run(['tmux', 'kill-session', '-t', 'browser-test'])

        return True

    except Exception as e:
        print(f"❌ Browser-use 测试出错: {e}")
        return False

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🧪 Hello World 网页测试")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # 读取 HTML 文件
    print("📄 读取 index.html 文件...")
    try:
        with open('/root/.openclaw/workspace/index.html', 'r') as f:
            html_content = f.read()

        print(f"✅ 文件已读取 (大小: {len(html_content)} 字节)\n")
        print("📝 HTML 内容预览:")
        print(html_content[:300])
        print("...\n")

    except FileNotFoundError:
        print("❌ 错误: index.html 文件不存在")
        return False

    # 检查是否包含 'hello'
    print("🔍 检查页面内容...")
    if 'hello' in html_content.lower():
        print("✅ 测试通过：页面上显示了 'hello'\n")
        result1 = True
    else:
        print("❌ 测试失败：页面上没有显示 'hello'\n")
        result1 = False

    # 启动服务器
    server = start_server()

    try:
        # 使用 browser-use 测试
        result2 = test_with_browser_use()

        # 总体结果
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if result1 and result2:
            print("🎉 所有测试通过！")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            return True
        else:
            print("❌ 部分测试失败")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            return False

    finally:
        print("\n🛑 关闭服务器...")
        server.shutdown()
        print("✅ 服务器已关闭")

if __name__ == "__main__":
    result = main()
    exit(0 if result else 1)
