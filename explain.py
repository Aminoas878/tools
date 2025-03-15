import random

class ProblemExplainer:
    def __init__(self):
        self.knowledge_base = {
            'geometry': {
                'pattern': ['三角形', '面积', '勾股定理'],
                'explanation': "几何问题一般需要：\n1. 画图辅助理解\n2. 确定已知条件\n3. 应用相关公式\n4. 分步计算验证"
            },
            'algebra': {
                'pattern': ['方程', '变量', '求解'],
                'explanation': "代数问题解法：\n1. 设定未知数\n2. 建立等量关系\n3. 解方程\n4. 验证解的正确性"
            },
            'probability': {
                'pattern': ['概率', '可能性', '组合'],
                'explanation': "概率问题步骤：\n1. 确定样本空间\n2. 计算有利事件\n3. 应用概率公式\n4. 考虑排列组合"
            }
        }
    
    def analyze_question(self, question):
        question = question.lower()
        for category, data in self.knowledge_base.items():
            if any(keyword in question for keyword in data['pattern']):
                return category, data['explanation']
        return 'general', "通用解题思路：\n1. 仔细阅读题目\n2. 分解问题要素\n3. 尝试多种解法\n4. 检查计算过程"

    def explain_problem(self, question):
        category, explanation = self.analyze_question(question)
        print(f"\n=== 题目分析 ===")
        print(f"检测到题型: {category.upper()}")
        print("\n=== 推荐解题步骤 ===")
        print(explanation)
        print("\n=== 拓展建议 ===")
        self._show_additional_resources(category)

    def _show_additional_resources(self, category):
        resources = {
            'geometry': ["1. 复习三角形性质", "2. 练习勾股定理应用题"],
            'algebra': ["1. 练习一元二次方程", "2. 学习方程组解法"],
            'probability': ["1. 复习排列组合", "2. 练习古典概型题"],
            'general': ["1. 整理错题本", "2. 定时复习基础知识"]
        }
        print("\n".join(resources.get(category, resources['general'])))

    def interactive_mode(self):
        while True:
            print("\n输入题目内容（输入q退出）：")
            question = input()
            if question.lower() == 'q':
                break
            self.explain_problem(question)

if __name__ == "__main__":
    explainer = ProblemExplainer()
    explainer.interactive_mode()