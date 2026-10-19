import base64
import os
import time
import streamlit as st

# Cấu hình trang web Streamlit full màn hình
st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Hàm cài đặt ảnh nền vừa khít màn hình & tùy chỉnh nút tàng hình
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

    # Tùy chỉnh CSS: vừa khít màn hình (100% 100%)
    button_style = ""
    if is_start_screen:
        # Làm nút bấm tàng hình / trong suốt để đè lên nút vẽ sẵn trong ảnh
        button_style = """
        .stButton > button {
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            box-shadow: none !important;
            height: 70px !important;
            cursor: pointer !important;
        }
        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.15) !important;
            border-radius: 35px !important;
        }
        """
    else:
        # Nút bấm hiển thị cho các màn hình khác
        button_style = """
        .stButton > button {
            border-radius: 20px;
            font-weight: bold;
            font-size: 18px;
            background-color: rgba(255, 243, 224, 0.9);
            color: #8D4B38;
            border: 3px solid #FFB74D;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            padding: 10px 20px;
        }
        """

    st.markdown(
        f"""
        <style>
        .stApp {{
            {bg_css}
            background-attachment: fixed;
            background-size: 100% 100% !important;
            background-position: center;
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


# Khởi tạo các biến trạng thái game
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"
if "day" not in st.session_state:
    st.session_state.day = 3
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ==========================================
# MÀN HÌNH 1: START GAME (MÀN HÌNH CHÍNH)
# ==========================================
if st.session_state.game_state == "START":
    set_bg_and_style("bg_start", is_start_screen=True)

    # Đẩy nút tàng hình xuống đúng vị trí nút "START GAME" hồng vẽ trên ảnh
    st.markdown("<br>" * 15, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1.3, 1.2])
    with col2:
        # Nút bấm tàng hình đè lên nút vẽ trên ảnh
        if st.button("START_GAME_BTN", use_container_width=True):
            st.session_state.game_state = "PLAYING"
            st.rerun()

# ==========================================
# MÀN HÌNH 2: BẾP & LÀM BÁNH (GAMEPLAY)
# ==========================================
elif st.session_state.game_state == "PLAYING":
    set_bg_and_style("bg_play")

    # Khoảng không gian trên màn hình bếp
    st.markdown("<br>" * 12, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🔥 GIAO BÁNH & XEM TỔNG KẾT 🔥", use_container_width=True
        ):
            st.session_state.coins += 100
            st.session_state.game_state = "SUMMARY"
            st.rerun()

# ==========================================
# MÀN HÌNH 3: HẾT GIỜ RỒI! (TỔNG KẾT NGÀY)
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
                st.session_state.game_state = "PLAYING"
                st.rerun()
        with btn_col2:
            if st.button("🏠 TRANG CHỦ", use_container_width=True):
                st.session_state.game_state = "START"
                st.rerun()
