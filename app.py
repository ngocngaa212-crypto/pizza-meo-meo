import base64
import os
import random
import time
import streamlit as st

st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Hàm tự động đọc file ảnh nền (hỗ trợ png/jpg)
def set_bg_image(image_base_name):
    image_file = None
    for ext in [".png", ".jpg", ".jpeg"]:
        if os.path.exists(image_base_name + ext):
            image_file = image_base_name + ext
            break

    if image_file:
        try:
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{encoded_string}");
                    background-attachment: fixed;
                    background-size: cover;
                    background-position: center;
                }}
                .stButton>button {{
                    border-radius: 15px;
                    font-weight: bold;
                    background-color: #FFF3E0;
                    color: #8D4B38;
                    border: 2px solid #FFB74D;
                }}
                #MainMenu {{visibility: hidden;}}
                footer {{visibility: hidden;}}
                header {{visibility: hidden;}}
                </style>
                """,
                unsafe_allow_html=True,
            )
        except Exception:
            pass


# Khởi tạo trạng thái
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"
if "day" not in st.session_state:
    st.session_state.day = 3
if "coins" not in st.session_state:
    st.session_state.coins = 100

# ==========================================
# MÀN HÌNH 1: START GAME
# ==========================================
if st.session_state.game_state == "START":
    set_bg_image("bg_start")

    st.markdown("<br>" * 12, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🐾 START GAME 🐾", use_container_width=True):
            st.session_state.game_state = "PLAYING"
            st.rerun()

# ==========================================
# MÀN HÌNH 2: BẾP & LÀM BÁNH
# ==========================================
elif st.session_state.game_state == "PLAYING":
    set_bg_image("bg_play")

    st.markdown(
        f"""
        <div style="background: rgba(255, 248, 225, 0.85); padding: 10px; border-radius: 15px; margin-bottom: 20px;">
            <b>📅 Ngày {st.session_state.day} - 12:45</b> | 
            <b>😊 88% Hài lòng</b> | 
            <b>🪙 {st.session_state.coins} xu</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_order, col_kitchen = st.columns([1, 2])

    with col_order:
        st.markdown(
            """
            <div style="background: rgba(255, 248, 225, 0.9); padding: 15px; border-radius: 15px; border: 2px dashed #FFB74D;">
                <h4>📋 Đơn hàng hiện tại</h4>
                <p><b>🐱 Miu Cam:</b> Pizza Đế mỏng + Sốt cà chua + Phô mai + Xúc xích</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_kitchen:
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.85); padding: 15px; border-radius: 15px; text-align: center;">
                <h4>🧑‍🍳 Bếp đang chuẩn bị bánh...</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔥 Đưa vào Lò Nướng & Giao Bánh 🔥", use_container_width=True):
            st.success("Đã giao bánh cho Miu Cam! (+100 xu)")
            st.session_state.coins += 100
            time.sleep(1)
            st.session_state.game_state = "SUMMARY"
            st.rerun()

# ==========================================
# MÀN HÌNH 3: HẾT GIỜ RỒI!
# ==========================================
elif st.session_state.game_state == "SUMMARY":
    set_bg_image("bg_summary")

    st.markdown("<br>" * 10, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌻 BẮT ĐẦU NGÀY MỚI", use_container_width=True):
            st.session_state.day += 1
            st.session_state.game_state = "PLAYING"
            st.rerun()

    with col2:
        if st.button("🏠 Về màn hình chính", use_container_width=True):
            st.session_state.game_state = "START"
            st.rerun()
