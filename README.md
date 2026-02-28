# Tekla License Auto-Switch

自动切换 Tekla Structures Diamond License 给 LEO (中国) 和 AUGER (加拿大)。

## 功能

- 定时自动切换 Tekla License
- 支持 LEO 和 AUGER 两个用户
- 自动截图确认
- 基于 Playwright 浏览器自动化

## 文件

- `2_tekla_skill.py` - 主切换脚本
- `1_save_auth.py` - 保存登录状态
- `tekla_license_enhanced.py` - 增强版（备用）

## 定时任务

| 时间 (EST) | 用户 | 说明 |
|-----------|------|------|
| 19:00 | LEO | 切给中国办公室 |
| 20:00 | AUGER | 切给加拿大办公室 |

## 使用方法

```bash
# 切换给 LEO
python 2_tekla_skill.py LEO

# 切换给 AUGER
python 2_tekla_skill.py AUGER
```

## 依赖

```bash
pip install playwright
python -m playwright install chromium
```

## 注意

- 需要 Tekla Admin 账号登录状态
- 首次运行需执行 `1_save_auth.py` 保存登录态
- 仅支持 Windows（Playwright + Edge/Chrome）
