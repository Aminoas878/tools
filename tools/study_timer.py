import os
import json
import time
import datetime
import threading
import platform
from typing import Dict, List, Any, Optional

class StudyTimer:
    """学习计时器，用于管理学习时间和休息时间"""
    
    def __init__(self, storage_path: str = "study_timer"):
        """初始化学习计时器
        
        Args:
            storage_path: 数据存储路径
        """
        self.storage_path = storage_path
        self.sessions_file = os.path.join(storage_path, "sessions.json")
        self.config_file = os.path.join(storage_path, "config.json")
        self.sessions = []
        self.current_session = None
        self.timer_thread = None
        self.running = False
        self.paused = False
        self.elapsed_seconds = 0
        
        # 默认配置
        self.config = {
            "study_duration": 25 * 60,  # 25分钟
            "short_break": 5 * 60,      # 5分钟
            "long_break": 15 * 60,      # 15分钟
            "sessions_before_long_break": 4,
            "notification_enabled": True
        }
        
        # 确保存储目录存在
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
        # 加载现有数据
        self._load_data()
    
    def _load_data(self) -> None:
        """从文件加载会话和配置"""
        # 加载会话
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            except json.JSONDecodeError:
                print("会话文件损坏，创建新的会话文件")
                self.sessions = []
        
        # 加载配置
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 更新默认配置
                    self.config.update(loaded_config)
            except json.JSONDecodeError:
                print("配置文件损坏，使用默认配置")
    
    def _save_sessions(self) -> None:
        """保存会话到文件"""
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)
    
    def _save_config(self) -> None:
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def update_config(self, study_duration: int = None, short_break: int = None,
                     long_break: int = None, sessions_before_long_break: int = None,
                     notification_enabled: bool = None) -> Dict[str, Any]:
        """更新配置
        
        Args:
            study_duration: 学习时长（秒）
            short_break: 短休息时长（秒）
            long_break: 长休息时长（秒）
            sessions_before_long_break: 长休息前的学习次数
            notification_enabled: 是否启用通知
            
        Returns:
            更新后的配置
        """
        if study_duration is not None:
            self.config["study_duration"] = study_duration
        if short_break is not None:
            self.config["short_break"] = short_break
        if long_break is not None:
            self.config["long_break"] = long_break
        if sessions_before_long_break is not None:
            self.config["sessions_before_long_break"] = sessions_before_long_break
        if notification_enabled is not None:
            self.config["notification_enabled"] = notification_enabled
            
        self._save_config()
        return self.config
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置
        
        Returns:
            当前配置
        """
        return self.config
    
    def start_session(self, subject: str = "学习") -> Dict[str, Any]:
        """开始一个新的学习会话
        
        Args:
            subject: 学习主题
            
        Returns:
            新的学习会话
        """
        if self.running:
            self.stop_session()
            
        self.current_session = {
            "id": len(self.sessions) + 1,
            "subject": subject,
            "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "duration": 0,
            "pauses": []
        }
        
        self.running = True
        self.paused = False
        self.elapsed_seconds = 0
        
        # 启动计时器线程
        self.timer_thread = threading.Thread(target=self._timer_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
        return self.current_session
    
    def _timer_loop(self) -> None:
        """计时器循环"""
        start_time = time.time()
        
        while self.running:
            if not self.paused:
                current_time = time.time()
                self.elapsed_seconds = int(current_time - start_time)
                
                # 检查是否达到学习时间
                if self.elapsed_seconds >= self.config["study_duration"] and self.config["notification_enabled"]:
                    self._show_notification("学习时间结束", "该休息一下了！")
                
            time.sleep(1)
    
    def _show_notification(self, title: str, message: str) -> None:
        """显示通知
        
        Args:
            title: 通知标题
            message: 通知内容
        """
        system = platform.system()
        
        try:
            if system == "Windows":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5)
            elif system == "Darwin":  # macOS
                os.system(f"""osascript -e 'display notification "{message}" with title "{title}"'""")
            elif system == "Linux":
                os.system(f"""notify-send "{title}" "{message}" """)
            else:
                print(f"\n{title}: {message}")
        except Exception:
            # 如果通知失败，退回到控制台输出
            print(f"\n{title}: {message}")
    
    def pause_session(self) -> Dict[str, Any]:
        """暂停当前会话
        
        Returns:
            当前会话
        """
        if not self.running or self.paused:
            return self.current_session
            
        self.paused = True
        pause_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.current_session:
            self.current_session["pauses"].append({
                "start_time": pause_time,
                "end_time": None
            })
            
        return self.current_session
    
    def resume_session(self) -> Dict[str, Any]:
        """恢复当前会话
        
        Returns:
            当前会话
        """
        if not self.running or not self.paused:
            return self.current_session
            
        self.paused = False
        resume_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.current_session and self.current_session["pauses"]:
            last_pause = self.current_session["pauses"][-1]
            if last_pause["end_time"] is None:
                last_pause["end_time"] = resume_time
                
        return self.current_session
    
    def stop_session(self) -> Dict[str, Any]:
        """停止当前会话
        
        Returns:
            完成的会话
        """
        if not self.running:
            return None
            
        self.running = False
        
        if self.timer_thread:
            self.timer_thread.join(1)
            
        if self.current_session:
            # 如果会话暂停中，结束最后一个暂停
            if self.paused and self.current_session["pauses"]:
                last_pause = self.current_session["pauses"][-1]
                if last_pause["end_time"] is None:
                    last_pause["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 计算总时长（减去暂停时间）
            total_seconds = self.elapsed_seconds
            pause_seconds = 0
            
            for pause in self.current_session["pauses"]:
                if pause["end_time"] is None:
                    continue
                    
                start = datetime.datetime.strptime(pause["start_time"], "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(pause["end_time"], "%Y-%m-%d %H:%M:%S")
                pause_seconds += (end - start).total_seconds()
                
            self.current_session["duration"] = total_seconds - pause_seconds
            self.current_session["end_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 保存会话
            self.sessions.append(self.current_session)
            self._save_sessions()
            
            completed_session = self.current_session
            self.current_session = None
            return completed_session
            
        return None
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """获取当前会话
        
        Returns:
            当前会话，如果没有则返回None
        """
        if not self.running:
            return None
            
        # 创建会话的副本，添加当前状态
        session_copy = self.current_session.copy() if self.current_session else None
        
        if session_copy:
            session_copy["elapsed_seconds"] = self.elapsed_seconds
            session_copy["status"] = "paused" if self.paused else "running"
            
        return session_copy
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """获取所有会话
        
        Returns:
            会话列表
        """
        return self.sessions
    
    def get_sessions_by_date(self, date: str) -> List[Dict[str, Any]]:
        """按日期获取会话
        
        Args:
            date: 日期字符串 (YYYY-MM-DD)
            
        Returns:
            指定日期的会话列表
        """
        return [session for session in self.sessions 
                if session["start_time"].startswith(date)]
    
    def get_sessions_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        """按主题获取会话
        
        Args:
            subject: 学习主题
            
        Returns:
            指定主题的会话列表
        """
        subject = subject.lower()
        return [session for session in self.sessions 
                if subject in session["subject"].lower()]
    
    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """获取学习统计
        
        Args:
            days: 统计的天数
            
        Returns:
            学习统计信息
        """
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=days-1)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 按日期分组
        daily_stats = {}
        for i in range(days):
            date = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            daily_stats[date] = {"total_duration": 0, "sessions_count": 0}
        
        # 按主题分组
        subjects = {}
        
        # 总计
        total_duration = 0
        total_sessions = 0
        
        for session in self.sessions:
            session_start = datetime.datetime.strptime(session["start_time"], "%Y-%m-%d %H:%M:%S")
            
            if session_start >= start_date:
                date = session_start.strftime("%Y-%m-%d")
                
                if date in daily_stats:
                    daily_stats[date]["total_duration"] += session["duration"]
                    daily_stats[date]["sessions_count"] += 1
                
                subject = session["subject"]
                if subject in subjects:
                    subjects[subject]["total_duration"] += session["duration"]
                    subjects[subject]["sessions_count"] += 1
                else:
                    subjects[subject] = {
                        "total_duration": session["duration"],
                        "sessions_count": 1
                    }
                
                total_duration += session["duration"]
                total_sessions += 1
        
        return {
            "total_duration": total_duration,
            "total_sessions": total_sessions,
            "daily_stats": daily_stats,
            "subjects": subjects
        }
    
    def format_duration(self, seconds: int) -> str:
        """格式化时长
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化后的时长字符串
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours}小时{minutes}分钟{seconds}秒"
        elif minutes > 0:
            return f"{minutes}分钟{seconds}秒"
        else:
            return f"{seconds}秒"

def interactive_mode():
    """交互式学习计时器"""
    timer = StudyTimer()
    
    while True:
        print("\n===== 学习计时器 =====")
        
        current_session = timer.get_current_session()
        if current_session:
            status = "暂停中" if current_session["status"] == "paused" else "进行中"
            elapsed = timer.format_duration(current_session["elapsed_seconds"])
            print(f"当前会话: {current_session['subject']} ({status}, 已学习 {elapsed})")
            print("1. 暂停/恢复会话")
            print("2. 结束会话")
        else:
            print("没有进行中的会话")
            print("1. 开始新会话")
        
        print("3. 查看今日学习")
        print("4. 查看学习统计")
        print("5. 查看所有会话")
        print("6. 按主题查找会话")
        print("7. 设置")
        print("0. 退出")
        
        choice = input("\n请选择操作: ")
        
        if choice == "1":
            if current_session:
                if current_session["status"] == "paused":
                    timer.resume_session()
                    print("会话已恢复")
                else:
                    timer.pause_session()
                    print("会话已暂停")
            else:
                subject = input("请输入学习主题: ")
                timer.start_session(subject)
                print(f"已开始 '{subject}' 学习会话")
                
        elif choice == "2" and current_session:
            session = timer.stop_session()
            duration = timer.format_duration(session["duration"])
            print(f"会话已结束，总学习时间: {duration}")
            
        elif choice == "3":
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            sessions = timer.get_sessions_by_date(today)
            
            if not sessions:
                print("今天还没有学习记录")
            else:
                total_seconds = sum(session["duration"] for session in sessions)
                total_time = timer.format_duration(total_seconds)
                
                print(f"\n今日学习 ({len(sessions)}个会话, 总计 {total_time}):")
                for i, session in enumerate(sessions):
                    duration = timer.format_duration(session["duration"])
                    start_time = session["start_time"].split()[1]
                    end_time = session["end_time"].split()[1] if session["end_time"] else "进行中"
                    print(f"{i+1}. {session['subject']}: {start_time} - {end_time}, 时长 {duration}")
                    
        elif choice == "4":
            days = input("请输入统计天数 (默认7天): ")
            try:
                days = int(days) if days else 7
                stats = timer.get_statistics(days)
                
                total_time = timer.format_duration(stats["total_duration"])
                print(f"\n===== 学习统计 (近{days}天) =====")
                print(f"总学习时间: {total_time}")
                print(f"总会话数: {stats['total_sessions']}")
                
                print("\n每日学习时间:")
                for date, data in sorted(stats["daily_stats"].items()):
                    time_str = timer.format_duration(data["total_duration"])
                    print(f"{date}: {time_str} ({data['sessions_count']}个会话)")
                
                print("\n按主题统计:")
                sorted_subjects = sorted(stats["subjects"].items(), 
                                        key=lambda x: x[1]["total_duration"], 
                                        reverse=True)
                for subject, data in sorted_subjects:
                    time_str = timer.format_duration(data["total_duration"])
                    print(f"{subject}: {time_str} ({data['sessions_count']}个会话)")
                    
            except ValueError:
                print("无效的天数，使用默认值7")
                
        elif choice == "5":
            sessions = timer.get_all_sessions()
            if not sessions:
                print("没有学习记录")
            else:
                print(f"\n所有学习会话 ({len(sessions)}个):")
                for i, session in enumerate(sessions[-10:]):  # 只显示最近10个
                    duration = timer.format_duration(session["duration"])
                    print(f"{i+1}. [{session['start_time']}] {session['subject']}, 时长 {duration}")
                
                if len(sessions) > 10:
                    print(f"... 还有 {len(sessions) - 10} 个会话未显示")
                    
        elif choice == "6":
            subject = input("请输入要查找的主题: ")
            sessions = timer.get_sessions_by_subject(subject)
            
            if not sessions:
                print(f"没有找到与 '{subject}' 相关的会话")
            else:
                total_seconds = sum(session["duration"] for session in sessions)
                total_time = timer.format_duration(total_seconds)
                
                print(f"\n找到 {len(sessions)} 个相关会话, 总计 {total_time}:")
                for i, session in enumerate(sessions):
                    duration = timer.format_duration(session["duration"])
                    print(f"{i+1}. [{session['start_time']}] {session['subject']}, 时长 {duration}")
                    
        elif choice == "7":
            print("\n===== 设置 =====")
            print("1. 修改学习时长")
            print("2. 修改休息时长")
            print("3. 修改通知设置")
            print("0. 返回")
            
            setting_choice = input("\n请选择设置: ")
            
            if setting_choice == "1":
                minutes = input("请输入学习时长(分钟): ")
                try:
                    minutes = int(minutes)
                    timer.update_config(study_duration=minutes * 60)
                    print(f"学习时长已设置为 {minutes} 分钟")
                except ValueError:
                    print("无效的时间")
                    
            elif setting_choice == "2":
                short_break = input("请输入短休息时长(分钟): ")
                long_break = input("请输入长休息时长(分钟): ")
                sessions = input("请输入长休息前的学习次数: ")
                
                try:
                    config_updates = {}
                    if short_break:
                        config_updates["short_break"] = int(short_break) * 60
                    if long_break:
                        config_updates["long_break"] = int(long_break) * 60
                    if sessions:
                        config_updates["sessions_before_long_break"] = int(sessions)
                        
                    timer.update_config(**config_updates)
                    print("休息设置已更新")
                except ValueError:
                    print("无效的时间")
                    
            elif setting_choice == "3":
                enabled = input("是否启用通知 (y/n): ").lower()
                if enabled in ("y", "n"):
                    timer.update_config(notification_enabled=(enabled == "y"))
                    status = "启用" if enabled == "y" else "禁用"
                    print(f"通知已{status}")
                    
        elif choice == "0":
            if timer.get_current_session():
                confirm = input("有正在进行的会话，确定要退出吗? (y/n): ").lower()
                if confirm != "y":
                    continue
                    
                timer.stop_session()
                
            print("感谢使用学习计时器！")
            break
            
        else:
            print("无效的选择，请重试")

if __name__ == "__main__":
    interactive_mode() 