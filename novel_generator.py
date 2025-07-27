#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class WorldSetting:
    """世界观设定"""
    cultivation_levels: List[str]  # 修炼等级
    sects: List[Dict[str, Any]]   # 门派信息
    regions: List[Dict[str, Any]] # 地域设定
    magic_system: Dict[str, Any]  # 法术体系
    artifacts: List[Dict[str, Any]] # 法宝设定
    background_story: str         # 背景故事

@dataclass
class Character:
    """角色设定"""
    name: str
    age: int
    gender: str
    cultivation_level: str
    personality: str
    background: str
    relationships: List[Dict[str, str]]
    abilities: List[str]
    goals: str
    role_type: str  # 主角、配角、反派等

@dataclass
class ChapterOutline:
    """章节大纲"""
    chapter_number: int
    title: str
    main_events: List[str]
    character_development: str
    plot_progression: str
    cultivation_progress: str
    conflicts: List[str]
    estimated_word_count: int

@dataclass
class Chapter:
    """完整章节"""
    outline: ChapterOutline
    content: str
    actual_word_count: int
    key_plot_points: List[str]
    character_changes: List[str]
    next_chapter_setup: str
    summary: str

class NovelGenerator:
    """修仙小说生成器主类"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_dir = f"novel_projects/{project_name}"
        self.world_setting: WorldSetting = None
        self.characters: List[Character] = []
        self.overall_outline: List[ChapterOutline] = []
        self.chapters: List[Chapter] = []
        self.current_chapter = 0
        
        # 创建项目目录
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(f"{self.project_dir}/chapters", exist_ok=True)
        os.makedirs(f"{self.project_dir}/settings", exist_ok=True)
        
    def save_project_state(self):
        """保存项目状态"""
        state = {
            'project_name': self.project_name,
            'current_chapter': self.current_chapter,
            'world_setting': asdict(self.world_setting) if self.world_setting else None,
            'characters': [asdict(char) for char in self.characters],
            'overall_outline': [asdict(outline) for outline in self.overall_outline],
            'last_updated': datetime.datetime.now().isoformat()
        }
        
        with open(f"{self.project_dir}/project_state.json", 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_project_state(self):
        """加载项目状态"""
        state_file = f"{self.project_dir}/project_state.json"
        if os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                
            self.current_chapter = state.get('current_chapter', 0)
            
            if state.get('world_setting'):
                self.world_setting = WorldSetting(**state['world_setting'])
                
            self.characters = [Character(**char_data) for char_data in state.get('characters', [])]
            self.overall_outline = [ChapterOutline(**outline_data) for outline_data in state.get('overall_outline', [])]
    
    def create_world_setting(self) -> WorldSetting:
        """第一步：创建世界观设定"""
        logging.info("开始创建世界观设定...")
        
        # 默认修仙世界观模板
        world_setting = WorldSetting(
            cultivation_levels=[
                "凡人", "练气期", "筑基期", "金丹期", "元婴期", 
                "化神期", "合体期", "大乘期", "渡劫期", "真仙"
            ],
            sects=[
                {
                    "name": "青云门",
                    "type": "正派",
                    "specialty": "剑修",
                    "location": "青云山",
                    "strength": "强大"
                },
                {
                    "name": "魔音寺",
                    "type": "邪派", 
                    "specialty": "音律攻击",
                    "location": "黑风谷",
                    "strength": "中等"
                }
            ],
            regions=[
                {
                    "name": "东荒",
                    "type": "修仙圣地",
                    "features": ["灵气浓郁", "宗门林立", "机缘众多"],
                    "dangers": ["妖兽横行", "秘境危险"]
                }
            ],
            magic_system={
                "five_elements": ["金", "木", "水", "火", "土"],
                "special_paths": ["剑道", "丹道", "阵法", "符箓", "炼器"],
                "cultivation_resources": ["灵石", "丹药", "功法", "法宝"]
            },
            artifacts=[
                {
                    "name": "青锋剑",
                    "grade": "法器",
                    "description": "锋利无比的飞剑"
                }
            ],
            background_story="这是一个修仙者追求长生不老的世界，强者为尊，弱肉强食..."
        )
        
        self.world_setting = world_setting
        self.save_world_setting()
        logging.info("世界观设定创建完成")
        return world_setting
    
    def save_world_setting(self):
        """保存世界观设定"""
        if self.world_setting:
            with open(f"{self.project_dir}/settings/world_setting.json", 'w', encoding='utf-8') as f:
                json.dump(asdict(self.world_setting), f, ensure_ascii=False, indent=2)
    
    def create_main_characters(self) -> List[Character]:
        """第二步：创建主要角色"""
        logging.info("开始创建主要角色...")
        
        # 主角设定
        protagonist = Character(
            name="林逸",
            age=18,
            gender="男",
            cultivation_level="凡人",
            personality="坚韧不拔，重情重义，天赋异禀",
            background="出身贫寒，意外获得修仙机缘",
            relationships=[],
            abilities=["超强感知力", "快速修炼"],
            goals="成为绝世强者，保护重要的人",
            role_type="主角"
        )
        
        # 主要配角
        mentor = Character(
            name="玄机老人",
            age=800,
            gender="男", 
            cultivation_level="化神期",
            personality="睿智深沉，亦师亦友",
            background="隐世高人，主角的引路人",
            relationships=[{"relation": "师父", "target": "林逸"}],
            abilities=["阵法大师", "丹道宗师"],
            goals="培养优秀弟子",
            role_type="导师"
        )
        
        self.characters = [protagonist, mentor]
        self.save_characters()
        logging.info("主要角色创建完成")
        return self.characters
    
    def save_characters(self):
        """保存角色设定"""
        characters_data = [asdict(char) for char in self.characters]
        with open(f"{self.project_dir}/settings/characters.json", 'w', encoding='utf-8') as f:
            json.dump(characters_data, f, ensure_ascii=False, indent=2)
    
    def generate_overall_outline(self, target_chapters: int = 300) -> List[ChapterOutline]:
        """第三步：生成整体大纲"""
        logging.info(f"开始生成{target_chapters}章的整体大纲...")
        
        # 分阶段规划
        phases = [
            {"name": "入门期", "chapters": 50, "theme": "获得机缘，初入修仙世界"},
            {"name": "成长期", "chapters": 100, "theme": "历练成长，结识伙伴"},
            {"name": "崛起期", "chapters": 100, "theme": "声名鹊起，面临大敌"},
            {"name": "巅峰期", "chapters": 50, "theme": "巅峰对决，拯救世界"}
        ]
        
        outlines = []
        chapter_num = 1
        
        for phase in phases:
            for i in range(phase["chapters"]):
                outline = ChapterOutline(
                    chapter_number=chapter_num,
                    title=f"第{chapter_num}章",
                    main_events=[f"{phase['theme']}相关情节"],
                    character_development="主角实力和心境成长",
                    plot_progression="推进主线剧情",
                    cultivation_progress="修为提升",
                    conflicts=["内在冲突", "外在挑战"],
                    estimated_word_count=3000
                )
                outlines.append(outline)
                chapter_num += 1
        
        self.overall_outline = outlines[:target_chapters]
        self.save_overall_outline()
        logging.info("整体大纲生成完成")
        return self.overall_outline
    
    def save_overall_outline(self):
        """保存整体大纲"""
        outlines_data = [asdict(outline) for outline in self.overall_outline]
        with open(f"{self.project_dir}/overall_outline.json", 'w', encoding='utf-8') as f:
            json.dump(outlines_data, f, ensure_ascii=False, indent=2)
    
    def generate_detailed_chapter_outline(self, chapter_number: int) -> ChapterOutline:
        """第四步：生成详细章节大纲"""
        logging.info(f"生成第{chapter_number}章详细大纲...")
        
        if chapter_number <= len(self.overall_outline):
            base_outline = self.overall_outline[chapter_number - 1]
            
            # 根据章节位置生成详细内容
            detailed_outline = ChapterOutline(
                chapter_number=chapter_number,
                title=f"第{chapter_number}章 初入青云门",
                main_events=[
                    "主角到达青云门山脚",
                    "遇到入门考核",
                    "展现天赋震惊长老",
                    "成功拜入青云门"
                ],
                character_development="主角从紧张到自信的心理变化",
                plot_progression="正式开始修仙之路",
                cultivation_progress="检测到极品灵根",
                conflicts=["入门考核的挑战", "其他考生的竞争"],
                estimated_word_count=3000
            )
            
            return detailed_outline
        else:
            raise ValueError(f"章节号{chapter_number}超出范围")
    
    def generate_chapter_content(self, chapter_outline: ChapterOutline) -> Chapter:
        """第五步：生成章节内容"""
        logging.info(f"生成第{chapter_outline.chapter_number}章内容...")
        
        # 这里应该调用AI API生成具体内容，现在用模板代替
        content = f"""
{chapter_outline.title}

　　晨光熹微，青云山脉在薄雾中若隐若现，如同仙境一般。山脚下，一个身着粗布衣衫的少年正仰望着那高耸入云的山峰，眼中满含着向往与决心。

　　这少年正是林逸，今日是青云门三年一度的入门大考之日。

　　"各位考生，入门考核即将开始！"一声洪亮的声音从山门处传来，只见一位身着青色道袍的中年修士缓缓走出，身后跟着数位长老。

　　林逸深吸一口气，跟随着人群向前走去。第一关是灵根检测，这是最基础也是最重要的一关。

　　"下一位！"长老的声音传来。

　　林逸走上前去，将手按在了那颗晶莹剔透的测灵石上。刹那间，五色光芒从石头中迸发而出，直冲云霄！

　　"极品五行灵根！"长老惊呼出声，在场所有人都被这突如其来的异象震惊了。

　　这一刻，林逸知道，自己的修仙之路真正开始了...

"""
        
        chapter = Chapter(
            outline=chapter_outline,
            content=content,
            actual_word_count=len(content),
            key_plot_points=["主角到达青云门", "通过入门考核", "展现极品灵根"],
            character_changes=["主角正式踏入修仙世界", "获得青云门认可"],
            next_chapter_setup="主角将被分配师父，开始正式修炼",
            summary=f"第{chapter_outline.chapter_number}章：主角林逸参加青云门入门考核，展现极品五行灵根天赋，成功拜入青云门，正式开始修仙之路。"
        )
        
        return chapter
    
    def save_chapter(self, chapter: Chapter):
        """保存章节"""
        chapter_file = f"{self.project_dir}/chapters/chapter_{chapter.outline.chapter_number:03d}.json"
        chapter_data = {
            'outline': asdict(chapter.outline),
            'content': chapter.content,
            'actual_word_count': chapter.actual_word_count,
            'key_plot_points': chapter.key_plot_points,
            'character_changes': chapter.character_changes,
            'next_chapter_setup': chapter.next_chapter_setup,
            'summary': chapter.summary,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        # 同时保存纯文本版本用于阅读
        text_file = f"{self.project_dir}/chapters/chapter_{chapter.outline.chapter_number:03d}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(chapter.content)
    
    def generate_next_chapter(self) -> Chapter:
        """生成下一章"""
        next_chapter_num = self.current_chapter + 1
        
        if next_chapter_num > len(self.overall_outline):
            raise ValueError("已达到计划章节数上限")
        
        # 生成详细大纲
        detailed_outline = self.generate_detailed_chapter_outline(next_chapter_num)
        
        # 生成章节内容
        chapter = self.generate_chapter_content(detailed_outline)
        
        # 保存章节
        self.save_chapter(chapter)
        self.chapters.append(chapter)
        
        # 更新当前章节数
        self.current_chapter = next_chapter_num
        self.save_project_state()
        
        logging.info(f"第{next_chapter_num}章生成完成")
        return chapter
    
    def get_progress_report(self) -> Dict[str, Any]:
        """获取进度报告"""
        total_words = sum(len(chapter.content) for chapter in self.chapters)
        
        return {
            'project_name': self.project_name,
            'current_chapter': self.current_chapter,
            'total_planned_chapters': len(self.overall_outline),
            'completion_rate': f"{(self.current_chapter / len(self.overall_outline) * 100):.1f}%",
            'total_words': total_words,
            'average_words_per_chapter': total_words // max(1, len(self.chapters)),
            'estimated_total_words': len(self.overall_outline) * 3000,
            'last_chapter_summary': self.chapters[-1].summary if self.chapters else "暂无章节"
        }

if __name__ == "__main__":
    # 示例使用
    generator = NovelGenerator("修仙传说")
    
    # 完整流程演示
    print("=== 修仙小说生成系统 ===")
    
    # 1. 创建世界观
    world = generator.create_world_setting()
    print("✓ 世界观设定完成")
    
    # 2. 创建角色
    characters = generator.create_main_characters()
    print("✓ 主要角色创建完成")
    
    # 3. 生成整体大纲
    outline = generator.generate_overall_outline(300)
    print("✓ 整体大纲生成完成")
    
    # 4. 生成第一章
    first_chapter = generator.generate_next_chapter()
    print("✓ 第一章生成完成")
    
    # 5. 显示进度报告
    report = generator.get_progress_report()
    print("\n=== 进度报告 ===")
    for key, value in report.items():
        print(f"{key}: {value}")