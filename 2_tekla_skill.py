#!/usr/bin/env python3
"""
Tekla License 自动切换 - macOS 版
使用已保存的登录状态（state.json）免登录直接切换
"""

import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def switch_tekla_license(target_user):
    """切换 Tekla License 给指定用户"""
    
    print(f"🎯 OpenClaw 任务：将许可切换给 {target_user}...")
    
    # 检查通行证文件
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    state_file = os.path.join(workspace_dir, "state.json")
    if not os.path.exists(state_file):
        print(f"❌ 错误：找不到通行证文件 {state_file}")
        print("   请先运行: python3 1_save_auth.py")
        return False
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        try:
            context = browser.new_context(storage_state=state_file)
            page = context.new_page()
            
            # 访问 License 页面
            print("🌐 访问 Tekla Admin...")
            page.goto("https://admin.account.tekla.com/#/tekla/reseller/9e191570-7ecc-4b1d-ba24-c15117ffaf79/customer/8e59826e-0c87-463a-81dd-beabc3bf97f5/ra/licenses")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
            # 1. 关闭引导弹窗和 Cookie 弹窗
            print("📝 关闭弹窗...")
            try:
                page.get_by_role("button", name="Close the guide").click(timeout=5000)
                print("   ✅ 已关闭引导")
            except:
                pass
            
            try:
                page.get_by_role("button", name="Accept all cookies").click(timeout=5000)
                print("   ✅ 已接受 cookies")
            except:
                pass
            page.wait_for_timeout(1000)
            
            # 2. 点击 Diamond 许可
            print("💎 展开 Diamond 许可...")
            page.get_by_text("Tekla Structures Diamond - Named User").click()
            page.wait_for_timeout(2000)
            
            # 3. 展开 Assignments 区块
            print("📝 展开 Assignments...")
            try:
                page.locator("text=Assignments").click(timeout=10000)
                print("   ✅ 已展开 Assignments")
            except Exception as e:
                print(f"   ⚠️ 无法展开 Assignments: {e}")
            page.wait_for_timeout(2000)
            
            # 4. 勾选 "Show all users"
            print("👥 显示所有用户...")
            try:
                show_all = page.get_by_label("Show all users")
                if not show_all.is_checked():
                    show_all.check()
                    print("   ✅ 已勾选 Show all users")
                else:
                    print("   ℹ️ Show all users 已勾选")
            except Exception as e:
                print(f"   ⚠️ 无法勾选 Show all users: {e}")
            page.wait_for_timeout(2000)
            
            # 5. 核心切换逻辑
            print(f"🔄 执行切换: {'Auger' if target_user.upper() == 'AUGER' else 'Leo'}")
            
            # 用户 profile ID
            LEO_PROFILE_ID = "0d951a9a-464b-4376-a2df-3f628f505893"
            AUGER_PROFILE_ID = "dc1e57fe-d4be-41e6-9a26-80b0e6107609"
            
            if target_user.upper() == "LEO":
                # 切换到 Leo (中国)
                print("   🔍 处理 Auger...")
                try:
                    auger_checkbox = page.locator(f"input[data-test-profile-id='{AUGER_PROFILE_ID}']")
                    if auger_checkbox.count() > 0:
                        # 使用 force=True 强制点击
                        auger_checkbox.first.evaluate("el => { if(el.checked && !el.disabled) el.click(); }")
                        print("   ✅ 已取消 Auger")
                    else:
                        print("   ℹ️ 找不到 Auger")
                except Exception as e:
                    print(f"   ⚠️ 处理 Auger 时出错: {e}")
                
                print("   🔍 处理 Leo...")
                try:
                    leo_checkbox = page.locator(f"input[data-test-profile-id='{LEO_PROFILE_ID}']")
                    if leo_checkbox.count() > 0:
                        # 点击勾选
                        if not leo_checkbox.first.is_checked():
                            leo_checkbox.first.click(force=True)
                            print("   ✅ 已勾选 Leo")
                        else:
                            print("   ℹ️ Leo 已勾选")
                    else:
                        print("   ❌ 找不到 Leo")
                        return False
                except Exception as e:
                    print(f"   ❌ 勾选 Leo 时出错: {e}")
                    return False
                
                print("\n✅ 许可已成功切换给 Leo (中国)")
                
            elif target_user.upper() == "AUGER":
                # 切换到 Auger (加拿大)
                print("   🔍 处理 Leo...")
                try:
                    leo_checkbox = page.locator(f"input[data-test-profile-id='{LEO_PROFILE_ID}']")
                    if leo_checkbox.count() > 0:
                        leo_checkbox.first.evaluate("el => { if(el.checked && !el.disabled) el.click(); }")
                        print("   ✅ 已取消 Leo")
                    else:
                        print("   ℹ️ 找不到 Leo")
                except Exception as e:
                    print(f"   ⚠️ 处理 Leo 时出错: {e}")
                
                print("   🔍 处理 Auger...")
                try:
                    auger_checkbox = page.locator(f"input[data-test-profile-id='{AUGER_PROFILE_ID}']")
                    if auger_checkbox.count() > 0:
                        # 点击勾选 - 直接点击复选框
                        if not auger_checkbox.first.is_checked():
                            auger_checkbox.first.click(force=True)
                            print("   ✅ 已勾选 Auger")
                        else:
                            print("   ℹ️ Auger 已勾选")
                    else:
                        print("   ❌ 找不到 Auger")
                        return False
                except Exception as e:
                    print(f"   ❌ 勾选 Auger 时出错: {e}")
                    return False
                
                print("\n✅ 许可已成功切换给 Auger (加拿大)")
            else:
                print(f"❌ 错误：未知的目标用户 '{target_user}'，只能是 LEO 或 AUGER")
                return False
            
            page.wait_for_timeout(1000)
            
            # 6. 保存更改
            try:
                save_btn = page.get_by_role("button", name="Save")
                if save_btn.is_visible(timeout=3000):
                    save_btn.click()
                    print("   💾 已保存更改")
                    page.wait_for_timeout(2000)
            except:
                pass
            
            # 截图确认
            screenshot_dir = os.path.join(workspace_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"switch_{target_user.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            page.screenshot(path=screenshot_path)
            print(f"   📸 已保存截图: {screenshot_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 自动化过程出错: {e}")
            screenshot_dir = os.path.join(workspace_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            error_screenshot = os.path.join(screenshot_dir, f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
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
