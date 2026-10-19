import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Pizza Meo Meo 🐾",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Style ẩn toàn bộ khung thừa của Streamlit để hiển thị tràn màn hình
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
    }
    body {
        margin: 0;
        overflow: hidden;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def get_base64_image(image_base_name):
    for possible_name in [
        f"{image_base_name}.png.jpg",
        f"{image_base_name}.jpg",
        f"{image_base_name}.png",
        f"{image_base_name}.jpeg",
    ]:
        if os.path.exists(possible_name):
            try:
                with open(possible_name, "rb") as f:
                    return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
            except Exception:
                pass
    return ""


bg_start_data = get_base64_image("bg_start")
bg_play_data = get_base64_image("bg_play")
bg_summary_data = get_base64_image("bg_summary")

html_code = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    * {{
        box-sizing: border-box;
        user-select: none;
    }}
    body, html {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background-color: #333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    #game-container {{
        position: relative;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    canvas {{
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        cursor: pointer;
    }}
</style>
</head>
<body>
<div id="game-container">
    <canvas id="gameCanvas" width="1280" height="720"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Load Images
const images = {{}};
const bgStartSrc = "{bg_start_data}";
const bgPlaySrc = "{bg_play_data}";
const bgSummarySrc = "{bg_summary_data}";

if (bgStartSrc) {{ images.start = new Image(); images.start.src = bgStartSrc; }}
if (bgPlaySrc) {{ images.play = new Image(); images.play.src = bgPlaySrc; }}
if (bgSummarySrc) {{ images.summary = new Image(); images.summary.src = bgSummarySrc; }}

// Audio Context Web Audio API
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function playSound(type) {{
    if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    if (type === 'pop') {{
        osc.frequency.setValueAtTime(400, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.08);
    }} else if (type === 'bake') {{
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(300, audioCtx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    }} else if (type === 'coin') {{
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.setValueAtTime(1200, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.25);
    }}
}}

// Game State Management
let gameState = 'START'; // START, PLAY, SUMMARY
let day = 3;
let coins = 100;

// Current Pizza State
let hasCrust = false;
let hasSauce = false;
let hasCheese = false;
let toppings = []; // {{ type: 'pepperoni'|'mushroom'|'pepper'|'olive', x: number, y: number }}
let selectedTool = null; // 'crust', 'sauce', 'cheese', 'pepperoni', 'mushroom', 'pepper', 'olive'

// Topping Tray Definitions (Responsive Coords)
const trays = [
    {{ id: 'crust', name: 'Đế bánh', x: 250, y: 440, w: 120, h: 180, color: '#D7CCC8' }},
    {{ id: 'sauce', name: 'Sốt cà', x: 650, y: 430, w: 90, h: 80, color: '#EF5350' }},
    {{ id: 'cheese', name: 'Phô mai', x: 750, y: 430, w: 90, h: 80, color: '#FFEE58' }},
    {{ id: 'pepperoni', name: 'Xúc xích', x: 850, y: 430, w: 90, h: 80, color: '#D32F2F' }},
    {{ id: 'mushroom', name: 'Nấm', x: 650, y: 520, w: 90, h: 80, color: '#8D6E63' }},
    {{ id: 'pepper', name: 'Ớt chuông', x: 750, y: 520, w: 90, h: 80, color: '#66BB6A' }},
    {{ id: 'olive', name: 'Ô liu', x: 850, y: 520, w: 90, h: 80, color: '#424242' }}
];

// Oven Area
const ovenArea = {{ x: 1040, y: 380, w: 200, h: 250 }};

// Pizza Area on Board
const pizzaCenter = {{ x: 495, y: 535, r: 130 }};

// Order Criteria
const currentOrder = {{
    customer: "Miu Cam",
    sauce: true,
    cheese: true,
    pepperoni: 5,
    mushroom: 3,
    pepper: 2
}};

// Event Listeners
canvas.addEventListener('click', function(e) {{
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    if (gameState === 'START') {{
        // Start Game Button Area (Fit exactly on button)
        if (x >= 400 && x <= 880 && y >= 450 && y <= 550) {{
            playSound('pop');
            gameState = 'PLAY';
            resetPizza();
        }}
    }} else if (gameState === 'PLAY') {{
        // Check Trays Selection
        let clickedTray = false;
        trays.forEach(tray => {{
            if (x >= tray.x && x <= tray.x + tray.w && y >= tray.y && y <= tray.y + tray.h) {{
                selectedTool = tray.id;
                playSound('pop');
                clickedTray = true;
                
                // Direct Crust Application
                if (tray.id === 'crust') {{
                    hasCrust = true;
                }}
            }}
        }});

        // Click on Oven -> Finish & Bake
        if (x >= ovenArea.x && x <= ovenArea.x + ovenArea.w && y >= ovenArea.y && y <= ovenArea.y + ovenArea.h) {{
            if (hasCrust) {{
                playSound('bake');
                setTimeout(() => playSound('coin'), 300);
                coins += 100;
                gameState = 'SUMMARY';
            }}
            return;
        }}

        // Click on Pizza Area to Place Topping
        if (!clickedTray) {{
            const dist = Math.hypot(x - pizzaCenter.x, y - pizzaCenter.y);
            if (dist <= pizzaCenter.r) {{
                if (!hasCrust) {{
                    hasCrust = true;
                    playSound('pop');
                }} else if (selectedTool === 'sauce') {{
                    hasSauce = true;
                    playSound('pop');
                }} else if (selectedTool === 'cheese') {{
                    hasCheese = true;
                    playSound('pop');
                }} else if (['pepperoni', 'mushroom', 'pepper', 'olive'].includes(selectedTool)) {{
                    toppings.push({{ type: selectedTool, x: x, y: y }});
                    playSound('pop');
                }}
            }}
        }}
    }} else if (gameState === 'SUMMARY') {{
        // Next Day Button
        if (x >= 400 && x <= 620 && y >= 480 && y <= 560) {{
            playSound('pop');
            day += 1;
            gameState = 'PLAY';
            resetPizza();
        }}
        // Home Button
        if (x >= 660 && x <= 880 && y >= 480 && y <= 560) {{
            playSound('pop');
            gameState = 'START';
        }}
    }}
}});

function resetPizza() {{
    hasCrust = false;
    hasSauce = false;
    hasCheese = false;
    toppings = [];
    selectedTool = null;
}}

// Render Loop
function render() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'START') {{
        if (images.start && images.start.complete) {{
            ctx.drawImage(images.start, 0, 0, canvas.width, canvas.height);
        }} else {{
            ctx.fillStyle = '#FFF3E0';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#8D4B38';
            ctx.font = 'bold 48px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Tiệm Pizza Của Những Chú Mèo 🐾', canvas.width/2, 250);
            
            ctx.fillStyle = '#FFB74D';
            ctx.beginPath();
            ctx.roundRect(440, 450, 400, 80, 40);
            ctx.fill();
            ctx.fillStyle = '#FFF';
            ctx.fillText('START GAME', canvas.width/2, 505);
        }}
    }} else if (gameState === 'PLAY') {{
        if (images.play && images.play.complete) {{
            ctx.drawImage(images.play, 0, 0, canvas.width, canvas.height);
        }} else {{
            ctx.fillStyle = '#FFE0B2';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }}

        // Draw Interactive Pizza
        if (hasCrust) {{
            ctx.save();
            ctx.fillStyle = '#E5A967';
            ctx.beginPath();
            ctx.arc(pizzaCenter.x, pizzaCenter.y, pizzaCenter.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.lineWidth = 10;
            ctx.strokeStyle = '#C68642';
            ctx.stroke();

            // Inner Dough
            ctx.fillStyle = '#F5D6A7';
            ctx.beginPath();
            ctx.arc(pizzaCenter.x, pizzaCenter.y, pizzaCenter.r - 12, 0, Math.PI * 2);
            ctx.fill();

            // Sauce
            if (hasSauce) {{
                ctx.fillStyle = '#D32F2F';
                ctx.beginPath();
                ctx.arc(pizzaCenter.x, pizzaCenter.y, pizzaCenter.r - 22, 0, Math.PI * 2);
                ctx.fill();
            }}

            // Cheese
            if (hasCheese) {{
                ctx.fillStyle = '#FFF176';
                ctx.beginPath();
                ctx.arc(pizzaCenter.x, pizzaCenter.y, pizzaCenter.r - 28, 0, Math.PI * 2);
                ctx.fill();
            }}

            // Toppings
            toppings.forEach(top => {{
                ctx.beginPath();
                if (top.type === 'pepperoni') {{
                    ctx.fillStyle = '#B71C1C';
                    ctx.arc(top.x, top.y, 14, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#D32F2F';
                    ctx.arc(top.x - 2, top.y - 2, 10, 0, Math.PI * 2);
                    ctx.fill();
                }} else if (top.type === 'mushroom') {{
                    ctx.fillStyle = '#795548';
                    ctx.arc(top.x, top.y, 10, 0, Math.PI * 2);
                    ctx.fill();
                }} else if (top.type === 'pepper') {{
                    ctx.fillStyle = '#388E3C';
                    ctx.rect(top.x - 8, top.y - 8, 16, 8);
                    ctx.fill();
                }} else if (top.type === 'olive') {{
                    ctx.fillStyle = '#212121';
                    ctx.arc(top.x, top.y, 8, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }});
            ctx.restore();
        }}

        // Highlight Selected Tray
        if (selectedTool) {{
            const activeTray = trays.find(t => t.id === selectedTool);
            if (activeTray) {{
                ctx.strokeStyle = '#FF9800';
                ctx.lineWidth = 4;
                ctx.strokeRect(activeTray.x - 2, activeTray.y - 2, activeTray.w + 4, activeTray.h + 4);
            }}
        }}

    }} else if (gameState === 'SUMMARY') {{
        if (images.summary && images.summary.complete) {{
            ctx.drawImage(images.summary, 0, 0, canvas.width, canvas.height);
        }} else {{
            ctx.fillStyle = '#FFF3E0';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#8D4B38';
            ctx.font = 'bold 42px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('HẾT NGÀY LÀM VIỆC! 🐾', canvas.width/2, 250);
            ctx.fillText(`Tổng doanh thu: ${{coins}} Xu`, canvas.width/2, 330);
        }}
    }}

    requestAnimationFrame(render);
}}

render();
</script>
</body>
</html>
"""

components.html(html_code, height=720, scrolling=False)
