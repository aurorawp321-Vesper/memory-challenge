import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="极简记忆挑战", layout="centered")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { background-color: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }
        .header { margin-bottom: 30px; text-align: center; }
        .timer { font-size: 32px; color: #D4AF37; font-variant-numeric: tabular-nums; letter-spacing: 2px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; width: 90vw; max-width: 400px; }
        .card { height: 85px; background: #1a1a1a; border: 1px solid #333; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 36px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; }
        .card.flipped { transform: rotateY(180deg); background: #262626; border-color: #D4AF37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }
        .card.matched { background: #D4AF37; color: #000; border-color: #D4AF37; animation: match-pulse 0.5s forwards; cursor: default; }
        @keyframes match-pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 0.8; } }
        .success-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); flex-direction: column; align-items: center; justify-content: center; z-index: 100; }
        .success-title { color: #D4AF37; font-size: 40px; margin: 0; letter-spacing: 4px; }
        .btn { background: none; border: 1px solid #D4AF37; color: #D4AF37; padding: 12px 40px; margin-top: 30px; cursor: pointer; transition: 0.3s; font-size: 16px; }
        .btn:hover { background: #D4AF37; color: #000; }
    </style>
</head>
<body>
    <div class="header"><div class="timer" id="timer">00.00s</div></div>
    <div class="grid" id="grid"></div>
    <div class="success-overlay" id="success">
        <h1 class="success-title">挑战成功</h1>
        <p id="final-time" style="color: #888; margin-top: 15px;"></p>
        <button class="btn" onclick="initGame()">重新挑战</button>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        const symbols = ['◈', '▣', '◬', '○', '★', '✚', '✧', '♠', '◈', '▣', '◬', '○', '★', '✚', '✧', '♠'];
        let cards = []; let flipped = []; let matched = 0; let startTime = null; let timer = null;
        function initGame() {
            const grid = document.getElementById('grid'); grid.innerHTML = '';
            document.getElementById('success').style.display = 'none';
            cards = [...symbols].sort(() => Math.random() - 0.5);
            flipped = []; matched = 0; startTime = Date.now();
            clearInterval(timer);
            timer = setInterval(() => { document.getElementById('timer').innerText = ((Date.now() - startTime)/1000).toFixed(2) + 's'; }, 50);
            cards.forEach((s, i) => {
                const c = document.createElement('div'); c.className = 'card'; c.dataset.s = s;
                c.onclick = () => {
                    if (flipped.length < 2 && !c.classList.contains('flipped') && !c.classList.contains('matched')) {
                        c.classList.add('flipped'); c.innerText = s; flipped.push(c);
                        if (flipped.length === 2) setTimeout(check, 500);
                    }
                };
                grid.appendChild(c);
            });
        }
        function check() {
            const [a, b] = flipped;
            if (a.dataset.s === b.dataset.s) {
                a.classList.add('matched'); b.classList.add('matched'); matched += 2;
                if (matched === 16) {
                    clearInterval(timer); document.getElementById('success').style.display = 'flex';
                    document.getElementById('final-time').innerText = "结算用时: " + document.getElementById('timer').innerText;
                    confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 }, colors: ['#D4AF37', '#ffffff'] });
                }
            } else { a.classList.remove('flipped'); a.innerText = ''; b.classList.remove('flipped'); b.innerText = ''; }
            flipped = [];
        }
        initGame();
    </script>
</body>
</html>
"""

components.html(game_html, height=800)
