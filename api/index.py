from flask import Flask, jsonify, Response, request
import random
import gender_guesser.detector as gender

app = Flask(__name__)

MALE_ROASTS = [
    "{name} bhai, tera hairstyle dekh ke barber ne bhi apology letter bhej diya!",
    "{name}, tu itna lazy hai ki alarm bhi tujhe dekh ke snooze ho jaata hai!",
    "Bhai {name}, tere confidence aur reality ka kabhi milan nahi hoga!",
    "{name}, teri crush tujhe dekh ke phone silent pe daal deti hai!",
    "{name} bhai, tera fashion sense dekh ke mannequin bhi resign kar de!",
    "Bhai {name}, tera face unlock dekh ke phone bhi password maangta hai!",
    "{name}, tu gym jaata hai ya sirf mirror selfies lene?",
    "{name} bhai, tere jokes sunke log network issue pretend karte hain!",
    "{name}, teri personality free trial jaisi hai — boring aur limited!",
    "{name}, tere paas talent kam aur overconfidence zyada hai!",
    "Bhai {name}, tu itna unlucky hai ki Ludo mein bhi har jaata hai!",
    "{name}, tera haircut toh lagta hai lawn mower se hua hai!",
    "{name} bhai, tu relationship mein bhi buffering karta hoga!",
    "{name}, tere doston ne tujhe group photo mein crop kar diya!",
    "{name}, tu itna fake hai ki filter bhi confuse ho jaata hai!",
    "{name}, tera face dekh ke Google captcha bhi doubt karta hai!",
    "Bhai {name}, tere paas attitude toh iPhone wala hai, budget Nokia wala!",
    "{name}, teri love life error 404 hai!",
    "{name} bhai, tu exam mein cheating bhi fail kar deta hai!",
    "{name}, teri dressing sense dekh ke traffic cones jealous ho jaaye!",
    "{name}, tu PUBG mein bhi bot se haar jaata hoga!",
    "{name}, tere dance moves dekh ke DJ ne gaana band kar diya!",
    "{name}, tu itna boring hai ki Netflix bhi skip intro kar de!",
    "Bhai {name}, tere future ko dekh ke astrologer bhi ro diya!",
    "{name}, tu selfie leta nahi, public warning deta hai!",
    "{name}, teri beard bhi tujhe support nahi karti!",
    "{name}, tu itna kanjoos hai ki calculator bhi tujhe ignore karta hai!",
    "{name}, teri smile toothpaste ad ka anti-example hai!",
    "Bhai {name}, tera brain airplane mode mein rehta hai!",
    "{name}, teri crush ne tujhe 'bhai' bhi nahi bola — direct ignore kiya!",
    "{name}, tu itna slow hai ki turtle bhi overtake kar de!",
    "{name}, tera face dekh ke camera app crash ho gaya!",
    "{name}, tere kapde dekh ke lagta hai donation box loot ke aaya hai!",
    "{name}, tu itna awkward hai ki Siri bhi answer dene se mana kar de!",
    "{name}, tere room ka mess UNESCO heritage site ban sakta hai!",
    "{name}, teri love story trailer mein hi flop ho gayi!",
    "{name}, tu itna gareeb hai ki dreams bhi EMI pe aate hain!",
    "{name}, tera WiFi bhi tujhe dekh ke disconnect ho jaata hai!",
    "{name}, tu itna useless hai ki mute button bhi tujhe ignore karta hai!",
    "{name}, teri hairstyle dekh ke birds ne nest banana mana kar diya!",
    "{name}, tu itna unlucky hai ki recharge ke baad bhi network nahi aata!",
    "{name}, tere paas swag kam aur lag zyada hai!",
    "{name}, teri body dekh ke dumbbells bhi laugh karte hain!",
    "{name}, tu gym se zyada canteen mein active rehta hai!",
    "{name}, tera breakup bhi probably mutual relief tha!",
    "{name}, tu itna irritating hai ki ads bhi skip kar dein tujhe!",
    "{name}, teri DP dekh ke Instagram dark mode mein chala gaya!",
    "{name}, tere dance steps earthquake warning lagte hain!",
    "{name}, tu itna broke hai ki wallet kholte hi hawa nikalti hai!",
    "{name}, tera face reveal disaster movie se zyada dangerous tha!",
]

FEMALE_ROASTS = [
    "{name}, tera makeup budget India ka GDP lagta hai!",
    "{name}, teri selfies dekh ke filters bhi overwork ho gaye!",
    "{name}, tu itna drama karti hai ki daily soap writers inspire ho jaaye!",
    "{name}, tere mood swings stock market se zyada dangerous hain!",
    "{name}, teri shopping list dekh ke bank account ro deta hai!",
    "{name}, tera attitude VIP hai par reality local train!",
    "{name}, tu itni loud hai ki mic bhi mute ho jaata hai!",
    "{name}, teri bestie bhi tere secrets leak kar deti hogi!",
    "{name}, tera fashion sense dekh ke rainbow bhi confused hai!",
    "{name}, tu itni late reply karti hai ki message retirement le le!",
    "{name}, teri crush tujhe dekh ke airplane mode laga deta hai!",
    "{name}, tere fake tears pe Oscar bhi refuse kar de!",
    "{name}, tera eyeliner bhi straight nahi rehta jaise tera mood!",
    "{name}, tu itna gossip karti hai ki news channels job offer de!",
    "{name}, tere nails weapon category mein aate hain!",
    "{name}, tera ex abhi bhi therapy mein hoga!",
    "{name}, tu itna overreact karti hai ki mosquitoes bhi darr jaaye!",
    "{name}, teri shopping cart dekh ke Amazon bhi panic ho gaya!",
    "{name}, tera makeup remove karte hi Face ID fail ho gaya!",
    "{name}, teri squad photos mein sab filter ka kamaal hota hai!",
    "{name}, tu itna attention maangti hai ki sun bhi jealous ho jaaye!",
    "{name}, tera breakup quote status dekh ke Shakespeare bhi cringe kare!",
    "{name}, tere reels dekh ke algorithm bhi confuse ho gaya!",
    "{name}, tu itni toxic hai ki plants bhi murjha jaaye!",
    "{name}, teri voice note sunke WhatsApp hang ho gaya!",
    "{name}, tere tantrums dekh ke toddlers bhi inspired ho jaaye!",
    "{name}, tera phone screen time NASA track kar raha hai!",
    "{name}, tu itni fake laugh karti hai ki hyena bhi insult feel kare!",
    "{name}, tere outfit choices dekh ke mirror ne resignation de diya!",
    "{name}, tera crush tujhe sirf meme source maanta hai!",
    "{name}, tu itna overspend karti hai ki wallet suicide kar le!",
    "{name}, tere captions reality se zyada fictional hote hain!",
    "{name}, tu itna confuse rehti hai ki GPS bhi lost ho jaaye!",
    "{name}, teri friends bhi tere bina zyada khush lagti hain!",
    "{name}, tera makeup tutorial dekh ke paint brush retire ho gaya!",
    "{name}, tu itni dramatic hai ki thunder bhi background music lagta hai!",
    "{name}, teri dressing sense traffic signals se inspired lagti hai!",
    "{name}, tere crush ne tujhe close friends mein bhi add nahi kiya!",
    "{name}, tera room dekh ke tornado bhi sharma jaaye!",
    "{name}, tu itni lazy hai ki charger bhi tere paas rehna refuse kare!",
    "{name}, tera confidence TikTok trend jaisa temporary hai!",
    "{name}, tu itni over smart banti hai ki Google bhi ignore kar de!",
    "{name}, tere ex ne freedom day celebrate kiya hoga!",
    "{name}, tera attitude free hai phir bhi koi nahi leta!",
    "{name}, tu itna complain karti hai ki customer care bhi block kar de!",
    "{name}, teri beauty sleep bhi kaam nahi kar rahi!",
    "{name}, tu itni broke hai ki shopping cart sirf wishlist ban ke reh gayi!",
    "{name}, tere dance reels dekh ke tripod hil gaya!",
    "{name}, teri fake smile pe emojis bhi trust nahi karte!",
    "{name}, tera social life bas Instagram stories tak limited hai!",
]



HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Friend Comedy Generator - Aurora Style</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                45deg,
                rgba(0, 255, 150, 0.1) 0%,
                rgba(0, 200, 255, 0.1) 25%,
                rgba(150, 0, 255, 0.1) 50%,
                rgba(255, 0, 150, 0.1) 75%,
                rgba(0, 255, 150, 0.1) 100%
            );
            background-size: 400% 400%;
            animation: aurora 15s ease infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .glow-sphere {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.3;
            animation: float 20s ease-in-out infinite;
            pointer-events: none;
            z-index: 1;
        }

        .glow-1 {
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(0, 255, 150, 0.5), transparent);
            top: -100px;
            left: -100px;
            animation-delay: 0s;
        }

        .glow-2 {
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, rgba(0, 200, 255, 0.5), transparent);
            bottom: -50px;
            right: -50px;
            animation-delay: 5s;
        }

        .glow-3 {
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(150, 0, 255, 0.5), transparent);
            top: 50%;
            right: 10%;
            animation-delay: 10s;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(30px, -30px); }
        }

        .container {
            position: relative;
            z-index: 10;
            max-width: 600px;
            width: 95%;
            padding: 40px;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.8s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h1 {
            text-align: center;
            color: #fff;
            margin-bottom: 10px;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #00ff96, #00c8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 255, 150, 0.3);
        }

        .subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 30px;
            font-size: 0.95rem;
            letter-spacing: 0.5px;
        }

        .input-group {
            position: relative;
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input[type="text"] {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid rgba(0, 255, 150, 0.3);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        input[type="text"]:focus {
            outline: none;
            border-color: rgba(0, 255, 150, 0.8);
            background: rgba(0, 255, 150, 0.05);
            box-shadow: 0 0 20px rgba(0, 255, 150, 0.2);
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        button {
            flex: 1;
            padding: 15px 20px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn-submit {
            background: linear-gradient(135deg, #00ff96, #00c8ff);
            color: #000;
            box-shadow: 0 4px 15px rgba(0, 255, 150, 0.3);
        }

        .btn-submit:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 255, 150, 0.5);
        }

        .btn-submit:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn-clear {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }

        .btn-clear:hover:not(:disabled) {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.6);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .timer-section {
            display: none;
            text-align: center;
            margin: 30px 0;
        }

        .timer-section.active {
            display: block;
        }

        .timer {
            font-size: 3rem;
            color: #00ff96;
            font-weight: bold;
            text-shadow: 0 0 20px rgba(0, 255, 150, 0.5);
            animation: pulse 1s ease-in-out;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .timer-label {
            color: rgba(255, 255, 255, 0.7);
            margin-top: 10px;
            font-size: 0.95rem;
        }

        .results-section {
            display: none;
            margin-top: 30px;
        }

        .results-section.active {
            display: block;
        }

        .result-title {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .result-title::before {
            content: '';
            width: 3px;
            height: 20px;
            background: linear-gradient(135deg, #00ff96, #00c8ff);
            border-radius: 2px;
        }

        .funny-lines {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .line {
            background: rgba(0, 255, 150, 0.08);
            border-left: 3px solid rgba(0, 255, 150, 0.5);
            padding: 15px;
            border-radius: 8px;
            color: rgba(255, 255, 255, 0.95);
            line-height: 1.6;
            animation: slideInLeft 0.5s ease forwards;
            opacity: 0;
        }

        .line:nth-child(1) { animation-delay: 0.2s; }
        .line:nth-child(2) { animation-delay: 0.4s; }
        .line:nth-child(3) { animation-delay: 0.6s; }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .greeting {
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
            font-size: 1.3rem;
            font-weight: 600;
        }

        .greeting .name {
            background: linear-gradient(135deg, #00ff96, #00c8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .error {
            background: rgba(255, 100, 100, 0.1);
            border-left: 3px solid #ff6464;
            padding: 12px;
            border-radius: 8px;
            color: #ff9a9a;
            margin-top: 15px;
            display: none;
        }

        .error.active {
            display: block;
        }

        @media (max-width: 600px) {
            .container {
                padding: 30px 20px;
            }

            h1 {
                font-size: 2rem;
            }

            .button-group {
                flex-direction: column;
            }

            .timer {
                font-size: 2.5rem;
            }

            input[type="text"] {
                padding: 12px 15px;
                font-size: 1rem;
            }

            button {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
        }

        @media (max-width: 400px) {
            .container {
                padding: 20px 15px;
            }

            h1 {
                font-size: 1.6rem;
            }

            .subtitle {
                font-size: 0.85rem;
            }

            .timer {
                font-size: 2rem;
            }

            .greeting {
                font-size: 1.1rem;
            }
        }

        .sparkle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ff96;
            border-radius: 50%;
            pointer-events: none;
            animation: sparkleAnim 1s ease-out forwards;
        }

        @keyframes sparkleAnim {
            to {
                transform: translate(var(--tx), var(--ty));
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="glow-sphere glow-1"></div>
    <div class="glow-sphere glow-2"></div>
    <div class="glow-sphere glow-3"></div>

    <div class="container">
        <h1>✨ Even AI Roast YOU </h1>
        <p class="subtitle">Troll Your Loved Ones</p>

        <div class="input-group">
            <label for="nameInput">Type Your Name:</label>
            <input 
                type="text" 
                id="nameInput" 
                placeholder="Type your name..." 
                autocomplete="off"
            >
        </div>

        <div class="button-group">
            <button class="btn-submit" id="submitBtn">Enter</button>
            <button class="btn-clear" id="clearBtn">Clear</button>
        </div>

        <div class="error" id="errorMsg"></div>

        <div class="timer-section" id="timerSection">
            <div class="timer" id="timerCount">5</div>
            <div class="timer-label">Loading your Roast...</div>
        </div>

        <div class="results-section" id="resultsSection">
            <div class="greeting" id="greeting"></div>
            <div class="result-title">Roasting</div>
            <div class="funny-lines" id="funnyLinesContainer"></div>
        </div>
    </div>

    <script>
        const nameInput = document.getElementById('nameInput');
        const submitBtn = document.getElementById('submitBtn');
        const clearBtn = document.getElementById('clearBtn');
        const timerSection = document.getElementById('timerSection');
        const resultsSection = document.getElementById('resultsSection');
        const errorMsg = document.getElementById('errorMsg');
        const funnyLinesContainer = document.getElementById('funnyLinesContainer');
        const greeting = document.getElementById('greeting');
        const timerCount = document.getElementById('timerCount');

        submitBtn.addEventListener('click', async () => {
            const name = nameInput.value.trim();

            errorMsg.classList.remove('active');

            if (!name) {
                showError('Please enter your name!');
                return;
            }

            if (name.length < 2) {
                showError('Name should be at least 2 characters!');
                return;
            }

            resultsSection.classList.remove('active');
            timerSection.classList.add('active');
            submitBtn.disabled = true;
            clearBtn.disabled = true;
            nameInput.disabled = true;

            let timeLeft = 5;
            timerCount.textContent = timeLeft;

            const timerInterval = setInterval(() => {
                timeLeft--;
                timerCount.textContent = timeLeft;

                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    fetchAndDisplayLines(name);
                }
            }, 1000);
        });

        clearBtn.addEventListener('click', () => {
            nameInput.value = '';
            nameInput.focus();
            timerSection.classList.remove('active');
            resultsSection.classList.remove('active');
            errorMsg.classList.remove('active');
            submitBtn.disabled = false;
            clearBtn.disabled = false;
            nameInput.disabled = false;
        });

        async function fetchAndDisplayLines(name) {
            try {
                const response = await fetch(`/api/getlines?name=${encodeURIComponent(name)}`);
                const data = await response.json();

                timerSection.classList.remove('active');
                resultsSection.classList.add('active');

                const displayName = name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();

                greeting.innerHTML = `Hey <span class="name">${displayName}</span>, Bura Na Mano AI hu! 😂`;

                funnyLinesContainer.innerHTML = '';
                data.lines.forEach(line => {
                    const lineEl = document.createElement('div');
                    lineEl.className = 'line';
                    lineEl.innerHTML = `"${line}"`;
                    funnyLinesContainer.appendChild(lineEl);
                    
                    createSparkles(lineEl);
                });

                submitBtn.disabled = false;
                clearBtn.disabled = false;
                nameInput.disabled = false;

            } catch (error) {
                showError('Failed to load comedy lines. Please try again!');
                timerSection.classList.remove('active');
                submitBtn.disabled = false;
                clearBtn.disabled = false;
                nameInput.disabled = false;
            }
        }

        function showError(message) {
            errorMsg.textContent = message;
            errorMsg.classList.add('active');
        }

        function createSparkles(element) {
            const rect = element.getBoundingClientRect();
            for (let i = 0; i < 5; i++) {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                
                const angle = (Math.PI * 2 * i) / 5;
                const velocity = 40 + Math.random() * 40;
                const tx = Math.cos(angle) * velocity;
                const ty = Math.sin(angle) * velocity;
                
                sparkle.style.setProperty('--tx', `${tx}px`);
                sparkle.style.setProperty('--ty', `${ty}px`);
                sparkle.style.left = rect.width / 2 + 'px';
                sparkle.style.top = '0px';
                
                element.appendChild(sparkle);
                
                setTimeout(() => sparkle.remove(), 1000);
            }
        }

        nameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                submitBtn.click();
            }
        });

        window.addEventListener('load', () => {
            nameInput.focus();
        });
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return Response(HTML_TEMPLATE, mimetype='text/html')

@app.route('/api/getlines', methods=['GET'])
def get_lines():
    try:
        name = request.args.get('name', 'Friend')
        # Capitalize the name properly
        name = name.strip().capitalize()
        
        lines = random.sample(FUNNY_LINES, 3)
        # Replace {name} placeholder with actual name
        personalized_lines = [line.replace('{name}', name) for line in lines]
        
        return jsonify({'lines': personalized_lines})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
