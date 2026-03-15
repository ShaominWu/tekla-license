# 🫘 小豆豆 Tekla License Skill

自动切换 Tekla Structures Diamond License 给 LEO (中国) 和 AUGER (加拿大)。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🫘 **小豆豆助手** | 活泼可靠的自动化代理 |
| 🔄 **自动切换** | 定时自动切换 License |
| 🔐 **免登录** | 保存登录状态，自动复用 |
| 📸 **截图确认** | 每次切换自动截图留档 |
| 🖥️ **后台运行** | Headless 模式，静默执行 |
| 📝 **完整日志** | 记录每次操作 |

---

## 🏗️ 系统架构

### 时区对照表

| 加拿大东部时间 | 中国时间 | 切换给谁 | 办公室 |
|--------------|---------|---------|--------|
| 20:00 (晚上8点) | 次日 9:00-10:00 | 🇨🇦 **Auger** | 加拿大早上开始 |
| 21:00 (晚上9点) | 次日 10:00-11:00 (冬令时) / 9:00-10:00 (夏令时) | 🇨🇳 **Leo** | 中国早上开始 |

**设计理念**: 在加拿大晚上时间切换，确保中国/加拿大两边早上上班时都有 License 可用。

---

## 📁 文件结构

```
tekla-license/
├── SKILL.md                      # 本文件（完整方案）
├── README.md                     # 快速开始指南
├── 1_save_auth.py                # 保存登录状态（首次运行）
├── 2_tekla_skill.py              # 主切换脚本
├── tekla_license_enhanced.py     # 增强版（备用）
├── xiaodoudou-tekla.sh           # 🫘 小豆豆主程序
├── crontab.txt                   # 定时任务配置
├── venv/                         # Python 虚拟环境
│   └── bin/python3              # 隔离的 Python
├── state.json                    # 登录状态（首次运行生成）
├── logs/                         # 运行日志
│   └── tekla-YYYYMMDD-HHMM.log
└── screenshots/                  # 截图记录
    ├── switch_leo_YYYYMMDD.png
    └── switch_auger_YYYYMMDD.png
```

---

## 👥 用户配置

License 在以下两个用户之间切换：

| 用户 | 姓名 | 地区 | 邮箱环境变量 |
|------|------|------|-------------|
| **Leo** | Lee, Leo | 🇨🇳 中国 | `TEKLA_USER_CHINA` |
| **Auger** | Auger-Dostaler, Louis-Simon | 🇨🇦 加拿大 | `TEKLA_USER_CANADA` |

---

## 🚀 首次设置

### 1. 安装依赖

```bash
cd tekla-license

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装 Playwright
pip install playwright

# 安装 Chromium 浏览器
python -m playwright install chromium
```

### 2. 保存登录状态

```bash
./xiaodoudou-tekla.sh --auth
```

执行后会：
1. 弹出浏览器窗口
2. 访问 https://admin.account.tekla.com/
3. 输入 Trimble 账号密码登录
4. 如有 MFA 验证码，完成验证
5. 确保进入 Licenses 页面
6. 按回车保存登录状态到 `state.json`

### 3. 测试手动切换

```bash
# 测试切换给 Auger (加拿大)
./xiaodoudou-tekla.sh --auger

# 测试切换给 Leo (中国)
./xiaodoudou-tekla.sh --leo
```

### 4. 安装定时任务

```bash
# 安装定时任务
crontab crontab.txt

# 查看已安装的定时任务
crontab -l
```

---

## 🫘 召唤小豆豆

### 手动使用

```bash
cd /Users/bear/.openclaw/workspace/tekla-license

# 首次登录保存状态
./xiaodoudou-tekla.sh --auth

# 切换给 Auger (加拿大)
./xiaodoudou-tekla.sh --auger

# 切换给 Leo (中国)
./xiaodoudou-tekla.sh --leo

# 查看状态（登录状态、截图记录）
./xiaodoudou-tekla.sh --status
```

### 自动定时任务（加拿大东部时间）

| 时间 | 任务 | 说明 |
|:---|:---|:---|
| **20:00** 🌙 | 切给 Auger | 加拿大办公室早上准备 |
| **21:00** 🌃 | 切给 Leo | 中国办公室早上准备 |

---

## 🔧 技术细节

| 项目 | 配置 |
|:---|:---|
| **操作系统** | macOS (Apple Silicon / Intel) |
| **Python** | 3.x (虚拟环境隔离) |
| **浏览器** | Playwright + Chromium |
| **运行模式** | Headless (无界面，后台静默) |
| **登录方式** | Cookie 状态持久化 |
| **目标网站** | https://admin.account.tekla.com/ |
| **License 类型** | Tekla Structures Diamond - Named User |
| **截图** | 每次切换自动截图保存 |
| **日志** | 时间戳命名，便于追溯 |

### 浏览器自动化流程

```
1. 加载 state.json 登录状态
2. 访问 admin.account.tekla.com
3. 点击 "Licenses" 菜单
4. 展开 "Tekla Structures Diamond - Named User"
5. 根据目标用户勾选/取消复选框:
   - Leo (Lee, Leo) ← 中国
   - Auger-Dostaler, Louis-Simon ← 加拿大
6. 保存更改
7. 截图确认
8. 关闭浏览器
```

---

## 🛠️ 维护指南

### 登录状态过期

如果提示登录失效，重新运行：
```bash
./xiaodoudou-tekla.sh --auth
```

### 查看截图记录

```bash
# 列出所有截图
ls -la screenshots/

# 预览最近的一张
open screenshots/$(ls -t screenshots/ | head -1)
```

### 查看运行日志

```bash
# 列出所有日志
ls -la logs/

# 查看今天的日志
cat logs/tekla-$(date +%Y%m%d)*.log

# 查看最近的日志
cat logs/$(ls -t logs/ | head -1)
```

### 手动运行测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 直接运行 Python 脚本（调试用）
python3 2_tekla_skill.py LEO
python3 2_tekla_skill.py AUGER
```

### 调整定时任务

编辑 `crontab.txt`，然后重新加载：
```bash
crontab crontab.txt
```

---

## 📝 Mac 移植修改记录

从 Linux 移植到 macOS 的修改：

| 项目 | 原配置 (Linux) | 修改后 (Mac) |
|------|---------------|-------------|
| **路径** | `/home/wuyongjie/.openclaw/...` | `/Users/bear/.openclaw/workspace/tekla-license/` |
| **Python** | 系统 Python | 虚拟环境 `venv/` |
| **浏览器** | 系统 Chrome/Edge | Playwright 安装的 Chromium |
| **state.json** | 绝对路径 | 相对路径（脚本所在目录） |
| **截图** | 绝对路径 | 相对路径 `screenshots/` |
| **日志** | 绝对路径 | 相对路径 `logs/` |
| **截图命名** | 固定文件名 | 带时间戳的动态命名 |

---

## ⚠️ 限制与注意事项

- **单 License**: 同一时间只能分配给一个人
- **网络依赖**: 需要稳定的网络连接访问 Tekla Admin
- **登录状态**: 可能定期过期，需要重新运行 `--auth`
- **时区**: 基于加拿大东部时间，注意夏令时变化
- **截图**: 截图文件会累积，定期手动清理

---

## 💾 备份

重要文件：
- `state.json` - 登录状态（重新登录可恢复）
- `screenshots/` - 操作记录（可选备份）

备份命令：
```bash
tar -czf tekla-license-backup-$(date +%Y%m%d).tar.gz \
  --exclude='venv' \
  --exclude='logs' \
  --exclude='screenshots/*.png' \
  tekla-license/
```

---

## 🫘 小豆豆说

> "每天晚上 8 点我会把 License 切给 Auger（加拿大），
> 晚上 9 点我会把 License 切给 Leo（中国）。
> 这样两边早上 9 点上班都有 License 可用~
> 
> 如果登录过期了，记得喊我用 `--auth` 重新登录！
> 有事叫我，没事我不吵你~ 🫘"

---

## 🔗 相关项目

- **小豆豆 File Delivery Skill**: `/Users/bear/.openclaw/workspace/file-delivery/`
  - 文件自动上传 Google Drive
  - 发送邮件通知客户
  - 每天 8点、10点运行

---

## 🆕 Agent-Browser 手动操作指南

当自动化脚本失效时，可以使用 agent-browser 进行半自动操作：

### 登录流程

```bash
# 1. 打开浏览器（显示界面）
agent-browser open https://admin.account.tekla.com/ --headed

# 2. 输入邮箱
agent-browser type "[ref=邮箱输入框]" "jt@morissetconstruction.com"
agent-browser click "下一步"

# 3. 输入密码
agent-browser type "[ref=密码输入框]" "Jacobe@1926"
agent-browser click "登录"

# 4. 输入邮箱验证码（需要手动查看邮箱）
agent-browser type "[ref=验证码输入框]" "XXXXXX"
agent-browser click "继续"
```

### License 切换步骤

1. **关闭引导教程**
   ```bash
   agent-browser click "Close the guide"
   ```

2. **进入 Licenses 页面**
   ```bash
   agent-browser click "Licenses"
   ```

3. **展开 Diamond License**
   ```bash
   agent-browser click "Tekla Structures Diamond - Named User"
   ```

4. **滚动到 Assignments 部分**
   ```bash
   agent-browser scroll down 500
   ```

5. **展开 Assignments**
   ```bash
   agent-browser click "Assignments"
   ```

6. **显示所有用户**
   ```bash
   agent-browser check "Show all users"
   ```

7. **取消勾选当前用户**
   ```bash
   agent-browser uncheck "Lee, Leo"
   ```

8. **勾选目标用户**
   ```bash
   agent-browser check "Auger-Dostaler, Louis-Simon"
   ```

9. **截图确认**
   ```bash
   agent-browser screenshot ./switch_complete.png
   ```

### 用户列表

| 用户 | 邮箱 | 地区 |
|------|------|------|
| Auger-Dostaler, Louis-Simon | louis-simon@morissetconstruction.com | 🇨🇦 加拿大 |
| Lee, Leo | leodetailing@163.com | 🇨🇳 中国 |
| Qin, Vivian | vivian_23cd@163.com | - |
| Moreau, David | david@morissetconstruction.com | - |
| Morisset, Jean-Thomas | jt@morissetconstruction.com | Admin |

### 切换逻辑

- Diamond License 有 **2 个座位**
- 当前分配：**Auger + Vivian** 或 **Leo + Vivian**
- 切换时：取消一个用户，添加另一个用户
- 系统自动保存，无需手动点击 Save

---

*版本: 2026.03.15 | 作者: Shaomin Wu | 助手: 小豆豆 🫘*
