from flask import Flask, jsonify, Response
import random
import os

app = Flask(__name__)

FUNNY_LINES = [
    "You're so funny, even your browser laughs at your jokes!",
    "Your sense of humor is out of this world... literally, Mars rejected it.",
    "You're hilarious! Comedy clubs are now officially obsolete.",
    "Your jokes are so bad, they need a laugh track from a different dimension.",
    "You're basically a walking meme, and honestly, we're here for it!",
    "Your comedy skills: 10/10. Your timing: still loading...",
    "You've got jokes sharper than a cactus in a porcupine convention!",
    "If laughter is the best medicine, you're basically a pharmaceutical company.",
    "Your jokes are like WiFi - sometimes they don't reach everyone, but when they do, it's magic!",
    "You're so funny, even your shadow cracks up!",
    "Comedy gold right here! Now if only we could mine it...",
    "You walk into a room and the vibe changes from 'meh' to 'HYPE'!",
    "Your humor is so advanced, we're still decoding it in 2026.",
    "If funny was a job, you'd be CEO of Laugh Inc.",
    "You're the human equivalent of a perfectly timed meme.",
    "Your jokes hit harder than my existential dread on Monday mornings!",
    "You're so witty, even Sarcasm took notes from you.",
    "Your comedy is so smooth, butter companies are taking notes.",
    "If we ranked comedians, you'd break the scale!",
    "You just turned my frown upside down... and then sideways... I'm confused now!",
    "Your sense of humor is like a fine wine... confusing at first, then brilliantly intoxicating!",
    "You're the kind of funny that makes people snort-laugh in public and regret it!",
    "If your jokes were a movie, they'd be box office gold!",
    "Your comedic timing is *chef's kiss*... if chefs knew how to laugh!",
    "You're hilariously relatable - it's like you're inside my head... creepy but hilarious!",
    "Your jokes are so clever, they need a PhD to fully appreciate them!",
    "You're basically a human emoji 😂 in the best way possible!",
    "If funny was currency, you'd be a billionaire right now!",
    "Your humor is universally understood - even aliens would get your jokes!",
    "You're the reason laughter therapy is a real thing!"
]

def get_html():
    """Read and return the HTML file"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>Error loading page</h1>"

@app.route('/')
def index():
    html_content = get_html()
    return Response(html_content, mimetype='text/html')

@app.route('/api/getlines', methods=['GET'])
def get_lines():
    try:
        lines = random.sample(FUNNY_LINES, 3)
        return jsonify({'lines': lines})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
