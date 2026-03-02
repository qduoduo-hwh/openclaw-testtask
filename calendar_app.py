#!/usr/bin/env python3
"""
日历应用
功能：
1. 查看当前月份的日历
2. 指定年月查看日历
3. 添加日程/事件
"""

import calendar
import json
import os
from datetime import datetime
from typing import Dict, List

class CalendarApp:
    def __init__(self):
        self.events_file = '/root/.openclaw/workspace/calendar_events.json'
        self.events = self._load_events()

    def _load_events(self) -> Dict[str, List[str]]:
        """加载事件数据"""
        if os.path.exists(self.events_file):
            with open(self.events_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_events(self):
        """保存事件数据"""
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)

    def show_calendar(self, year=None, month=None):
        """显示日历"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        print(f"\n{'='*50}")
        print(f"📅 {year}年 {month}月")
        print('='*50)

        # 显示日历
        cal = calendar.TextCalendar(calendar.SUNDAY)
        month_str = cal.formatmonth(year, month)
        print(month_str)

        # 显示该月的事件
        month_key = f"{year}-{month:02d}"
        if month_key in self.events:
            print(f"\n📌 {month}月的日程：")
            for date, events in self.events[month_key].items():
                print(f"   {date}: {', '.join(events)}")
        else:
            print(f"\n📌 {month}月暂无日程")

        print('='*50)

    def add_event(self, year, month, day, event):
        """添加事件"""
        month_key = f"{year}-{month:02d}"
        day_key = f"{day}日"

        if month_key not in self.events:
            self.events[month_key] = {}

        if day_key not in self.events[month_key]:
            self.events[month_key][day_key] = []

        self.events[month_key][day_key].append(event)
        self._save_events()

        print(f"✅ 已添加日程：{year}年{month}月{day}日 - {event}")

    def show_events(self, year=None, month=None):
        """显示事件"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month

        month_key = f"{year}-{month:02d}"

        if month_key not in self.events or not self.events[month_key]:
            print(f"📅 {year}年{month}月暂无日程")
            return

        print(f"\n📋 {year}年{month}月的日程：")
        print('='*50)
        for date, events in sorted(self.events[month_key].items()):
            print(f"📌 {date}:")
            for event in events:
                print(f"   • {event}")
        print('='*50)

    def interactive_mode(self):
        """交互模式"""
        print("\n🗓️  欢迎使用日历应用")
        print("="*50)

        while True:
            print("\n请选择操作：")
            print("1. 查看当前月份日历")
            print("2. 查看指定年月日历")
            print("3. 添加日程")
            print("4. 查看日程")
            print("5. 退出")

            choice = input("\n请输入选项 (1-5): ").strip()

            if choice == '1':
                self.show_calendar()

            elif choice == '2':
                try:
                    year = int(input("请输入年份: ").strip())
                    month = int(input("请输入月份 (1-12): ").strip())
                    if 1 <= month <= 12:
                        self.show_calendar(year, month)
                    else:
                        print("❌ 月份无效，请输入 1-12")
                except ValueError:
                    print("❌ 请输入有效的数字")

            elif choice == '3':
                try:
                    year = int(input("请输入年份: ").strip())
                    month = int(input("请输入月份 (1-12): ").strip())
                    day = int(input("请输入日期: ").strip())
                    event = input("请输入日程内容: ").strip()

                    if event:
                        self.add_event(year, month, day, event)
                    else:
                        print("❌ 日程内容不能为空")
                except ValueError:
                    print("❌ 请输入有效的数字")

            elif choice == '4':
                year = input("请输入年份 (留空查看当前年份): ").strip()
                month = input("请输入月份 (留空查看当前月份): ").strip()

                y = int(year) if year else None
                m = int(month) if month else None

                self.show_events(y, m)

            elif choice == '5':
                print("👋 再见！")
                break

            else:
                print("❌ 无效选项，请重新输入")

def main():
    import sys

    app = CalendarApp()

    if len(sys.argv) == 1:
        # 交互模式
        app.interactive_mode()
    else:
        # 命令行模式
        if sys.argv[1] == 'show':
            year = int(sys.argv[2]) if len(sys.argv) > 2 else None
            month = int(sys.argv[3]) if len(sys.argv) > 3 else None
            app.show_calendar(year, month)
        elif sys.argv[1] == 'add':
            if len(sys.argv) >= 5:
                year = int(sys.argv[2])
                month = int(sys.argv[3])
                day = int(sys.argv[4])
                event = ' '.join(sys.argv[5:])
                app.add_event(year, month, day, event)
            else:
                print("用法: python calendar_app.py add <年> <月> <日> <事件内容>")
        elif sys.argv[1] == 'events':
            year = int(sys.argv[2]) if len(sys.argv) > 2 else None
            month = int(sys.argv[3]) if len(sys.argv) > 3 else None
            app.show_events(year, month)
        else:
            print("用法:")
            print("  交互模式: python calendar_app.py")
            print("  查看日历: python calendar_app.py show [年] [月]")
            print("  添加日程: python calendar_app.py add <年> <月> <日> <事件内容>")
            print("  查看日程: python calendar_app.py events [年] [月]")

if __name__ == '__main__':
    main()
