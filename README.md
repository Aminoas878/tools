﻿# 学习工具集 (Learning Tools)

这个仓库包含了一系列为学生和自学者设计的实用工具，旨在提高学习效率、辅助知识管理和增强学习体验。

## 🔍 工具概览

### 1. 问题解释器 (tools/explain.py)

这是一个智能问题分析工具，能够识别不同类型的学习问题并提供解题思路。

**主要功能：**
- 自动识别问题类型（几何、代数、概率等）
- 提供结构化的解题步骤和方法
- 推荐相关学习资源和练习题
- 交互式问题分析模式

**适用场景：**
- 遇到难以理解的数学问题
- 需要解题思路指导
- 学习不同类型问题的解题方法

### 2. 数据统计分析 (tools/statistics.py)

一个强大的数据统计和分析工具，帮助您处理和可视化学习数据。

**主要功能：**
- 基本统计分析（均值、中位数、标准差等）
- 数据可视化（直方图、散点图、箱线图等）
- 相关性分析和回归分析
- 数据导入导出功能

**适用场景：**
- 分析考试成绩和学习表现
- 处理实验数据和研究结果
- 制作数据报告和可视化图表

### 3. 笔记管理器 (tools/note_manager.py)

一个功能强大的笔记管理系统，帮助您组织和检索学习笔记。

**主要功能：**
- 创建、编辑和删除笔记
- 使用标签系统分类笔记
- 全文搜索功能，快速找到需要的信息
- 标签统计和分析，了解学习重点分布

**适用场景：**
- 整理课堂笔记和学习资料
- 构建个人知识库
- 准备考试复习材料

### 4. 单词记忆助手 (tools/vocabulary_trainer.py)

基于艾宾浩斯遗忘曲线设计的单词记忆工具，科学安排复习计划。

**主要功能：**
- 智能复习计划，根据记忆效果调整复习间隔
- 单词测验模式，检验记忆效果
- 详细的学习进度统计
- 标签分类系统，按主题组织单词

**适用场景：**
- 学习外语单词
- 记忆专业术语
- 准备语言考试

### 5. 学习计时器 (tools/study_timer.py)

基于番茄工作法的学习时间管理工具，帮助您保持专注和高效。

**主要功能：**
- 自定义学习和休息时长
- 详细记录和统计学习会话
- 按主题分类学习时间
- 学习提醒通知，防止过度疲劳

**适用场景：**
- 需要长时间专注学习
- 想要追踪学习时间分配
- 提高学习效率和防止拖延

## 💻 安装与使用

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/Aminoas878/tools.git
cd tools

# 安装依赖包
pip install -r requirements.txt
```

### 使用方法

每个工具都可以独立运行：

```python
# 运行问题解释器
python tools/explain.py

# 运行数据统计分析
python tools/statistics.py

# 运行笔记管理器
python tools/note_manager.py

# 运行单词记忆助手
python tools/vocabulary_trainer.py

# 运行学习计时器
python tools/study_timer.py
```

## 📊 数据存储

- 所有工具默认将数据存储在各自的目录中（notes/、vocabulary/、study_timer/、statistics/）
- 数据以JSON格式保存，便于备份和迁移
- 所有数据存储在本地，保护您的隐私

## 🔧 自定义与扩展

每个工具都提供了丰富的自定义选项：

- 笔记管理器：自定义标签系统
- 单词记忆助手：调整复习算法参数
- 学习计时器：自定义工作和休息时间
- 数据统计分析：自定义图表样式和分析参数

高级用户可以通过修改源代码进一步扩展功能。

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加一些很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## ❤️ 赞助支持

如果您觉得这些工具对您有所帮助，欢迎通过GitHub Sponsors支持我的工作！您的赞助将帮助我：

- 开发更多实用学习工具
- 改进现有功能和用户体验
- 提供更好的文档和教程
- 维护和更新代码库
### 国外用户（PayPal/信用卡）

### 国内用户（支付宝）
<div align="center">
  <img src="https://github.com/Aminoas878/tools/raw/master/docs/sponsors/qrcode_2drainbow.png" width="300" alt="赞助二维码">
  <br>
  <small>扫码后内容自动更新，有效期至2024-12-31</small>
</div>

## 📜 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件 
