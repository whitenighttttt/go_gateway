#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import datetime
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from novel_generator import NovelGenerator, WorldSetting, Character, ChapterOutline, Chapter
from ai_content_generator import create_ai_generator, AIContentGenerator

class EnhancedNovelGenerator(NovelGenerator):
    """增强版修仙小说生成器"""
    
    def __init__(self, project_name: str, ai_type: str = "local", ai_api_key: Optional[str] = None):
        super().__init__(project_name)
        self.ai_generator = create_ai_generator(ai_type, ai_api_key)
        self.chapter_history = []  # 存储章节历史记录
        self.generation_log = []   # 生成日志
        
    def log_generation_step(self, step: str, details: str):
        """记录生成步骤"""
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'step': step,
            'details': details
        }
        self.generation_log.append(log_entry)
        logging.info(f"{step}: {details}")
    
    def create_enhanced_world_setting(self, custom_requirements: str = "") -> WorldSetting:
        """创建增强的世界观设定"""
        self.log_generation_step("世界观设定", "开始创建详细世界观")
        
        prompt = self.ai_generator.generate_world_setting_prompt()
        if custom_requirements:
            prompt += f"\n\n特殊要求：\n{custom_requirements}"
        
        # 如果使用AI生成，这里调用AI API
        # ai_response = self.ai_generator.generate_content(prompt)
        
        # 目前使用增强的默认模板
        world_setting = WorldSetting(
            cultivation_levels=[
                "凡人", "练气初期", "练气中期", "练气后期", "练气大圆满",
                "筑基初期", "筑基中期", "筑基后期", "筑基大圆满",
                "金丹初期", "金丹中期", "金丹后期", "金丹大圆满",
                "元婴初期", "元婴中期", "元婴后期", "元婴大圆满",
                "化神初期", "化神中期", "化神后期", "化神大圆满",
                "合体初期", "合体中期", "合体后期", "合体大圆满",
                "大乘初期", "大乘中期", "大乘后期", "大乘大圆满",
                "渡劫初期", "渡劫中期", "渡劫后期", "渡劫大圆满",
                "真仙", "金仙", "太乙金仙", "大罗金仙", "仙帝"
            ],
            sects=[
                {
                    "name": "青云门",
                    "type": "正派",
                    "specialty": "剑修",
                    "location": "青云山脉",
                    "strength": "超级势力",
                    "founder": "青云真仙",
                    "disciples": 50000,
                    "territory": "东荒三分之一"
                },
                {
                    "name": "天音宗",
                    "type": "正派",
                    "specialty": "音律修炼",
                    "location": "天音谷",
                    "strength": "一流势力",
                    "founder": "天音仙子",
                    "disciples": 30000,
                    "territory": "中州北部"
                },
                {
                    "name": "魔音寺",
                    "type": "邪派",
                    "specialty": "魔音攻击",
                    "location": "黑风谷",
                    "strength": "一流势力",
                    "founder": "魔音老祖",
                    "disciples": 20000,
                    "territory": "西漠边缘"
                },
                {
                    "name": "万药谷",
                    "type": "中立",
                    "specialty": "炼丹医道",
                    "location": "药王山",
                    "strength": "超级势力",
                    "founder": "药王仙人",
                    "disciples": 15000,
                    "territory": "南荒核心"
                },
                {
                    "name": "器宗",
                    "type": "中立",
                    "specialty": "炼器制宝",
                    "location": "炼器峰",
                    "strength": "一流势力",
                    "founder": "器祖",
                    "disciples": 10000,
                    "territory": "北冥火山"
                }
            ],
            regions=[
                {
                    "name": "东荒",
                    "type": "修仙圣地",
                    "features": ["灵气最浓郁", "宗门最多", "天才辈出"],
                    "dangers": ["妖兽王者", "上古秘境", "天劫频繁"],
                    "special_locations": ["青云山", "万兽森林", "无极海"]
                },
                {
                    "name": "中州",
                    "type": "繁华地带", 
                    "features": ["交通枢纽", "贸易中心", "文化荟萃"],
                    "dangers": ["势力复杂", "暗流涌动", "争斗不断"],
                    "special_locations": ["天音谷", "帝都", "拍卖行"]
                },
                {
                    "name": "西漠",
                    "type": "荒凉之地",
                    "features": ["环境恶劣", "邪修聚集", "宝物埋藏"],
                    "dangers": ["魔修横行", "沙暴肆虐", "诅咒之地"],
                    "special_locations": ["黑风谷", "血沙漠", "镇魔塔"]
                },
                {
                    "name": "南荒",
                    "type": "原始森林",
                    "features": ["古树参天", "灵药遍地", "部族众多"],
                    "dangers": ["毒虫猛兽", "瘴气弥漫", "古咒陷阱"],
                    "special_locations": ["药王山", "毒龙潭", "精灵王国"]
                },
                {
                    "name": "北冥",
                    "type": "极地冰原",
                    "features": ["千年不化", "寒气逼人", "矿藏丰富"],
                    "dangers": ["极寒之力", "冰魄妖兽", "雪崩冰裂"],
                    "special_locations": ["炼器峰", "冰宫", "玄冰洞"]
                }
            ],
            magic_system={
                "five_elements": {
                    "金": {"properties": "锋利、坚硬", "colors": "金白", "creatures": "金鸾"},
                    "木": {"properties": "生长、治愈", "colors": "青绿", "creatures": "青龙"},
                    "水": {"properties": "柔韧、变化", "colors": "蓝黑", "creatures": "玄武"},
                    "火": {"properties": "炽热、毁灭", "colors": "红橙", "creatures": "朱雀"},
                    "土": {"properties": "厚重、防御", "colors": "黄褐", "creatures": "白虎"}
                },
                "special_paths": {
                    "剑道": {"difficulty": "困难", "power": "极高", "description": "以剑为本，剑心通明"},
                    "丹道": {"difficulty": "极难", "power": "辅助", "description": "炼制丹药，医人救世"},
                    "阵法": {"difficulty": "极难", "power": "群攻", "description": "布置阵法，困敌杀敌"},
                    "符箓": {"difficulty": "中等", "power": "中等", "description": "制作符箓，快速施法"},
                    "炼器": {"difficulty": "困难", "power": "辅助", "description": "炼制法宝，装备提升"},
                    "驭兽": {"difficulty": "中等", "power": "中高", "description": "驯服妖兽，并肩作战"},
                    "音律": {"difficulty": "困难", "power": "群攻", "description": "以音为攻，乱人心智"}
                },
                "cultivation_resources": {
                    "灵石": ["下品", "中品", "上品", "极品", "仙石"],
                    "丹药": ["聚气丹", "筑基丹", "结金丹", "破婴丹", "化神丹"],
                    "功法": ["黄级", "玄级", "地级", "天级", "仙级"],
                    "法宝": ["法器", "宝器", "灵器", "仙器", "先天灵宝"]
                }
            },
            artifacts=[
                {
                    "name": "青锋剑",
                    "grade": "上品法器",
                    "description": "锋利无比的飞剑，可破金断石",
                    "origin": "青云门传承宝物"
                },
                {
                    "name": "炼心鼎",
                    "grade": "极品宝器",
                    "description": "炼丹神鼎，可提高丹药品质",
                    "origin": "万药谷镇谷之宝"
                },
                {
                    "name": "天音琴",
                    "grade": "灵器",
                    "description": "音律攻击法宝，琴音杀人于无形",
                    "origin": "天音宗传承至宝"
                }
            ],
            background_story="""
这是一个修仙者追求长生不老的世界。天地分为五大区域：东荒、中州、西漠、南荒、北冥。
东荒灵气最为浓郁，是各大正派宗门的聚集地，其中青云门实力最强。
中州为各势力交汇之地，既有繁华也有暗流。
西漠环境恶劣，多为邪修盘踞。
南荒原始森林密布，隐藏着古老的秘密。
北冥冰天雪地，是炼器师的天堂。

在这个世界中，修仙者按修为分为练气、筑基、金丹、元婴、化神、合体、大乘、渡劫、真仙等境界。
每个境界又分初期、中期、后期、大圆满四个小境界。
修仙者可以修炼五行法术，也可以专精剑道、丹道、阵法等特殊道路。

千年前，魔道大兴，正邪大战，最终正道获胜，邪修退居西漠。
但近年来又有魔道复苏的迹象，暗流涌动，大世将临...
"""
        )
        
        self.world_setting = world_setting
        self.save_world_setting()
        self.log_generation_step("世界观设定", "详细世界观创建完成")
        return world_setting
    
    def create_enhanced_characters(self) -> List[Character]:
        """创建增强的角色设定"""
        self.log_generation_step("角色设定", "开始创建主要角色")
        
        characters = [
            # 主角
            Character(
                name="林逸",
                age=18,
                gender="男",
                cultivation_level="凡人",
                personality="坚韧不拔，重情重义，天赋异禀，心思敏捷",
                background="出身贫寒山村，父母早亡，意外获得修仙传承",
                relationships=[],
                abilities=["极品五行灵根", "过目不忘", "天生剑心", "超强悟性"],
                goals="成为绝世强者，保护重要的人，探索修仙大道",
                role_type="主角"
            ),
            
            # 师父
            Character(
                name="玄机真人",
                age=800,
                gender="男",
                cultivation_level="化神后期",
                personality="睿智深沉，亦师亦友，神秘莫测",
                background="青云门太上长老，隐世高人，主角的引路人",
                relationships=[{"relation": "师父", "target": "林逸"}],
                abilities=["阵法大师", "丹道宗师", "剑道通神", "占卜预知"],
                goals="培养优秀弟子，守护青云门",
                role_type="导师"
            ),
            
            # 青梅竹马/女主角
            Character(
                name="苏婉儿",
                age=17,
                gender="女",
                cultivation_level="练气期",
                personality="温柔善良，聪慧坚强，对主角情深",
                background="同村少女，与主角青梅竹马，也有修仙天赋",
                relationships=[{"relation": "青梅竹马", "target": "林逸"}],
                abilities=["上品水灵根", "医术精通", "心灵手巧"],
                goals="跟随林逸修仙，成为他的助力",
                role_type="女主角"
            ),
            
            # 师兄
            Character(
                name="张浩然",
                age=25,
                gender="男",
                cultivation_level="筑基中期",
                personality="豪爽正直，义薄云天，护短",
                background="青云门内门弟子，主角的师兄",
                relationships=[{"relation": "师兄", "target": "林逸"}],
                abilities=["上品金灵根", "剑法精湛", "领导能力强"],
                goals="保护师弟，振兴青云门",
                role_type="师兄"
            ),
            
            # 反派师兄
            Character(
                name="李冥",
                age=30,
                gender="男",
                cultivation_level="筑基后期",
                personality="阴险狡诈，嫉妒心重，心狠手辣",
                background="青云门内门弟子，因嫉妒主角天赋而生恨",
                relationships=[{"relation": "敌对师兄", "target": "林逸"}],
                abilities=["中品火灵根", "阴毒功法", "诡计多端"],
                goals="除掉林逸，获得更多资源",
                role_type="早期反派"
            ),
            
            # 门派长老
            Character(
                name="青云子",
                age=1200,
                gender="男",
                cultivation_level="合体初期",
                personality="威严慈祥，公正严明，德高望重",
                background="青云门掌门，实力强大的修仙者",
                relationships=[{"relation": "掌门", "target": "林逸"}],
                abilities=["极品风灵根", "青云剑诀", "门派管理"],
                goals="守护青云门，培养后辈",
                role_type="门派长者"
            ),
            
            # 主要反派
            Character(
                name="血魔老祖",
                age=2000,
                gender="男",
                cultivation_level="大乘中期",
                personality="嗜血残忍，野心勃勃，城府极深",
                background="魔道巨擘，千年前正邪大战的幸存者",
                relationships=[{"relation": "宿敌", "target": "林逸"}],
                abilities=["血道魔功", "魅惑之术", "不死之身"],
                goals="魔道复兴，统治修仙界",
                role_type="最终反派"
            )
        ]
        
        self.characters = characters
        self.save_characters()
        self.log_generation_step("角色设定", f"创建了{len(characters)}个主要角色")
        return self.characters
    
    def generate_enhanced_outline(self, target_chapters: int = 300) -> List[ChapterOutline]:
        """生成增强的整体大纲"""
        self.log_generation_step("大纲生成", f"开始生成{target_chapters}章的详细大纲")
        
        # 详细的阶段规划
        phases = [
            {
                "name": "入门期", 
                "chapters": 50, 
                "theme": "获得机缘，初入修仙世界",
                "key_events": ["获得传承", "拜入青云门", "初次修炼", "同门交往", "小试身手"],
                "cultivation_range": ["凡人", "练气大圆满"],
                "main_conflicts": ["资质怀疑", "门内竞争", "基础挑战"]
            },
            {
                "name": "成长期", 
                "chapters": 100, 
                "theme": "历练成长，结识伙伴",
                "key_events": ["门派试炼", "秘境探险", "结识盟友", "初恋情愫", "强敌出现"],
                "cultivation_range": ["筑基初期", "金丹初期"],
                "main_conflicts": ["生死历练", "情感纠葛", "宗门危机"]
            },
            {
                "name": "崛起期", 
                "chapters": 100, 
                "theme": "声名鹊起，面临大敌",
                "key_events": ["名震一方", "跨域冒险", "强者对决", "门派大战", "身世揭秘"],
                "cultivation_range": ["金丹中期", "元婴后期"],
                "main_conflicts": ["正邪对立", "权力斗争", "命运抉择"]
            },
            {
                "name": "巅峰期", 
                "chapters": 50, 
                "theme": "巅峰对决，拯救世界",
                "key_events": ["魔道复苏", "最终决战", "牺牲拯救", "大道圆满", "飞升成仙"],
                "cultivation_range": ["化神期", "真仙"],
                "main_conflicts": ["存亡之战", "道心考验", "终极选择"]
            }
        ]
        
        outlines = []
        chapter_num = 1
        
        for phase in phases:
            chapters_per_event = phase["chapters"] // len(phase["key_events"])
            
            for i, event in enumerate(phase["key_events"]):
                for j in range(chapters_per_event):
                    if chapter_num > target_chapters:
                        break
                        
                    # 计算修炼进度
                    progress = (i * chapters_per_event + j) / phase["chapters"]
                    
                    outline = ChapterOutline(
                        chapter_number=chapter_num,
                        title=f"第{chapter_num}章 {event}相关情节",
                        main_events=[f"{event}的具体展开", "角色互动", "剧情推进"],
                        character_development=f"主角在{phase['name']}的成长",
                        plot_progression=f"推进{event}相关剧情",
                        cultivation_progress=f"修为提升-{phase['cultivation_range'][0]}向{phase['cultivation_range'][1]}发展",
                        conflicts=phase["main_conflicts"],
                        estimated_word_count=3000
                    )
                    outlines.append(outline)
                    chapter_num += 1
        
        self.overall_outline = outlines[:target_chapters]
        self.save_overall_outline()
        self.log_generation_step("大纲生成", f"生成了{len(self.overall_outline)}章的详细大纲")
        return self.overall_outline
    
    def generate_detailed_chapter_outline(self, chapter_number: int) -> ChapterOutline:
        """生成详细章节大纲"""
        self.log_generation_step("详细大纲", f"生成第{chapter_number}章的详细大纲")
        
        if chapter_number > len(self.overall_outline):
            raise ValueError(f"章节号{chapter_number}超出范围")
        
        base_outline = self.overall_outline[chapter_number - 1]
        
        # 根据章节位置和前面章节的内容生成更详细的大纲
        previous_summary = ""
        if self.chapters:
            previous_summary = self.chapters[-1].summary if self.chapters else "故事开始"
        
        # 生成具体的章节内容大纲
        if chapter_number == 1:
            detailed_outline = ChapterOutline(
                chapter_number=1,
                title="第一章 山村少年",
                main_events=[
                    "介绍主角林逸的出身和现状",
                    "展现山村的贫困生活",
                    "意外发现修仙传承",
                    "决心踏上修仙之路"
                ],
                character_development="从普通山村少年到有志修仙者的转变",
                plot_progression="故事开端，为后续修仙之路做铺垫",
                cultivation_progress="尚未开始修炼，但获得修仙机缘",
                conflicts=["内心的渴望与现实的差距", "对未知世界的恐惧"],
                estimated_word_count=3000
            )
        elif chapter_number <= 10:
            detailed_outline = ChapterOutline(
                chapter_number=chapter_number,
                title=f"第{chapter_number}章 初入修仙",
                main_events=[
                    "学习基础修炼知识",
                    "第一次感应灵气",
                    "遇到修仙界的人或事",
                    "对修仙世界的初步了解"
                ],
                character_development="逐渐适应修仙者的身份",
                plot_progression="建立修仙世界观，为拜师做准备",
                cultivation_progress="练气初期的修炼",
                conflicts=["修炼的困难", "对力量的渴望"],
                estimated_word_count=3000
            )
        else:
            # 基于基础大纲生成详细内容
            detailed_outline = ChapterOutline(
                chapter_number=chapter_number,
                title=f"第{chapter_number}章 " + base_outline.title.split(' ')[-1] if ' ' in base_outline.title else base_outline.title,
                main_events=base_outline.main_events,
                character_development=base_outline.character_development,
                plot_progression=base_outline.plot_progression,
                cultivation_progress=base_outline.cultivation_progress,
                conflicts=base_outline.conflicts,
                estimated_word_count=3000
            )
        
        return detailed_outline
    
    def generate_enhanced_chapter_content(self, chapter_outline: ChapterOutline) -> Chapter:
        """生成增强的章节内容"""
        self.log_generation_step("内容生成", f"生成第{chapter_outline.chapter_number}章的内容")
        
        # 获取前面章节的内容摘要用于保持连贯性
        previous_content = ""
        if self.chapters:
            previous_content = self.chapters[-1].content[-500:]  # 获取上一章的最后500字
        
        # 生成章节内容的提示词
        prompt = self.ai_generator.generate_chapter_content_prompt(
            chapter_outline, 
            self.world_setting, 
            self.characters, 
            previous_content
        )
        
        # 调用AI生成内容（这里使用模板，实际可以接入AI API）
        content = self._generate_specific_chapter_content(chapter_outline.chapter_number)
        
        # 分析生成的内容，提取关键信息
        key_plot_points = self._extract_plot_points(content)
        character_changes = self._extract_character_changes(content, chapter_outline.chapter_number)
        next_chapter_setup = self._generate_next_chapter_setup(chapter_outline.chapter_number)
        summary = self._generate_chapter_summary(content, chapter_outline.chapter_number)
        
        chapter = Chapter(
            outline=chapter_outline,
            content=content,
            actual_word_count=len(content),
            key_plot_points=key_plot_points,
            character_changes=character_changes,
            next_chapter_setup=next_chapter_setup,
            summary=summary
        )
        
        self.log_generation_step("内容生成", f"第{chapter_outline.chapter_number}章内容生成完成，共{len(content)}字")
        return chapter
    
    def _generate_specific_chapter_content(self, chapter_number: int) -> str:
        """生成特定章节的内容"""
        if chapter_number == 1:
            return """
第一章 山村少年

　　青山如黛，白云悠悠。

　　在东荒边陲的一个小山村里，一个十八岁的少年正坐在村口的大石头上，望着远方连绵不绝的青云山脉，眼中满含着向往和不甘。

　　这少年名叫林逸，出身贫寒，父母早亡，只靠着村里的接济勉强度日。虽然生活艰难，但他从小就聪慧过人，听村里的老人讲述修仙者的传说时，总是听得最认真的那一个。

　　"要是我也能修仙就好了..."林逸轻声自语，目光中闪过一丝渴望。

　　就在这时，一阵奇异的光芒从山林深处传来，紧接着是一声惊天动地的巨响！

　　林逸心中一惊，本能地向光芒传来的方向看去，只见山林中有一道金光冲天而起，随即又迅速消失不见。

　　"那是什么？"林逸喃喃自语，心中涌起一股强烈的好奇心。

　　犹豫了片刻，林逸还是决定去看看。他沿着山路向着光芒消失的地方走去，越走越深入，不知不觉已经来到了平时很少有人涉足的深山之中。

　　在一个隐蔽的山洞里，林逸发现了一个身着道袍、仙风道骨的老者。老者已经没有了呼吸，但脸上却带着安详的笑容。

　　在老者身边，有一枚散发着微光的玉简。

　　林逸小心翼翼地拿起玉简，刚一触碰，大量的信息就涌入了他的脑海：《基础练气法》、修仙者的等级、灵根的重要性...

　　原来，这位老者是一位修仙者，在寿元将尽之时回到此地，留下了自己的传承。

　　"这...这是真的吗？"林逸的手在颤抖，不敢相信自己竟然如此幸运。

　　按照玉简中的记录，林逸开始尝试感应天地灵气。令他惊喜的是，他竟然很快就感应到了丝丝缕缕的灵气！

　　"我真的可以修仙！"林逸激动得几乎要跳起来。

　　从这一刻起，他知道自己的命运将彻底改变。他要走出这个小山村，去见识更广阔的修仙世界！

　　夜幕降临，林逸怀着激动的心情回到村中，开始暗自修炼起来。他知道，这只是万里长征的第一步，前路充满未知和挑战，但他已经做好了准备。

　　修仙之路，从此开始！
"""
        elif chapter_number == 2:
            return """
第二章 初修练气

　　接下来的几天里，林逸一边维持着平常的生活，一边暗中修炼着《基础练气法》。

　　每当夜深人静的时候，他就会按照玉简中的法门，尝试感应和吸收天地间的灵气。

　　修炼的过程比想象中更加困难。灵气虽然存在，但想要将其引入体内并加以炼化，却需要极大的专注力和毅力。

　　"呼..."林逸睁开眼睛，额头已经渗出了细密的汗珠。

　　经过三天的努力，他终于成功地将一丝灵气引入了体内，虽然微弱，但这已经是巨大的进步了。

　　"按照玉简中的记载，我现在算是踏入了练气期的门槛。"林逸心中欣喜，但很快又冷静下来。

　　他知道这只是开始，练气期分为九个层次，而他现在连第一层都没有稳固。

　　更重要的是，他需要更好的修炼环境和资源。村子里的灵气实在太稀薄了，而且他也不能一直隐瞒自己的修炼。

　　正当林逸为未来的修炼之路发愁时，村子里来了一个意想不到的客人。

　　那是一个中年道士，仙风道骨，眼神深邃，身上散发着一股让人不敢直视的威压。

　　"这位道长，您这是？"村长小心翼翼地询问着。

　　"贫道路过此地，感应到这里有修仙的气息，特来查看一二。"道士的声音平和，但林逸听了却心中一紧。

　　难道是自己修炼的事情被发现了？

　　道士的目光在村民中扫过，最终停留在了林逸身上。

　　"就是你吧，小友。"道士微微一笑，"贫道青云门外门长老王青松，感应到你身上有修仙者的气息。"

　　林逸的心跳加速，但还是硬着头皮上前行礼："晚辈林逸，见过道长。"

　　王青松仔细打量着林逸，突然伸出手按在了他的手腕上。一股温和的真元流入林逸体内，探查着他的情况。

　　"有趣..."王青松收回手，眼中闪过一丝惊讶，"小友不仅有修仙根基，而且是极品五行灵根！这等天赋，万中无一啊！"

　　"什么是五行灵根？"林逸疑惑地问道。

　　"灵根是修仙者的天赋所在，分为金木水火土五行。普通人能有一种上品灵根就已经很了不起了，而你竟然五种灵根俱全，且都是极品！"王青松越说越激动，"小友，你可愿意拜入我青云门？"

　　林逸心中狂喜，但表面还是保持冷静："青云门是什么样的门派？"

　　"青云门乃是东荒第一大派，门中弟子十万余人，实力强大。如果你能拜入门中，必定前途无量！"

　　林逸没有立即答应，而是问道："那我需要做什么？"

　　"三日后，青云门将在此地举行入门考核。以你的天赋，通过考核不在话下。"王青松说道，"不过在此之前，你还需要将修为稍作提升，至少要达到练气期一层。"

　　"多谢道长指点！"林逸心中感激不已。

　　王青松点点头，留下了一瓶丹药和一本更详细的修炼法决后便离开了。

　　看着道士远去的身影，林逸握紧了拳头。三天时间，他要全力冲击练气期一层！

　　修仙世界的大门，即将向他敞开！
"""
        else:
            # 其他章节使用通用模板
            return f"""
第{chapter_number}章 修炼之路

　　随着修为的不断提升，林逸对修仙世界的了解也越来越深入。

　　在青云门的这段时间里，他不仅学会了更多的修炼法门，还结识了许多志同道合的师兄弟。

　　然而，修仙之路从来不是一帆风顺的。在这个强者为尊的世界里，每一步都充满了挑战和危险。

　　今日，林逸又将面临新的考验...

　　"林师弟，听说今天有一个重要的任务需要我们去完成。"张浩然走过来对林逸说道。

　　"什么任务？"林逸询问。

　　"据说是门派附近出现了妖兽作乱，需要我们去清除。这对我们来说既是任务，也是历练的好机会。"

　　林逸点点头，心中既有紧张也有期待。自从修炼以来，他还没有真正经历过实战，这次正好是检验自己实力的机会。

　　准备好必要的法器和丹药后，几人踏上了执行任务的道路...

　　（此处为第{chapter_number}章的内容，实际使用时会根据具体大纲生成更详细的内容）
"""
    
    def _extract_plot_points(self, content: str) -> List[str]:
        """从内容中提取关键剧情点"""
        # 简单的关键词提取，实际可以用NLP技术
        plot_points = []
        if "修仙" in content:
            plot_points.append("修仙相关情节")
        if "青云门" in content:
            plot_points.append("青云门相关")
        if "灵根" in content:
            plot_points.append("天赋展现")
        if "考核" in content:
            plot_points.append("入门考核")
        
        return plot_points or ["主要剧情推进"]
    
    def _extract_character_changes(self, content: str, chapter_number: int) -> List[str]:
        """提取角色变化"""
        changes = []
        if chapter_number == 1:
            changes = ["林逸获得修仙传承", "从普通人向修仙者转变"]
        elif chapter_number == 2:
            changes = ["林逸开始正式修炼", "被青云门长老发现"]
        else:
            changes = ["角色实力或认知的进一步发展"]
        
        return changes
    
    def _generate_next_chapter_setup(self, chapter_number: int) -> str:
        """生成下一章的铺垫"""
        if chapter_number == 1:
            return "林逸将开始正式修炼，为加入修仙门派做准备"
        elif chapter_number == 2:
            return "林逸将参加青云门的入门考核"
        else:
            return f"第{chapter_number + 1}章将继续推进主线剧情，角色面临新的挑战"
    
    def _generate_chapter_summary(self, content: str, chapter_number: int) -> str:
        """生成章节总结"""
        if chapter_number == 1:
            return "第1章：林逸在山村发现修仙传承，获得《基础练气法》，决心踏上修仙之路。"
        elif chapter_number == 2:
            return "第2章：林逸开始修炼，被青云门长老发现其极品五行灵根的天赋，获得入门考核机会。"
        else:
            return f"第{chapter_number}章：主角修炼成长，剧情继续推进。"
    
    def generate_progress_report(self) -> Dict[str, Any]:
        """生成详细的进度报告"""
        total_words = sum(chapter.actual_word_count for chapter in self.chapters)
        
        # 计算各阶段进度
        phase_progress = {}
        current_phase = "入门期"
        if self.current_chapter > 50:
            current_phase = "成长期"
        if self.current_chapter > 150:
            current_phase = "崛起期"
        if self.current_chapter > 250:
            current_phase = "巅峰期"
        
        report = {
            'project_info': {
                'project_name': self.project_name,
                'creation_time': datetime.datetime.now().isoformat(),
                'ai_type': self.ai_generator.api_type
            },
            'progress': {
                'current_chapter': self.current_chapter,
                'total_planned_chapters': len(self.overall_outline),
                'completion_rate': f"{(self.current_chapter / len(self.overall_outline) * 100):.1f}%",
                'current_phase': current_phase
            },
            'content_stats': {
                'total_words': total_words,
                'average_words_per_chapter': total_words // max(1, len(self.chapters)),
                'estimated_total_words': len(self.overall_outline) * 3000,
                'estimated_remaining_words': (len(self.overall_outline) - self.current_chapter) * 3000
            },
            'story_elements': {
                'world_setting_created': self.world_setting is not None,
                'main_characters_count': len(self.characters),
                'cultivation_levels': len(self.world_setting.cultivation_levels) if self.world_setting else 0,
                'sects_count': len(self.world_setting.sects) if self.world_setting else 0
            },
            'latest_chapter': {
                'summary': self.chapters[-1].summary if self.chapters else "暂无章节",
                'key_points': self.chapters[-1].key_plot_points if self.chapters else [],
                'next_setup': self.chapters[-1].next_chapter_setup if self.chapters else ""
            },
            'generation_log': self.generation_log[-10:]  # 最近10条日志
        }
        
        return report
    
    def save_detailed_project_state(self):
        """保存详细的项目状态"""
        # 保存基础状态
        super().save_project_state()
        
        # 保存额外的详细信息
        detailed_state = {
            'chapter_history': self.chapter_history,
            'generation_log': self.generation_log,
            'ai_generator_type': self.ai_generator.api_type,
            'enhanced_features': True
        }
        
        with open(f"{self.project_dir}/detailed_state.json", 'w', encoding='utf-8') as f:
            json.dump(detailed_state, f, ensure_ascii=False, indent=2)
    
    def generate_batch_chapters(self, count: int) -> List[Chapter]:
        """批量生成多个章节"""
        self.log_generation_step("批量生成", f"开始批量生成{count}个章节")
        
        generated_chapters = []
        
        for i in range(count):
            try:
                chapter = self.generate_next_chapter()
                generated_chapters.append(chapter)
                
                # 保存每个章节后更新状态
                self.save_detailed_project_state()
                
                self.log_generation_step("批量生成", f"第{chapter.outline.chapter_number}章生成完成")
                
            except Exception as e:
                self.log_generation_step("批量生成", f"第{self.current_chapter + 1}章生成失败: {str(e)}")
                break
        
        self.log_generation_step("批量生成", f"批量生成完成，共生成{len(generated_chapters)}章")
        return generated_chapters

if __name__ == "__main__":
    # 示例使用增强版生成器
    print("=== 增强版修仙小说生成系统 ===")
    
    # 创建生成器实例
    generator = EnhancedNovelGenerator("修仙传说", ai_type="local")
    
    # 完整流程演示
    try:
        # 1. 创建世界观
        world = generator.create_enhanced_world_setting()
        print("✓ 增强世界观设定完成")
        
        # 2. 创建角色
        characters = generator.create_enhanced_characters()
        print(f"✓ 创建了{len(characters)}个主要角色")
        
        # 3. 生成整体大纲
        outline = generator.generate_enhanced_outline(300)
        print(f"✓ 生成了{len(outline)}章的详细大纲")
        
        # 4. 生成前几章
        for i in range(3):
            chapter = generator.generate_next_chapter()
            print(f"✓ 第{chapter.outline.chapter_number}章生成完成")
        
        # 5. 生成详细报告
        report = generator.generate_progress_report()
        print("\n=== 详细进度报告 ===")
        print(f"项目名称: {report['project_info']['project_name']}")
        print(f"当前进度: {report['progress']['completion_rate']}")
        print(f"总字数: {report['content_stats']['total_words']}")
        print(f"当前阶段: {report['progress']['current_phase']}")
        print(f"最新章节: {report['latest_chapter']['summary']}")
        
        print("\n✓ 小说生成系统演示完成！")
        
    except Exception as e:
        print(f"✗ 生成过程中出现错误: {str(e)}")
        logging.error(f"生成错误: {str(e)}")