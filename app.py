
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RSA Asylum Assistance</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: #f7f8f6;
    color: #192d35;
    line-height: 1.6;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 7%;
    background: white;
    border-bottom: 1px solid #e9eeeb;
}

.brand {
    font-size: 19px;
    font-weight: 800;
    color: #173c40;
}

.brand span {
    color: #168b79;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 22px;
}

select {
    padding: 10px;
    border: 1px solid #dce5e1;
    border-radius: 9px;
    background: white;
    color: #193a3d;
}

.hero {
    padding: 75px 7% 65px;
    background: linear-gradient(120deg, #103b3e, #176b60);
    color: white;
}

.hero-content {
    max-width: 760px;
}

.eyebrow {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 13px;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: clamp(36px, 6vw, 58px);
    line-height: 1.12;
    margin-bottom: 20px;
    letter-spacing: -1.5px;
}

.hero p {
    color: #dcebe6;
    font-size: 17px;
    max-width: 620px;
    margin-bottom: 28px;
}

.primary-btn {
    display: inline-block;
    background: #f2b96b;
    color: #263b36;
    text-decoration: none;
    padding: 14px 23px;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.2s;
}

.primary-btn:hover {
    background: #ffd08f;
    transform: translateY(-2px);
}

.notice {
    margin: 30px 7%;
    padding: 17px 20px;
    background: #fff5e8;
    border: 1px solid #f2dfc4;
    border-radius: 12px;
    color: #72532e;
    font-size: 14px;
}

.section {
    padding: 48px 7%;
}

.section-heading {
    margin-bottom: 25px;
}

.section-heading h2 {
    font-size: 28px;
    margin-bottom: 7px;
    color: #173c40;
}

.section-heading p {
    color: #697a78;
}

.cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 17px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 17px;
    border: 1px solid #e9eeeb;
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(22, 54, 48, 0.08);
}

.card-icon {
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    font-size: 24px;
    margin-bottom: 18px;
}

.green { background: #e4f3ed; }
.orange { background: #fff0dc; }
.purple { background: #eeeafa; }
.pink { background: #f8e9ed; }

.card h3 {
    font-size: 17px;
    margin-bottom: 8px;
}

.card p {
    color: #71807c;
    font-size: 14px;
}

.chat-section {
    padding: 25px 7% 65px;
}

.chat-box {
    background: white;
    border: 1px solid #e5ece8;
    border-radius: 20px;
    padding: 28px;
    max-width: 760px;
    box-shadow: 0 10px 35px rgba(20, 54, 46, 0.05);
}

.chat-top {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 23px;
}

.bot-icon {
    width: 48px;
    height: 48px;
    background: #e4f3ed;
    border-radius: 15px;
    display: grid;
    place-items: center;
    font-size: 23px;
}

.chat-top p {
    font-size: 13px;
    color: #71807c;
}

.message {
    background: #edf5f1;
    padding: 17px;
    border-radius: 4px 16px 16px 16px;
    font-size: 14px;
    margin-bottom: 20px;
}

.chat-input {
    display: flex;
    gap: 10px;
}

.chat-input input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border: 1px solid #dce5e1;
    border-radius: 10px;
    font-size: 14px;
}

.chat-input button {
    background: #176b60;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: bold;
    cursor: pointer;
}

.chat-input button:hover {
    background: #104c46;
}

#chat-response {
    margin-top: 15px;
    font-size: 14px;
    color: #657771;
}

footer {
    background: #12383a;
    color: #dcebe6;
    padding: 28px 7%;
    font-size: 13px;
}

footer p + p {
    margin-top: 7px;
}

@media (max-width: 850px) {
    .cards {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 520px) {
    nav {
        padding: 16px 5%;
    }

    .nav-right {
        gap: 8px;
    }

    .hero {
        padding: 55px 6%;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .section, .chat-section {
        padding-left: 6%;
        padding-right: 6%;
    }

    .chat-input {
        flex-direction: column;
    }

    .chat-input button {
        padding: 14px;
    }
}
</style>
</head>

<body>

<nav>
    <div class="brand">RSA <span>Asylum Assistance</span></div>
    <div class="nav-right">
        <select aria-label="Choose language">
            <option>English</option>
            <option>isiZulu</option>
            <option>isiXhosa</option>
            <option>Sesotho</option>
            <option>French</option>
            <option>Swahili</option>
        </select>
    </div>
</nav>

<section class="hero">
    <div class="hero-content">
        <span class="eyebrow">INFORMATION • GUIDANCE • SUPPORT</span>
        <h1>A little guidance can make a big difference.</h1>
        <p>
            Find clear, accessible information about seeking
            asylum and understanding the process in South Africa.
            Start with a question. We'll help you find your way.
        </p>
        <a href="#chat" class="primary-btn">Explore assistance →</a>
    </div>
</section>

<div class="notice">
    <strong>Important information:</strong>
    This is an independent demonstration project, not an official
    Department of Home Affairs service. Do not enter real personal
    or confidential information.
</div>

<section class="section">
    <div class="section-heading">
        <h2>How can we help you?</h2>
        <p>Explore the information and guidance available.</p>
    </div>

    <div class="cards">
        <div class="card">
            <div class="card-icon green">📄</div>
            <h3>Asylum applications</h3>
            <p>Learn about the asylum application process and the steps involved.</p>
        </div>

        <div class="card">
            <div class="card-icon orange">⚖️</div>
            <h3>Your rights</h3>
            <p>Explore refugee rights, responsibilities and important information.</p>
        </div>

        <div class="card">
            <div class="card-icon purple">📁</div>
            <h3>Supporting documents</h3>
            <p>Understand documents and information that may be relevant.</p>
        </div>

        <div class="card">
            <div class="card-icon pink">👨‍👩‍👧</div>
            <h3>Family information</h3>
            <p>Learn about family members and dependant information.</p>
        </div>
    </div>
</section>

<section class="chat-section" id="chat">
    <div class="section-heading">
        <h2>Let's start a conversation.</h2>
        <p>Have a question? Begin exploring the assistance service.</p>
    </div>

    <div class="chat-box">
        <div class="chat-top">
            <div class="bot-icon">✦</div>
            <div>
                <strong>RSA Assistance Guide</strong>
                <p>Information support prototype</p>
            </div>
        </div>

        <div class="message">
            Hello! Welcome to RSA Asylum Assistance.
            What would you like to learn about today?
        </div>

        <form class="chat-input" onsubmit="sendMessage(event)">
            <input id="user-message" type="text"
                placeholder="Type your question here..."
                aria-label="Your question">
            <button type="submit">Send →</button>
        </form>

        <div id="chat-response" aria-live="polite"></div>
    </div>
</section>

<footer>
    <p><strong>RSA Asylum Assistance</strong></p>
    <p>An independent information-support prototype.</p>
    <p>Not an official government service. Information must be
    verified with the relevant authorities.</p>
</footer>

<script>
function sendMessage(event) {
    event.preventDefault();

    const input = document.getElementById("user-message");
    const response = document.getElementById("chat-response");

    if (!input.value.trim()) {
        response.textContent = "Please enter a question first.";
        return;
    }

    response.textContent =
        "Thank you for your question. The automated assistance " +
        "feature is still being developed. Please do not enter " +
        "personal or confidential information.";

    input.value = "";
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
