#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试脚本
验证AI修仙小说生成系统的基本功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """测试基本功能"""
    print("AI修仙小说生成系统 - 基本功能测试")
    print("=" * 50)
    
    try:
        # 测试导入模块
        print("1. 测试模块导入...")
        from novel_generation_system import NovelManager, NovelDatabase
        from ai_integration import OpenAIGenerator, NovelAIGenerator
        from config import get_config
        print("✓ 模块导入成功")
        
        # 测试配置
        print("2. 测试配置加载...")
        config = get_config("novel")
        print(f"✓ 配置加载成功，小说标题：{config.get('NOVEL_TITLE', '未知')}")
        
        # 测试数据库
        print("3. 测试数据库初始化...")
        db = NovelDatabase()
        print("✓ 数据库初始化成功")
        
        # 测试小说管理器
        print("4. 测试小说管理器...")
        novel_manager = NovelManager("测试小说")
        print("✓ 小说管理器创建成功")
        
        # 测试世界观构建
        print("5. 测试世界观构建...")
        cultivation_system = novel_manager.world_builder.create_cultivation_system()
        print(f"✓ 修仙体系构建成功，包含 {len(cultivation_system['realms'])} 个境界")
        
        # 测试角色创建
        print("6. 测试角色创建...")
        main_character = novel_manager.character_builder.create_main_character("测试主角")
        print(f"✓ 角色创建成功：{main_character.name}")
        
        # 测试AI生成器
        print("7. 测试AI生成器...")
        ai_generator = OpenAIGenerator()  # 不传入API key，使用模拟生成
        novel_ai = NovelAIGenerator(ai_generator)
        print("✓ AI生成器创建成功")
        
        # 测试章节生成
        print("8. 测试章节生成...")
        outline = novel_manager.outline_generator.generate_chapter_outline(1, "测试上下文")
        chapter = novel_manager.chapter_generator.generate_chapter(outline, None)
        print(f"✓ 章节生成成功，字数：{chapter.word_count}")
        
        # 测试文件保存
        print("9. 测试文件保存...")
        novel_manager._save_chapter_to_file(chapter)
        print("✓ 文件保存成功")
        
        # 检查输出目录
        output_dir = Path("novel_output/测试小说")
        if output_dir.exists():
            files = list(output_dir.glob("*.txt"))
            print(f"✓ 输出目录创建成功，包含 {len(files)} 个文件")
        
        print("\n" + "=" * 50)
        print("所有测试通过！系统运行正常。")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

def test_world_building():
    """测试世界观构建"""
    print("\n世界观构建详细测试")
    print("-" * 30)
    
    try:
        from novel_generation_system import NovelManager
        
        novel_manager = NovelManager("世界观测试")
        
        # 测试修仙体系
        print("构建修仙体系...")
        cultivation = novel_manager.world_builder.create_cultivation_system()
        print(f"境界数量：{len(cultivation['realms'])}")
        for realm in cultivation['realms'][:3]:  # 只显示前3个
            print(f"  - {realm['name']}: {len(realm['levels'])} 个小境界")
        
        # 测试地理环境
        print("\n构建地理环境...")
        geography = novel_manager.world_builder.create_geography()
        print(f"大陆数量：{len(geography['continents'])}")
        for continent in geography['continents']:
            print(f"  - {continent['name']}: {continent['description']}")
        
        # 测试历史背景
        print("\n构建历史背景...")
        history = novel_manager.world_builder.create_history()
        print(f"传说数量：{len(history['ancient_legends'])}")
        print(f"重大事件：{len(history['major_events'])}")
        print(f"传奇人物：{len(history['legendary_figures'])}")
        
        return True
        
    except Exception as e:
        print(f"世界观构建测试失败：{e}")
        return False

def test_character_creation():
    """测试角色创建"""
    print("\n角色创建详细测试")
    print("-" * 30)
    
    try:
        from novel_generation_system import NovelManager
        
        novel_manager = NovelManager("角色测试")
        
        # 创建主角
        print("创建主角...")
        main_char = novel_manager.character_builder.create_main_character("林逸")
        print(f"主角：{main_char.name}")
        print(f"角色：{main_char.role}")
        print(f"性格：{main_char.personality}")
        print(f"境界：{main_char.cultivation_level}")
        print(f"能力：{', '.join(main_char.abilities)}")
        
        # 创建配角
        print("\n创建配角...")
        master = novel_manager.character_builder.create_supporting_character(
            "玄清子", "师父", "慈祥严厉，深不可测"
        )
        print(f"师父：{master.name}")
        print(f"角色：{master.role}")
        print(f"性格：{master.personality}")
        
        return True
        
    except Exception as e:
        print(f"角色创建测试失败：{e}")
        return False

def test_chapter_generation():
    """测试章节生成"""
    print("\n章节生成详细测试")
    print("-" * 30)
    
    try:
        from novel_generation_system import NovelManager
        
        novel_manager = NovelManager("章节测试")
        
        # 生成大纲
        print("生成章节大纲...")
        outline = novel_manager.outline_generator.generate_chapter_outline(1, "主角开始修仙")
        print(f"章节标题：{outline.title}")
        print(f"主要事件：{outline.main_events}")
        print(f"涉及角色：{outline.characters_involved}")
        print(f"修仙内容：{outline.cultivation_content}")
        
        # 生成章节
        print("\n生成章节内容...")
        chapter = novel_manager.chapter_generator.generate_chapter(outline, None)
        print(f"章节标题：{chapter.title}")
        print(f"字数：{chapter.word_count}")
        print(f"总结：{chapter.summary}")
        print(f"下章计划：{chapter.next_chapter_plan}")
        
        # 保存章节
        print("\n保存章节...")
        novel_manager._save_chapter_to_file(chapter)
        print("章节保存成功")
        
        return True
        
    except Exception as e:
        print(f"章节生成测试失败：{e}")
        return False

def main():
    """主函数"""
    print("开始AI修仙小说生成系统测试")
    print("=" * 60)
    
    # 运行基本功能测试
    if not test_basic_functionality():
        print("基本功能测试失败，停止后续测试")
        return
    
    # 运行详细测试
    test_world_building()
    test_character_creation()
    test_chapter_generation()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("系统已成功创建，可以开始生成修仙小说了。")

if __name__ == "__main__":
    main()