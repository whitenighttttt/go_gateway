#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI修仙小说生成系统演示
完整的使用示例
"""

import os
import sys
import json
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from novel_generation_system import NovelManager, NovelDatabase, WorldBuilder, CharacterBuilder
from ai_integration import OpenAIGenerator, NovelAIGenerator, CultivationPromptTemplates, QualityChecker
from config import get_config, NovelConfig, AIConfig

class NovelGenerationDemo:
    """小说生成演示类"""
    
    def __init__(self, novel_title: str = "修仙之路"):
        self.novel_title = novel_title
        self.config = get_config("novel")
        
        # 初始化AI生成器
        self.ai_generator = OpenAIGenerator(api_key=AIConfig.OPENAI_API_KEY)
        self.novel_ai = NovelAIGenerator(self.ai_generator)
        self.quality_checker = QualityChecker(self.ai_generator)
        
        # 初始化小说管理器
        self.novel_manager = NovelManager(novel_title)
        
        print(f"初始化修仙小说生成系统：{novel_title}")
        print("=" * 60)
    
    def demo_world_building(self):
        """演示世界观构建"""
        print("\n1. 世界观构建演示")
        print("-" * 30)
        
        # 构建修仙体系
        print("构建修仙体系...")
        cultivation_system = self.novel_manager.world_builder.create_cultivation_system()
        print(f"✓ 修仙体系构建完成，包含 {len(cultivation_system['realms'])} 个境界")
        
        # 构建地理环境
        print("构建地理环境...")
        geography = self.novel_manager.world_builder.create_geography()
        print(f"✓ 地理环境构建完成，包含 {len(geography['continents'])} 个大陆")
        
        # 构建历史背景
        print("构建历史背景...")
        history = self.novel_manager.world_builder.create_history()
        print(f"✓ 历史背景构建完成，包含 {len(history['ancient_legends'])} 个传说")
        
        return {
            "cultivation_system": cultivation_system,
            "geography": geography,
            "history": history
        }
    
    def demo_character_creation(self):
        """演示角色创建"""
        print("\n2. 角色创建演示")
        print("-" * 30)
        
        characters = {}
        
        # 创建主角
        print("创建主角...")
        main_character = self.novel_manager.character_builder.create_main_character("林逸")
        characters["主角"] = main_character
        print(f"✓ 主角创建完成：{main_character.name}")
        
        # 创建师父
        print("创建师父...")
        master = self.novel_manager.character_builder.create_supporting_character(
            "玄清子", "师父", "慈祥严厉，深不可测"
        )
        characters["师父"] = master
        print(f"✓ 师父创建完成：{master.name}")
        
        # 创建女主角
        print("创建女主角...")
        heroine = self.novel_manager.character_builder.create_supporting_character(
            "苏雨晴", "女主角", "聪慧机敏，性格坚韧"
        )
        characters["女主角"] = heroine
        print(f"✓ 女主角创建完成：{heroine.name}")
        
        return characters
    
    def demo_chapter_generation(self, chapter_number: int = 1):
        """演示章节生成"""
        print(f"\n3. 章节生成演示（第{chapter_number}章）")
        print("-" * 30)
        
        # 生成章节大纲
        print("生成章节大纲...")
        context = "主角林逸刚刚踏上修仙之路，正在寻找修炼功法"
        outline = self.novel_manager.outline_generator.generate_chapter_outline(chapter_number, context)
        print(f"✓ 大纲生成完成：{outline.title}")
        
        # 生成章节内容
        print("生成章节内容...")
        chapter = self.novel_manager.chapter_generator.generate_chapter(outline, None)
        print(f"✓ 章节生成完成，字数：{chapter.word_count}")
        
        # 质量检查
        print("进行质量检查...")
        quality_report = self.quality_checker.check_chapter_quality(chapter.content)
        print(f"✓ 质量检查完成")
        
        # 保存章节
        self.novel_manager._save_chapter_to_file(chapter)
        print(f"✓ 章节已保存到文件")
        
        return {
            "outline": outline,
            "chapter": chapter,
            "quality_report": quality_report
        }
    
    def demo_ai_integration(self):
        """演示AI集成功能"""
        print("\n4. AI集成功能演示")
        print("-" * 30)
        
        # 使用AI生成世界观设定
        print("使用AI生成修仙体系...")
        prompt = CultivationPromptTemplates.world_setting_prompt("cultivation_system")
        ai_cultivation = self.novel_ai.generate_world_setting("cultivation_system", prompt)
        print("✓ AI修仙体系生成完成")
        
        # 使用AI生成角色设定
        print("使用AI生成主角设定...")
        character_prompt = CultivationPromptTemplates.character_prompt("主角")
        ai_character = self.novel_ai.generate_character("主角", character_prompt)
        print("✓ AI角色设定生成完成")
        
        # 使用AI生成章节大纲
        print("使用AI生成章节大纲...")
        outline_prompt = CultivationPromptTemplates.chapter_outline_prompt(1, "主角开始修仙")
        ai_outline = self.novel_ai.generate_chapter_outline(1, "主角开始修仙", outline_prompt)
        print("✓ AI章节大纲生成完成")
        
        return {
            "ai_cultivation": ai_cultivation,
            "ai_character": ai_character,
            "ai_outline": ai_outline
        }
    
    def demo_volume_generation(self, volume_number: int = 1):
        """演示整卷生成"""
        print(f"\n5. 整卷生成演示（第{volume_number}卷）")
        print("-" * 30)
        
        print(f"开始生成第{volume_number}卷...")
        self.novel_manager.generate_volume(volume_number)
        print(f"✓ 第{volume_number}卷生成完成")
        
        # 统计信息
        total_chapters = NovelConfig.CHAPTERS_PER_VOLUME
        total_words = total_chapters * NovelConfig.WORDS_PER_CHAPTER
        print(f"  章节数：{total_chapters}")
        print(f"  预计字数：{total_words:,}")
    
    def demo_data_export(self):
        """演示数据导出"""
        print("\n6. 数据导出演示")
        print("-" * 30)
        
        print("导出小说数据...")
        self.novel_manager.export_novel_data()
        print("✓ 数据导出完成")
        
        # 显示输出目录结构
        output_dir = Path(f"novel_output/{self.novel_title}")
        if output_dir.exists():
            print(f"输出目录：{output_dir}")
            for file in output_dir.glob("*"):
                if file.is_file():
                    print(f"  📄 {file.name}")
    
    def run_full_demo(self):
        """运行完整演示"""
        print("开始AI修仙小说生成系统完整演示")
        print("=" * 60)
        
        try:
            # 1. 世界观构建
            world_data = self.demo_world_building()
            
            # 2. 角色创建
            characters = self.demo_character_creation()
            
            # 3. AI集成演示
            ai_results = self.demo_ai_integration()
            
            # 4. 单章生成演示
            chapter_data = self.demo_chapter_generation(1)
            
            # 5. 整卷生成演示（可选，注释掉以节省时间）
            # self.demo_volume_generation(1)
            
            # 6. 数据导出
            self.demo_data_export()
            
            print("\n" + "=" * 60)
            print("演示完成！")
            print("生成的文件保存在 novel_output 目录中")
            
            return {
                "world_data": world_data,
                "characters": characters,
                "ai_results": ai_results,
                "chapter_data": chapter_data
            }
            
        except Exception as e:
            print(f"演示过程中出现错误：{e}")
            return None

def interactive_demo():
    """交互式演示"""
    print("AI修仙小说生成系统 - 交互式演示")
    print("=" * 50)
    
    # 获取小说标题
    novel_title = input("请输入小说标题（默认：修仙之路）：").strip()
    if not novel_title:
        novel_title = "修仙之路"
    
    # 创建演示实例
    demo = NovelGenerationDemo(novel_title)
    
    # 显示菜单
    while True:
        print("\n请选择要演示的功能：")
        print("1. 世界观构建")
        print("2. 角色创建")
        print("3. 单章生成")
        print("4. AI集成功能")
        print("5. 整卷生成")
        print("6. 数据导出")
        print("7. 完整演示")
        print("0. 退出")
        
        choice = input("\n请输入选择（0-7）：").strip()
        
        if choice == "0":
            print("退出演示")
            break
        elif choice == "1":
            demo.demo_world_building()
        elif choice == "2":
            demo.demo_character_creation()
        elif choice == "3":
            chapter_num = input("请输入章节号（默认：1）：").strip()
            chapter_num = int(chapter_num) if chapter_num.isdigit() else 1
            demo.demo_chapter_generation(chapter_num)
        elif choice == "4":
            demo.demo_ai_integration()
        elif choice == "5":
            volume_num = input("请输入卷号（默认：1）：").strip()
            volume_num = int(volume_num) if volume_num.isdigit() else 1
            demo.demo_volume_generation(volume_num)
        elif choice == "6":
            demo.demo_data_export()
        elif choice == "7":
            demo.run_full_demo()
        else:
            print("无效选择，请重新输入")

def main():
    """主函数"""
    print("AI修仙小说生成系统")
    print("=" * 50)
    
    # 检查是否有API key
    if not AIConfig.OPENAI_API_KEY:
        print("⚠️  未设置OpenAI API Key，将使用模拟生成")
        print("如需使用真实AI生成，请设置环境变量：OPENAI_API_KEY")
        print()
    
    # 选择演示模式
    print("请选择演示模式：")
    print("1. 自动完整演示")
    print("2. 交互式演示")
    
    mode = input("请输入选择（1-2）：").strip()
    
    if mode == "1":
        # 自动完整演示
        demo = NovelGenerationDemo()
        demo.run_full_demo()
    elif mode == "2":
        # 交互式演示
        interactive_demo()
    else:
        print("无效选择，运行自动演示")
        demo = NovelGenerationDemo()
        demo.run_full_demo()

if __name__ == "__main__":
    main()