# 修仙小说AI生成系统

这是一套完整的AI生成长篇中文传统修仙小说的系统，支持从世界观设定到章节生成的全流程自动化创作。

## 🌟 系统特色

- **完整流程覆盖**：从世界观构建到章节内容生成的全链路支持
- **传统修仙风格**：专门针对中文修仙小说的文化背景和写作特点
- **AI内容生成**：支持多种AI API接入（OpenAI、Claude等）
- **百万字规模**：支持300万字长篇小说的规划和生成
- **结构化管理**：完善的项目管理和进度跟踪系统
- **可扩展设计**：模块化架构，易于功能扩展和定制

## 📋 核心流程

### 1. 世界观设定 (World Building)
- **修炼等级体系**：从凡人到仙帝的完整境界划分
- **门派势力**：正派、邪派、中立派的详细设定
- **地域划分**：五大修仙区域（东荒、中州、西漠、南荒、北冥）
- **法术体系**：五行、剑道、丹道、阵法等修炼路径
- **法宝分级**：从法器到先天灵宝的完整体系
- **背景故事**：千年正邪大战的历史背景

### 2. 角色设定 (Character Creation)
- **主角设定**：天才少年，极品五行灵根
- **师父导师**：隐世高人，传授修炼之道
- **同门师兄弟**：正面反面角色的复杂关系
- **女主角色**：青梅竹马或门派仙子
- **反派角色**：从门内小人到魔道巨擘
- **配角长辈**：门派长老、家族前辈等

### 3. 大纲生成 (Outline Creation)
#### 四大阶段规划：
- **入门期** (1-50章)：获得机缘，初入修仙世界
- **成长期** (51-150章)：历练成长，结识伙伴
- **崛起期** (151-250章)：声名鹊起，面临大敌
- **巅峰期** (251-300章)：巅峰对决，拯救世界

### 4. 章节细节概括 (Chapter Outline)
每章包含：
- 章节标题（吸引眼球）
- 主要事件列表（3-5个情节点）
- 角色发展描述
- 剧情推进要点
- 修炼进展情况
- 冲突和矛盾设置
- 情感发展线索
- 下章预告铺垫

### 5. 章节内容生成 (Content Generation)
- **字数控制**：每章约3000字
- **文风统一**：传统修仙小说风格
- **结构完整**：起承转合的章节结构
- **对话生动**：符合角色性格的对话
- **描写细腻**：环境描写和心理描写并重
- **节奏把控**：紧张悬念与舒缓节奏的平衡

### 6. 生成后总结 (Post-Generation Summary)
- **本章总结**：主要情节和关键事件
- **角色变化**：实力提升和心境成长
- **重要伏笔**：为后续剧情埋下线索
- **情感发展**：角色关系的变化
- **下章设置**：下一章的创作方向指导

## 🏗️ 系统架构

```
novel_generator.py          # 基础生成器类
├── WorldSetting           # 世界观设定数据类
├── Character              # 角色设定数据类
├── ChapterOutline         # 章节大纲数据类
├── Chapter                # 完整章节数据类
└── NovelGenerator         # 主要生成器类

ai_content_generator.py     # AI内容生成模块
├── AIContentGenerator     # AI生成器基类
├── LocalAIGenerator       # 本地模板生成器
├── OpenAIGenerator        # OpenAI API生成器
└── ClaudeGenerator        # Claude API生成器

enhanced_novel_generator.py # 增强版生成器
├── EnhancedNovelGenerator  # 集成所有功能的主类
├── 详细日志记录
├── 进度跟踪管理
└── 批量生成功能

demo_usage.py              # 演示和使用示例
```

## 📁 项目文件结构

生成的每个小说项目都有以下结构：

```
novel_projects/
└── 项目名称/
    ├── project_state.json          # 项目状态信息
    ├── detailed_state.json         # 详细状态信息
    ├── overall_outline.json        # 整体大纲
    ├── settings/
    │   ├── world_setting.json      # 世界观设定
    │   └── characters.json         # 角色设定
    └── chapters/
        ├── chapter_001.json        # 章节详细信息
        ├── chapter_001.txt         # 章节纯文本
        ├── chapter_002.json
        ├── chapter_002.txt
        └── ...
```

## 🚀 快速开始

### 1. 基础使用

```python
from enhanced_novel_generator import EnhancedNovelGenerator

# 创建项目
generator = EnhancedNovelGenerator("我的修仙小说", ai_type="local")

# 完整流程
world = generator.create_enhanced_world_setting()      # 创建世界观
characters = generator.create_enhanced_characters()     # 创建角色
outline = generator.generate_enhanced_outline(300)     # 生成300章大纲

# 生成章节
first_chapter = generator.generate_next_chapter()      # 生成第一章
second_chapter = generator.generate_next_chapter()     # 生成第二章

# 批量生成
chapters = generator.generate_batch_chapters(10)       # 批量生成10章

# 查看进度
report = generator.generate_progress_report()
print(f"完成进度: {report['progress']['completion_rate']}")
```

### 2. 自定义世界观

```python
# 带自定义要求的世界观创建
custom_requirements = """
- 现代都市修仙背景
- 科技与修仙结合
- 国际修仙组织
- 现代科学理论融入修炼体系
"""

world = generator.create_enhanced_world_setting(custom_requirements)
```

### 3. AI API配置

```python
# 使用OpenAI
generator = EnhancedNovelGenerator("项目名", ai_type="openai", ai_api_key="your_api_key")

# 使用Claude
generator = EnhancedNovelGenerator("项目名", ai_type="claude", ai_api_key="your_api_key")
```

## 🔧 AI接入配置

### OpenAI集成
```python
# 在ai_content_generator.py中添加实际的OpenAI调用
import openai

class OpenAIGenerator(AIContentGenerator):
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_length,
            temperature=0.8
        )
        return response.choices[0].message.content
```

### Claude集成
```python
# 使用Anthropic的Claude API
import anthropic

class ClaudeGenerator(AIContentGenerator):
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=max_length,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
```

## 📊 进度追踪

系统提供详细的进度报告：

```python
report = generator.generate_progress_report()

# 包含信息：
# - 项目基本信息
# - 完成进度百分比
# - 当前所在阶段
# - 字数统计
# - 角色和世界观元素统计
# - 最新章节信息
# - 生成日志
```

## 🎨 自定义扩展

### 添加新的AI生成器
```python
class YourAIGenerator(AIContentGenerator):
    def __init__(self, api_key: str):
        super().__init__("your_ai_type", api_key)
        
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        # 实现你的AI调用逻辑
        return generated_content
```

### 自定义章节模板
```python
def custom_chapter_template(chapter_number: int, context: dict) -> str:
    # 根据章节号和上下文生成自定义内容
    return custom_content
```

## 📈 性能优化

- **批量生成**：支持一次生成多个章节
- **状态保存**：自动保存项目进度，支持断点续写
- **内存管理**：大型项目的内存优化
- **并发处理**：支持多线程章节生成（适用于AI API调用）

## 🔍 质量控制

- **内容一致性检查**：确保前后章节的连贯性
- **角色发展跟踪**：监控角色成长轨迹
- **情节逻辑验证**：检测剧情发展的合理性
- **字数控制**：每章字数的精确控制

## 📝 使用示例

运行演示脚本：

```bash
python demo_usage.py
```

选择演示选项：
1. 完整工作流程演示
2. 章节生成详细过程
3. 批量生成功能
4. 自定义功能演示
5. 运行所有演示

## 🐛 常见问题

### Q: 如何修改默认的世界观设定？
A: 在`create_enhanced_world_setting()`方法中修改`WorldSetting`的参数，或者传入`custom_requirements`参数。

### Q: 生成的内容如何保证质量？
A: 系统使用结构化的提示词工程，结合多层次的内容检查和优化。建议接入高质量的AI API以获得更好效果。

### Q: 如何处理大型项目的内存占用？
A: 系统支持分章节保存，可以在生成过程中释放已保存章节的内存。对于超大项目，建议使用批量生成功能。

### Q: 可以中途修改角色设定吗？
A: 是的，可以通过修改`characters`列表和重新保存项目状态来更新角色设定。

## 🤝 贡献指南

欢迎贡献代码、报告bug或提出新功能建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🔮 未来规划

- [ ] 支持更多AI模型接入
- [ ] 图形界面（GUI）开发
- [ ] 多语言支持
- [ ] 云端协作功能
- [ ] 内容质量自动评估
- [ ] 读者反馈集成
- [ ] 自动配图生成
- [ ] 音频朗读功能

---

**注意**：本系统目前使用模板内容作为演示，实际使用时建议接入高质量的AI API以获得更好的生成效果。