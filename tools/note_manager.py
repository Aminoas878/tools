import os
import json
import datetime
from typing import List, Dict, Any

class NoteManager:
    """笔记管理系统，用于创建、存储、分类和搜索学习笔记"""
    
    def __init__(self, storage_path: str = "notes"):
        """初始化笔记管理器
        
        Args:
            storage_path: 笔记存储路径
        """
        self.storage_path = storage_path
        self.notes_file = os.path.join(storage_path, "notes.json")
        self.notes = []
        
        # 确保存储目录存在
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            
        # 加载现有笔记
        self._load_notes()
    
    def _load_notes(self) -> None:
        """从文件加载笔记"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                print("笔记文件损坏，创建新的笔记文件")
                self.notes = []
    
    def _save_notes(self) -> None:
        """保存笔记到文件"""
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
    
    def add_note(self, title: str, content: str, tags: List[str] = None) -> Dict[str, Any]:
        """添加新笔记
        
        Args:
            title: 笔记标题
            content: 笔记内容
            tags: 笔记标签列表
            
        Returns:
            新创建的笔记
        """
        if tags is None:
            tags = []
            
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.notes.append(note)
        self._save_notes()
        return note
    
    def get_all_notes(self) -> List[Dict[str, Any]]:
        """获取所有笔记
        
        Returns:
            笔记列表
        """
        return self.notes
    
    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """搜索笔记
        
        Args:
            query: 搜索关键词
            
        Returns:
            匹配的笔记列表
        """
        query = query.lower()
        results = []
        
        for note in self.notes:
            if (query in note["title"].lower() or 
                query in note["content"].lower() or
                any(query in tag.lower() for tag in note["tags"])):
                results.append(note)
                
        return results
    
    def get_notes_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """按标签获取笔记
        
        Args:
            tag: 标签名称
            
        Returns:
            包含指定标签的笔记列表
        """
        return [note for note in self.notes if tag in note["tags"]]
    
    def update_note(self, note_id: int, title: str = None, content: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """更新笔记
        
        Args:
            note_id: 笔记ID
            title: 新标题（可选）
            content: 新内容（可选）
            tags: 新标签列表（可选）
            
        Returns:
            更新后的笔记，如果笔记不存在则返回None
        """
        for note in self.notes:
            if note["id"] == note_id:
                if title is not None:
                    note["title"] = title
                if content is not None:
                    note["content"] = content
                if tags is not None:
                    note["tags"] = tags
                    
                note["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_notes()
                return note
                
        return None
    
    def delete_note(self, note_id: int) -> bool:
        """删除笔记
        
        Args:
            note_id: 笔记ID
            
        Returns:
            是否成功删除
        """
        for i, note in enumerate(self.notes):
            if note["id"] == note_id:
                del self.notes[i]
                self._save_notes()
                return True
                
        return False
    
    def get_tags_summary(self) -> Dict[str, int]:
        """获取标签统计
        
        Returns:
            标签及其出现次数的字典
        """
        tags_count = {}
        
        for note in self.notes:
            for tag in note["tags"]:
                if tag in tags_count:
                    tags_count[tag] += 1
                else:
                    tags_count[tag] = 1
                    
        return tags_count

def interactive_mode():
    """交互式笔记管理"""
    note_manager = NoteManager()
    
    while True:
        print("\n===== 笔记管理系统 =====")
        print("1. 添加笔记")
        print("2. 查看所有笔记")
        print("3. 搜索笔记")
        print("4. 按标签查看笔记")
        print("5. 更新笔记")
        print("6. 删除笔记")
        print("7. 查看标签统计")
        print("0. 退出")
        
        choice = input("\n请选择操作: ")
        
        if choice == "1":
            title = input("请输入笔记标题: ")
            content = input("请输入笔记内容: ")
            tags_input = input("请输入笔记标签（用逗号分隔）: ")
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            note = note_manager.add_note(title, content, tags)
            print(f"笔记已添加，ID: {note['id']}")
            
        elif choice == "2":
            notes = note_manager.get_all_notes()
            if not notes:
                print("没有笔记")
            else:
                print("\n所有笔记:")
                for note in notes:
                    print(f"ID: {note['id']}, 标题: {note['title']}, 标签: {', '.join(note['tags'])}")
                    
        elif choice == "3":
            query = input("请输入搜索关键词: ")
            results = note_manager.search_notes(query)
            
            if not results:
                print("没有找到匹配的笔记")
            else:
                print(f"\n找到 {len(results)} 条匹配的笔记:")
                for note in results:
                    print(f"ID: {note['id']}, 标题: {note['title']}, 标签: {', '.join(note['tags'])}")
                    
        elif choice == "4":
            tag = input("请输入标签: ")
            notes = note_manager.get_notes_by_tag(tag)
            
            if not notes:
                print(f"没有包含标签 '{tag}' 的笔记")
            else:
                print(f"\n包含标签 '{tag}' 的笔记:")
                for note in notes:
                    print(f"ID: {note['id']}, 标题: {note['title']}")
                    
        elif choice == "5":
            note_id = int(input("请输入要更新的笔记ID: "))
            title = input("请输入新标题（留空保持不变）: ")
            content = input("请输入新内容（留空保持不变）: ")
            tags_input = input("请输入新标签（用逗号分隔，留空保持不变）: ")
            
            title = title if title else None
            content = content if content else None
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else None
            
            updated_note = note_manager.update_note(note_id, title, content, tags)
            
            if updated_note:
                print("笔记已更新")
            else:
                print(f"未找到ID为 {note_id} 的笔记")
                
        elif choice == "6":
            note_id = int(input("请输入要删除的笔记ID: "))
            success = note_manager.delete_note(note_id)
            
            if success:
                print("笔记已删除")
            else:
                print(f"未找到ID为 {note_id} 的笔记")
                
        elif choice == "7":
            tags_summary = note_manager.get_tags_summary()
            
            if not tags_summary:
                print("没有标签")
            else:
                print("\n标签统计:")
                for tag, count in sorted(tags_summary.items(), key=lambda x: x[1], reverse=True):
                    print(f"{tag}: {count}条笔记")
                    
        elif choice == "0":
            print("感谢使用笔记管理系统！")
            break
            
        else:
            print("无效的选择，请重试")

if __name__ == "__main__":
    interactive_mode() 