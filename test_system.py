#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试脚本 - 验证修仙小说生成系统功能
"""

def main():
    """主测试函数"""
    print("=" * 60)
    print("修仙小说AI生成系统 - 功能验证")
    print("=" * 60)
    
    try:
        # 测试模块导入
        print("\n1. 测试模块导入...")
        from enhanced_novel_generator import EnhancedNovelGenerator
        print("✓ 模块导入成功")
        
        # 创建生成器实例
        print("\n2. 创建生成器实例...")
        generator = EnhancedNovelGenerator("测试项目", ai_type="local")
        print(f"✓ 生成器创建成功，项目目录: {generator.project_dir}")
        
        # 创建世界观
        print("\n3. 创建世界观设定...")
        world = generator.create_enhanced_world_setting()
        print(f"✓ 世界观创建成功")
        print(f"  修炼等级: {len(world.cultivation_levels)} 个")
        print(f"  门派数量: {len(world.sects)} 个")
        print(f"  地域划分: {len(world.regions)} 个")
        
        # 创建角色
        print("\n4. 创建主要角色...")
        characters = generator.create_enhanced_characters()
        print(f"✓ 角色创建成功，共 {len(characters)} 个角色")
        for char in characters[:3]:  # 显示前3个角色
            print(f"  {char.name} ({char.role_type}) - {char.cultivation_level}")
        
        # 生成大纲
        print("\n5. 生成整体大纲...")
        outline = generator.generate_enhanced_outline(20)  # 生成20章用于测试
        print(f"✓ 大纲生成成功，共 {len(outline)} 章")
        
        # 生成第一章
        print("\n6. 生成第一章...")
        chapter = generator.generate_next_chapter()
        print(f"✓ 第一章生成成功")
        print(f"  标题: {chapter.outline.title}")
        print(f"  字数: {chapter.actual_word_count}")
        print(f"  关键情节: {', '.join(chapter.key_plot_points)}")
        
        # 生成进度报告
        print("\n7. 生成进度报告...")
        report = generator.generate_progress_report()
        print(f"✓ 进度报告生成成功")
        print(f"  项目名称: {report['project_info']['project_name']}")
        print(f"  完成进度: {report['progress']['completion_rate']}")
        print(f"  总字数: {report['content_stats']['total_words']}")
        
        print("\n" + "=" * 60)
        print("✓ 所有功能测试通过！系统运行正常")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 修仙小说生成系统测试成功！")
    else:
        print("\n❌ 系统测试失败，请检查代码。")