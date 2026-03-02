# 日历应用监控配置指南

## 已完成的工作 ✅

### 1. 创建了监控脚本
- `monitor_calendar.py` - 统计访问并发送到飞书
- `calendar_server.py` - 自定义 HTTP 服务器（带访问记录）
- `setup_cron.sh` - 自动设置定时任务

### 2. 服务状态
- ✅ 日历服务器运行在端口 80
- ✅ 访问记录已启用
- ✅ Cron 任务已设置（每10分钟执行一次）

### 3. 当前访问统计
```json
{
"timestamp": "2026-03-03 07:23:02",
"last_10min": 1,
"custom_log": 1,
"nginx_log": 0
}
```

## 需要配置 ⚙️

### 配置飞书 Webhook URL

1. 在飞书中创建一个机器人，获取 Webhook URL
2. 将 URL 保存到文件：

```bash
mkdir -p /root/.openclaw/workspace/logs
echo "你的飞书WebhookURL" > /root/.openclaw/workspace/logs/feishu-webhook.txt
```

3. 测试发送：
```bash
python3 /root/.openclaw/workspace/monitor_calendar.py
```

## 使用说明

### 手动统计
```bash
# 显示统计信息
python3 /root/.openclaw/workspace/monitor_calendar.py stats

# 手动发送报告到飞书
python3 /root/.openclaw/workspace/monitor_calendar.py
```

### 查看定时任务
```bash
crontab -l
```

### 查看日志
```bash
# 监控任务日志
cat /tmp/calendar-monitor.log

# 访问日志
cat /root/.openclaw/workspace/logs/calendar-access.log

# 统计历史
cat /root/.openclaw/workspace/logs/calendar-stats.json
```

### 重启服务
```bash
# 停止当前服务器
pkill -f "calendar_server.py"

# 启动新服务器
nohup python3 /root/.openclaw/workspace/calendar_server.py > /tmp/calendar-server.log 2>&1 &
```

## Cron 定时任务

```cron
*/10 * * * * cd /root/.openclaw/workspace && python3 monitor_calendar.py >> /tmp/calendar-monitor.log 2>&1
```

含义：每10分钟执行一次统计并发送到飞书

## 工作流程

1. 用户访问 http://118.196.41.220
2. calendar_server.py 记录访问到日志文件
3. 每10分钟，monitor_calendar.py 统计最近10分钟的访问量
4. 通过飞书 Webhook 发送统计报告到飞书群
