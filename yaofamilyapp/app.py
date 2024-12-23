from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management
app.permanent_session_lifetime = timedelta(minutes=30)

# Simulated list of users (username: password)
users = {
    "user1": "password1",
    "user2": "password2",
    "admin": "admin123",
    "guest": "guest123"
}

# Store messages in a list
messages = []

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session.permanent = True
            session["user"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html", error=None)

# Chat Page
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" in session:
        username = session["user"]
        if request.method == "POST":
            message = request.form["message"]
            messages.append(f"{username}: {message}")
        return render_template("chat.html", username=username, messages=messages)
    else:
        return redirect(url_for("login"))

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
