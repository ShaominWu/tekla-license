#!/usr/bin/env python3
"""
Tekla License 认证保存工具
运行一次，手动登录后保存登录状态（Cookie）
之后 OpenClaw 可以直接使用，无需再次登录
"""

from playwright.sync_api import sync_playwright

def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("🌐 正在打开 Trimble 登录页...")
        page.goto("https://admin.account.tekla.com/")
        
        print("\n" + "="*60)
        print("📝 请在弹出的浏览器中完成登录")
        print("   1. 输入邮箱和密码")
        print("   2. 如有MFA验证码，请完成验证")
        print("   3. 确保进入 Licenses 页面")
        print("="*60 + "\n")
        
        input("✅ 确认已登录成功并看到 Licenses 页面后，按回车继续...")
        
        # 保存登录状态到文件
        import os
        workspace_dir = os.path.dirname(os.path.abspath(__file__))
        state_file = os.path.join(workspace_dir, "state.json")
        context.storage_state(path=state_file)
        print(f"\n✅ 登录通行证已保存: {state_file}")
        print("   小豆豆以后可以直接使用，无需再次登录！")
        
        browser.close()

if __name__ == "__main__":
    save_login_state()
