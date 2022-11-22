from website import create_app
from random import randint
from website.database import User, Numbers, db
from flask import render_template, request, redirect, url_for, flash, send_file, Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = create_app()

@app.route("/")
def default():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html", user = current_user)

@app.route("/process-list")
def process_list():
    return render_template("process-list.html", user = current_user)

@app.route("/process")
@login_required
def process():
    numbers = []
    for _ in range(1,11):
        number = randint(1,1000000)
        numbers.append(number)
        db.session.add(Numbers(number = number, user_id = current_user.id))
    db.session.commit()
    file = open("numbers.txt", "w")
    for number in reversed(numbers):
        file.write(str(number) + "\n")
    file.close()
    return send_file("../numbers.txt", as_attachment=True)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        user = User.query.filter_by(email=request.form["email"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                flash(f"Logged in successfully! Welcome back, {user.username}.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("home"))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    data = request.form
    valid_sign_up_details = False
    print(data)
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        valid_sign_up_details = check_sign_up_details(email, username, password, confirm_password)

        if valid_sign_up_details:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

    return (
        redirect(url_for("home"))
        if valid_sign_up_details
        else render_template("sign-up.html", user=current_user)
    )

def check_sign_up_details(email, username, password, confirm_password) -> bool:
    if email and username and password and confirm_password:
        if len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        if len(username) < 2:
            flash("Username must be greater than 1 character.", category="error")
        if len(password) < 5:
            flash("Password must be greater than 4 characters.", category="error")
            return False
        else:
            valid_details = True
            if password != confirm_password:
                flash("Passwords don't match.", category="error")
                valid_details = False
            if User.query.filter_by(email=email).first() != None:
                flash("Email already exists.", category="error")
                valid_details = False
            if User.query.filter_by(username=username).first() != None:
                flash("Username already exists.", category="error")
                valid_details = False
            return valid_details
    else:
        flash("Please fill out all fields.", category="error")
    return False

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=25565)
