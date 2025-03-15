import sqlite3
import pandas as pd
from datetime import datetime

class WrongQuestionManager:
    def __init__(self):
        self.conn = sqlite3.connect('wrong_questions.db')
        self._create_table()
    
    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS questions
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          question TEXT NOT NULL,
                          subject TEXT,
                          error_count INTEGER DEFAULT 1,
                          last_error DATE)''')
    
    def add_question(self, question, subject):
        check = self.conn.execute('SELECT * FROM questions WHERE question=?', (question,)).fetchone()
        if check:
            new_count = check[3] + 1
            self.conn.execute('UPDATE questions SET error_count=?, last_error=? WHERE id=?',
                            (new_count, datetime.now().date(), check[0]))
        else:
            self.conn.execute('INSERT INTO questions (question, subject, last_error) VALUES (?,?,?)',
                             (question, subject, datetime.now().date()))
        self.conn.commit()
    
    def show_statistics(self):
        df = pd.read_sql('SELECT * FROM questions', self.conn)
        if df.empty:
            print("暂无错题记录")
            return
        
        print("\n=== 错题统计 ===")
        print(f"总错题数: {len(df)}")
        print(f"总错误次数: {df['error_count'].sum()}")
        
        print("\n=== 按学科统计 ===")
        print(df.groupby('subject')['error_count'].agg(['count', 'sum']))
        
        print("\n=== 最近错题 ===")
        print(df.sort_values('last_error', ascending=False).head(5)[['question', 'last_error']])

    def run(self):
        while True:
            print("\n1. 添加错题\n2. 查看统计\n3. 退出")
            choice = input("请选择操作: ")
            if choice == '1':
                question = input("输入错题内容: ")
                subject = input("所属学科: ")
                self.add_question(question, subject)
                print("已记录！")
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                break

if __name__ == "__main__":
    manager = WrongQuestionManager()
    manager.run()