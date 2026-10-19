import random
import time
import streamlit as st

# Cấu hình trang web Streamlit
st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS mô phỏng chính xác màu sắc và giao diện pastel trong ảnh
st.markdown(
    """
<style>
    /* Tổng thể nền pastel cam kem */
    .stApp {
        background-color: #FFF3E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Ẩn bớt thanh Streamlit thừa để giống game thật */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* MÀN HÌNH START GAME */
    .start-container {
        text-align: center;
        background: linear-gradient(180deg, #FFE0B2 0%, #FFF3E0 100%);
        padding: 50px 20px;
        border-radius: 25px;
        border: 4px solid #FFB74D;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 10px 25px rgba(255, 152, 0, 0.2);
    }
    .game-title {
        color: #8D4B38;
        font-size: 55px;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 2px 2px #FFE0B2;
    }
    .game-subtitle {
        color: #B16A5B;
        font-size: 20px;
        margin-bottom: 30px;
    }
    
    /* MÀN HÌNH GAMEPLAY - HEADER TOP BAR */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFE0B2;
        padding: 10px 25px;
        border-radius: 20px;
        border: 3px solid #FFB74D;
        margin-bottom: 15px;
    }
    .top-badge {
        background-color: #FFF;
        padding: 6px 16px;
        border-radius: 15px;
        font-weight: bold;
        color: #8D4B38;
        border: 2px solid #FFB74D;
    }

    /* KHÁCH HÀNG & BÓNG THOẠI */
    .customer-row {
        display: flex;
        justify-content: space-around;
        background-color: #FFF8E1;
        padding: 15px;
        border-radius: 20px;
        border: 3px solid #FFE0B2;
        margin-bottom: 20px;
    }
    .customer-card {
        text-align: center;
        position: relative;
    }
    .speech-bubble {
        background-color: #FFFFFF;
        border: 2px solid #8D4B38;
        border-radius: 15px;
        padding: 8px 12px;
        font-size: 13px;
        margin-bottom: 8px;
        position: relative;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* ĐƠN HÀNG BÊN TRÁI */
    .order-card {
        background-color: #FFF8E1;
        border: 3px dashed #FFB74D;
        border-radius: 20px;
        padding: 20px;
        color: #5D4037;
    }

    /* QUẦY BẾP & NGUYÊN LIỆU */
    .kitchen-counter {
        background-color: #D7CCC8;
        border-radius: 20px;
        padding: 15px;
        border: 4px solid #A1887F;
    }
    .ingredient-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        background-color: #BCAAA4;
        padding: 12px;
        border-radius: 15px;
    }
    .ingredient-box {
        background-color: #EFEBE9;
        border: 2px solid #8D6E63;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        color: #4E342E;
    }

    /* PIZZA VẼ TRÊN THỚT */
    .pizza-board {
        background-color: #D7CCC8;
        border-radius: 50%;
        width: 220px;
        height: 220px;
        margin: 0 auto;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 5px solid #8D6E63;
    }
    .pizza-crust {
        background-color: #E6A15C;
        border-radius: 50%;
        width: 190px;
        height: 190px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .pizza-sauce {
        background-color: #D64045;
        border-radius: 50%;
        width: 155px;
        height: 155px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .pizza-cheese {
        background-color: #FFD166;
        border-radius: 50%;
        width: 125px;
        height: 125px;
        position: relative;
    }
    .topping-item {
        position: absolute;
        font-size: 18px;
        transform: translate(-50%, -50%);
    }

    /* MÀN HÌNH TỔNG KẾT HẾT GIỜ */
    .summary-card {
        background-color: #FFF8E1;
        border: 4px solid #FFB74D;
        border-radius: 25px;
        padding: 30px;
        max-width: 850px;
        margin: 20px auto;
    }
    .summary-header {
        text-align: center;
        color: #8D4B38;
        font-size: 38px;
        font-weight: bold;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .metric-box {
        background-color: #FFF;
        border: 2px solid #FFE0B2;
        padding: 15px 25px;
        border-radius: 18px;
        text-align: center;
        font-weight: bold;
    }
    .review-item {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- KHỞI TẠO NGUYÊN LIỆU & KHÁCH HÀNG ---
INGREDIENTS = {
    "sauce": {"Sốt cà chua 🥫": "🍅"},
    "cheese": {"Phô mai 🧀": "🧀"},
    "toppings": {
        "Xúc xích 🥓": "🥓",
        "Thịt xông khói 🍖": "🍖",
        "Nấm 🍄": "🍄",
        "Ớt chuông 🫑": "🫑",
        "Ô liu 🫒": "🫒",
        "Dứa 🍍": "🍍",
    },
}

ALL_CATS = [
    {"name": "Miu Cam", "avatar": "🐱"},
    {"name": "Mun Mun", "avatar": "🐈‍⬛"},
    {"name": "Bánh Bao", "avatar": "😸"},
    {"name": "Đốm Sữa", "avatar": "😺"},
]

TOPPING_POSITIONS = [
    (50, 50),
    (30, 30),
    (70, 30),
    (30, 70),
    (70, 70),
    (50, 25),
    (25, 50),
    (75, 50),
    (50, 75),
    (40, 40),
    (60, 40),
    (40, 60),
]

# --- QUẢN LÝ TRẠNG THÁI (STATE) ---
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"  # START, PLAYING, SUMMARY
if "day" not in st.session_state:
    st.session_state.day = 3
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "day_coins" not in st.session_state:
    st.session_state.day_coins = 0
if "satisfaction" not in st.session_state:
    st.session_state.satisfaction = 88
if "customers_served" not in st.session_state:
    st.session_state.customers_served = 0
if "correct_orders" not in st.session_state:
    st.session_state.correct_orders = 0
if "reviews" not in st.session_state:
    st.session_state.reviews = []
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_pizza" not in st.session_state:
    st.session_state.current_pizza = {
        "dough": True,
        "sauce": False,
        "cheese": False,
        "toppings": [],
    }


def reset_day():
    st.session_state.day_coins = 0
    st.session_state.customers_served = 0
    st.session_state.correct_orders = 0
    st.session_state.reviews = []
    # Tạo hàng đợi 4 khách hàng
    st.session_state.queue = []
    for cat in ALL_CATS:
        num_t = random.randint(2, 3)
        toppings = random.sample(
            list(INGREDIENTS["toppings"].keys()), num_t
        )
        st.session_state.queue.append(
            {
                "cat": cat,
                "order": {
                    "sauce": True,
                    "cheese": True,
                    "toppings": toppings,
                },
            }
        )
    reset_pizza()


def reset_pizza():
    st.session_state.current_pizza = {
        "dough": True,
        "sauce": False,
        "cheese": False,
        "toppings": [],
    }


# ==========================================
# 1. MÀN HÌNH CHÍNH (START GAME)
# ==========================================
if st.session_state.game_state == "START":
    st.markdown(
        """
    <div class="start-container">
        <div style="font-size: 80px;">🐱🍕</div>
        <div class="game-title">Pizza Meo Meo</div>
        <div class="game-subtitle">🐾 Tiệm pizza của những chú mèo~ 🐾</div>
        <p>Chào mừng bạn đến với tiệm pizza dễ thương nhất thế giới mèo!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🐾 START GAME 🐾", use_container_width=True, type="primary"
        ):
            reset_day()
            st.session_state.game_state = "PLAYING"
            st.rerun()

# ==========================================
# 2. MÀN HÌNH GAMEPLAY (BẾP & LÀM BÁNH)
# ==========================================
elif st.session_state.game_state == "PLAYING":
    # 2.1 Thanh trạng thái trên cùng
    st.markdown(
        f"""
    <div class="top-bar">
        <div class="top-badge">📅 Ngày {st.session_state.day} - 12:45</div>
        <div class="top-badge">😊 {st.session_state.satisfaction}% Hài lòng</div>
        <div class="top-badge">🪙 {st.session_state.coins} xu</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 2.2 Hàng khách hàng mèo xếp hàng
    st.markdown("### 🐾 Hàng Khách Hàng Đang Chờ")
    cat_cols = st.columns(4)

    for idx, item in enumerate(st.session_state.queue):
        cat_info = item["cat"]
        order_info = item["order"]
        is_current = idx == 0

        with cat_cols[idx]:
            border_style = (
                "border: 3px solid #FF9800; background-color: #FFF3E0;"
                if is_current
                else "opacity: 0.7;"
            )
            top_emojis = " ".join(
                [INGREDIENTS["toppings"][t] for t in order_info["toppings"]]
            )

            st.markdown(
                f"""
            <div class="customer-card" style="{border_style} padding: 10px; border-radius: 15px;">
                <div class="speech-bubble">🍕 {top_emojis}</div>
                <div style="font-size: 40px;">{cat_info['avatar']}</div>
                <b>{cat_info['name']}</b>
                {'<br><small style="color:#FF9800;">(Đang phục vụ)</small>' if is_current else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # 2.3 Khu vực làm bánh chính (Cột trái: Đơn hàng, Cột phải: Bếp)
    col_order, col_kitchen = st.columns([1, 2])

    current_customer = st.session_state.queue[0] if st.session_state.queue else None

    with col_order:
        if current_customer:
            c_name = current_customer["cat"]["name"]
            c_order = current_customer["order"]
            toppings_list_html = "".join(
                [f"<li>{t}</li>" for t in c_order["toppings"]]
            )

            st.markdown(
                f"""
            <div class="order-card">
                <h3>📋 Đơn hàng hiện tại</h3>
                <h4>🐱 Khách hàng: {c_name}</h4>
                <p><b>Pizza yêu cầu:</b></p>
                <ul>
                    <li>Đế bánh</li>
                    <li>Sốt cà chua</li>
                    <li>Phô mai</li>
                    {toppings_list_html}
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col_kitchen:
        st.markdown("### 🧑‍🍳 Quầy Bếp Làm Bánh")

        # Hiển thị bánh pizza trực quan trên thớt
        cur_p = st.session_state.current_pizza
        sauce_bg = (
            'class="pizza-sauce"'
            if cur_p["sauce"]
            else 'style="background:transparent;"'
        )
        cheese_bg = (
            'class="pizza-cheese"'
            if cur_p["cheese"]
            else 'style="background:transparent;"'
        )

        # Tạo topping html rải rác
        topping_htmls = []
        pos_i = 0
        for t in cur_p["toppings"]:
            emoji = INGREDIENTS["toppings"][t]
            for _ in range(3):
                top_p, left_p = TOPPING_POSITIONS[pos_i % len(TOPPING_POSITIONS)]
                topping_htmls.append(
                    f'<span class="topping-item" style="top:{top_p}%; left:{left_p}%;">{emoji}</span>'
                )
                pos_i += 2

        st.markdown(
            f"""
        <div class="pizza-board">
            <div class="pizza-crust">
                <div {sauce_bg}>
                    <div {cheese_bg}>
                        {''.join(topping_htmls)}
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Quầy 8 khay nguyên liệu bấm chọn
        st.write("<b>Chạm vào nguyên liệu để thêm vào bánh:</b>", unsafe_allow_html=True)

        g_col1, g_col2, g_col3, g_col4 = st.columns(4)

        with g_col1:
            if st.button(
                "🍅 Sốt cà chua",
                use_container_width=True,
                disabled=cur_p["sauce"],
            ):
                cur_p["sauce"] = True
                st.rerun()
            if st.button("🍄 Nấm", use_container_width=True):
                cur_p["toppings"].append("Nấm 🍄")
                st.rerun()

        with g_col2:
            if st.button(
                "🧀 Phô mai",
                use_container_width=True,
                disabled=cur_p["cheese"],
            ):
                cur_p["cheese"] = True
                st.rerun()
            if st.button("🫑 Ớt chuông", use_container_width=True):
                cur_p["toppings"].append("Ớt chuông 🫑")
                st.rerun()

        with g_col3:
            if st.button("🥓 Xúc xích", use_container_width=True):
                cur_p["toppings"].append("Xúc xích 🥓")
                st.rerun()
            if st.button("🫒 Ô liu", use_container_width=True):
                cur_p["toppings"].append("Ô liu 🫒")
                st.rerun()

        with g_col4:
            if st.button("🍖 Thịt xông khói", use_container_width=True):
                cur_p["toppings"].append("Thịt xông khói 🍖")
                st.rerun()
            if st.button("🍍 Dứa", use_container_width=True):
                cur_p["toppings"].append("Dứa 🍍")
                st.rerun()

        st.markdown("---")

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🧹 Làm lại bánh mới", use_container_width=True):
                reset_pizza()
                st.rerun()

        with btn_col2:
            if st.button(
                "🔥 Đưa vào Lò Nướng & Giao Bánh 🔥",
                type="primary",
                use_container_width=True,
            ):
                # Xử lý chấm điểm bánh
                target = current_customer["order"]
                correct = True
                stars = 5
                comment = "Tuyệt vời! Đúng chiếc bánh tôi muốn!"

                if not cur_p["sauce"] or not cur_p["cheese"]:
                    correct = False
                    stars -= 2

                set_target = set(target["toppings"])
                set_user = set(cur_p["toppings"])

                if set_target != set_user:
                    correct = False
                    stars -= 1
                    comment = "Khá ngon, nhưng vẫn thiếu/sai chút gì đó!"

                if stars < 3:
                    comment = "Cũng được, lần sau hãy chú ý đơn hàng nhé!"

                earned = 100 if correct else 60
                st.session_state.coins += earned
                st.session_state.day_coins += earned
                st.session_state.customers_served += 1
                if correct:
                    st.session_state.correct_orders += 1

                # Lưu đánh giá
                st.session_state.reviews.append(
                    {
                        "name": current_customer["cat"]["name"],
                        "avatar": current_customer["cat"]["avatar"],
                        "stars": "⭐" * stars,
                        "comment": comment,
                    }
                )

                # Chuyển sang khách tiếp theo
                st.session_state.queue.pop(0)
                reset_pizza()

                # Nếu hết khách -> Sang màn hình Tổng kết
                if not st.session_state.queue:
                    st.session_state.game_state = "SUMMARY"

                st.rerun()

# ==========================================
# 3. MÀN HÌNH TỔNG KẾT (HẾT GIỜ RỒI!)
# ==========================================
elif st.session_state.game_state == "SUMMARY":
    st.balloons()
    st.markdown(
        f"""
    <div class="summary-card">
        <div class="summary-header">🐱 HẾT GIỜ RỒI! 🐾</div>
        <p style="text-align:center;">Tiệm Pizza Meo Meo đã kết thúc ngày hôm nay!</p>
        <h4 style="text-align:center; color:#FF9800;">🐾 Tổng kết ngày {st.session_state.day} 🐾</h4>
        
        <div class="metric-container">
            <div class="metric-box">
                <div>💰 Tổng doanh thu</div>
                <div style="font-size:24px; color:#E65100;">{st.session_state.day_coins} xu</div>
            </div>
            <div class="metric-box">
                <div>🐾 Khách đã phục vụ</div>
                <div style="font-size:24px; color:#E65100;">{st.session_state.customers_served} / 4</div>
            </div>
            <div class="metric-box">
                <div>⭐ Đơn chính xác</div>
                <div style="font-size:24px; color:#E65100;">{st.session_state.correct_orders} / 4</div>
            </div>
        </div>

        <h4 style="color:#8D4B38;">💬 Đánh giá của khách hàng:</h4>
    """,
        unsafe_allow_html=True,
    )

    for rev in st.session_state.reviews:
        st.markdown(
            f"""
        <div class="review-item">
            <div><b>{rev['avatar']} {rev['name']}</b></div>
            <div style="color:#FFB300;">{rev['stars']}</div>
            <div><i>"{rev['comment']}"</i></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🌻 BẮT ĐẦU NGÀY MỚI",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.day += 1
            reset_day()
            st.session_state.game_state = "PLAYING"
            st.rerun()

    with col2:
        if st.button("🏠 Về màn hình chính", use_container_width=True):
            st.session_state.game_state = "START"
            st.rerun()
