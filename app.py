
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RSA Asylum Assistance</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f3f5f8;
                margin: 0;
                padding: 30px;
                color: #243047;
            }

            .container {
                max-width: 650px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
            }

            h1 {
                color: #174b3a;
            }

            .notice {
                background-color: #fff4dc;
                padding: 15px;
                border-radius: 8px;
            }

            button {
                background-color: #176b50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 7px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>RSA Asylum Assistance</h1>

            <p>Welcome to the RSA Asylum Assistance chatbot.</p>

            <p>
                This prototype provides general information
                about asylum procedures in South Africa.
            </p>

            <div class="notice">
                <strong>Important:</strong>
                This is an independent demonstration,
                not an official Department of Home Affairs service.
                Do not enter real personal information.
            </div>

            <h2>How can we assist you?</h2>

            <ul>
                <li>Asylum application information</li>
                <li>Refugee rights and responsibilities</li>
                <li>Supporting documents</li>
                <li>Family and dependant information</li>
            </ul>

            <button onclick="alert('Welcome! The chatbot is coming soon.')">
                Start a conversation
            </button>

        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
