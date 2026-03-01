#!/bin/bash
# 🫘 小豆豆 - Tekla License 切换助手

WORKSPACE="/Users/bear/.openclaw/workspace/tekla-license"
VENV="$WORKSPACE/venv"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PINK='\033[1;35m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${PINK}🫘 小豆豆 Tekla License 助手${NC}"
echo "==========================="

# 检查虚拟环境
if [ ! -d "$VENV" ]; then
    echo -e "${YELLOW}⚠️  虚拟环境不存在${NC}"
    exit 1
fi

# 激活虚拟环境
source "$VENV/bin/activate"

cd "$WORKSPACE"

# 检查登录状态
if [ ! -f "state.json" ]; then
    echo -e "${YELLOW}⚠️  尚未保存登录状态${NC}"
    echo ""
    echo "首次使用需要先登录："
    echo "  ./xiaodoudou-tekla.sh --auth"
    echo ""
    exit 1
fi

# 根据参数执行不同操作
case "$1" in
    --auth)
        echo "🔐 保存登录状态..."
        echo "请在弹出的浏览器中登录 Tekla Admin"
        python3 1_save_auth.py
        echo -e "${GREEN}🫘 登录状态已保存！${NC}"
        ;;
    --leo)
        echo -e "${BLUE}🇨🇳 切换许可给 Leo (中国)...${NC}"
        python3 2_tekla_skill.py LEO
        echo -e "${GREEN}🫘 切换完成！${NC}"
        ;;
    --auger)
        echo -e "${BLUE}🇨🇦 切换许可给 Auger (加拿大)...${NC}"
        python3 2_tekla_skill.py AUGER
        echo -e "${GREEN}🫘 切换完成！${NC}"
        ;;
    --status)
        echo "📊 检查登录状态..."
        if [ -f "state.json" ]; then
            echo -e "${GREEN}  ✅ 已保存登录状态${NC}"
            ls -lh state.json
        else
            echo -e "${YELLOW}  ⚠️  未保存登录状态${NC}"
        fi
        echo ""
        echo "📸 截图记录："
        if [ -d "screenshots" ]; then
            ls -1 screenshots/ | tail -5
        else
            echo "  暂无截图"
        fi
        ;;
    *)
        echo "小豆豆能帮你切换 Tekla License："
        echo ""
        echo "  ./xiaodoudou-tekla.sh --auth    首次登录保存状态"
        echo "  ./xiaodoudou-tekla.sh --leo     切换给 Leo (中国)"
        echo "  ./xiaodoudou-tekla.sh --auger   切换给 Auger (加拿大)"
        echo "  ./xiaodoudou-tekla.sh --status  查看状态"
        echo ""
        echo -e "${BLUE}🇨🇳 中国时间 9:00 → Leo${NC}"
        echo -e "${BLUE}🇨🇦 加拿大时间 8:00 → Auger${NC}"
        echo ""
        echo -e "${PINK}🫘 有事叫我，没事我不吵你~${NC}"
        ;;
esac
