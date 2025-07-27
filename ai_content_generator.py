#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from novel_generator import WorldSetting, Character, ChapterOutline

class AIContentGenerator:
    """AI内容生成器"""
    
    def __init__(self, api_type: str = "openai", api_key: Optional[str] = None):
        """
        初始化AI内容生成器
        
        Args:
            api_type: API类型 (openai, claude, local等)
            api_key: API密钥
        """
        self.api_type = api_type
        self.api_key = api_key
        
    def generate_world_setting_prompt(self) -> str:
        """生成世界观设定的提示词"""
        return """
请创建一个详细的中国传统修仙小说世界观设定，包括：

1. 修炼等级体系（从凡人到仙人的完整阶段）
2. 主要门派势力（正派、邪派、中立派等，至少5个）
3. 地域划分（不同的修仙圣地、凡间国度等）
4. 法术体系（五行、剑道、丹道、阵法等）
5. 法宝等级分类
6. 世界背景故事

要求：
- 符合中国传统修仙文化
- 具有完整的逻辑体系
- 为后续300万字小说提供丰富背景
- 以JSON格式返回，便于程序处理
"""

    def generate_character_creation_prompt(self, world_setting: WorldSetting) -> str:
        """生成角色创建的提示词"""
        world_context = json.dumps(asdict(world_setting), ensure_ascii=False, indent=2)
        
        return f"""
基于以下世界观设定，创建修仙小说的主要角色：

世界观设定：
{world_context}

请创建以下角色：
1. 主角（18岁少年，天赋异禀，有主角光环）
2. 师父/导师角色（传授主角修炼的长者）
3. 同门师兄弟（2-3个，有正面也有负面）
4. 女主角（可以是同门或其他门派）
5. 主要反派（强大的敌对势力）
6. 配角长辈（门派长老、家族长辈等）

每个角色需要包含：
- 基本信息（姓名、年龄、性别、修为等级）
- 性格特点
- 背景故事
- 人际关系
- 特殊能力
- 角色目标
- 在故事中的作用

以JSON格式返回角色信息。
"""

    def generate_outline_prompt(self, world_setting: WorldSetting, characters: List[Character], target_chapters: int) -> str:
        """生成大纲创建的提示词"""
        world_context = json.dumps(asdict(world_setting), ensure_ascii=False, indent=2)
        char_context = json.dumps([asdict(char) for char in characters], ensure_ascii=False, indent=2)
        
        return f"""
基于以下世界观和角色设定，创建一部{target_chapters}章的修仙小说大纲：

世界观设定：
{world_context}

主要角色：
{char_context}

请按照以下结构创建大纲：

第一阶段：入门期（1-50章）
- 主角获得修仙机缘
- 拜入门派
- 初步修炼
- 同门关系建立

第二阶段：成长期（51-150章）
- 修为快速提升
- 历练冒险
- 结识重要人物
- 面临第一次重大危机

第三阶段：崛起期（151-250章）
- 声名鹊起
- 参与门派斗争
- 与其他天才竞争
- 面临更大敌人

第四阶段：巅峰期（251-{target_chapters}章）
- 达到高深修为
- 最终大战
- 拯救苍生
- 修成正果

每章需要包含：
- 章节标题
- 主要事件
- 角色发展
- 剧情推进
- 修炼进展
- 冲突矛盾
- 预计字数

以JSON格式返回大纲信息。
"""

    def generate_detailed_chapter_outline_prompt(self, 
                                               chapter_number: int,
                                               world_setting: WorldSetting,
                                               characters: List[Character],
                                               previous_chapters_summary: str,
                                               overall_outline: str) -> str:
        """生成详细章节大纲的提示词"""
        
        return f"""
请为第{chapter_number}章创建详细大纲。

背景信息：
- 世界观：{world_setting.background_story}
- 主要角色：{[char.name for char in characters]}
- 前面章节总结：{previous_chapters_summary}
- 整体大纲：{overall_outline}

请创建第{chapter_number}章的详细大纲，包含：
1. 章节标题（有吸引力）
2. 主要事件列表（3-5个关键情节）
3. 角色发展描述
4. 剧情推进要点
5. 修炼进展
6. 冲突和矛盾
7. 情感发展
8. 为下一章的铺垫

要求：
- 符合修仙小说的节奏
- 保持故事连贯性
- 每章3000字左右的内容量
- 有起承转合的结构
"""

    def generate_chapter_content_prompt(self, 
                                      chapter_outline: ChapterOutline,
                                      world_setting: WorldSetting,
                                      characters: List[Character],
                                      previous_chapter_content: str = "",
                                      writing_style: str = "传统修仙") -> str:
        """生成章节内容的提示词"""
        
        outline_context = asdict(chapter_outline)
        char_context = {char.name: asdict(char) for char in characters}
        
        return f"""
请根据以下大纲写出第{chapter_outline.chapter_number}章的完整内容：

章节大纲：
{json.dumps(outline_context, ensure_ascii=False, indent=2)}

角色信息：
{json.dumps(char_context, ensure_ascii=False, indent=2)}

世界观背景：
- 修炼等级：{world_setting.cultivation_levels}
- 门派信息：{world_setting.sects}
- 法术体系：{world_setting.magic_system}

上一章内容摘要：
{previous_chapter_content[-500:] if previous_chapter_content else "这是第一章"}

写作要求：
1. 字数：约3000字
2. 风格：{writing_style}，文笔优美，描写细腻
3. 结构：起承转合，有紧张感和悬念
4. 对话：生动自然，符合角色性格
5. 描写：环境描写和心理描写并重
6. 节奏：快慢结合，高潮迭起

注意事项：
- 使用中文全角标点符号
- 段落开头使用全角空格缩进
- 保持故事连贯性
- 体现修仙世界的特色
- 推进主线剧情
- 刻画角色成长

请直接输出章节正文内容，不需要额外说明。
"""

    def generate_chapter_summary_prompt(self, chapter_content: str, chapter_number: int) -> str:
        """生成章节总结的提示词"""
        
        return f"""
请为第{chapter_number}章生成详细总结：

章节内容：
{chapter_content}

请提供以下总结信息：
1. 本章主要情节（3-5个要点）
2. 角色发展变化
3. 修炼进展
4. 重要伏笔或线索
5. 情感发展
6. 为下一章的铺垫内容
7. 一句话概括本章

格式要求：
- 简洁明了
- 便于后续章节参考
- 突出重点信息
"""

    def generate_next_chapter_setup_prompt(self, 
                                         current_chapter_summary: str,
                                         overall_progress: str,
                                         target_chapter_number: int) -> str:
        """生成下一章设置的提示词"""
        
        return f"""
基于当前进度，为第{target_chapter_number}章提供创作指导：

当前章节总结：
{current_chapter_summary}

整体进度：
{overall_progress}

请提供第{target_chapter_number}章的：
1. 建议主题
2. 主要冲突
3. 角色发展方向
4. 剧情推进要点
5. 需要解决的问题
6. 可以引入的新元素
7. 与前面章节的呼应

要求保持故事节奏和逻辑连贯性。
"""

class LocalAIGenerator(AIContentGenerator):
    """本地AI生成器（使用模板和规则）"""
    
    def __init__(self):
        super().__init__("local")
        
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        """生成内容（简单模板实现）"""
        if "章节内容" in prompt:
            return self._generate_chapter_template()
        elif "总结" in prompt:
            return self._generate_summary_template()
        else:
            return "AI生成的内容（需要接入具体的AI API）"
    
    def _generate_chapter_template(self) -> str:
        """生成章节模板"""
        templates = [
            """
第{chapter}章 灵根觉醒

　　晨光熹微，青云山脉在薄雾中若隐若现，如同仙境一般。林逸早早起身，今日是他期待已久的灵根检测之日。

　　"师兄，听说今年的新弟子中有不少天才。"一位青云门弟子低声议论着。

　　林逸深吸一口气，走向检测大殿。殿内已经聚集了数十名和他年龄相仿的少年，每个人脸上都写满了紧张和期待。

　　"下一位，林逸！"长老的声音响起。

　　林逸走上前去，将手按在测灵石上。刹那间，五色光芒从石中迸发，直冲云霄！在场所有人都震惊了。

　　"极品五行灵根！"长老惊呼出声，"千年难遇的天才！"

　　这一刻，林逸知道，自己的修仙之路正式开始了...
""",
            """
第{chapter}章 初入门派

　　青云门，作为东荒最强的正道门派之一，其雄伟壮观让林逸叹为观止。

　　"新弟子们，欢迎加入青云门。"一位白发苍苍的长老缓缓开口，"从今日起，你们将在这里学习修仙之道。"

　　林逸看着周围的师兄师姐们，每一个都散发着非凡的气息。他暗下决心，一定要在这里闯出一番天地。

　　"林逸，你的天赋确实不凡，但修仙一途，天赋只是基础，更重要的是毅力和机缘。"长老看着他说道。

　　"弟子定当牢记教诲！"林逸恭敬回答。

　　从这一刻开始，他的修仙传奇正式拉开了序幕...
"""
        ]
        
        import random
        return random.choice(templates)
    
    def _generate_summary_template(self) -> str:
        """生成总结模板"""
        return """
本章总结：
1. 主要情节：主角参加门派考核，展现天赋
2. 角色发展：从紧张不安到自信坚定
3. 修炼进展：检测出极品灵根
4. 重要伏笔：暗示主角的特殊身世
5. 情感发展：对修仙世界的向往更加强烈
6. 下章铺垫：将被分配师父，开始正式修炼
7. 一句话概括：主角展现天赋，正式踏入修仙门第
"""

# API接口集成类（可以根据需要扩展）
class OpenAIGenerator(AIContentGenerator):
    """OpenAI API生成器"""
    
    def __init__(self, api_key: str):
        super().__init__("openai", api_key)
        
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        """调用OpenAI API生成内容"""
        # 这里需要实际的OpenAI API调用
        # import openai
        # openai.api_key = self.api_key
        # response = openai.ChatCompletion.create(...)
        return "需要配置OpenAI API密钥和调用逻辑"

class ClaudeGenerator(AIContentGenerator):
    """Claude API生成器"""
    
    def __init__(self, api_key: str):
        super().__init__("claude", api_key)
        
    def generate_content(self, prompt: str, max_length: int = 3000) -> str:
        """调用Claude API生成内容"""
        # 这里需要实际的Claude API调用
        return "需要配置Claude API密钥和调用逻辑"

# 工厂函数
def create_ai_generator(ai_type: str = "local", api_key: Optional[str] = None) -> AIContentGenerator:
    """创建AI生成器"""
    if ai_type == "local":
        return LocalAIGenerator()
    elif ai_type == "openai":
        if not api_key:
            raise ValueError("OpenAI需要API密钥")
        return OpenAIGenerator(api_key)
    elif ai_type == "claude":
        if not api_key:
            raise ValueError("Claude需要API密钥")
        return ClaudeGenerator(api_key)
    else:
        raise ValueError(f"不支持的AI类型: {ai_type}")