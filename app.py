import random
import time
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS cho phong cách mèo & hiệu ứng bánh Pizza
st.markdown(
    """
<style>
    .stApp {
        background-color: #FFF9F0;
    }
    .cat-card {
        background-color: #FFEED9;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #FFC09F;
        margin-bottom: 15px;
    }
    .pizza-plate {
        background-color: #E8D8C8;
        border-radius: 50%;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 4px dashed #B08968;
        width: 320px;
        height: 320px;
        margin: 0 auto;
    }
    .pizza-crust {
        background-color: #E6A15C;
        border-radius: 50%;
        width: 280px;
        height: 280px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        position: relative;
    }
    .pizza-sauce {
        background-color: #D64045;
        border-radius: 50%;
        width: 230px;
        height: 230px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .pizza-cheese {
        background-color: #FFD166;
        border-radius: 50%;
        width: 190px;
        height: 190px;
        position: relative;
        overflow: hidden;
    }
    .topping-item {
        position: absolute;
        font-size: 20px;
        user-select: none;
        transform: translate(-50%, -50%);
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- KHỞI TẠO NGUYÊN LIỆU ---
INGREDIENTS = {
    "sauce": {"Sốt Cà Chua 🍅": "🍅"},
    "cheese": {"Phô Mai 🧀": "🧀"},
    "toppings": {
        "Xúc xích 🥓": "🥓",
        "Nấm 🍄": "🍄",
        "Ớt chuông 🫑": "🫑",
        "Thịt xông khói 🍖": "🍖",
        "Ô liu 🫒": "🫒",
    },
}

CAT_CUSTOMERS = [
    {"name": "Mèo Béo Miu Miu 🐱", "avatar": "🐱", "personality": "Thèm ăn"},
    {"name": "Tiểu Mộc Mèo 😸", "avatar": "😸", "personality": "Vui vẻ"},
    {"name": "Quý Bà Hoàng Gia 😺", "avatar": "😺", "personality": "Khó tính"},
    {"name": "Mèo Mập Mập 😸", "avatar": "😸", "personality": "Dễ tính"},
    {"name": "Hoàng Tử Mèo 🐈‍⬛", "avatar": "🐈‍⬛", "personality": "Sang chảnh"},
]

# Tọa độ ngẫu nhiên cố định tương đối quanh hình tròn bánh (bán kính <= 40%)
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
    (38, 40),
    (62, 40),
    (40, 62),
    (60, 62),
]

# --- QUẢN LÝ STATE ---
if "day" not in st.session_state:
    st.session_state.day = 1
if "total_money" not in st.session_state:
    st.session_state.total_money = 0
if "day_money" not in st.session_state:
    st.session_state.day_money = 0
if "customers_served" not in st.session_state:
    st.session_state.customers_served = 0
if "day_customers" not in st.session_state:
    st.session_state.day_customers = 0
if "satisfaction_scores" not in st.session_state:
    st.session_state.satisfaction_scores = []
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
if "current_order" not in st.session_state:
    st.session_state.current_order = None
if "day_ended" not in st.session_state:
    st.session_state.day_ended = False

MAX_CUSTOMERS_PER_DAY = 3


# --- HÀM TẠO ĐƠN HÀNG MỚI ---
def generate_new_customer():
    cat = random.choice(CAT_CUSTOMERS)
    num_toppings = random.randint(2, 4)
    chosen_toppings = random.sample(
        list(INGREDIENTS["toppings"].keys()), num_toppings
    )

    st.session_state.current_customer = cat
    st.session_state.current_order = {
        "sauce": True,
        "cheese": True,
        "toppings": chosen_toppings,
    }


if (
    st.session_state.current_customer is None
    and not st.session_state.day_ended
):
    generate_new_customer()

# --- TIÊU ĐỀ KHU VỰC ---
st.title("🍕 Pizza Meo Meo – Tiệm Pizza Trong Thế Giới Mèo 🐾")

# Sidebar - Thống kê quán
st.sidebar.header("📊 Thông Tin Tiệm Bánh")
st.sidebar.markdown(f"🗓️ **Ngày làm việc:** {st.session_state.day}")
st.sidebar.markdown(f"💰 **Tổng doanh thu:** {st.session_state.total_money}$")
st.sidebar.markdown(
    f"👥 **Tổng khách đã phục vụ:** {st.session_state.customers_served}"
)
st.sidebar.markdown("---")

if st.sidebar.button("Làm lại từ đầu 🔄"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- MÀN HÌNH TỔNG KẾT CUỐI NGÀY ---
if st.session_state.day_ended:
    st.balloons()
    st.markdown("## 🌙 Cửa hàng đóng cửa! Tổng kết Ngày " + str(st.session_state.day))

    avg_sat = (
        sum(st.session_state.satisfaction_scores)
        / len(st.session_state.satisfaction_scores)
        if st.session_state.satisfaction_scores
        else 0
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Doanh thu hôm nay", f"{st.session_state.day_money}$")
    col2.metric("🐾 Số khách phục vụ", f"{st.session_state.day_customers}")
    col3.metric("❤️ Độ hài lòng TB", f"{avg_sat:.1f}/100")

    st.success(
        f"Bạn đã hoàn thành tuyệt vời Ngày {st.session_state.day}! Hãy nghỉ ngơi để chuẩn bị cho ngày tiếp theo."
    )

    if st.button("Mở cửa Ngày Tiếp Theo ☀️"):
        st.session_state.day += 1
        st.session_state.day_money = 0
        st.session_state.day_customers = 0
        st.session_state.day_ended = False
        generate_new_customer()
        st.rerun()

else:
    # --- MÀN HÌNH CHƠI GAME HÀNG NGÀY ---
    customer = st.session_state.current_customer
    order = st.session_state.current_order

    # 1. Khách hàng giao đơn
    st.markdown(
        f"""
    <div class="cat-card">
        <h3>{customer['avatar']} Khách hàng: {customer['name']} ({customer['personality']})</h3>
        <p><i>"Meo meo! Tôi muốn một chiếc pizza nóng hổi có:"</i></p>
        <ul>
            <li><b>Đế bánh + Sốt Cà Chua 🍅 + Phô Mai 🧀</b></li>
            <li><b>Topping:</b> {', '.join(order['toppings'])}</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Khách hàng thứ {st.session_state.day_customers + 1}/{MAX_CUSTOMERS_PER_DAY} trong Ngày {st.session_state.day}"
    )

    # 2. Khay chọn nguyên liệu
    st.markdown("### 🧑‍🍳 Khay Nguyên Liệu Bếp")

    col_base, col_top = st.columns([1, 1])

    with col_base:
        st.subheader("1. Cơ bản")
        has_dough = st.checkbox("Bột nhào (Đế bánh) 🫓", value=True)
        has_sauce = st.checkbox("Sốt Cà Chua 🍅", value=True)
        has_cheese = st.checkbox("Phô Mai 🧀", value=True)

    with col_top:
        st.subheader("2. Khay Topping")
        selected_toppings = []
        for top_name, emoji in INGREDIENTS["toppings"].items():
            if st.checkbox(f"{top_name}"):
                selected_toppings.append(top_name)

    # 3. Hiển thị chiếc Pizza thực tế với Topping rải đều
    st.markdown("### 🍕 Chiếc Pizza Của Bạn:")

    # Tạo HTML cho topping rải rác xung quanh
    topping_elements = []
    if selected_toppings and has_cheese:
        pos_idx = 0
        # Mỗi loại topping được chọn sẽ đặt 4-5 miếng ở các vị trí khác nhau
        for t in selected_toppings:
            emoji = INGREDIENTS["toppings"][t]
            for _ in range(4):
                top_percent, left_percent = TOPPING_POSITIONS[
                    pos_idx % len(TOPPING_POSITIONS)
                ]
                topping_elements.append(
                    f'<span class="topping-item" style="top:{top_percent}%; left:{left_percent}%;">{emoji}</span>'
                )
                pos_idx += 3

    pizza_toppings_html = "".join(topping_elements)

    sauce_style = (
        'class="pizza-sauce"' if has_sauce else 'style="background:transparent;"'
    )
    cheese_style = (
        'class="pizza-cheese"'
        if has_cheese
        else 'style="background:transparent;"'
    )

    if has_dough:
        st.markdown(
            f"""
        <div class="pizza-plate">
            <div class="pizza-crust">
                <div {sauce_style}>
                    <div {cheese_style}>
                        {pizza_toppings_html}
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ Bạn chưa chuẩn bị Bột nhào (Đế bánh)!")

    # 4. Nướng và Giao bánh
    st.markdown("---")
    if st.button("🔥 Đưa Vào Lò Nướng & Giao Cho Khách 🐾"):
        if not has_dough:
            st.error("❌ Không thể nướng pizza mà không có đế bánh!")
        else:
            with st.spinner("🔥 Đang nướng pizza trong lò nướng thơm lừng..."):
                time.sleep(1.8)

            score = 100
            reasons = []

            if not has_sauce:
                score -= 25
                reasons.append("Thiếu sốt cà chua")
            if not has_cheese:
                score -= 25
                reasons.append("Thiếu phô mai")

            target_toppings = set(order["toppings"])
            user_toppings = set(selected_toppings)

            missing = target_toppings - user_toppings
            extra = user_toppings - target_toppings

            if missing:
                score -= len(missing) * 15
                reasons.append(f"Thiếu: {', '.join(missing)}")
            if extra:
                score -= len(extra) * 10
                reasons.append(
                    f"Thừa nguyên liệu khách không gọi: {', '.join(extra)}"
                )

            score = max(0, score)

            base_pay = 20
            tip = int((score / 100) * 15)
            earned_money = base_pay + tip if score >= 50 else 5

            st.session_state.day_money += earned_money
            st.session_state.total_money += earned_money
            st.session_state.day_customers += 1
            st.session_state.customers_served += 1
            st.session_state.satisfaction_scores.append(score)

            st.markdown("### 📝 Đánh Giá Của Khách Hàng:")
            if score == 100:
                st.balloons()
                st.success(
                    f"🎉 {customer['name']}: 'Meo meo! Tuyệt vời hoàn hảo! Đúng vị tôi thích!' (+{earned_money}$)"
                )
            elif score >= 70:
                st.info(
                    f"😊 {customer['name']}: 'Khá ngon! Lần sau nhớ làm cẩn thận hơn nhé!' (+{earned_money}$)"
                )
            else:
                st.error(
                    f"😿 {customer['name']}: 'Bánh sai nhiều quá... Meo meo thất vọng!' (+{earned_money}$)"
                )

            if reasons:
                st.caption("Chi tiết: " + "; ".join(reasons))

            if st.session_state.day_customers >= MAX_CUSTOMERS_PER_DAY:
                st.session_state.day_ended = True
            else:
                generate_new_customer()

            time.sleep(1)
            st.button("Tiếp tục 🐾")
