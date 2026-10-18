import streamlit as st
import random

st.set_page_config(
    page_title="Pizza Meo Meo",
    page_icon="🐱",
    layout="wide"
)

# ===== KHOI TAO GAME =====
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "day" not in st.session_state:
    st.session_state.day = 1
if "served" not in st.session_state:
    st.session_state.served = 0
if "order" not in st.session_state:
    st.session_state.order = None
if "ingredients" not in st.session_state:
    st.session_state.ingredients = {
        "Đế bánh": 10,
        "Sốt cà chua": 10,
        "Phô mai": 10,
        "Xúc xích": 5,
        "Nấm": 5,
        "Ớt chuông": 5
    }
if "pizza" not in st.session_state:
    st.session_state.pizza = []
if "baked" not in st.session_state:
    st.session_state.baked = False
if "oven" not in st.session_state:
    st.session_state.oven = 1
if "message" not in st.session_state:
    st.session_state.message = "Meo meo! Chào mừng đến tiệm!"

TOPPINGS = ["Xúc xích", "Nấm", "Ớt chuông"]

EMOJI = {
    "Đế bánh": "🍞",
    "Sốt cà chua": "🍅",
    "Phô mai": "🧀",
    "Xúc xích": "🌭",
    "Nấm": "🍄",
    "Ớt chuông": "🫑"
}

CATS = [
    ("Miu Cam", "🐈"),
    ("Mun Mun", "🐈‍⬛"),
    ("Bánh Bao", "😺"),
    ("Đốm Sữa", "🐱"),
    ("Mây Nhỏ", "😸")
]

PRICE = {
    "Đế bánh": 5,
    "Sốt cà chua": 3,
    "Phô mai": 4,
    "Xúc xích": 6,
    "Nấm": 4,
    "Ớt chuông": 3
}

# ===== GIAO DIEN =====
st.markdown("""
<style>
.stApp {
    background-color: #fff7ef;
}
h1, h2, h3 {
    color: #b64d36;
}
div.stButton > button {
    border-radius: 12px;
    border: 1px solid #f0c6b3;
    background-color: #f5b6a1;
    color: #713727;
    font-weight: bold;
}
div[data-testid="stMetric"] {
    background: white;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #f5d7c9;
}
</style>
""", unsafe_allow_html=True)

st.title("🐱🍕 PIZZA MEO MEO")
st.write("Thế giới mèo - nơi những chiếc pizza được tạo ra bằng tình yêu!")

a, b, c = st.columns(3)
a.metric("🪙 Xu mèo", st.session_state.coins)
b.metric("🐾 Khách đã phục vụ", st.session_state.served)
c.metric("📅 Ngày", st.session_state.day)

st.divider()

kitchen, oven = st.columns([1, 1.4])

# ===== KHU VUC NGUYEN LIEU =====
with kitchen:
    st.header("🧺 Quầy nguyên liệu")

    for name, quantity in st.session_state.ingredients.items():
        st.write(f"{EMOJI[name]} {name}: *{quantity}*")

    st.subheader("🛒 Mua nguyên liệu")

    item = st.selectbox(
        "Chọn nguyên liệu",
        list(PRICE.keys())
    )
    amount = st.selectbox("Số lượng", [1, 2, 3, 5])
    cost = PRICE[item] * amount

    st.caption(f"Giá cần trả: {cost} xu")

    if st.button("Mua nguyên liệu"):
        if st.session_state.coins >= cost:
            st.session_state.coins -= cost
            st.session_state.ingredients[item] += amount
            st.success("Mua thành công! Meo meo!")
            st.rerun()
        else:
            st.warning("Bạn chưa đủ xu rồi!")

# ===== KHU VUC LAM BANH =====
with oven:
    st.header("🍕 Bàn làm pizza")

    if st.session_state.order is None:
        st.info("Một bé mèo đang đói bụng!")
        if st.button("🔔 Nhận đơn hàng"):
            cat = random.choice(CATS)
            toppings = random.sample(
                TOPPINGS, k=random.choice([1, 2])
            )
            st.session_state.order = {
                "cat": cat,
                "toppings": toppings
            }
            st.session_state.pizza = []
            st.session_state.baked = False
            st.rerun()
    else:
        cat, cat_emoji = st.session_state.order["cat"]
        wanted = st.session_state.order["toppings"]

        st.subheader(f"{cat_emoji} Khách hàng: {cat}")
        st.write("Khách muốn pizza có:")
        st.success(" + ".join(
            EMOJI[x] + " " + x for x in wanted
        ))

        st.subheader("👩‍🍳 Thêm nguyên liệu vào bánh")

        for name in PRICE:
            if st.button(
                f"{EMOJI[name]} Thêm {name}",
                key="add_" + name,
                disabled=st.session_state.baked
            ):
                if st.session_state.ingredients[name] <= 0:
                    st.warning("Hết nguyên liệu! Hãy mua thêm.")
                elif name in st.session_state.pizza:
                    st.info("Bạn đã thêm nguyên liệu này rồi!")
                else:
                    st.session_state.pizza.append(name)
                    st.session_state.ingredients[name] -= 1
                    st.rerun()

        st.subheader("🎨 Chiếc bánh của bạn")

        if not st.session_state.pizza:
            st.markdown("## 🍞")
            st.caption("Hãy thêm nguyên liệu để làm bánh!")
        else:
            st.markdown(
                "## " + " ".join(
                    EMOJI[x] for x in st.session_state.pizza
                )
            )
            st.write(" + ".join(st.session_state.pizza))

        if st.button(
            "🧹 Làm lại bánh",
            disabled=st.session_state.baked
        ):
            for name in st.session_state.pizza:
                st.session_state.ingredients[name] += 1
            st.session_state.pizza = []
            st.rerun()

        if st.button(
            "🔥 Đưa bánh vào lò",
            disabled=st.session_state.baked
        ):
            pizza = st.session_state.pizza

            if not all(x in pizza for x in [
                "Đế bánh", "Sốt cà chua", "Phô mai"
            ]):
                st.warning(
                    "Cần có đế bánh, sốt cà chua và phô mai!"
                )
            elif not all(x in pizza for x in wanted):
                st.warning("Bánh chưa đúng yêu cầu của khách!")
            else:
                st.session_state.baked = True
                st.success("Pizza đã chín! Thơm quá! 🍕")
                st.rerun()

        if st.session_state.baked:
            if st.button("🐱 Giao bánh cho khách"):
                reward = 25 + st.session_state.oven * 5
                st.session_state.coins += reward
                st.session_state.served += 1
                st.session_state.message = (
                    f"{cat} rất vui! Bạn nhận được {reward} xu!"
                )
                st.session_state.order = None
                st.session_state.pizza = []
                st.session_state.baked = False
                st.rerun()

st.divider()

st.subheader("💌 Tin nhắn từ thế giới mèo")
st.write(st.session_state.message)

left, right = st.columns(2)

with left:
    if st.button("🌙 Kết thúc ngày"):
        st.session_state.day += 1
        st.session_state.coins += 15
        st.session_state.message = (
            "Ngày mới bắt đầu! Bạn được thưởng 15 xu."
        )
        st.rerun()

with right:
    if st.button("🔥 Nâng cấp lò nướng (75 xu)"):
        if st.session_state.coins >= 75:
            st.session_state.coins -= 75
            st.session_state.oven += 1
            st.session_state.message = (
                "Lò nướng đã được nâng cấp!"
            )
            st.rerun()
        else:
            st.warning("Bạn cần thêm xu để nâng cấp!")

st.caption("🐾 Pizza Meo Meo - Tiệm pizza đáng yêu nhất thế giới mèo!")
