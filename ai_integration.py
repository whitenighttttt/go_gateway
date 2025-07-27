#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模型集成模块
用于生成修仙小说的具体内容
"""

import json
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Optional
import time

class AIGenerator:
    """AI生成器基类"""
    
    def __init__(self, api_key: str = None, model_name: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def generate_text(self, prompt: str, max_tokens: int = 2000) -> str:
        """生成文本"""
        raise NotImplementedError("子类必须实现此方法")

class OpenAIGenerator(AIGenerator):
    """OpenAI API生成器"""
    
    def generate_text(self, prompt: str, max_tokens: int = 2000) -> str:
        """使用OpenAI API生成文本"""
        if not self.api_key:
            return self._mock_generate(prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "你是一个专业的修仙小说作家，擅长创作传统修仙小说。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.8
        }
        
        try:
            # 使用urllib替代requests
            data_bytes = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                self.base_url,
                data=data_bytes,
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API调用失败: {e}")
            return self._mock_generate(prompt)
    
    def _mock_generate(self, prompt: str) -> str:
        """模拟生成（当没有API key时使用）"""
        return f"模拟生成的内容: {prompt[:100]}..."

class NovelAIGenerator:
    """小说AI生成器"""
    
    def __init__(self, ai_generator: AIGenerator):
        self.ai = ai_generator
    
    def generate_world_setting(self, setting_type: str, requirements: str) -> Dict[str, Any]:
        """生成世界观设定"""
        prompt = f"""
请为修仙小说生成{setting_type}设定，要求：
{requirements}

请以JSON格式返回，包含详细的设定内容。
"""
        
        response = self.ai.generate_text(prompt)
        try:
            # 尝试解析JSON
            return json.loads(response)
        except:
            # 如果解析失败，返回结构化数据
            return {
                "type": setting_type,
                "content": response,
                "generated_at": time.time()
            }
    
    def generate_character(self, character_type: str, requirements: str) -> Dict[str, Any]:
        """生成角色设定"""
        prompt = f"""
请为修仙小说生成{character_type}角色设定，要求：
{requirements}

请包含以下信息：
- 姓名
- 性格特点
- 背景故事
- 修仙境界
- 特殊能力
- 人际关系

请以JSON格式返回。
"""
        
        response = self.ai.generate_text(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "type": character_type,
                "content": response,
                "generated_at": time.time()
            }
    
    def generate_chapter_outline(self, chapter_number: int, context: str, requirements: str) -> Dict[str, Any]:
        """生成章节大纲"""
        prompt = f"""
请为修仙小说第{chapter_number}章生成详细大纲，上下文：
{context}

要求：
{requirements}

请包含以下内容：
- 章节标题
- 主要事件（列表）
- 涉及角色
- 修仙内容
- 情节发展
- 字数目标：3000字

请以JSON格式返回。
"""
        
        response = self.ai.generate_text(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "chapter_number": chapter_number,
                "title": f"第{chapter_number}章",
                "content": response,
                "generated_at": time.time()
            }
    
    def generate_chapter_content(self, outline: Dict[str, Any], previous_chapter: Optional[Dict] = None) -> str:
        """生成章节内容"""
        context = ""
        if previous_chapter:
            context = f"上一章内容：{previous_chapter.get('summary', '')}"
        
        prompt = f"""
请根据以下大纲生成修仙小说章节内容：

章节大纲：
{json.dumps(outline, ensure_ascii=False, indent=2)}

{context}

要求：
1. 字数控制在3000字左右
2. 符合修仙小说的语言风格
3. 包含详细的修炼描写
4. 情节连贯，人物对话自然
5. 有适当的悬念和冲突

请直接返回章节内容，不要包含标题。
"""
        
        return self.ai.generate_text(prompt, max_tokens=4000)
    
    def generate_chapter_summary(self, content: str) -> str:
        """生成章节总结"""
        prompt = f"""
请为以下修仙小说章节生成总结：

章节内容：
{content[:1000]}...

请生成100字左右的总结，包含：
1. 主要情节
2. 人物发展
3. 修为进展
4. 为下章铺垫的内容
"""
        
        return self.ai.generate_text(prompt, max_tokens=500)
    
    def generate_next_chapter_plan(self, current_chapter: Dict[str, Any], summary: str) -> str:
        """生成下章计划"""
        prompt = f"""
基于当前章节的总结：
{summary}

请为下一章制定详细的写作计划，包含：
1. 主要情节方向
2. 需要重点描写的内容
3. 人物互动安排
4. 修仙元素设计
5. 需要注意的细节

请生成200字左右的详细计划。
"""
        
        return self.ai.generate_text(prompt, max_tokens=800)

class CultivationPromptTemplates:
    """修仙小说提示词模板"""
    
    @staticmethod
    def world_setting_prompt(setting_type: str) -> str:
        """世界观设定提示词"""
        templates = {
            "cultivation_system": """
请设计一个完整的修仙体系，包含：
1. 境界划分（从练气到渡劫，每个境界的特点）
2. 功法分类（心法、功法、秘术等）
3. 战斗技能（剑法、刀法、法术等）
4. 修炼资源（灵石、丹药、法宝等）
5. 突破条件（每个境界的突破要求）
""",
            "geography": """
请设计修仙世界的地理环境，包含：
1. 主要大陆和区域
2. 各大宗门分布
3. 秘境和险地
4. 资源分布
5. 势力格局
""",
            "history": """
请设计修仙世界的历史背景，包含：
1. 上古传说
2. 重大历史事件
3. 传奇人物
4. 宗门起源
5. 正邪对立的历史
"""
        }
        return templates.get(setting_type, "请设计修仙世界的设定")
    
    @staticmethod
    def character_prompt(character_type: str) -> str:
        """角色设定提示词"""
        templates = {
            "主角": """
请设计一个修仙小说的主角，包含：
1. 姓名和基本特征
2. 性格特点（优缺点）
3. 背景故事（家庭、机缘等）
4. 修仙天赋和特殊体质
5. 成长轨迹规划
6. 核心价值观
""",
            "师父": """
请设计主角的师父角色，包含：
1. 姓名和身份
2. 修为境界
3. 性格特点
4. 教学风格
5. 与主角的关系
6. 背景故事
""",
            "反派": """
请设计一个反派角色，包含：
1. 姓名和身份
2. 修为境界
3. 性格特点
4. 作恶动机
5. 与主角的冲突
6. 背景故事
"""
        }
        return templates.get(character_type, "请设计一个修仙小说角色")
    
    @staticmethod
    def chapter_outline_prompt(chapter_number: int, context: str) -> str:
        """章节大纲提示词"""
        return f"""
请为修仙小说第{chapter_number}章设计详细大纲。

当前故事背景：
{context}

请设计包含以下要素的大纲：
1. 章节标题（吸引人且符合修仙风格）
2. 主要事件（3-5个关键情节）
3. 涉及角色（主角、配角、反派等）
4. 修仙内容（修炼、战斗、突破等）
5. 情节发展（冲突、转折、高潮）
6. 为下章铺垫的内容

要求：
- 符合修仙小说的节奏
- 有足够的冲突和悬念
- 包含修炼和战斗元素
- 人物对话和互动自然
- 字数控制在3000字左右
"""
    
    @staticmethod
    def chapter_content_prompt(outline: Dict[str, Any]) -> str:
        """章节内容生成提示词"""
        return f"""
请根据以下大纲生成修仙小说章节内容：

章节标题：{outline.get('title', '')}
主要事件：{outline.get('main_events', [])}
涉及角色：{outline.get('characters_involved', [])}
修仙内容：{outline.get('cultivation_content', '')}

写作要求：
1. 字数控制在3000字左右
2. 使用修仙小说的语言风格
3. 包含详细的修炼描写和战斗场景
4. 人物对话自然，符合角色性格
5. 情节连贯，有适当的悬念
6. 环境描写要营造修仙氛围
7. 包含修仙术语和功法描述

请直接返回章节内容，不要包含标题。
"""

class QualityChecker:
    """质量检查器"""
    
    def __init__(self, ai_generator: AIGenerator):
        self.ai = ai_generator
    
    def check_chapter_quality(self, content: str) -> Dict[str, Any]:
        """检查章节质量"""
        prompt = f"""
请检查以下修仙小说章节的质量：

{content[:2000]}...

请从以下方面进行评价：
1. 情节连贯性（1-10分）
2. 人物一致性（1-10分）
3. 修仙元素运用（1-10分）
4. 语言风格（1-10分）
5. 整体质量（1-10分）

请指出需要改进的地方，并给出具体建议。
"""
        
        response = self.ai.generate_text(prompt)
        return {
            "evaluation": response,
            "word_count": len(content),
            "check_time": time.time()
        }
    
    def suggest_improvements(self, content: str, issues: str) -> str:
        """建议改进方案"""
        prompt = f"""
基于以下问题：
{issues}

请为以下章节内容提供具体的改进建议：

{content[:1500]}...

请提供：
1. 具体的修改建议
2. 改进后的示例段落
3. 写作技巧建议
"""
        
        return self.ai.generate_text(prompt)

# 使用示例
if __name__ == "__main__":
    # 创建AI生成器
    ai_generator = OpenAIGenerator()  # 不传入API key，使用模拟生成
    novel_ai = NovelAIGenerator(ai_generator)
    
    # 生成世界观设定
    cultivation_system = novel_ai.generate_world_setting(
        "cultivation_system", 
        CultivationPromptTemplates.world_setting_prompt("cultivation_system")
    )
    
    print("修仙体系设定：")
    print(json.dumps(cultivation_system, ensure_ascii=False, indent=2))