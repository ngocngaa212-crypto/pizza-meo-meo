import base64
import os
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


# Hàm đọc và cài đặt ảnh nền tự động cho Streamlit
def set_bg_image(image_base_name):
    image_file = None
    # Tìm kiếm các tên file ảnh thực tế trên GitHub
    for possible_name in [
        f"{image_base_name}.png.jpg",
        f"{image_base_name}.jpg",
        f"{image_base_name}.png",
        f"{image_base_name}.jpeg",
    ]:
        if os.path.exists(possible_name):
            image_file = possible_name
            break

    if image_file:
        try:
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{encoded_string}");
                    background-attachment: fixed;
                    background-size: cover;
                    background-position: center;
                }}
                /* CSS tùy chỉnh cho các nút bấm đẹp mắt & nổi bật */
                .stButton>button {{
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 18px;
                    background-color: #FFF3E0;
                    color: #8D4B38;
                    border: 3px solid #FFB74D;
                    box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
                    padding: 10px 20px;
                }}
                .stButton>button:hover {{
                    background-color: #FFE0B2;
                    border-color: #E65100;
                    color: #E65100;
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


# Khởi tạo các biến trạng thái game (Session State)
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
    set_bg_image("bg_start")

    # Tạo khoảng trống đẩy nút START GAME xuống đúng vị trí trên hình nền
    st.markdown("<br>" * 14, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🐾 START GAME 🐾", use_container_width=True):
            st.session_state.game_state = "PLAYING"
            st.rerun()

# ==========================================
# MÀN HÌNH 2: BẾP & LÀM BÁNH (GAMEPLAY)
# ==========================================
elif st.session_state.game_state == "PLAYING":
    set_bg_image("bg_play")

    # Thanh thông tin trên cùng
    st.markdown(
        f"""
        <div style="background: rgba(255, 248, 225, 0.9); padding: 12px 20px; border-radius: 15px; border: 2px solid #FFB74D; margin-bottom: 20px; display: flex; justify-content: space-between; font-size: 16px;">
            <b>📅 Ngày {st.session_state.day} - 12:45</b>
            <b>😊 88% Hài lòng</b>
            <b>🪙 {st.session_state.coins} xu</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_order, col_kitchen = st.columns([1, 2])

    with col_order:
        st.markdown(
            """
            <div style="background: rgba(255, 248, 225, 0.95); padding: 18px; border-radius: 18px; border: 3px dashed #FFB74D;">
                <h4 style="color: #8D4B38; margin-top: 0;">📋 Đơn hàng hiện tại</h4>
                <p><b>🐱 Miu Cam:</b> Pizza Đế mỏng + Sốt cà chua + Phô mai + Xúc xích</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_kitchen:
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 18px; text-align: center; border: 2px solid #FFB74D;">
                <h4 style="color: #8D4B38; margin: 0;">🧑‍🍳 Bếp đang nướng bánh...</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🔥 Đưa vào Lò Nướng & Giao Bánh 🔥", use_container_width=True
        ):
            st.success("🎉 Đã hoàn thành đơn hàng cho Miu Cam! (+100 xu)")
            st.session_state.coins += 100
            time.sleep(1)
            st.session_state.game_state = "SUMMARY"
            st.rerun()

# ==========================================
# MÀN HÌNH 3: HẾT GIỜ RỒI! (TỔNG KẾT NGÀY)
# ==========================================
elif st.session_state.game_state == "SUMMARY":
    set_bg_image("bg_summary")

    # Tạo khoảng trống căn chỉnh các nút bấm
    st.markdown("<br>" * 12, unsafe_allow_html=True)

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
