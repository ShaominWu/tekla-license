#!/usr/bin/env python3
"""
Tekla License 自动切换 - OpenClaw 专属技能
使用已保存的登录状态（state.json）免登录直接切换
"""

import sys
import os
from playwright.sync_api import sync_playwright

def switch_tekla_license(target_user):
    """切换 Tekla License 给指定用户"""
    
    print(f"🎯 OpenClaw 任务：将许可切换给 {target_user}...")
    
    # 检查通行证文件
    state_file = "/home/wuyongjie/.openclaw/agents/Office-Automa/state.json"
    if not os.path.exists(state_file):
        print(f"❌ 错误：找不到通行证文件 {state_file}")
        print("   请先运行: python3 1_save_auth.py")
        return False
    
    with sync_playwright() as p:
        # headless=True 表示后台静默运行，不弹窗
        browser = p.chromium.launch(headless=True)
        
        try:
            # 加载已保存的登录状态，直接绕过登录！
            context = browser.new_context(storage_state=state_file)
            page = context.new_page()
            
            # 直接访问 License 页面
            print("🌐 访问 Tekla Admin...")
            page.goto("https://admin.account.tekla.com/")
            page.wait_for_load_state("networkidle")
            
            # 1. 点击左侧 Licenses 菜单
            print("📝 点击 Licenses 菜单...")
            page.get_by_role("link", name="Licenses").click()
            page.wait_for_load_state("networkidle")
            
            # 2. 点击 Diamond 许可栏展开
            print("💎 展开 Diamond 许可详情...")
            page.get_by_text("Tekla Structures Diamond - Named User").click()
            
            # 等待人员分配列表加载
            page.wait_for_selector("text=Assignments", timeout=10000)
            
            # 3. 核心切换逻辑
            print(f"🔄 执行切换: {'Auger' if target_user.upper() == 'AUGER' else 'Leo'}")
            
            # 获取复选框
            leo_checkbox = page.get_by_label("Lee, Leo")
            auger_checkbox = page.get_by_label("Auger-Dostaler, Louis-Simon")
            
            if target_user.upper() == "AUGER":
                # 切换到 Auger (加拿大)
                if leo_checkbox.is_checked():
                    leo_checkbox.uncheck()
                    print("   ✅ 已取消 Leo")
                
                if not auger_checkbox.is_checked():
                    auger_checkbox.check()
                    print("   ✅ 已勾选 Auger")
                
                print("\n✅ 许可已成功切换给 Auger (加拿大)")
                
            elif target_user.upper() == "LEO":
                # 切换到 Leo (中国)
                if auger_checkbox.is_checked():
                    auger_checkbox.uncheck()
                    print("   ✅ 已取消 Auger")
                
                if not leo_checkbox.is_checked():
                    leo_checkbox.check()
                    print("   ✅ 已勾选 Leo")
                
                print("\n✅ 许可已成功切换给 Leo (中国)")
            else:
                print(f"❌ 错误：未知的目标用户 '{target_user}'，只能是 LEO 或 AUGER")
                return False
            
            # 4. 保存更改（如果有Save按钮）
            try:
                save_btn = page.get_by_role("button", name="Save")
                if save_btn.is_visible(timeout=3000):
                    save_btn.click()
                    print("   💾 已保存更改")
                    page.wait_for_timeout(2000)
            except:
                pass  # 可能没有Save按钮，自动保存
            
            # 截图确认
            screenshot_path = f"/home/wuyongjie/.openclaw/agents/Office-Automa/screenshots/switch_{target_user.lower()}_{os.path.basename(__file__)}.png"
            page.screenshot(path=screenshot_path)
            print(f"   📸 已保存截图: {screenshot_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 自动化过程出错: {e}")
            error_screenshot = "/home/wuyongjie/.openclaw/agents/Office-Automa/screenshots/error.png"
            page.screenshot(path=error_screenshot)
            print(f"   📸 错误截图: {error_screenshot}")
            return False
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        success = switch_tekla_license(target)
        sys.exit(0 if success else 1)
    else:
        print("用法: python3 2_tekla_skill.py [LEO|AUGER]")
        sys.exit(1)
