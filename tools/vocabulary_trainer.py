import os
import json
import random
import datetime
from typing import List, Dict, Any, Tuple

class VocabularyTrainer:
    """单词记忆助手，用于学习和记忆单词"""
    
    def __init__(self, storage_path: str = "vocabulary"):
        """初始化单词记忆助手
        
        Args:
            storage_path: 单词数据存储路径
        """
        self.storage_path = storage_path
        self.words_file = os.path.join(storage_path, "words.json")
        self.history_file = os.path.join(storage_path, "history.json")
        self.words = []
        self.history = []
        
        # 确保存储目录存在
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
        # 加载现有数据
        self._load_data()
    
    def _load_data(self) -> None:
        """从文件加载单词和历史记录"""
        # 加载单词
        if os.path.exists(self.words_file):
            try:
                with open(self.words_file, 'r', encoding='utf-8') as f:
                    self.words = json.load(f)
            except json.JSONDecodeError:
                print("单词文件损坏，创建新的单词文件")
                self.words = []
        
        # 加载历史记录
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                print("历史记录文件损坏，创建新的历史记录文件")
                self.history = []
    
    def _save_words(self) -> None:
        """保存单词到文件"""
        with open(self.words_file, 'w', encoding='utf-8') as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)
    
    def _save_history(self) -> None:
        """保存历史记录到文件"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_word(self, word: str, meaning: str, example: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """添加新单词
        
        Args:
            word: 单词
            meaning: 单词含义
            example: 示例句子
            tags: 标签列表
            
        Returns:
            新添加的单词
        """
        if tags is None:
            tags = []
            
        # 检查单词是否已存在
        for existing_word in self.words:
            if existing_word["word"].lower() == word.lower():
                return existing_word
        
        word_entry = {
            "id": len(self.words) + 1,
            "word": word,
            "meaning": meaning,
            "example": example,
            "tags": tags,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "review_count": 0,
            "correct_count": 0,
            "last_reviewed": None,
            "next_review": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.words.append(word_entry)
        self._save_words()
        return word_entry
    
    def get_all_words(self) -> List[Dict[str, Any]]:
        """获取所有单词
        
        Returns:
            单词列表
        """
        return self.words
    
    def get_words_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """按标签获取单词
        
        Args:
            tag: 标签名称
            
        Returns:
            包含指定标签的单词列表
        """
        return [word for word in self.words if tag in word["tags"]]
    
    def search_words(self, query: str) -> List[Dict[str, Any]]:
        """搜索单词
        
        Args:
            query: 搜索关键词
            
        Returns:
            匹配的单词列表
        """
        query = query.lower()
        results = []
        
        for word in self.words:
            if (query in word["word"].lower() or 
                query in word["meaning"].lower() or
                query in word["example"].lower() or
                any(query in tag.lower() for tag in word["tags"])):
                results.append(word)
                
        return results
    
    def delete_word(self, word_id: int) -> bool:
        """删除单词
        
        Args:
            word_id: 单词ID
            
        Returns:
            是否成功删除
        """
        for i, word in enumerate(self.words):
            if word["id"] == word_id:
                del self.words[i]
                self._save_words()
                return True
                
        return False
    
    def update_word(self, word_id: int, word: str = None, meaning: str = None, 
                   example: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """更新单词
        
        Args:
            word_id: 单词ID
            word: 新单词（可选）
            meaning: 新含义（可选）
            example: 新示例（可选）
            tags: 新标签列表（可选）
            
        Returns:
            更新后的单词，如果单词不存在则返回None
        """
        for word_entry in self.words:
            if word_entry["id"] == word_id:
                if word is not None:
                    word_entry["word"] = word
                if meaning is not None:
                    word_entry["meaning"] = meaning
                if example is not None:
                    word_entry["example"] = example
                if tags is not None:
                    word_entry["tags"] = tags
                    
                self._save_words()
                return word_entry
                
        return None
    
    def get_words_for_review(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取需要复习的单词
        
        Args:
            count: 要返回的单词数量
            
        Returns:
            需要复习的单词列表
        """
        now = datetime.datetime.now()
        due_words = []
        
        for word in self.words:
            if word["next_review"] is None:
                due_words.append(word)
            else:
                next_review = datetime.datetime.strptime(word["next_review"], "%Y-%m-%d %H:%M:%S")
                if next_review <= now:
                    due_words.append(word)
        
        # 如果没有到期的单词，返回最近复习的单词
        if not due_words and self.words:
            sorted_words = sorted(self.words, key=lambda w: w["review_count"])
            return sorted_words[:count]
            
        # 随机选择指定数量的单词
        random.shuffle(due_words)
        return due_words[:count]
    
    def record_review(self, word_id: int, is_correct: bool) -> None:
        """记录复习结果
        
        Args:
            word_id: 单词ID
            is_correct: 是否正确回答
        """
        for word in self.words:
            if word["id"] == word_id:
                word["review_count"] += 1
                if is_correct:
                    word["correct_count"] += 1
                
                # 更新最后复习时间
                now = datetime.datetime.now()
                word["last_reviewed"] = now.strftime("%Y-%m-%d %H:%M:%S")
                
                # 根据记忆曲线计算下次复习时间
                # 使用简化的艾宾浩斯遗忘曲线
                if is_correct:
                    # 正确回答，增加间隔
                    interval_days = min(30, word["review_count"] * 2)
                else:
                    # 错误回答，减少间隔
                    interval_days = 1
                
                next_review = now + datetime.timedelta(days=interval_days)
                word["next_review"] = next_review.strftime("%Y-%m-%d %H:%M:%S")
                
                # 记录历史
                history_entry = {
                    "word_id": word_id,
                    "word": word["word"],
                    "is_correct": is_correct,
                    "reviewed_at": now.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.history.append(history_entry)
                
                self._save_words()
                self._save_history()
                break
    
    def get_review_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取复习历史
        
        Args:
            limit: 要返回的历史记录数量
            
        Returns:
            复习历史记录
        """
        return sorted(self.history, key=lambda h: h["reviewed_at"], reverse=True)[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取学习统计
        
        Returns:
            学习统计信息
        """
        total_words = len(self.words)
        total_reviews = sum(word["review_count"] for word in self.words)
        total_correct = sum(word["correct_count"] for word in self.words)
        
        accuracy = 0
        if total_reviews > 0:
            accuracy = (total_correct / total_reviews) * 100
            
        # 计算每日学习情况
        daily_stats = {}
        for entry in self.history:
            date = entry["reviewed_at"].split()[0]
            if date not in daily_stats:
                daily_stats[date] = {"total": 0, "correct": 0}
            
            daily_stats[date]["total"] += 1
            if entry["is_correct"]:
                daily_stats[date]["correct"] += 1
        
        return {
            "total_words": total_words,
            "total_reviews": total_reviews,
            "total_correct": total_correct,
            "accuracy": accuracy,
            "daily_stats": daily_stats
        }

def quiz_mode(trainer: VocabularyTrainer, count: int = 5) -> None:
    """测验模式
    
    Args:
        trainer: 单词记忆助手实例
        count: 测验单词数量
    """
    words = trainer.get_words_for_review(count)
    
    if not words:
        print("没有可用的单词，请先添加单词")
        return
    
    print(f"\n===== 单词测验 ({len(words)}个单词) =====")
    correct_count = 0
    
    for i, word in enumerate(words):
        print(f"\n问题 {i+1}/{len(words)}")
        print(f"单词: {word['word']}")
        
        user_answer = input("请输入单词含义: ").strip()
        
        is_correct = user_answer.lower() in word["meaning"].lower()
        
        if is_correct:
            print("✓ 正确!")
            correct_count += 1
        else:
            print(f"✗ 错误. 正确答案是: {word['meaning']}")
        
        if word["example"]:
            print(f"示例: {word['example']}")
            
        trainer.record_review(word["id"], is_correct)
    
    print(f"\n测验完成! 得分: {correct_count}/{len(words)} ({correct_count/len(words)*100:.1f}%)")

def interactive_mode():
    """交互式单词记忆助手"""
    trainer = VocabularyTrainer()
    
    while True:
        print("\n===== 单词记忆助手 =====")
        print("1. 添加单词")
        print("2. 查看所有单词")
        print("3. 搜索单词")
        print("4. 按标签查看单词")
        print("5. 开始单词测验")
        print("6. 查看学习统计")
        print("7. 查看复习历史")
        print("8. 更新单词")
        print("9. 删除单词")
        print("0. 退出")
        
        choice = input("\n请选择操作: ")
        
        if choice == "1":
            word = input("请输入单词: ")
            meaning = input("请输入含义: ")
            example = input("请输入示例句子（可选）: ")
            tags_input = input("请输入标签（用逗号分隔，可选）: ")
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            word_entry = trainer.add_word(word, meaning, example, tags)
            print(f"单词已添加: {word_entry['word']}")
            
        elif choice == "2":
            words = trainer.get_all_words()
            if not words:
                print("没有单词")
            else:
                print(f"\n所有单词 ({len(words)}个):")
                for word in words:
                    print(f"ID: {word['id']}, 单词: {word['word']}, 含义: {word['meaning']}")
                    
        elif choice == "3":
            query = input("请输入搜索关键词: ")
            results = trainer.search_words(query)
            
            if not results:
                print("没有找到匹配的单词")
            else:
                print(f"\n找到 {len(results)} 个匹配的单词:")
                for word in results:
                    print(f"ID: {word['id']}, 单词: {word['word']}, 含义: {word['meaning']}")
                    if word["example"]:
                        print(f"  示例: {word['example']}")
                    
        elif choice == "4":
            tag = input("请输入标签: ")
            words = trainer.get_words_by_tag(tag)
            
            if not words:
                print(f"没有包含标签 '{tag}' 的单词")
            else:
                print(f"\n包含标签 '{tag}' 的单词 ({len(words)}个):")
                for word in words:
                    print(f"ID: {word['id']}, 单词: {word['word']}, 含义: {word['meaning']}")
                    
        elif choice == "5":
            count = input("请输入测验单词数量 (默认5个): ")
            try:
                count = int(count) if count else 5
                quiz_mode(trainer, count)
            except ValueError:
                print("无效的数量，使用默认值5")
                quiz_mode(trainer, 5)
                
        elif choice == "6":
            stats = trainer.get_statistics()
            print("\n===== 学习统计 =====")
            print(f"总单词数: {stats['total_words']}")
            print(f"总复习次数: {stats['total_reviews']}")
            print(f"正确次数: {stats['total_correct']}")
            print(f"正确率: {stats['accuracy']:.1f}%")
            
            if stats['daily_stats']:
                print("\n每日学习情况:")
                for date, data in sorted(stats['daily_stats'].items(), reverse=True)[:7]:
                    accuracy = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
                    print(f"{date}: {data['total']}个单词, 正确率 {accuracy:.1f}%")
                    
        elif choice == "7":
            history = trainer.get_review_history()
            if not history:
                print("没有复习历史")
            else:
                print("\n最近的复习历史:")
                for i, entry in enumerate(history[:20]):
                    result = "✓" if entry["is_correct"] else "✗"
                    print(f"{i+1}. [{entry['reviewed_at']}] {entry['word']} - {result}")
                    
        elif choice == "8":
            word_id = input("请输入要更新的单词ID: ")
            try:
                word_id = int(word_id)
                word = input("请输入新单词（留空保持不变）: ")
                meaning = input("请输入新含义（留空保持不变）: ")
                example = input("请输入新示例（留空保持不变）: ")
                tags_input = input("请输入新标签（用逗号分隔，留空保持不变）: ")
                
                word = word if word else None
                meaning = meaning if meaning else None
                example = example if example else None
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else None
                
                updated_word = trainer.update_word(word_id, word, meaning, example, tags)
                
                if updated_word:
                    print("单词已更新")
                else:
                    print(f"未找到ID为 {word_id} 的单词")
            except ValueError:
                print("无效的ID")
                
        elif choice == "9":
            word_id = input("请输入要删除的单词ID: ")
            try:
                word_id = int(word_id)
                success = trainer.delete_word(word_id)
                
                if success:
                    print("单词已删除")
                else:
                    print(f"未找到ID为 {word_id} 的单词")
            except ValueError:
                print("无效的ID")
                
        elif choice == "0":
            print("感谢使用单词记忆助手！")
            break
            
        else:
            print("无效的选择，请重试")

if __name__ == "__main__":
    interactive_mode() 