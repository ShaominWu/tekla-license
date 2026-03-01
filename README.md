# 🫘 小豆豆 Tekla License Auto-Switch

自动切换 Tekla Structures Diamond License 给 LEO (中国) 和 AUGER (加拿大)。

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 🫘 **小豆豆助手** | 活泼可靠的自动化代理 |
| 🔄 **自动切换** | 每天晚上 8 点切给 Auger，早上 9 点切给 Leo |
| 🔐 **免登录** | 保存登录状态，自动复用 |
| 📸 **截图确认** | 每次切换自动截图留档 |
| 🖥️ **后台运行** | headless 模式，不打扰工作 |

---

## 🏗️ 系统架构

### 时区对照

| 加拿大东部时间 | 中国时间 | 切换给谁 | 说明 |
|--------------|---------|---------|------|
| 20:00 (8PM) | 次日 9:00 | 🇨🇦 **Auger** | 加拿大早上开始工作 |
| 21:00 (9PM) | 次日 10:00 (冬令时) / 9:00 (夏令时) | 🇨🇳 **Leo** | 中国早上开始工作 |

---

## 📁 文件结构

```
tekla-license/
├── README.md                    # 本文件
├── 1_save_auth.py               # 保存登录状态（首次运行）
├── 2_tekla_skill.py             # 主切换脚本
├── tekla_license_enhanced.py    # 增强版（备用）
├── xiaodoudou-tekla.sh          # 🫘 小豆豆主程序
├── crontab.txt                  # 定时任务配置
├── venv/                        # Python 虚拟环境
├── state.json                   # 登录状态（自动生成）
├── logs/                        # 运行日志
└── screenshots/                 # 截图记录
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd tekla-license
python3 -m venv venv
source venv/bin/activate
pip install playwright
python -m playwright install chromium
```

### 2. 首次登录保存状态

```bash
./xiaodoudou-tekla.sh --auth
```

- 浏览器会自动弹出
- 登录 Tekla Admin (admin.account.tekla.com)
- 如有 MFA 验证码，完成验证
- 登录成功后按回车保存状态

### 3. 测试手动切换

```bash
# 切换给 Auger (加拿大)
./xiaodoudou-tekla.sh --auger

# 切换给 Leo (中国)
./xiaodoudou-tekla.sh --leo
```

### 4. 安装定时任务

```bash
crontab crontab.txt
```

---

## 🫘 召唤小豆豆

```bash
# 首次登录保存状态
./xiaodoudou-tekla.sh --auth

# 切换给 Auger (加拿大)
./xiaodoudou-tekla.sh --auger

# 切换给 Leo (中国)
./xiaodoudou-tekla.sh --leo

# 查看状态
./xiaodoudou-tekla.sh --status
```

---

## 📝 定时任务时间表

| 时间 (加拿大东部) | 时间 (中国) | 切换给谁 | 命令 |
|------------------|------------|---------|------|
| 20:00 | 次日 9:00-10:00 | 🇨🇦 Auger | `--auger` |
| 21:00 | 次日 10:00-11:00 | 🇨🇳 Leo | `--leo` |

---

## 🔧 技术细节

| 项目 | 配置 |
|:---|:---|
| **操作系统** | macOS (Apple Silicon) |
| **Python** | 3.x (虚拟环境) |
| **浏览器** | Playwright + Chromium |
| **运行模式** | Headless (后台静默) |
| **登录方式** | 保存 Cookie 状态 |
| **截图** | 每次切换自动截图 |
| **日志** | logs/ 文件夹 |

---

## 🛠️ 维护

### 登录失效怎么办？

如果状态过期，重新运行：
```bash
./xiaodoudou-tekla.sh --auth
```

### 查看截图

```bash
ls -la screenshots/
open screenshots/switch_leo_20260301.png  # 预览截图
```

### 查看日志

```bash
ls -la logs/
cat logs/tekla-20260301-2000.log
```

---

## 📝 Mac 移植修改

| 原配置 (Linux) | 修改后 (Mac) |
|---------------|-------------|
| `/home/wuyongjie/...` | `/Users/bear/.openclaw/workspace/tekla-license/` |
| 系统 Python | Python 虚拟环境 `venv/` |
| Playwright 依赖 | 本地安装 Chromium |
| 截图路径 | 相对路径 `screenshots/` |
| 日志路径 | 相对路径 `logs/` |

---

## 🫘 小豆豆说

> "每天晚上 8 点我会把许可切给 Auger（加拿大），
> 晚上 9 点我会把许可切给 Leo（中国）。
> 这样两边早上上班都有许可可用~
> 有事叫我，没事我不吵你！"

---

*版本: 2026.03.01 | 作者: Shaomin Wu | 助手: 小豆豆 🫘*
