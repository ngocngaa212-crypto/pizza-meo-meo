import random
import html
import streamlit as st

st.set_page_config(
    page_title="Pizza Meo Meo",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. DU LIEU GAME
# ==========================================

TOPPINGS = {
    "Xúc xích": "#c84c42",
    "Nấm": "#e7d7b9",
    "Ớt chuông": "#56a66b",
    "Thịt xông khói": "#bd6756",
    "Ô liu": "#49403c",
}

CAT_NAMES = [
    ("Miu Cam", "🐈"),
    ("Mun Mun", "🐈‍⬛"),
    ("Bánh Bao", "😺"),
    ("Bông Gòn", "😻"),
    ("Đốm Sữa", "🐱"),
]

BASE_PRICE = 50
CUSTOMERS_PER_DAY = 4

def new_order():
    name, face = random.choice(CAT_NAMES)
    wanted = random.sample(
        list(TOPPINGS.keys()),
        random.randint(1, 3)
    )
    return {
        "name": name,
        "face": face,
        "wanted": wanted,
        "price": BASE_PRICE + 10 * len(wanted),
    }

def start_day():
    st.session_state.phase = "game"
    st.session_state.day += 1
    st.session_state.daily_revenue = 0
    st.session_state.served = 0
    st.session_state.correct = 0
    st.session_state.reviews = []
    st.session_state.order = new_order()
    st.session_state.pizza = []
    st.session_state.baked = False

def init_state():
    defaults = {
        "phase": "start",
        "day": 0,
        "coins": 100,
        "daily_revenue": 0,
        "served": 0,
        "correct": 0,
        "reviews": [],
        "order": None,
        "pizza": [],
        "baked": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ==========================================
# 2. DO HOA SVG
# ==========================================

def pizza_svg(toppings=None, baked=False):
    """Ve banh pizza va topping da chon."""
    toppings = toppings or []

    # Cac vi tri topping tren mat banh
    positions = [
        (100, 57), (143, 77), (160, 119),
        (139, 158), (96, 165), (62, 139),
        (55, 98), (105, 105), (119, 130),
        (79, 120), (133, 99), (92, 78),
        (111, 145), (72, 82), (151, 139),
    ]

    pieces = []

    for index, item in enumerate(toppings):
        x, y = positions[index % len(positions)]

        if item == "Xúc xích":
            pieces.append(
                f'<ellipse cx="{x}" cy="{y}" rx="10" ry="7" '
                'transform="rotate(-25 '
                f'{x} {y})" fill="#bd5145" '
                'stroke="#8d332b" stroke-width="2"/>'
            )
            pieces.append(
                f'<ellipse cx="{x-2}" cy="{y-1}" rx="5" ry="2" '
                'fill="#ef9b78" opacity=".8"/>'
            )

        elif item == "Nấm":
            pieces.append(
                f'<path d="M{x-10} {y+2} '
                f'Q{x-11} {y-10} {x} {y-9} '
                f'Q{x+11} {y-10} {x+10} {y+2} Z" '
                'fill="#e5d5b5" stroke="#a58a69" stroke-width="2"/>'
            )
            pieces.append(
                f'<rect x="{x-4}" y="{y}" width="8" height="8" '
                'rx="2" fill="#c5a984"/>'
            )

        elif item == "Ớt chuông":
            pieces.append(
                f'<path d="M{x-8} {y-5} '
                f'Q{x-14} {y+2} {x-4} {y+8} '
                f'L{x+5} {y+6} Q{x+12} {y-2} {x+5} {y-7} Z" '
                'fill="#4c9b59" stroke="#28723b" stroke-width="2"/>'
            )

        elif item == "Thịt xông khói":
            pieces.append(
                f'<path d="M{x-10} {y-6} '
                f'Q{x-3} {y-11} {x} {y-3} '
                f'T{x+10} {y+5} L{x+7} {y+9} '
                f'Q{x} {y+2} {x-10} {y-6} Z" '
                'fill="#bd6756" stroke="#8d4136" stroke-width="2"/>'
            )

        elif item == "Ô liu":
            pieces.append(
                f'<ellipse cx="{x}" cy="{y}" rx="7" ry="8" '
                'fill="#403735"/>'
            )
            pieces.append(
                f'<ellipse cx="{x}" cy="{y}" rx="3" ry="4" '
                'fill="#f3d8a2"/>'
            )

    cheese = ""
    if not baked:
        cheese = (
            '<circle cx="105" cy="112" r="74" '
            'fill="#ffdc7e" opacity=".38"/>'
        )
    else:
        cheese = (
            '<circle cx="105" cy="112" r="73" '
            'fill="#d99a42" opacity=".20"/>'
        )

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 210 210" width="100%">
      <defs>
        <radialGradient id="crust">
          <stop offset="75%" stop-color="#f8d18b"/>
          <stop offset="100%" stop-color="#bd7b3d"/>
        </radialGradient>
        <radialGradient id="sauce">
          <stop offset="0%" stop-color="#ed6a4e"/>
          <stop offset="100%" stop-color="#c94335"/>
        </radialGradient>
      </defs>
      <ellipse cx="105" cy="110" rx="100" ry="98"
               fill="#d6b89c" opacity=".25"/>
      <circle cx="105" cy="105" r="96" fill="url(#crust)"/>
      <circle cx="105" cy="105" r="82" fill="url(#sauce)"/>
      {cheese}
      <circle cx="105" cy="105" r="73"
              fill="#ffdd84" stroke="#e6ad4e" stroke-width="2"/>
      {''.join(pieces)}
      <circle cx="105" cy="105" r="96" fill="none"
              stroke="#a96c39" stroke-width="3"/>
    </svg>
    """

def ingredient_svg(name):
    """Minh hoa rieng tung khay nguyen lieu."""
    common_start = """
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 120 82" width="100%">
      <rect x="4" y="7" width="112" height="68" rx="13"
            fill="#f5dfc4" stroke="#d6b28b" stroke-width="3"/>
    """
    art = ""

    if name == "Bột nhào":
        art = """
        <ellipse cx="60" cy="46" rx="31" ry="19"
                 fill="#d8b17c"/>
        <ellipse cx="60" cy="41" rx="31" ry="19"
                 fill="#f7dca6" stroke="#d2a66c" stroke-width="3"/>
        <path d="M39 40 Q60 29 81 41"
              fill="none" stroke="#fff0c9" stroke-width="3"/>
        """

    elif name == "Đế bánh":
        art = """
        <circle cx="60" cy="41" r="30"
                fill="#c58a4f"/>
        <circle cx="60" cy="41" r="23"
                fill="#f8dca1"/>
        <circle cx="60" cy="41" r="30"
                fill="none" stroke="#a66d39" stroke-width="3"/>
        """

    elif name == "Sốt cà chua":
        art = """
        <path d="M32 26 L87 26 L82 58 Q60 70 37 58 Z"
              fill="#d9dce0" stroke="#939da6" stroke-width="3"/>
        <ellipse cx="60" cy="27" rx="28" ry="8"
                 fill="#ef6b4d" stroke="#bd4536" stroke-width="3"/>
        <path d="M40 42 Q60 54 80 42"
              fill="none" stroke="#ff9b75" stroke-width="4"/>
        """

    elif name == "Phô mai":
        art = """
        <path d="M30 55 L35 25 L63 38 L85 24 L91 55 Z"
              fill="#ffdc6c" stroke="#d4a83f" stroke-width="3"/>
        <circle cx="49" cy="45" r="4" fill="#fff0a7"/>
        <circle cx="73" cy="48" r="4" fill="#fff0a7"/>
        """

    elif name == "Xúc xích":
        art = """
        <ellipse cx="43" cy="42" rx="13" ry="9"
                 fill="#bd5145" transform="rotate(-25 43 42)"/>
        <ellipse cx="72" cy="39" rx="13" ry="9"
                 fill="#d05b49" transform="rotate(25 72 39)"/>
        <path d="M37 39 L47 45 M67 36 L77 42"
              stroke="#f6ad89" stroke-width="3"/>
        """

    elif name == "Nấm":
        art = """
        <path d="M31 43 Q30 20 47 23 Q62 22 62 43 Z"
              fill="#c4a27b" stroke="#927352" stroke-width="3"/>
        <rect x="42" y="42" width="10" height="17" rx="4"
              fill="#f5e5c9"/>
        <path d="M62 47 Q62 29 79 29 Q95 29 95 47 Z"
              fill="#d7bd99" stroke="#a58a69" stroke-width="3"/>
        <rect x="74" y="46" width="10" height="12" rx="3"
              fill="#f5e5c9"/>
        """

    elif name == "Ớt chuông":
        art = """
        <path d="M33 30 Q43 22 51 31 Q60 22 68 31
                 Q81 26 84 39 L77 57 Q60 66 43 57 Z"
              fill="#56a66b" stroke="#327947" stroke-width="3"/>
        <path d="M59 27 L60 37"
              stroke="#327947" stroke-width="4"/>
        """

    elif name == "Thịt xông khói":
        art = """
        <path d="M28 29 Q38 21 46 32 T64 32 T83 32 L91 42
                 Q82 51 73 42 T55 42 T37 42 Z"
              fill="#bd6756" stroke="#904538" stroke-width="3"/>
        <path d="M34 31 Q44 38 49 33 T67 34 T85 35"
              fill="none" stroke="#ffd3aa" stroke-width="4"/>
        """

    elif name == "Ô liu":
        art = """
        <ellipse cx="43" cy="40" rx="11" ry="14"
                 fill="#45403c"/>
        <ellipse cx="70" cy="34" rx="11" ry="14"
                 fill="#45403c"/>
        <ellipse cx="79" cy="52" rx="10" ry="12"
                 fill="#45403c"/>
        <circle cx="43" cy="40" r="4" fill="#f4dfb4"/>
        <circle cx="70" cy="34" r="4" fill="#f4dfb4"/>
        <circle cx="79" cy="52" r="3" fill="#f4dfb4"/>
        """

    return common_start + art + "</svg>"

def oven_svg():
    return """
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 220 220" width="100%">
      <rect x="20" y="25" width="180" height="170" rx="20"
            fill="#e5a47c" stroke="#a85e43" stroke-width="6"/>
      <rect x="36" y="60" width="148" height="105" rx="12"
            fill="#783f37" stroke="#a85e43" stroke-width="5"/>
      <path d="M60 144 Q45 125 63 103 Q65 87 79 78
               Q74 106 93 109 Q104 91 99 76
               Q130 99 125 124 Q151 102 146 90
               Q175 127 148 145 Z"
            fill="#ffb74d"/>
      <path d="M83 145 Q72 127 93 113 Q90 132 108 139
               Q121 124 119 113 Q144 135 125 145 Z"
            fill="#ffe28a"/>
      <circle cx="65" cy="43" r="5" fill="#fff0cf"/>
      <circle cx="83" cy="43" r="5" fill="#fff0cf"/>
      <rect x="118" y="36" width="55" height="14" rx="7"
            fill="#fff0cf"/>
    </svg>
    """

# ==========================================
# 3. GIAO DIEN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #fff6eb;
    color: #51372e;
}
.block-container {
    max-width: 1200px;
    padding-top: 1.4rem;
}
h1, h2, h3 {
    color: #a64f3c;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 43px;
    background: #ffe0cd;
    border: 1px solid #e6b89f;
    color: #713d32;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #ffc9ae;
    border-color: #d9977a;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. MAN HINH BAT DAU
# ==========================================

if st.session_state.phase == "start":

    st.markdown("""
    <div style="
        text-align:center;
        background:linear-gradient(135deg,#ffe3d2,#fff0ca);
        border:3px solid #efc3a8;
        border-radius:28px;
        padding:35px 15px;">
        <div style="font-size:28px;color:#9e523b">
            WELCOME TO
        </div>
        <h1 style="font-size:48px;margin:5px 0">
            PIZZA MEO MEO
        </h1>
        <p style="font-size:20px">
            Tiệm pizza nhỏ giữa thế giới mèo
        </p>
        <div style="font-size:20px">
            🍕 Làm bánh · Phục vụ khách · Kiếm xu
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown(pizza_svg(),unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("START GAME", use_container_width=True):
            start_day()
            st.rerun()

# ==========================================
# 5. MAN HINH CHOI GAME
# ==========================================

elif st.session_state.phase == "game":

    st.title("Pizza Meo Meo")
    st.caption(f"Ngày {st.session_state.day} · Tiệm bánh của thế giới mèo")

    a, b, c, d = st.columns(4)
    a.metric("Tổng xu", st.session_state.coins)
    b.metric("Doanh thu hôm nay", st.session_state.daily_revenue)
    c.metric("Khách đã phục vụ",
             f"{st.session_state.served}/{CUSTOMERS_PER_DAY}")
    d.metric("Đơn hoàn hảo", st.session_state.correct)

    st.progress(st.session_state.served / CUSTOMERS_PER_DAY)

    st.divider()
    st.subheader("Khách hàng đang chờ")

    customer_cols = st.columns(4)
    faces = ["🐈", "🐈‍⬛", "😺", "😸"]

    for i, col in enumerate(customer_cols):
        with col:
            if i == 0 and st.session_state.order:
                order = st.session_state.order
                st.markdown(
                    f"<div style='text-align:center;"
                    f"background:#fff0dc;border:2px solid #e4bda1;"
                    f"border-radius:15px;padding:12px'>"
                    f"<div style='font-size:42px'>{order['face']}</div>"
                    f"<b>{html.escape(order['name'])}</b>"
                    f"<p>Đang gọi món!</p></div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:center;"
                    f"background:#fffaf2;border:2px solid #eed8c3;"
                    f"border-radius:15px;padding:12px'>"
                    f"<div style='font-size:42px'>{faces[i]}</div>"
                    f"<p>Đang chờ...</p></div>",
                    unsafe_allow_html=True
                )

    st.write("")

    if st.session_state.order is None:
        st.info("Hãy mời khách tiếp theo vào tiệm!")
        if st.session_state.served < CUSTOMERS_PER_DAY:
            if st.button("Mời khách tiếp theo"):
                st.session_state.order = new_order()
                st.session_state.pizza = []
                st.session_state.baked = False
                st.rerun()

    else:
        order = st.session_state.order
        wanted = order["wanted"]

        left, middle, right = st.columns([1, 1.4, 1])

        # DON HANG
        with left:
            st.subheader("Đơn hàng")
            st.markdown(
                f"*{html.escape(order['name'])} nói:*  \n"
                '"Cho tôi một chiếc pizza có:"'
            )
            st.write("Đế bánh + sốt cà chua + phô mai")
            for item in wanted:
                st.write(f"• {item}")

            st.info(f"Giá tối đa: {order['price']} xu")

        # BANH PIZZA
        with middle:
            st.subheader("Bàn làm bánh")

            st.markdown(
                pizza_svg(
                    st.session_state.pizza,
                    st.session_state.baked
                ),
                unsafe_allow_html=True
            )

            if st.session_state.pizza:
                st.caption(
                    "Topping: " + ", ".join(st.session_state.pizza)
                )
            else:
                st.caption("Bánh đang chờ nguyên liệu.")

            if st.button(
                "Làm lại bánh",
                use_container_width=True,
                disabled=st.session_state.baked
            ):
                st.session_state.pizza = []
                st.rerun()

        # LO NUONG
        with right:
            st.subheader("Lò nướng")

            st.markdown(oven_svg(), unsafe_allow_html=True)

            if st.session_state.baked:
                st.success("Bánh đã chín!")

            if st.button(
                "NƯỚNG PIZZA",
                use_container_width=True,
                disabled=st.session_state.baked
            ):
                st.session_state.baked = True
                st.rerun()

            if st.button(
                "GIAO PIZZA",
                use_container_width=True,
                disabled=not st.session_state.baked
            ):
                base_price = order["price"]
                made = set(st.session_state.pizza)
                expected = set(wanted)

                missing = expected - made
                extra = made - expected

                score = max(
                    0,
                    100 - 25 * len(missing) - 12 * len(extra)
                )
                payment = round(base_price * score / 100)

                if score == 100:
                    review = "⭐⭐⭐⭐⭐ Tuyệt vời! Đúng món tôi muốn!"
                    st.session_state.correct += 1
                elif score >= 70:
                    review = "⭐⭐⭐⭐ Khá ngon, nhưng chưa hoàn hảo."
                elif score >= 40:
                    review = "⭐⭐⭐ Lần sau hãy xem kỹ đơn hàng."
                else:
                    review = "⭐⭐ Pizza chưa đúng ý khách."

                st.session_state.coins += payment
                st.session_state.daily_revenue += payment
                st.session_state.served += 1

                st.session_state.reviews.append({
                    "name": order["name"],
                    "payment": payment,
                    "score": score,
                    "review": review
                })

                st.session_state.order = None
                st.session_state.pizza = []
                st.session_state.baked = False

                if st.session_state.served >= CUSTOMERS_PER_DAY:
                    st.session_state.phase = "summary"

                st.rerun()

        # KHAY NGUYEN LIEU
        st.divider()
        st.subheader("Khay nguyên liệu")

        tray_names = [
            "Bột nhào",
            "Đế bánh",
            "Sốt cà chua",
            "Phô mai",
            *TOPPINGS.keys()
        ]

        cols = st.columns(4)

        for i, item in enumerate(tray_names):
            with cols[i % 4]:
                st.markdown(
                    ingredient_svg(item),
                    unsafe_allow_html=True
                )
                st.caption(item)

                if item == "Bột nhào":
                    st.button(
                        "Bột nhào",
                        key="dough",
                        disabled=True,
                        use_container_width=True
                    )
                elif item == "Đế bánh":
                    st.button(
                        "Đế bánh",
                        key="base",
                        disabled=True,
                        use_container_width=True
                    )
                elif item == "Sốt cà chua":
                    st.button(
                        "Thêm sốt",
                        key="sauce",
                        disabled=True,
                        use_container_width=True
                    )
                elif item == "Phô mai":
                    st.button(
                        "Thêm phô mai",
                        key="cheese",
                        disabled=True,
                        use_container_width=True
                    )
                else:
                    already = item in st.session_state.pizza

                    if st.button(
                        "Đã thêm" if already else f"Thêm {item}",
                        key=f"add_{item}",
                        disabled=(
                            already or st.session_state.baked
                        ),
                        use_container_width=True
                    ):
                        st.session_state.pizza.append(item)
                        st.rerun()

        st.caption(
            "Bản thử nghiệm: đế bánh, sốt và phô mai được tính là "
            "phần nền mặc định; các topping được chọn tại khay."
        )

    st.divider()

    if st.button("Kết thúc ngày"):
        st.session_state.phase = "summary"
        st.session_state.order = None
        st.session_state.pizza = []
        st.session_state.baked = False
        st.rerun()

# ==========================================
# 6. TONG KET CUOI NGAY
# ==========================================

elif st.session_state.phase == "summary":

    st.title("🌙 Hết giờ rồi!")
    st.subheader(f"Tổng kết ngày {st.session_state.day}")

    a, b, c = st.columns(3)
    a.metric("Doanh thu", f"{st.session_state.daily_revenue} xu")
    b.metric("Khách phục vụ", st.session_state.served)
    c.metric("Đơn hoàn hảo", st.session_state.correct)

    st.divider()
    st.subheader("Đánh giá của khách")

    if not st.session_state.reviews:
        st.info("Hôm nay chưa có đánh giá.")
    else:
        for r in st.session_state.reviews:
            with st.container(border=True):
                st.write(f"**🐱 {r['name']}**")
                st.write(r["review"])
                st.caption(
                    f"Độ chính xác: {r['score']}% · "
                    f"Tiền nhận: {r['payment']} xu"
                )

    if st.session_state.served:
        ratio = st.session_state.correct / st.session_state.served

        if ratio >= 0.75:
            st.success("Tiệm mèo của bạn được yêu thích!")
        elif ratio >= 0.4:
            st.info("Khá tốt! Hãy tiếp tục cố gắng nhé.")
        else:
            st.warning("Ngày mai hãy đọc kỹ đơn hàng hơn!")

    st.divider()

    if st.button("BẮT ĐẦU NGÀY MỚI", use_container_width=True):
        start_day()
        st.rerun()

    if st.button("Về màn hình chính", use_container_width=True):
        st.session_state.phase = "start"
        st.rerun()

st.markdown("---")
st.caption("Pizza Meo Meo · Tiệm bánh nhỏ của thế giới mèo")
