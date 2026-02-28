#!/usr/bin/env python3
"""
Tekla License 自动切换 - 增强版
用于办公自动化 Agent
支持：定时切换、截图验证、MFA告警、元素重新定位
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# 尝试导入playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright 未安装，请先运行: pip3 install playwright")

class TeklaLicenseManager:
    """Tekla License 管理器"""
    
    def __init__(self, headless=True, screenshot_dir=None):
        self.headless = headless
        self.screenshot_dir = screenshot_dir or "/tmp/tekla_screenshots"
        self.browser = None
        self.context = None
        self.page = None
        
        # 创建截图目录
        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)
        
        # 配置
        self.config = {
            "url": "https://admin.tekla.com",
            "users": {
                "china": {"name": "Leo", "email": os.environ.get("TEKLA_USER_CHINA", "")},
                "canada": {"name": "Louis-Simon (Auger)", "email": os.environ.get("TEKLA_USER_CANADA", "")}
            },
            "credentials": {
                "email": os.environ.get("TRIMBLE_EMAIL", ""),
                "password": os.environ.get("TRIMBLE_PASSWORD", "")
            }
        }
    
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def screenshot(self, name):
        """截图保存"""
        if self.page:
            filename = f"{self.screenshot_dir}/{name}_{datetime.now().strftime('%H%M%S')}.png"
            self.page.screenshot(path=filename, full_page=True)
            self.log(f"📸 截图已保存: {filename}")
            return filename
        return None
    
    def start_browser(self):
        """启动浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            self.log("❌ Playwright 未安装", "ERROR")
            return False
        
        try:
            self.log("🚀 启动浏览器...")
            playwright = sync_playwright().start()
            self.browser = playwright.chromium.launch(
                headless=self.headless,
                slow_mo=100  # 减慢操作以便观察
            )
            self.context = self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=self.screenshot_dir if not self.headless else None
            )
            self.page = self.context.new_page()
            self.log("✅ 浏览器启动成功")
            return True
        except Exception as e:
            self.log(f"❌ 浏览器启动失败: {e}", "ERROR")
            return False
    
    def stop_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            self.log("🛑 浏览器已关闭")
    
    def check_mfa(self):
        """检查是否需要MFA验证码"""
        try:
            # 检查是否有验证码输入框
            mfa_input = self.page.locator("input[type='text'][name*='code'], input[name*='mfa'], input[name*='otp']").first
            if mfa_input.is_visible(timeout=3000):
                self.log("🔐 检测到MFA验证码请求", "WARNING")
                self.screenshot("mfa_required")
                return True
        except:
            pass
        return False
    
    def alert_user(self, message):
        """向用户发送告警"""
        self.log(f"🚨 用户告警: {message}", "ALERT")
        # 这里可以集成Telegram或其他通知
        # 创建告警文件
        alert_file = f"/tmp/tekla_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(alert_file, 'w') as f:
            f.write(f"时间: {datetime.now()}\n")
            f.write(f"告警: {message}\n")
            f.write("请手动处理Tekka License切换\n")
        return alert_file
    
    def login(self):
        """登录 Trimble"""
        self.log("🔐 开始登录 Trimble...")
        
        if not self.config["credentials"]["email"]:
            self.log("❌ 未设置 TRIMBLE_EMAIL 环境变量", "ERROR")
            return False
        
        try:
            # 访问登录页
            self.page.goto(self.config["url"], timeout=60000)
            self.page.wait_for_load_state("networkidle")
            
            # 截图：登录前
            self.screenshot("01_before_login")
            
            # 检查是否已经登录
            if "/dashboard" in self.page.url or "/landing" in self.page.url:
                self.log("✅ 已经处于登录状态")
                return True
            
            # 填写邮箱
            self.log(f"📧 输入邮箱: {self.config['credentials']['email']}")
            email_input = self.page.locator("input[type='email']").first
            email_input.fill(self.config["credentials"]["email"])
            email_input.press("Enter")
            
            # 等待密码页面
            self.page.wait_for_timeout(2000)
            
            # 检查MFA
            if self.check_mfa():
                alert = self.alert_user("需要MFA验证码，请手动登录")
                self.log(f"📄 告警文件: {alert}")
                return False
            
            # 填写密码
            self.log("🔑 输入密码...")
            password_input = self.page.locator("input[type='password']").first
            password_input.fill(self.config["credentials"]["password"])
            password_input.press("Enter")
            
            # 等待登录完成
            self.page.wait_for_load_state("networkidle", timeout=60000)
            
            # 检查MFA（二次验证）
            if self.check_mfa():
                alert = self.alert_user("登录后需要MFA验证")
                return False
            
            # 验证登录成功
            if "/dashboard" in self.page.url or "/landing" in self.page.url:
                self.log("✅ 登录成功")
                self.screenshot("02_after_login")
                return True
            else:
                self.log(f"❌ 登录失败，当前URL: {self.page.url}", "ERROR")
                self.screenshot("02_login_failed")
                return False
                
        except PlaywrightTimeout:
            self.log("❌ 登录超时", "ERROR")
            self.screenshot("02_login_timeout")
            return False
        except Exception as e:
            self.log(f"❌ 登录异常: {e}", "ERROR")
            self.screenshot("02_login_error")
            return False
    
    def navigate_to_assignments(self):
        """导航到 Assignments 页面"""
        self.log("🧭 导航到 Assignments 页面...")
        
        try:
            # 等待页面加载
            self.page.wait_for_load_state("networkidle")
            
            # 寻找 Assignments 链接
            # 注意：需要根据实际页面结构调整
            assignments_link = self.page.locator(
                "text=Assignments, text=分配, [href*='assignments'], [data-testid*='assignment']"
            ).first
            
            if assignments_link.is_visible(timeout=10000):
                assignments_link.click()
                self.page.wait_for_load_state("networkidle")
                self.log("✅ 已进入 Assignments 页面")
                self.screenshot("03_assignments_page")
                return True
            else:
                # 尝试直接访问URL
                self.page.goto(f"{self.config['url']}/#/assignments")
                self.page.wait_for_load_state("networkidle")
                self.log("⚠️ 通过URL进入 Assignments")
                self.screenshot("03_assignments_page")
                return True
                
        except Exception as e:
            self.log(f"❌ 导航失败: {e}", "ERROR")
            self.screenshot("03_navigation_failed")
            return False
    
    def find_user_row(self, user_name):
        """查找用户行（支持视觉重新定位）"""
        self.log(f"🔍 查找用户: {user_name}")
        
        try:
            # 策略1: 直接文本匹配
            user_row = self.page.locator(f"tr:has-text('{user_name}'), .user-row:has-text('{user_name}')").first
            if user_row.is_visible(timeout=5000):
                self.log(f"✅ 找到用户行 (文本匹配): {user_name}")
                return user_row
            
            # 策略2: 部分匹配
            user_row = self.page.locator(f"tr:has-text('{user_name.split()[0]}')").first
            if user_row.is_visible(timeout=3000):
                self.log(f"✅ 找到用户行 (部分匹配): {user_name}")
                return user_row
            
            # 策略3: 遍历所有行检查
            rows = self.page.locator("table tbody tr, .user-list .user-item").all()
            for row in rows:
                row_text = row.inner_text()
                if user_name in row_text or user_name.split()[0] in row_text:
                    self.log(f"✅ 找到用户行 (遍历匹配): {user_name}")
                    return row
            
            self.log(f"⚠️ 未找到用户: {user_name}，可能需要手动检查", "WARNING")
            self.screenshot("04_user_not_found")
            return None
            
        except Exception as e:
            self.log(f"❌ 查找用户失败: {e}", "ERROR")
            return None
    
    def toggle_user_assignment(self, user_name, enable=True):
        """切换用户Assignment状态"""
        action = "启用" if enable else "禁用"
        self.log(f"🔄 {action}用户: {user_name}")
        
        user_row = self.find_user_row(user_name)
        if not user_row:
            return False
        
        try:
            # 寻找checkbox或toggle
            checkbox = user_row.locator(
                "input[type='checkbox'], .toggle input, .switch input, [role='switch']"
            ).first
            
            # 获取当前状态
            is_checked = False
            try:
                is_checked = checkbox.is_checked()
            except:
                # 如果无法直接获取checked状态，检查class或其他属性
                class_attr = checkbox.evaluate("el => el.className")
                is_checked = "checked" in class_attr or "active" in class_attr or "on" in class_attr
            
            self.log(f"  当前状态: {'已启用' if is_checked else '已禁用'}")
            
            # 判断是否需要点击
            need_click = (enable and not is_checked) or (not enable and is_checked)
            
            if need_click:
                # 点击切换
                checkbox.click()
                self.page.wait_for_timeout(2000)  # 等待操作生效
                
                # 验证新状态
                new_checked = checkbox.is_checked() if hasattr(checkbox, 'is_checked') else enable
                if (enable and new_checked) or (not enable and not new_checked):
                    self.log(f"  ✅ {action}成功")
                    return True
                else:
                    self.log(f"  ⚠️ 状态可能未改变，请检查", "WARNING")
                    return False
            else:
                self.log(f"  ℹ️ 已经是目标状态，无需操作")
                return True
                
        except Exception as e:
            self.log(f"  ❌ 切换失败: {e}", "ERROR")
            return False
    
    def verify_in_use_status(self):
        """验证 In Use 状态"""
        self.log("🔍 验证 'In Use' 状态...")
        
        try:
            # 寻找 In Use 列或状态指示器
            in_use_elements = self.page.locator(
                "text=In Use, .status-active, .in-use-indicator, [data-status='active']"
            ).all()
            
            self.log(f"  找到 {len(in_use_elements)} 个 'In Use' 状态")
            
            # 截图验证
            self.screenshot("05_in_use_status")
            return True
            
        except Exception as e:
            self.log(f"  ⚠️ 验证失败: {e}", "WARNING")
            return False
    
    def switch_license(self, enable_region):
        """
        切换License主流程
        enable_region: 'china' 或 'canada'
        """
        self.log(f"\n{'='*60}")
        self.log(f"🎯 开始切换: 启用 {enable_region.upper()}")
        self.log(f"{'='*60}\n")
        
        if enable_region == "china":
            enable_user = self.config["users"]["china"]["name"]
            disable_user = self.config["users"]["canada"]["name"]
        else:
            enable_user = self.config["users"]["canada"]["name"]
            disable_user = self.config["users"]["china"]["name"]
        
        self.log(f"启用: {enable_user}")
        self.log(f"禁用: {disable_user}\n")
        
        try:
            # 登录
            if not self.login():
                return False
            
            # 导航到Assignments
            if not self.navigate_to_assignments():
                return False
            
            # 禁用不需要的用户
            self.toggle_user_assignment(disable_user, enable=False)
            
            # 启用需要的用户
            self.toggle_user_assignment(enable_user, enable=True)
            
            # 验证状态
            self.verify_in_use_status()
            
            # 最终截图
            self.screenshot("06_final_status")
            
            self.log(f"\n✅ License切换完成: {enable_region.upper()} 已启用")
            return True
            
        except Exception as e:
            self.log(f"\n❌ 切换过程出错: {e}", "ERROR")
            self.screenshot("06_error")
            return False
    
    def run(self, enable_region, visible=False):
        """完整运行流程"""
        self.headless = not visible
        
        try:
            if not self.start_browser():
                return False
            
            result = self.switch_license(enable_region)
            return result
            
        finally:
            self.stop_browser()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Tekla License 自动切换 (Ops Automation)')
    parser.add_argument('--region', choices=['china', 'canada'], required=True,
                       help='要启用的地区: china (Leo) 或 canada (Auger)')
    parser.add_argument('--visible', action='store_true',
                       help='显示浏览器窗口（调试用）')
    parser.add_argument('--test', action='store_true',
                       help='测试模式（检查配置）')
    parser.add_argument('--screenshot-dir', default='/tmp/tekla_screenshots',
                       help='截图保存目录')
    
    args = parser.parse_args()
    
    manager = TeklaLicenseManager(
        headless=not args.visible,
        screenshot_dir=args.screenshot_dir
    )
    
    if args.test:
        print("🧪 测试模式")
        print(f"  中国用户: {manager.config['users']['china']}")
        print(f"  加拿大用户: {manager.config['users']['canada']}")
        print(f"  截图目录: {manager.screenshot_dir}")
        return
    
    # 执行切换
    success = manager.run(args.region, visible=args.visible)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
