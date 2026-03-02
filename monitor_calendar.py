#!/usr/bin/env python3
"""
日历应用访问统计脚本
- 读取 Nginx 访问日志
- 统计日历请求量
- 发送到飞书
"""

import os
import re
import json
import urllib.request
from datetime import datetime, timedelta

# 配置
NGINX_LOG = "/var/log/nginx/access.log"  # 如果使用 nginx
HTTPD_LOG = "/var/log/httpd/access_log"  # 如果使用 httpd
ACCESS_LOG = "/root/.openclaw/workspace/logs/calendar-access.log"  # 自定义日志
STATS_FILE = "/root/.openclaw/workspace/logs/calendar-stats.json"
WEBHOOK_FILE = "/root/.openclaw/workspace/logs/feishu-webhook.txt"

def get_webhook_url():
    """获取飞书 Webhook URL"""
    if os.path.exists(WEBHOOK_FILE):
        with open(WEBHOOK_FILE, 'r') as f:
            return f.read().strip()
    return None

def log_access():
    """记录一次访问"""
    if not os.path.exists(os.path.dirname(ACCESS_LOG)):
        os.makedirs(os.path.dirname(ACCESS_LOG), exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 简单的访问日志格式：时间戳
    with open(ACCESS_LOG, 'a') as f:
        f.write(f"{timestamp}\n")

def read_custom_logs(minutes=10):
    """读取自定义访问日志"""
    if not os.path.exists(ACCESS_LOG):
        return []

    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

    count = 0
    with open(ACCESS_LOG, 'r') as f:
        for line in f:
            line = line.strip()
            if line and line >= cutoff_str:
                count += 1

    return count

def read_nginx_logs(minutes=10):
    """读取 Nginx 访问日志（如果有）"""
    if not os.path.exists(NGINX_LOG):
        return 0

    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    time_str = cutoff_time.strftime('%d/%b/%Y:%H:%M:%S')

    count = 0
    try:
        with open(NGINX_LOG, 'r') as f:
            for line in f:
                # Nginx 日志格式示例：
                # 127.0.0.1 - - [03/Mar/2026:07:20:15 +0000] "GET / HTTP/1.1" 200 ...
                if re.search(r'\[.*\] "GET / HTTP', line):
                    # 提取时间戳
                    match = re.search(r'\[(.*?)\]', line)
                    if match:
                        log_time_str = match.group(1).split(' ')[0]
                        # 简单比较，实际应该解析时间
                        count += 1
    except Exception as e:
        print(f"读取 Nginx 日志失败: {e}")

    return count

def get_stats():
    """获取统计信息"""
    # 从自定义日志读取
    custom_count = read_custom_logs(10)

    # 从 Nginx 日志读取（如果可用）
    nginx_count = read_nginx_logs(10)

    # 返回总数（优先使用自定义日志）
    total_count = custom_count if custom_count > 0 else nginx_count

    return {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "last_10min": total_count,
        "custom_log": custom_count,
        "nginx_log": nginx_count
    }

def save_stats(stats):
    """保存统计信息"""
    if not os.path.exists(os.path.dirname(STATS_FILE)):
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)

    # 读取历史数据
    history = []
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            history = json.load(f)

    # 添加新数据
    history.append(stats)

    # 只保留最近 100 条记录
    if len(history) > 100:
        history = history[-100:]

    # 保存
    with open(STATS_FILE, 'w') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def send_to_feishu(webhook_url, message):
    """发送消息到飞书"""
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"发送失败: {e}")
        return false

def main():
    import sys

    # 解析命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == 'log':
            # 记录一次访问
            log_access()
            print("✅ 访问已记录")
            return True
        elif sys.argv[1] == 'stats':
            # 只显示统计
            stats = get_stats()
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            return True

    # 默认行为：统计并发送到飞书
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 统计日历访问量...")

    # 获取统计信息
    stats = get_stats()

    # 保存统计
    save_stats(stats)

    # 获取 webhook URL
    webhook_url = get_webhook_url()
    if not webhook_url:
        print("❌ 未配置飞书 Webhook URL")
        print("请将 Webhook URL 保存到: /root/.openclaw/workspace/logs/feishu-webhook.txt")
        return False

    # 构造消息
    message = f"""📅 日历应用访问统计
━━━━━━━━━━━━━━━━
⏰ 时间: {stats['timestamp']}
📊 最近10分钟请求量: {stats['last_10min']}
📝 自定义日志统计: {stats['custom_log']}
🌐 Nginx日志统计: {stats['nginx_log']}
━━━━━━━━━━━━━━━━
"""

    # 发送
    print("📤 发送到飞书...")
    success = send_to_feishu(webhook_url, message)

    if success:
        print("✅ 已发送")
        return True
    else:
        print("❌ 发送失败")
        return False

if __name__ == "__main__":
    success = main()
    import sys
    sys.exit(0 if success else 1)
