import time
import streamlit as st

st.set_page_config(
    page_title="Tiệm Pizza Vui Vẻ", page_icon="🍕", layout="centered"
)

st.title("🍕 Tiệm Pizza Vui Vẻ - Làm Bánh Theo Yêu Cầu")
st.write(
    "Chào mừng bạn đến với tiệm pizza! Hãy thiết kế chiếc bánh hoàn hảo cho khách hàng nhé."
)

# Khởi tạo trạng thái game (Session State)
if "score" not in st.session_state:
    st.session_state.score = 0
if "orders_completed" not in st.session_state:
    st.session_state.orders_completed = 0

# Danh sách nguyên liệu
CRUST_OPTIONS = ["Đế dày giòn", "Đế mỏng truyền thống", "Đế phô mai viền"]
SAUCE_OPTIONS = ["Sốt Cà Chua Truyền Thống", "Sốt Kem Trắng", "Sốt BBQ"]
TOPPING_OPTIONS = [
    "Phô mai Mozzarella 🧀",
    "Xúc xích Pepperoni 🥓",
    "Nấm tươi 🍄",
    "Ớt chuông 🫑",
    "Hành tây 🧅",
    "Dứa (Thơm) 🍍",
]

# Tạo một đơn hàng ngẫu nhiên (nếu chưa có)
if "current_order" not in st.session_state:
    import random

    st.session_state.current_order = {
        "crust": random.choice(CRUST_OPTIONS),
        "sauce": random.choice(SAUCE_OPTIONS),
        "toppings": random.sample(
            TOPPING_OPTIONS, k=random.randint(2, 4)
        ),  # Khách yêu cầu 2-4 loại topping
    }

# Hiển thị yêu cầu của khách hàng
st.markdown("---")
st.subheader("📋 Yêu cầu từ Khách hàng:")
order = st.session_state.current_order
st.info(
    f"""
- **Loại đế:** {order['crust']}
- **Loại sốt:** {order['sauce']}
- **Topping yêu cầu:** {', '.join(order['toppings'])}
"""
)

# Giao diện cho người chơi làm bánh
st.markdown("---")
st.subheader("🧑‍🍳 Bếp làm bánh của bạn:")

with st.form("pizza_form"):
    player_crust = st.selectbox("1. Chọn đế bánh:", CRUST_OPTIONS)
    player_sauce = st.selectbox("2. Chọn loại sốt:", SAUCE_OPTIONS)

    st.write("3. Chọn các loại Topping (chọn những loại khách yêu cầu):")
    player_toppings = []
    for t in TOPPING_OPTIONS:
        if st.checkbox(t):
            player_toppings.append(t)

    submitted = st.form_submit_button("🔥 Đem đi nướng và Phục vụ!")

if submitted:
    # Tính điểm
    points = 0
    feedback = []

    if player_crust == order["crust"]:
        points += 30
        feedback.append("✅ Đúng loại đế bánh (+30đ)")
    else:
        feedback.append("❌ Sai loại đế bánh")

    if player_sauce == order["sauce"]:
        points += 30
        feedback.append("✅ Đúng loại sốt (+30đ)")
    else:
        feedback.append("❌ Sai loại sốt")

    # Tính điểm topping (khớp chính xác các topping khách muốn)
    set_order_t = set(order["toppings"])
    set_player_t = set(player_toppings)

    if set_order_t == set_player_t:
        points += 40
        feedback.append("✅ Topping chuẩn xác hoàn hảo! (+40đ)")
    else:
        # Tính điểm dựa trên độ chính xác tương đối
        intersection = len(set_order_t.intersection(set_player_t))
        union = len(set_order_t.union(set_player_t))
        match_score = int((intersection / union) * 40) if union > 0 else 0
        points += match_score
        feedback.append(
            f"⚠️ Topping chưa hoàn toàn khớp yêu cầu (+{match_score}đ)"
        )

    # Hiệu ứng nướng bánh
    with st.spinner("Đang nướng bánh trong lò vi sóng... Chờ xíu nhé! 🔥"):
        time.sleep(1.5)

    st.markdown("### Kết quả đánh giá:")
    for f in feedback:
        st.write(f)

    if points >= 90:
        st.balloons()
        st.success(
            f"🎉 Xuất sắc! Khách hàng cho bạn {points}/100 điểm và boa thêm tiền!"
        )
    elif points >= 50:
        st.warning(
            f"😊 Tạm ổn! Khách hàng ăn được với {points}/100 điểm."
        )
    else:
        st.error(
            f"😢 Khách chê vì làm sai ý họ quá nhiều! Bạn chỉ được {points}/100 điểm."
        )

    # Cập nhật tổng điểm
    st.session_state.score += points
    st.session_state.orders_completed += 1

    # Nút nhận đơn tiếp theo
    if st.button("🍕 Nhận đơn hàng tiếp theo"):
        # Tạo đơn mới
        st.session_state.current_order = {
            "crust": random.choice(CRUST_OPTIONS),
            "sauce": random.choice(SAUCE_OPTIONS),
            "toppings": random.sample(TOPPING_OPTIONS, k=random.randint(2, 4)),
        }
        st.rerun()

# Thanh sidebar hiển thị thông số quán
st.sidebar.title("📊 Thống kê Quán")
st.sidebar.metric(label="Tổng điểm", value=st.session_state.score)
st.sidebar.metric(
    label="Số bánh đã bán", value=st.session_state.orders_completed
)

if st.sidebar.button("Làm lại từ đầu 🔄"):
    st.session_state.score = 0
    st.session_state.orders_completed = 0
    if "current_order" in st.session_state:
        del st.session_state.current_order
    st.rerun()
