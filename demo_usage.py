#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修仙小说生成系统演示脚本

这个脚本演示了如何使用AI生成长篇中文传统修仙小说的完整流程
"""

import json
import os
from enhanced_novel_generator import EnhancedNovelGenerator

def demo_complete_workflow():
    """演示完整的小说生成工作流程"""
    print("=" * 60)
    print("修仙小说AI生成系统 - 完整流程演示")
    print("=" * 60)
    
    # 步骤1: 创建项目
    print("\n步骤1: 创建小说项目")
    print("-" * 30)
    
    project_name = "仙道传奇"
    generator = EnhancedNovelGenerator(project_name, ai_type="local")
    print(f"✓ 项目 '{project_name}' 创建成功")
    print(f"✓ 项目目录: {generator.project_dir}")
    
    # 步骤2: 世界观设定
    print("\n步骤2: 创建世界观设定")
    print("-" * 30)
    
    world_setting = generator.create_enhanced_world_setting()
    print(f"✓ 修炼等级体系: {len(world_setting.cultivation_levels)} 个等级")
    print(f"✓ 门派势力: {len(world_setting.sects)} 个门派")
    print(f"✓ 地域划分: {len(world_setting.regions)} 个区域")
    print(f"✓ 法宝类型: {len(world_setting.artifacts)} 种法宝")
    
    # 步骤3: 角色设定
    print("\n步骤3: 创建主要角色")
    print("-" * 30)
    
    characters = generator.create_enhanced_characters()
    for char in characters:
        print(f"✓ {char.name} ({char.role_type}) - {char.cultivation_level}")
    
    # 步骤4: 整体大纲
    print("\n步骤4: 生成整体大纲")
    print("-" * 30)
    
    target_chapters = 50  # 演示用较少章节
    outline = generator.generate_enhanced_outline(target_chapters)
    print(f"✓ 生成了 {len(outline)} 章的详细大纲")
    
    # 显示各阶段分布
    phases = ["入门期", "成长期", "崛起期", "巅峰期"]
    phase_chapters = [12, 20, 13, 5]  # 演示分配
    for phase, count in zip(phases, phase_chapters):
        print(f"  - {phase}: {count} 章")
    
    # 步骤5: 生成章节内容
    print("\n步骤5: 生成章节内容")
    print("-" * 30)
    
    # 生成前5章作为演示
    demo_chapters = 5
    for i in range(demo_chapters):
        chapter = generator.generate_next_chapter()
        word_count = chapter.actual_word_count
        print(f"✓ 第{chapter.outline.chapter_number}章: {chapter.outline.title} ({word_count}字)")
        print(f"  主要情节: {', '.join(chapter.key_plot_points)}")
        print(f"  下章预告: {chapter.next_chapter_setup}")
        print()
    
    # 步骤6: 进度报告
    print("\n步骤6: 生成进度报告")
    print("-" * 30)
    
    report = generator.generate_progress_report()
    print_progress_report(report)
    
    # 步骤7: 项目文件结构
    print("\n步骤7: 项目文件结构")
    print("-" * 30)
    
    show_project_structure(generator.project_dir)
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    return generator

def print_progress_report(report):
    """打印进度报告"""
    print(f"项目名称: {report['project_info']['project_name']}")
    print(f"完成进度: {report['progress']['completion_rate']}")
    print(f"当前阶段: {report['progress']['current_phase']}")
    print(f"已完成章节: {report['progress']['current_chapter']}/{report['progress']['total_planned_chapters']}")
    print(f"总字数: {report['content_stats']['total_words']:,} 字")
    print(f"平均每章: {report['content_stats']['average_words_per_chapter']} 字")
    print(f"预计总字数: {report['content_stats']['estimated_total_words']:,} 字")
    print(f"角色数量: {report['story_elements']['main_characters_count']} 个")
    print(f"门派数量: {report['story_elements']['sects_count']} 个")

def show_project_structure(project_dir):
    """显示项目文件结构"""
    if not os.path.exists(project_dir):
        print("项目目录不存在")
        return
    
    print(f"项目根目录: {project_dir}")
    
    # 遍历目录结构
    for root, dirs, files in os.walk(project_dir):
        level = root.replace(project_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"{subindent}{file} ({file_size} bytes)")

def demo_chapter_generation_details():
    """演示章节生成的详细过程"""
    print("\n" + "=" * 60)
    print("章节生成详细过程演示")
    print("=" * 60)
    
    # 创建一个简单的演示项目
    generator = EnhancedNovelGenerator("演示项目", ai_type="local")
    
    # 快速设置
    generator.create_enhanced_world_setting()
    generator.create_enhanced_characters()
    generator.generate_enhanced_outline(10)
    
    print("\n1. 生成详细章节大纲")
    print("-" * 30)
    
    chapter_outline = generator.generate_detailed_chapter_outline(1)
    print(f"章节标题: {chapter_outline.title}")
    print(f"主要事件:")
    for event in chapter_outline.main_events:
        print(f"  - {event}")
    print(f"角色发展: {chapter_outline.character_development}")
    print(f"剧情推进: {chapter_outline.plot_progression}")
    print(f"修炼进展: {chapter_outline.cultivation_progress}")
    
    print("\n2. 生成章节内容")
    print("-" * 30)
    
    chapter = generator.generate_enhanced_chapter_content(chapter_outline)
    print(f"实际字数: {chapter.actual_word_count}")
    print(f"关键剧情点: {', '.join(chapter.key_plot_points)}")
    print(f"角色变化: {', '.join(chapter.character_changes)}")
    
    print("\n3. 章节内容预览")
    print("-" * 30)
    
    # 显示章节内容的前300字
    preview = chapter.content[:300] + "..." if len(chapter.content) > 300 else chapter.content
    print(preview)
    
    print("\n4. 章节总结")
    print("-" * 30)
    
    print(f"本章总结: {chapter.summary}")
    print(f"下章设定: {chapter.next_chapter_setup}")

def demo_batch_generation():
    """演示批量生成功能"""
    print("\n" + "=" * 60)
    print("批量生成功能演示")
    print("=" * 60)
    
    # 创建项目
    generator = EnhancedNovelGenerator("批量生成测试", ai_type="local")
    
    # 设置基础要素
    generator.create_enhanced_world_setting()
    generator.create_enhanced_characters()
    generator.generate_enhanced_outline(20)
    
    print("\n开始批量生成5个章节...")
    print("-" * 30)
    
    chapters = generator.generate_batch_chapters(5)
    
    print(f"\n批量生成完成，共生成 {len(chapters)} 章")
    
    # 显示每章的基本信息
    for chapter in chapters:
        print(f"第{chapter.outline.chapter_number}章: {chapter.outline.title} ({chapter.actual_word_count}字)")
    
    # 显示总体统计
    total_words = sum(chapter.actual_word_count for chapter in chapters)
    print(f"\n总字数: {total_words}")
    print(f"平均每章: {total_words // len(chapters)} 字")

def demo_customization():
    """演示自定义功能"""
    print("\n" + "=" * 60)
    print("自定义功能演示")
    print("=" * 60)
    
    # 创建自定义项目
    generator = EnhancedNovelGenerator("自定义仙侠", ai_type="local")
    
    print("\n1. 自定义世界观要求")
    print("-" * 30)
    
    custom_requirements = """
    - 主要背景为现代都市修仙
    - 包含科技与修仙结合的元素
    - 有国际修仙组织设定
    - 修炼体系结合现代科学理论
    """
    
    print("自定义要求:")
    print(custom_requirements)
    
    world_setting = generator.create_enhanced_world_setting(custom_requirements)
    print("✓ 基于自定义要求创建世界观")
    
    print("\n2. 查看生成的门派信息")
    print("-" * 30)
    
    for sect in world_setting.sects:
        print(f"门派: {sect['name']} ({sect['type']})")
        print(f"  特色: {sect['specialty']}")
        print(f"  位置: {sect['location']}")
        print()

def main():
    """主函数 - 运行所有演示"""
    print("欢迎使用修仙小说AI生成系统！")
    print("\n可用的演示选项：")
    print("1. 完整工作流程演示")
    print("2. 章节生成详细过程")
    print("3. 批量生成功能")
    print("4. 自定义功能演示")
    print("5. 运行所有演示")
    
    choice = input("\n请选择要运行的演示 (1-5): ").strip()
    
    if choice == "1":
        demo_complete_workflow()
    elif choice == "2":
        demo_chapter_generation_details()
    elif choice == "3":
        demo_batch_generation()
    elif choice == "4":
        demo_customization()
    elif choice == "5":
        demo_complete_workflow()
        demo_chapter_generation_details()
        demo_batch_generation()
        demo_customization()
    else:
        print("无效选择，运行完整演示...")
        demo_complete_workflow()

if __name__ == "__main__":
    main()