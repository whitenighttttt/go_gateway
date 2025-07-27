#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
AI修仙小说生成系统的配置参数
"""

import os
from typing import Dict, Any

class NovelConfig:
    """小说配置"""
    
    # 小说基本信息
    NOVEL_TITLE = "修仙之路"
    AUTHOR = "AI作家"
    GENRE = "修仙小说"
    
    # 小说结构
    TOTAL_VOLUMES = 5  # 总卷数
    CHAPTERS_PER_VOLUME = 20  # 每卷章节数
    WORDS_PER_CHAPTER = 3000  # 每章字数
    
    # 目标总字数
    TARGET_TOTAL_WORDS = 300000  # 30万字
    
    # 修仙体系设定
    CULTIVATION_REALMS = [
        "练气期", "筑基期", "金丹期", "元婴期", "化神期",
        "炼虚期", "合体期", "大乘期", "渡劫期"
    ]
    
    # 主要角色设定
    MAIN_CHARACTERS = {
        "主角": {
            "name": "林逸",
            "personality": "坚韧不拔，重情重义，有正义感",
            "background": "出身平凡，天赋异禀",
            "initial_level": "练气一层"
        },
        "师父": {
            "name": "玄清子",
            "personality": "慈祥严厉，深不可测",
            "background": "隐世高人，修为通天",
            "level": "化神期"
        },
        "女主角": {
            "name": "苏雨晴",
            "personality": "聪慧机敏，性格坚韧",
            "background": "名门之后，天赋卓绝",
            "initial_level": "练气三层"
        }
    }
    
    # 世界观设定
    WORLD_SETTINGS = {
        "continents": [
            "东域大陆", "西域大陆", "南域大陆", "北域大陆"
        ],
        "major_sects": [
            "青云门", "蜀山剑派", "昆仑派", "峨眉派",
            "魔教", "血煞宗", "万兽宗", "冰心谷"
        ],
        "secret_realms": [
            "上古遗迹", "仙人洞府", "秘境空间", "时空裂缝"
        ]
    }

class AIConfig:
    """AI配置"""
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS = 4000
    OPENAI_TEMPERATURE = 0.8
    
    # 其他AI模型配置
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # 生成参数
    GENERATION_PARAMS = {
        "max_tokens": 4000,
        "temperature": 0.8,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1
    }

class DatabaseConfig:
    """数据库配置"""
    
    DB_PATH = "novel_database.db"
    BACKUP_INTERVAL = 10  # 每10章备份一次
    
    # 表结构
    TABLES = {
        "world_settings": """
            CREATE TABLE IF NOT EXISTS world_settings (
                id INTEGER PRIMARY KEY,
                setting_type TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "characters": """
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                role TEXT,
                personality TEXT,
                background TEXT,
                cultivation_level TEXT,
                abilities TEXT,
                relationships TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "chapters": """
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY,
                chapter_number INTEGER UNIQUE,
                title TEXT,
                content TEXT,
                word_count INTEGER,
                summary TEXT,
                next_chapter_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "outlines": """
            CREATE TABLE IF NOT EXISTS outlines (
                id INTEGER PRIMARY KEY,
                chapter_number INTEGER UNIQUE,
                title TEXT,
                main_events TEXT,
                characters_involved TEXT,
                cultivation_content TEXT,
                word_count_target INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
    }

class OutputConfig:
    """输出配置"""
    
    # 输出目录
    OUTPUT_DIR = "novel_output"
    CHAPTER_DIR = "chapters"
    SUMMARY_DIR = "summaries"
    DATA_DIR = "data"
    
    # 文件格式
    CHAPTER_FORMAT = "txt"
    SUMMARY_FORMAT = "json"
    DATA_FORMAT = "json"
    
    # 文件命名
    CHAPTER_FILENAME_TEMPLATE = "第{chapter_number:03d}章_{title}.{format}"
    VOLUME_FILENAME_TEMPLATE = "第{volume_number}卷_{title}.{format}"
    
    # 输出选项
    INCLUDE_METADATA = True
    INCLUDE_SUMMARY = True
    INCLUDE_NEXT_PLAN = True
    AUTO_BACKUP = True

class QualityConfig:
    """质量配置"""
    
    # 质量检查参数
    MIN_WORD_COUNT = 2500
    MAX_WORD_COUNT = 3500
    MIN_QUALITY_SCORE = 7.0
    
    # 检查项目
    CHECK_ITEMS = [
        "情节连贯性",
        "人物一致性", 
        "修仙元素运用",
        "语言风格",
        "整体质量"
    ]
    
    # 改进建议
    IMPROVEMENT_SUGGESTIONS = [
        "增加修炼描写",
        "丰富人物对话",
        "加强情节冲突",
        "完善环境描写",
        "优化语言表达"
    ]

class PromptConfig:
    """提示词配置"""
    
    # 系统提示词
    SYSTEM_PROMPT = """
你是一个专业的修仙小说作家，擅长创作传统修仙小说。
你的作品具有以下特点：
1. 情节紧凑，悬念迭起
2. 人物形象鲜明，性格立体
3. 修仙元素丰富，体系完整
4. 语言优美，意境深远
5. 符合中国传统修仙文化

请按照要求创作高质量的修仙小说内容。
"""
    
    # 角色提示词模板
    CHARACTER_PROMPTS = {
        "主角": "请设计一个修仙小说的主角，具有独特的性格特点和成长轨迹",
        "师父": "请设计主角的师父角色，具有深厚的修为和独特的教学风格",
        "反派": "请设计一个反派角色，具有明确的动机和与主角的冲突",
        "配角": "请设计一个配角角色，在故事中起到重要作用"
    }
    
    # 章节提示词模板
    CHAPTER_PROMPTS = {
        "outline": "请为修仙小说章节设计详细大纲，包含主要事件和修仙内容",
        "content": "请根据大纲生成修仙小说章节内容，字数控制在3000字左右",
        "summary": "请为章节生成总结，包含主要情节和人物发展",
        "next_plan": "请为下一章制定详细的写作计划"
    }

# 全局配置
CONFIG = {
    "novel": NovelConfig,
    "ai": AIConfig,
    "database": DatabaseConfig,
    "output": OutputConfig,
    "quality": QualityConfig,
    "prompt": PromptConfig
}

def get_config(section: str) -> Dict[str, Any]:
    """获取配置"""
    if section in CONFIG:
        config_class = CONFIG[section]
        return {key: getattr(config_class, key) 
                for key in dir(config_class) 
                if not key.startswith('_')}
    return {}

def update_config(section: str, key: str, value: Any):
    """更新配置"""
    if section in CONFIG:
        config_class = CONFIG[section]
        if hasattr(config_class, key):
            setattr(config_class, key, value)

if __name__ == "__main__":
    # 打印配置信息
    print("小说配置：")
    print(get_config("novel"))
    
    print("\nAI配置：")
    print(get_config("ai"))
    
    print("\n输出配置：")
    print(get_config("output"))