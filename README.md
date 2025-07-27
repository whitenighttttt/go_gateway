# AI修仙小说生成系统

一套完整的AI生成长篇百万字中文传统修仙小说流程系统，包含从世界观构建到章节生成的完整流程。

## 🎯 系统特点

- **完整流程**：从世界观→角色设定→大纲生成→章节生成→质量检查
- **AI驱动**：集成OpenAI等AI模型，自动生成高质量内容
- **数据管理**：SQLite数据库存储，支持数据持久化和备份
- **质量保证**：内置质量检查机制，确保内容质量
- **灵活配置**：模块化设计，支持自定义配置和扩展

## 📋 系统架构

```
AI修仙小说生成系统
├── 世界观构建 (WorldBuilder)
│   ├── 修仙体系设定
│   ├── 地理环境构建
│   └── 历史背景设定
├── 角色管理 (CharacterBuilder)
│   ├── 主角设定
│   ├── 配角创建
│   └── 反派设计
├── 大纲生成 (OutlineGenerator)
│   ├── 卷章规划
│   ├── 情节主线
│   └── 章节大纲
├── 内容生成 (ChapterGenerator)
│   ├── 章节内容生成
│   ├── 质量检查
│   └── 总结规划
└── 数据管理 (NovelDatabase)
    ├── 世界观数据
    ├── 角色数据
    ├── 章节数据
    └── 大纲数据
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd ai-novel-generation

# 安装依赖
pip install -r requirements.txt

# 设置API密钥（可选）
export OPENAI_API_KEY="your-api-key-here"
```

### 2. 运行演示

```bash
# 运行完整演示
python demo.py

# 或者直接运行主系统
python novel_generation_system.py
```

### 3. 基本使用

```python
from novel_generation_system import NovelManager
from ai_integration import OpenAIGenerator, NovelAIGenerator

# 创建小说管理器
novel_manager = NovelManager("我的修仙小说")

# 初始化小说
novel_data = novel_manager.initialize_novel()

# 生成章节
chapter = novel_manager.generate_chapter(1)

# 生成整卷
novel_manager.generate_volume(1)
```

## 📖 详细流程

### 1. 世界观构建阶段

**修仙体系设定**
- 境界划分：练气期→筑基期→金丹期→元婴期→化神期→炼虚期→合体期→大乘期→渡劫期
- 功法分类：心法、功法、秘术、战斗技能、法术、阵法、符箓、丹药、炼器
- 修炼资源：灵石、丹药、法宝、灵药、妖兽内丹

**地理环境构建**
- 四大大陆：东域、西域、南域、北域
- 宗门分布：正派宗门、魔教势力
- 秘境险地：上古遗迹、仙人洞府、秘境空间

**历史背景设定**
- 上古传说：盘古开天、女娲造人、封神大战
- 重大事件：仙魔大战、宗门分裂、天地大劫
- 传奇人物：三皇五帝、老子、庄子等

### 2. 角色设定阶段

**主角设定**
- 姓名：林逸
- 性格：坚韧不拔，重情重义，有正义感
- 背景：出身平凡，天赋异禀
- 能力：过目不忘，悟性极高，体质特殊

**重要配角**
- 师父：玄清子（化神期，慈祥严厉）
- 女主角：苏雨晴（聪慧机敏，名门之后）
- 反派：待定（根据情节需要创建）

### 3. 大纲生成阶段

**整体架构**
- 总卷数：5卷
- 每卷章节：20章
- 每章字数：3000字
- 目标总字数：30万字

**章节规划**
- 每章包含主要事件、涉及角色、修仙内容
- 情节连贯，有冲突和悬念
- 为下章做好铺垫

### 4. 章节生成阶段

**内容生成**
- 基于大纲生成3000字内容
- 符合修仙小说语言风格
- 包含修炼描写和战斗场景
- 人物对话自然，情节连贯

**质量检查**
- 情节连贯性检查
- 人物一致性检查
- 修仙元素运用检查
- 语言风格检查
- 整体质量评分

### 5. 总结与规划

**章节总结**
- 主要情节概括
- 人物发展记录
- 修为进展跟踪
- 为下章铺垫内容

**下章计划**
- 主要情节方向
- 重点描写内容
- 人物互动安排
- 修仙元素设计

## 🔧 配置说明

### 配置文件 (config.py)

```python
# 小说配置
NOVEL_TITLE = "修仙之路"
TOTAL_VOLUMES = 5
CHAPTERS_PER_VOLUME = 20
WORDS_PER_CHAPTER = 3000

# AI配置
OPENAI_API_KEY = "your-api-key"
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 4000

# 输出配置
OUTPUT_DIR = "novel_output"
CHAPTER_FORMAT = "txt"
INCLUDE_SUMMARY = True
```

### 环境变量

```bash
# OpenAI API密钥
export OPENAI_API_KEY="your-api-key-here"

# 其他AI模型密钥（可选）
export ANTHROPIC_API_KEY="your-anthropic-key"
export GOOGLE_API_KEY="your-google-key"
```

## 📁 输出结构

```
novel_output/
└── 修仙之路/
    ├── 第001章_修仙之路.txt
    ├── 第002章_修炼开始.txt
    ├── ...
    ├── 第020章_第一卷完结.txt
    └── novel_data.json
```

### 章节文件格式

```
标题：第001章 修仙之路
字数：3000
生成时间：2024-01-01T12:00:00
==================================================

[章节内容]

==================================================
章节总结：本章主要讲述了主角林逸踏上修仙之路的过程...
下章计划：下一章将继续主角的修炼之路，可能会遇到...
```

## 🤖 AI模型集成

### 支持的AI模型

- **OpenAI GPT**：主要生成模型
- **Anthropic Claude**：备用生成模型
- **Google Gemini**：备用生成模型

### 提示词模板

系统内置了专业的修仙小说提示词模板：

```python
# 世界观设定提示词
CultivationPromptTemplates.world_setting_prompt("cultivation_system")

# 角色设定提示词
CultivationPromptTemplates.character_prompt("主角")

# 章节大纲提示词
CultivationPromptTemplates.chapter_outline_prompt(1, "上下文")

# 章节内容提示词
CultivationPromptTemplates.chapter_content_prompt(outline)
```

## 📊 数据管理

### 数据库结构

```sql
-- 世界观设定表
CREATE TABLE world_settings (
    id INTEGER PRIMARY KEY,
    setting_type TEXT,
    content TEXT,
    created_at TIMESTAMP
);

-- 角色表
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    role TEXT,
    personality TEXT,
    background TEXT,
    cultivation_level TEXT,
    abilities TEXT,
    relationships TEXT,
    created_at TIMESTAMP
);

-- 章节表
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY,
    chapter_number INTEGER UNIQUE,
    title TEXT,
    content TEXT,
    word_count INTEGER,
    summary TEXT,
    next_chapter_plan TEXT,
    created_at TIMESTAMP
);
```

### 数据导出

```python
# 导出小说数据
novel_manager.export_novel_data()

# 导出格式：JSON
{
    "title": "修仙之路",
    "world_settings": {...},
    "characters": [...],
    "chapters": [...]
}
```

## 🎨 自定义扩展

### 添加新的AI模型

```python
class CustomAIGenerator(AIGenerator):
    def generate_text(self, prompt: str, max_tokens: int = 2000) -> str:
        # 实现自定义AI模型调用
        return "生成的内容"
```

### 自定义修仙体系

```python
# 修改config.py中的修仙体系
CULTIVATION_REALMS = [
    "练气期", "筑基期", "金丹期", "元婴期", "化神期",
    "炼虚期", "合体期", "大乘期", "渡劫期", "仙王期"  # 添加新境界
]
```

### 自定义输出格式

```python
# 修改输出配置
OUTPUT_CONFIG = {
    "CHAPTER_FORMAT": "md",  # 改为Markdown格式
    "INCLUDE_METADATA": True,
    "INCLUDE_SUMMARY": True
}
```

## 🔍 质量保证

### 质量检查项目

1. **情节连贯性**：检查章节间的情节连接
2. **人物一致性**：确保角色性格和行为一致
3. **修仙元素运用**：检查修仙元素的合理使用
4. **语言风格**：确保符合修仙小说的语言风格
5. **整体质量**：综合评分和建议

### 改进建议

- 增加修炼描写
- 丰富人物对话
- 加强情节冲突
- 完善环境描写
- 优化语言表达

## 📈 性能优化

### 生成速度优化

- 批量生成章节
- 并行处理多个章节
- 缓存常用数据
- 优化AI模型调用

### 内存使用优化

- 分块处理大文件
- 及时清理临时数据
- 使用生成器处理大量数据
- 数据库连接池

## 🐛 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 检查网络连接
   - 检查API配额是否用完

2. **生成内容质量差**
   - 调整提示词模板
   - 修改生成参数
   - 增加质量检查

3. **数据库错误**
   - 检查数据库文件权限
   - 重建数据库
   - 检查SQL语句

### 调试模式

```python
# 启用调试模式
import logging
logging.basicConfig(level=logging.DEBUG)

# 运行系统
novel_manager = NovelManager("测试小说")
```

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📞 联系方式

- 项目主页：[GitHub Repository]
- 问题反馈：[Issues]
- 邮箱：[your-email@example.com]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**注意**：使用AI生成内容时，请遵守相关法律法规和平台政策。生成的内容仅供学习和研究使用。