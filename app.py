import streamlit as st
import random

st.set_page_config(
    page_title="Pizza Meo Meo",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. DU LIEU TRO CHOI
# ==========================================

INGREDIENTS = {
    "Đế bánh": "🍞",
    "Sốt cà chua": "🍅",
    "Phô mai": "🧀",
    "Xúc xích": "🌭",
    "Nấm": "🍄",
    "Ớt chuông": "🫑",
    "Thịt xông khói": "🥓",
    "Ô liu": "🫒",
}

BASE_INGREDIENTS = [
    "Đế bánh", "Sốt cà chua", "Phô mai"
]

TOPPINGS = [
    "Xúc xích", "Nấm", "Ớt chuông",
    "Thịt xông khói", "Ô liu"
]

CATS = [
    ("Miu Cam", "🐈"),
    ("Mun Mun", "🐈‍⬛"),
    ("Bánh Bao", "😺"),
    ("Đốm Sữa", "🐱"),
    ("Mây Nhỏ", "😸"),
    ("Bông Gòn", "😻"),
    ("Mèo Sữa", "🐈"),
    ("Tiểu Meo", "😽"),
]

CUSTOMERS_PER_DAY = 4


def new_order():
    name, face = random.choice(CATS)
    wanted = random.sample(TOPPINGS, random.randint(1, 3))

    return {
        "cat": (name, face),
        "wanted": wanted,
        "price": 50 + len(wanted) * 10,
    }


def start_day():
    st.session_state.phase = "game"
    st.session_state.day += 1
    st.session_state.daily_revenue = 0
    st.session_state.daily_served = 0
    st.session_state.daily_correct = 0
    st.session_state.reviews = []
    st.session_state.order = new_order()
    st.session_state.pizza = []
    st.session_state.baked = False
    st.session_state.last_message = ""


def init_game():
    defaults = {
        "phase": "start",
        "day": 0,
        "coins": 100,
        "daily_revenue": 0,
        "daily_served": 0,
        "daily_correct": 0,
        "reviews": [],
        "order": None,
        "pizza": [],
        "baked": False,
        "last_message": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_game()

# ==========================================
# 2. GIAO DIEN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #fff7ef;
}
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #a94e3a;
}
div.stButton > button {
    background-color: #ffe0d2;
    color: #713d32;
    border: 1px solid #edc5b3;
    border-radius: 12px;
    font-weight: 600;
    min-height: 42px;
}
div.stButton > button:hover {
    background-color: #ffc7b2;
    border-color: #db987e;
}
.start-panel {
    background: linear-gradient(135deg, #ffe4d8, #fff2d5);
    border: 2px solid #f2c7b5;
    border-radius: 26px;
    padding: 28px 16px;
    text-align: center;
}
.customer-card {
    background: #fffaf3;
    border: 2px solid #e8c4a7;
    border-radius: 18px;
    padding: 12px;
    text-align: center;
}
.order-card {
    background: #fff0d8;
    border: 2px dashed #cf9873;
    border-radius: 16px;
    padding: 14px;
}
.counter-card {
    background: #f4d5b9;
    border: 3px solid #bd8768;
    border-radius: 18px;
    padding: 14px;
    text-align: center;
}
.pizza-base {
    width: 230px;
    height: 230px;
    max-width: 100%;
    margin: 10px auto;
    background: #ffe6a6;
    border: 10px solid #d79b5d;
    border-radius: 50%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-content: center;
    align-items: center;
    gap: 6px;
    padding: 22px;
    box-sizing: border-box;
    box-shadow: inset 0 0 0 4px #f8cf81;
}
.ingredient-emoji {
    font-size: 27px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MAN HINH BAT DAU
# ==========================================

if st.session_state.phase == "start":

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="start-panel">
        <div style="font-size:85px">🐱🍕</div>
        <h1 style="font-size:42px">PIZZA MEO MEO</h1>
        <p style="font-size:20px">
            Tiệm pizza nhỏ giữa thế giới mèo
        </p>
        <p>👩‍🍳 Làm bánh · 💗 Phục vụ · 🪙 Kiếm xu</p>
        <p>Hãy trở thành đầu bếp được yêu thích nhất!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    _, middle, _ = st.columns([1, 2, 1])

    with middle:
        if st.button("🐾 START GAME 🐾",
                     use_container_width=True):
            start_day()
            st.rerun()

    st.caption(
        "Mẹo nhỏ: Đọc thật kỹ đơn hàng để làm pizza chính xác nhé!"
    )


# ==========================================
# 4. MAN HINH CHOI GAME
# ==========================================

elif st.session_state.phase == "game":

    st.title("🐱🍕 Pizza Meo Meo")
    st.caption(f"☀️ Ngày {st.session_state.day} tại tiệm mèo")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("🪙 Tổng xu", st.session_state.coins)
    m2.metric("💰 Doanh thu hôm nay",
              st.session_state.daily_revenue)
    m3.metric(
        "🐾 Khách đã phục vụ",
        f"{st.session_state.daily_served}/{CUSTOMERS_PER_DAY}"
    )
    m4.metric("⭐ Đơn làm đúng",
              st.session_state.daily_correct)

    st.progress(
        st.session_state.daily_served / CUSTOMERS_PER_DAY,
        text="Tiến độ hôm nay"
    )

    st.divider()

    # Khach hang dung cho
    st.subheader("🐈 Khách hàng tại quầy")

    customer_columns = st.columns(4)
    waiting_faces = ["🐈", "🐈‍⬛", "😺", "😸"]

    for i, col in enumerate(customer_columns):
        with col:
            if i == 0 and st.session_state.order is not None:
                cat_name, cat_face = st.session_state.order["cat"]

                st.markdown(f"""
                <div class="customer-card">
                    <div style="font-size:53px">{cat_face}</div>
                    <b>{cat_name}</b>
                    <p>💬 Tôi muốn pizza!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="customer-card">
                    <div style="font-size:48px">{waiting_faces[i]}</div>
                    <b>Khách đang chờ</b>
                    <p>🍕 Meo meo!</p>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    # Tao don hang tiep theo
    if st.session_state.order is None:

        st.info("Khách tiếp theo đang chờ bạn!")

        if st.session_state.daily_served < CUSTOMERS_PER_DAY:
            if st.button("🔔 Mời khách tiếp theo",
                         use_container_width=True):
                st.session_state.order = new_order()
                st.session_state.pizza = []
                st.session_state.baked = False
                st.rerun()

    else:

        order = st.session_state.order
        wanted = order["wanted"]

        order_col, pizza_col, oven_col = st.columns([1, 1.5, 1])

        # ----------------------------------
        # DON HANG
        # ----------------------------------
        with order_col:

            st.subheader("📋 Đơn hàng")

            cat_name = order["cat"][0]

            st.markdown(f"""
            <div class="order-card">
                <h3>💌 {cat_name} nhắn:</h3>
                <p>"Làm cho tôi một chiếc pizza có..."</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("🍞 Đế bánh")
            st.write("🍅 Sốt cà chua")
            st.write("🧀 Phô mai")

            for item in wanted:
                st.write(f"{INGREDIENTS[item]} {item}")

            st.divider()

            st.write("*Giá tối đa:*")
            st.markdown(
                f"### 🪙 {order['price']} xu"
            )
            st.caption(
                "Thiếu topping hoặc thêm sai sẽ bị trừ tiền!"
            )

        # ----------------------------------
        # BAN LAM PIZZA
        # ----------------------------------
        with pizza_col:

            st.subheader("🍕 Bàn làm bánh")

            pizza = st.session_state.pizza

            if pizza:
                emoji_content = "".join(
                    f"<span class='ingredient-emoji'>"
                    f"{INGREDIENTS[item]}</span>"
                    for item in pizza
                )
            else:
                emoji_content = (
                    "<span style='font-size:45px'>🍞</span>"
                )

            st.markdown(f"""
            <div class="pizza-base">
                {emoji_content}
            </div>
            """, unsafe_allow_html=True)

            st.caption("Chiếc pizza của bạn")

            if pizza:
                st.write("Nguyên liệu đã chọn:")
                st.write(" · ".join(pizza))
            else:
                st.write("Chưa có nguyên liệu nào.")

            if st.button(
                "🧹 Làm lại bánh",
                use_container_width=True,
                disabled=st.session_state.baked
            ):
                st.session_state.pizza = []
                st.rerun()

        # ----------------------------------
        # LO NUONG
        # ----------------------------------
        with oven_col:

            st.subheader("🔥 Lò nướng")

            st.markdown("""
            <div class="counter-card">
                <div style="font-size:70px">♨️</div>
                <h3>Lò nướng mèo</h3>
                <p>Nướng bánh thật thơm!</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            if st.session_state.baked:
                st.success("Pizza đã chín! 🍕")

            if st.button(
                "🔥 NƯỚNG PIZZA",
                use_container_width=True,
                disabled=st.session_state.baked
            ):
                if not all(
                    item in st.session_state.pizza
                    for item in BASE_INGREDIENTS
                ):
                    st.warning(
                        "Cần có đế bánh, sốt cà chua và phô mai!"
                    )
                else:
                    st.session_state.baked = True
                    st.rerun()

            if st.button(
                "🐱 GIAO PIZZA",
                use_container_width=True,
                disabled=not st.session_state.baked
            ):
                base = set(BASE_INGREDIENTS)
                made = set(st.session_state.pizza)
                expected = set(wanted)

                actual_toppings = made - base
                missing = expected - actual_toppings
                extra = actual_toppings - expected

                # Cham diem do chinh xac
                score = max(
                    0,
                    100 - 25 * len(missing) - 12 * len(extra)
                )

                payment = round(order["price"] * score / 100)

                if score == 100:
                    review = "⭐⭐⭐⭐⭐ Hoàn hảo! Đúng chiếc bánh tôi muốn!"
                    st.session_state.daily_correct += 1
                elif score >= 70:
                    review = "⭐⭐⭐⭐ Khá ngon, nhưng vẫn thiếu chút gì đó!"
                elif score >= 40:
                    review = "⭐⭐⭐ Lần sau hãy chú ý đơn hàng nhé!"
                else:
                    review = "⭐⭐ Bánh chưa đúng ý tôi lắm!"

                st.session_state.coins += payment
                st.session_state.daily_revenue += payment
                st.session_state.daily_served += 1

                st.session_state.reviews.append({
                    "cat": cat_name,
                    "payment": payment,
                    "score": score,
                    "review": review
                })

                st.session_state.last_message = (
                    f"{cat_name} trả {payment} xu. {review}"
                )

                st.session_state.order = None
                st.session_state.pizza = []
                st.session_state.baked = False

                if (
                    st.session_state.daily_served
                    >= CUSTOMERS_PER_DAY
                ):
                    st.session_state.phase = "summary"

                st.rerun()

        # ----------------------------------
        # KHAY NGUYEN LIEU
        # ----------------------------------
        st.divider()
        st.subheader("🧺 Khay nguyên liệu")

        st.write(
            "Chọn từng nguyên liệu để thêm vào chiếc bánh. "
            "Mỗi loại chỉ được thêm một lần."
        )

        ingredient_cols = st.columns(4)

        for i, (item, emoji) in enumerate(INGREDIENTS.items()):

            with ingredient_cols[i % 4]:

                already_added = item in st.session_state.pizza

                label = (
                    f"✅ {emoji} {item}"
                    if already_added
                    else f"{emoji} {item}"
                )

                if st.button(
                    label,
                    key=f"ingredient_{item}",
                    use_container_width=True,
                    disabled=(
                        st.session_state.baked
                        or already_added
                    )
                ):
                    st.session_state.pizza.append(item)
                    st.rerun()

    st.divider()

    if st.session_state.last_message:
        st.info(st.session_state.last_message)

    if st.button("🌙 Kết thúc ngày",
                 use_container_width=True):
        st.session_state.phase = "summary"
        st.session_state.order = None
        st.session_state.pizza = []
        st.session_state.baked = False
        st.rerun()


# ==========================================
# 5. MAN HINH TONG KET CUOI NGAY
# ==========================================

elif st.session_state.phase == "summary":

    st.markdown("""
    <div class="start-panel">
        <div style="font-size:75px">🌙🐱🌙</div>
        <h1>HẾT GIỜ RỒI!</h1>
        <p>Tiệm Pizza Meo Meo đã kết thúc ngày hôm nay.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"📊 Tổng kết ngày {st.session_state.day}")

    a, b, c = st.columns(3)

    a.metric(
        "💰 Tổng doanh thu",
        f"{st.session_state.daily_revenue} xu"
    )
    b.metric(
        "🐈 Khách đã phục vụ",
        st.session_state.daily_served
    )
    c.metric(
        "⭐ Đơn làm đúng",
        st.session_state.daily_correct
    )

    st.divider()
    st.subheader("💌 Đánh giá của khách hàng")

    if st.session_state.reviews:

        for review in st.session_state.reviews:

            with st.container(border=True):
                st.write(f"🐱 *{review['cat']}*")
                st.write(review["review"])
                st.caption(
                    f"Độ chính xác: {review['score']}% "
                    f"· Nhận: {review['payment']} xu"
                )

    else:
        st.info("Hôm nay chưa có khách nào được phục vụ.")

    served = st.session_state.daily_served

    if served > 0:
        ratio = (
            st.session_state.daily_correct / served
        )

        if ratio >= 0.75:
            st.success(
                "🏆 Xuất sắc! Tiệm của bạn được yêu thích!"
            )
        elif ratio >= 0.4:
            st.info(
                "🐾 Khá tốt! Ngày mai hãy cố gắng hơn nhé!"
            )
        else:
            st.warning(
                "💗 Hãy đọc kỹ đơn hàng hơn vào ngày mai nha!"
            )

    st.divider()

    if st.button(
        "🌞 BẮT ĐẦU NGÀY MỚI",
        use_container_width=True
    ):
        start_day()
        st.rerun()

    if st.button(
        "🏠 Về màn hình chính",
        use_container_width=True
    ):
        st.session_state.phase = "start"
        st.rerun()


# ==========================================
# 6. CHAN TRANG
# ==========================================

st.markdown("---")
st.caption(
    "🐾 Pizza Meo Meo · Một chiếc pizza, ngàn niềm vui!"
)
