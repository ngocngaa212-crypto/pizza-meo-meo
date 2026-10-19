import base64
import os
import streamlit as st

st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def set_bg_and_style(image_base_name, is_start_screen=False):
    image_file = None
    for possible_name in [
        f"{image_base_name}.png.jpg",
        f"{image_base_name}.jpg",
        f"{image_base_name}.png",
        f"{image_base_name}.jpeg",
    ]:
        if os.path.exists(possible_name):
            image_file = possible_name
            break

    bg_css = ""
    if image_file:
        try:
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            bg_css = f'background-image: url("data:image/jpeg;base64,{encoded_string}");'
        except Exception:
            pass

    button_style = ""
    if is_start_screen:
        button_style = """
        .stButton > button {
            background: transparent !important;
            border: 2px dashed rgba(255, 152, 0, 0.6) !important;
            color: transparent !important;
            box-shadow: none !important;
            height: 52px !important;
            border-radius: 26px !important;
            cursor: pointer !important;
            margin-top: 42px !important;
            margin-left: 35px !important;
        }
        .stButton > button:hover {
            background: rgba(255, 183, 77, 0.3) !important;
            border: 2px solid #FF9800 !important;
        }
        """
    else:
        # Nút bấm trong màn hình bếp
        button_style = """
        .stButton > button {
            border-radius: 15px;
            font-weight: bold;
            font-size: 15px;
            background-color: rgba(255, 248, 225, 0.9);
            color: #8D4B38;
            border: 2px solid #FFB74D;
            box-shadow: 0px 3px 6px rgba(0,0,0,0.15);
            padding: 5px 10px;
        }
        .stButton > button:hover {
            background-color: #FFE0B2;
            color: #E65100;
        }
        """

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #FFF3E0;
            {bg_css}
            background-attachment: fixed;
            background-size: contain !important;
            background-position: center center;
            background-repeat: no-repeat;
        }}
        {button_style}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Khởi tạo dữ liệu game
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"
if "day" not in st.session_state:
    st.session_state.day = 3
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "current_pizza" not in st.session_state:
    st.session_state.current_pizza = []

# ==========================================
# MÀN HÌNH 1: START GAME
# ==========================================
if st.session_state.game_state == "START":
    set_bg_and_style("bg_start", is_start_screen=True)

    st.markdown("<br>" * 17, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1.0, 1.1])
    with col2:
        if st.button("START_GAME_BTN", use_container_width=True):
            st.session_state.game_state = "PLAYING"
            st.session_state.current_pizza = []
            st.rerun()

# ==========================================
# MÀN HÌNH 2: BẾP LÀM BÁNH
# ==========================================
elif st.session_state.game_state == "PLAYING":
    set_bg_and_style("bg_play")

    # Khoảng trống đẩy khu vực thao tác xuống bàn bếp
    st.markdown("<br>" * 11, unsafe_allow_html=True)

    # Chia cột khớp với vị trí các khay nguyên liệu trên hình
    col_de, col_banh, col_khay1, col_khay2, col_lo = st.columns(
        [1.2, 1.3, 1.2, 1.2, 1.1]
    )

    with col_de:
        st.write("🔴 **Khay bột**")
        if st.button("➕ Đặt đế bánh"):
            if "Đế bánh" not in st.session_state.current_pizza:
                st.session_state.current_pizza.append("Đế bánh")

    with col_banh:
        st.write("🍕 **Chiếc bánh đang làm:**")
        if not st.session_state.current_pizza:
            st.caption("(Chưa có nguyên liệu)")
        else:
            for item in st.session_state.current_pizza:
                st.write(f"• {item}")
        if st.button("🗑️ Làm lại"):
            st.session_state.current_pizza = []
            st.rerun()

    with col_khay1:
        st.write("🍅 **Sốt & Phô mai**")
        if st.button("➕ Sốt cà chua"):
            st.session_state.current_pizza.append("Sốt cà chua")
        if st.button("➕ Phô mai"):
            st.session_state.current_pizza.append("Phô mai")
        if st.button("➕ Nấm"):
            st.session_state.current_pizza.append("Nấm")

    with col_khay2:
        st.write("🥓 **Topping**")
        if st.button("➕ Xúc xích"):
            st.session_state.current_pizza.append("Xúc xích")
        if st.button("➕ Ớt chuông"):
            st.session_state.current_pizza.append("Ớt chuông")
        if st.button("➕ Ô liu"):
            st.session_state.current_pizza.append("Ô liu")

    with col_lo:
        st.write("🔥 **Lò nướng**")
        if st.button("🔥 Nướng & Giao bánh"):
            if len(st.session_state.current_pizza) >= 3:
                st.session_state.coins += 100
                st.session_state.game_state = "SUMMARY"
                st.rerun()
            else:
                st.warning("Cho thêm nguyên liệu vào bánh đã ní ơi!")

# ==========================================
# MÀN HÌNH 3: HẾT GIỜ RỒI!
# ==========================================
elif st.session_state.game_state == "SUMMARY":
    set_bg_and_style("bg_summary")

    st.markdown("<br>" * 16, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🌻 NGÀY MỚI", use_container_width=True):
                st.session_state.day += 1
                st.session_state.current_pizza = []
                st.session_state.game_state = "PLAYING"
                st.rerun()
        with btn_col2:
            if st.button("🏠 TRANG CHỦ", use_container_width=True):
                st.session_state.game_state = "START"
                st.rerun()
