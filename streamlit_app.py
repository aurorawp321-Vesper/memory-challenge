import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="极简记忆挑战 v2.1", layout="centered")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { background-color: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }
        .header { margin-bottom: 20px; text-align: center; }
        .status-text { font-size: 18px; color: #D4AF37; margin-bottom: 5px; height: 24px; letter-spacing: 2px; font-weight: 300; }
        .timer { font-size: 36px; color: #fff; font-variant-numeric: tabular-nums; letter-spacing: 2px; font-weight: 200; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; width: 90vw; max-width: 380px; }
        .card { height: 80px; background: #111; border: 1px solid #333; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 32px; transition: all 0.3s ease; position: relative; }
        .card.flipped { transform: rotateY(180deg); background: #1a1a1a; border-color: #D4AF37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); }
        .card.matched { background: #D4AF37; color: #000; border-color: #D4AF37; cursor: default; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; text-align: center; }
        .btn { background: none; border: 1px solid #D4AF37; color: #D4AF37; padding: 15px 50px; cursor: pointer; border-radius: 2px; font-size: 16px; letter-spacing: 4px; transition: 0.3s; }
        .btn:hover { background: #D4AF37; color: #000; }
    </style>
</head>
<body>
    <audio id="sound-flip" src="https://www.soundjay.com/buttons/sounds/button-16.mp3"></audio>
    <audio id="sound-match" src="https://www.soundjay.com/buttons/sounds/button-3.mp3"></audio>
    <audio id="sound-fail" src="https://www.soundjay.com/buttons/sounds/button-10.mp3"></audio>
    <audio id="sound-win" src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"></audio>

    <div id="start-screen" class="overlay">
        <h1 style="color: #D4AF37; font-weight: 200; letter-spacing: 10px; margin-bottom: 40px;">FOCUS</h1>
        <button class="btn" onclick="startPreview()">START CHALLENGE</button>
        <p style="color: #444; margin-top: 20px; font-size: 12px;">点击开始以激活音效反馈</p>
    </div>

    <div class="header">
        <div class="status-text" id="status">WAITING...</div>
        <div class="timer" id="timer">06.00s</div>
    </div>
    <div class="grid" id="grid"></div>
    
    <div id="success" class="overlay" style="display:none;">
        <h1 style="color: #D4AF37; font-weight: 200; font-size: 42px; letter-spacing: 8px;">PERFECT</h1>
        <p id="final-time" style="color: #666; font-size: 18px; margin-top: 10px;"></p>
        <button class="btn" onclick="location.reload()">RESTART</button>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        const symbols = ['◈', '▣', '◬', '○', '★', '✚', '✧', '♠', '◈', '▣', '◬', '○', '★', '✚', '✧', '♠'];
        let cards = []; let flipped = []; let matched = 0; let startTime = null; let timerInterval = null;
        let isPreviewing = true;

        function playSound(id) {
            const s = document.getElementById(id);
            s.currentTime = 0;
            s.play().catch(() => {});
        }

        function startPreview() {
            document.getElementById('start-screen').style.display = 'none';
            playSound('sound-flip'); 
            initGame();
        }

        function initGame() {
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            document.getElementById('status').innerText = 'MEMORIZING...';
            cards = [...symbols].sort(() => Math.random() - 0.5);
            
            cards.forEach((s, i) => {
                const c = document.createElement('div');
                c.className = 'card flipped';
                c.dataset.s = s;
                c.innerText = s;
                c.onclick = () => handleCardClick(c);
                grid.appendChild(c);
            });

            let previewSeconds = 6;
            document.getElementById('timer').innerText = "06.00s";
            
            const previewInterval = setInterval(() => {
                previewSeconds--;
                document.getElementById('timer').innerText = "0" + previewSeconds + ".00s";
                if (previewSeconds <= 0) {
                    clearInterval(previewInterval);
                    startRealGame();
                }
            }, 1000);
        }

        function startRealGame() {
            isPreviewing = false;
            document.getElementById('status').innerText = 'GO';
            document.querySelectorAll('.card').forEach(c => {
                c.classList.remove('flipped');
                c.innerText = '';
            });
            startTime = Date.now();
            timerInterval = setInterval(() => {
                document.getElementById('timer').innerText = ((Date.now() - startTime)/1000).toFixed(2) + 's';
            }, 50);
        }

        function handleCardClick(c) {
            if (isPreviewing || flipped.length >= 2 || c.classList.contains('flipped') || c.classList.contains('matched')) return;
            
            playSound('sound-flip');
            c.classList.add('flipped');
            c.innerText = c.dataset.s;
            flipped.push(c);

            if (flipped.length === 2) {
                setTimeout(checkMatch, 600);
            }
        }

        function checkMatch() {
            const [a, b] = flipped;
            if (a.dataset.s === b.dataset.s) {
                playSound('sound-match');
                a.classList.add('matched'); b.classList.add('matched');
                matched += 2;
                if (matched === 16) {
                    clearInterval(timerInterval);
                    playSound('sound-win');
                    document.getElementById('success').style.display = 'flex';
                    document.getElementById('final-time').innerText = "TIME: " + document.getElementById('timer').innerText;
                    confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 }, colors: ['#D4AF37', '#ffffff'] });
                }
            } else {
                playSound('sound-fail');
                a.classList.remove('flipped'); a.innerText = '';
                b.classList.remove('flipped'); b.innerText = '';
            }
            flipped = [];
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=800)
