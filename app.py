import random
import streamlit as st

st.set_page_config(
    page_title="Pizza Meo Meo", page_icon="🐱", layout="centered"
)

# Khởi tạo trạng thái trò chơi
if "coins" not in st.session_state:
  st.session_state.coins = 10
if "day" not in st.session_state:
  st.session_state.day = 1
if "current_customer" not in st.session_state:
  st.session_state.current_customer = None
if "order" not in st.session_state:
  st.session_state.order = None

# Danh sách khách hàng và yêu cầu
cat_customers = [
    {
        "name": "Mèo Mập",
        "avatar": "🐱",
        "text": "Meo... Ta thích pizza đơn giản: Chỉ cần sốt cà chua và phô mai!",
        "recipe": ["Đế bánh", "Sốt cà chua", "Phô mai"],
    },
    {
        "name": "Mèo Mun",
        "avatar": "🐈‍⬛",
        "text": (
            "Gừ... Ta muốn một chiếc pizza đặc biệt có Phô mai và thật nhiều"
            " Cá Ngừ!"
        ),
        "recipe": ["Đế bánh", "Sốt cà chua", "Phô mai", "Cá ngừ"],
    },
    {
        "name": "Mèo Cam",
        "avatar": "🐈",
        "text": (
            "Meow! Cho tôi chiếc pizza topping Catnip (cỏ bạc hà mèo) để phấn"
            " khích nào!"
        ),
        "recipe": ["Đế bánh", "Sốt cà chua", "Phô mai", "Catnip"],
    },
]

st.title("🍕 Pizza Meo Meo")
st.markdown(
    "Chào mừng bạn đến với cửa hàng pizza dành riêng cho các chú mèo khó"
    " tính!"
)

# Thanh trạng thái
col1, col2 = st.columns(2)
with col1:
  st.metric(label="Ngày", value=st.session_state.day)
with col2:
  st.metric(label="Tiền xu cá khô", value=f"{st.session_state.coins} 🐟")

st.divider()

# Nếu chưa có khách hàng, gọi khách mới
if st.session_state.current_customer is None:
  if st.button("🔔 Đón khách tiếp theo"):
    st.session_state.current_customer = random.choice(cat_customers)
    st.rerun()
else:
  customer = st.session_state.current_customer
  st.subheader(f"Khách hàng: {customer['avatar']} {customer['name']}")
  st.info(f'"{customer["text"]}"')

  st.write("### 🍳 Khu vực làm bánh:")
  selected_ingredients = st.multiselect(
      "Chọn các nguyên liệu cho vào bánh:",
      [
          "Đế bánh",
          "Sốt cà chua",
          "Phô mai",
          "Cá ngừ",
          "Catnip",
          "Xúc xích",
          "Dâu tây",
      ],
  )

  if st.button("✨ Đưa bánh cho khách"):
    # Kiểm tra nguyên liệu
    target_recipe = set(customer["recipe"])
    user_recipe = set(selected_ingredients)

    if user_recipe == target_recipe:
      st.success("🎉 Khách mèo kêu gừ gừ vì quá ngon! Bạn nhận được +10 🐟")
      st.session_state.coins += 10
    elif target_recipe.issubset(user_recipe):
      st.warning(
          "😐 Bánh hơi thừa nguyên liệu một chút, nhưng khách vẫn ăn. Bạn nhận"
          " được +5 🐟"
      )
      st.session_state.coins += 5
    else:
      st.error(
          "😿 Khách mèo lắc đầu bỏ đi vì làm sai công thức! Bạn bị mất 5 🐟"
      )
      st.session_state.coins = max(0, st.session_state.coins - 5)

    # Reset khách hàng để đón khách mới
    st.session_state.current_customer = None
    if st.button("Tiếp tục ngày mới"):
      st.session_state.day += 1
      st.rerun()
