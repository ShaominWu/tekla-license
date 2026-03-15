#!/usr/bin/env python3
"""
Tekla License 自动切换 - 使用 agent-browser
切换 Tekla Structures Diamond License 给 LEO 或 AUGER
"""

import sys
import os
import subprocess
import json
from datetime import datetime

WORKSPACE = "/Users/bear/.openclaw/workspace/tekla-license"
SCREENSHOTS_DIR = os.path.join(WORKSPACE, "screenshots")

def run_agent_browser(command, timeout=30):
    """运行 agent-browser 命令"""
    full_command = f"agent-browser {command}"
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def take_screenshot(name):
    """截图保存"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{name}_{timestamp}.png")
    
    success, stdout, stderr = run_agent_browser(f"screenshot {screenshot_path}")
    if success:
        print(f"   📸 截图已保存: {screenshot_path}")
        return screenshot_path
    else:
        print(f"   ⚠️ 截图失败: {stderr}")
        return None

def switch_license_with_agent_browser(target_user):
    """使用 agent-browser 切换 Tekla License"""
    
    target_user = target_user.upper()
    print(f"🎯 任务：将 Tekla License 切换给 {target_user}...")
    print(f"🫘 使用 agent-browser 自动化...")
    
    # 确保截图目录存在
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # 1. 打开 Tekla Admin 页面
    print("\n🌐 打开 Tekla Admin...")
    success, stdout, stderr = run_agent_browser("open https://admin.account.tekla.com/")
    if not success:
        print(f"❌ 无法打开页面: {stderr}")
        return False
    
    # 等待页面加载
    run_agent_browser("wait 3000")
    
    # 2. 检查是否需要登录（通过查找登录按钮或用户名）
    print("🔐 检查登录状态...")
    success, stdout, stderr = run_agent_browser("snapshot -i")
    
    if "login" in stdout.lower() or "sign in" in stdout.lower() or "password" in stdout.lower():
        print("⚠️ 需要登录，但 agent-browser 无法处理登录流程")
        print("   请先用浏览器手动登录，或检查 state.json 是否有效")
        take_screenshot("login_required")
        return False
    
    print("   ✅ 已登录")
    
    # 3. 点击 Licenses 菜单
    print("\n📝 进入 Licenses 页面...")
    
    # 尝试点击 Licenses 链接
    success, stdout, stderr = run_agent_browser('click "Licenses"')
    if not success:
        # 如果点击失败，直接访问 URL
        print("   🔄 直接访问 Licenses URL...")
        success, stdout, stderr = run_agent_browser(
            'open "https://admin.account.tekla.com/#/tekla/reseller/9e191570-7ecc-4b1d-ba24-c15117ffaf79/customer/8e59826e-0c87-463a-81dd-beabc3bf97f5/ra/licenses"'
        )
    
    if not success:
        print(f"❌ 无法进入 Licenses 页面: {stderr}")
        take_screenshot("error_licenses")
        return False
    
    run_agent_browser("wait 3000")
    take_screenshot("licenses_page")
    
    # 4. 点击 Users 标签
    print("\n👥 进入 Users 管理...")
    success, stdout, stderr = run_agent_browser('click "Users"')
    
    if not success:
        print("⚠️ 无法点击 Users，尝试查找用户列表...")
    else:
        run_agent_browser("wait 2000")
    
    take_screenshot("users_page")
    
    # 5. 获取页面快照，查找复选框
    print("\n🔍 查找用户复选框...")
    success, stdout, stderr = run_agent_browser("snapshot -i")
    
    if not success:
        print(f"❌ 无法获取页面快照: {stderr}")
        return False
    
    # 查找 Leo 和 Auger 的复选框
    leo_found = "Leo" in stdout or "Lee, Leo" in stdout
    auger_found = "Auger" in stdout or "Auger-Dostaler" in stdout
    
    print(f"   {'✅' if leo_found else '❌'} Leo 用户 {'找到' if leo_found else '未找到'}")
    print(f"   {'✅' if auger_found else '❌'} Auger 用户 {'找到' if auger_found else '未找到'}")
    
    if not leo_found and not auger_found:
        print("❌ 无法找到用户复选框，可能需要更新选择器")
        take_screenshot("error_users_not_found")
        return False
    
    # 6. 执行切换逻辑
    print(f"\n🔄 执行切换: {target_user}")
    
    if target_user == "AUGER":
        # 先取消 Leo
        if leo_found:
            print("   ⬜ 取消 Leo...")
            # 尝试找到 Leo 的复选框并取消勾选
            # 这里需要根据实际页面结构调整选择器
            run_agent_browser('eval "document.querySelector(\'[aria-label*=\"Leo\"] input[type=checkbox], [data-testid*=\"Leo\"] input[type=checkbox]\').checked = false"')
        
        # 勾选 Auger
        if auger_found:
            print("   ☑️  勾选 Auger...")
            run_agent_browser('eval "document.querySelector(\'[aria-label*=\"Auger\"] input[type=checkbox], [data-testid*=\"Auger\"] input[type=checkbox]\').checked = true"')
        
        print("\n✅ License 已切换给 Auger (加拿大)")
        
    elif target_user == "LEO":
        # 先取消 Auger
        if auger_found:
            print("   ⬜ 取消 Auger...")
            run_agent_browser('eval "document.querySelector(\'[aria-label*=\"Auger\"] input[type=checkbox], [data-testid*=\"Auger\"] input[type=checkbox]\').checked = false"')
        
        # 勾选 Leo
        if leo_found:
            print("   ☑️  勾选 Leo...")
            run_agent_browser('eval "document.querySelector(\'[aria-label*=\"Leo\"] input[type=checkbox], [data-testid*=\"Leo\"] input[type=checkbox]\').checked = true"')
        
        print("\n✅ License 已切换给 Leo (中国)")
    
    # 7. 等待并保存更改
    run_agent_browser("wait 2000")
    
    # 尝试点击 Save 按钮
    print("\n💾 保存更改...")
    success, stdout, stderr = run_agent_browser('click "Save"')
    if success:
        print("   ✅ 已点击 Save")
        run_agent_browser("wait 2000")
    else:
        print("   ℹ️  可能没有 Save 按钮（自动保存）")
    
    # 8. 最终截图确认
    run_agent_browser("wait 2000")
    final_screenshot = take_screenshot(f"switch_{target_user.lower()}_complete")
    
    print(f"\n🫘 切换完成！截图: {final_screenshot}")
    
    # 关闭浏览器
    run_agent_browser("close")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python3 tekla_agent_browser.py [LEO|AUGER]")
        print("")
        print("示例:")
        print("  python3 tekla_agent_browser.py AUGER   # 切换给 Auger (加拿大)")
        print("  python3 tekla_agent_browser.py LEO     # 切换给 Leo (中国)")
        sys.exit(1)
    
    target = sys.argv[1].upper()
    
    if target not in ["LEO", "AUGER"]:
        print(f"❌ 错误: 目标用户必须是 LEO 或 AUGER，不是 '{target}'")
        sys.exit(1)
    
    print("=" * 60)
    print("🫘 小豆豆 Tekla License 切换 (agent-browser 版)")
    print("=" * 60)
    print()
    
    success = switch_license_with_agent_browser(target)
    
    print()
    print("=" * 60)
    if success:
        print(f"✅ 成功切换给 {target}")
    else:
        print(f"❌ 切换失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
