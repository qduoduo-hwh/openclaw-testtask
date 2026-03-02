#!/bin/bash
# 设置定时任务

# 添加 cron 任务：每10分钟执行一次统计
(crontab -l 2>/dev/null | grep -v "monitor_calendar.py"; echo "*/10 * * * * cd /root/.openclaw/workspace && python3 monitor_calendar.py >> /tmp/calendar-monitor.log 2>&1") | crontab -

# 显示当前 cron 任务
echo "✅ Cron 任务已设置："
echo "━━━━━━━━━━━━━━━━"
crontab -l | grep "monitor_calendar.py"
echo "━━━━━━━━━━━━━━━━"

# 测试执行一次
echo ""
echo "🧪 测试执行一次统计任务..."
python3 /root/.openclaw/workspace/monitor_calendar.py

echo ""
echo "✅ 设置完成！"
echo "📊 日历访问统计每10分钟会自动发送到飞书"
