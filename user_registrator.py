from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # binding DB and Flask App


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(40), nullable=False)


@app.route("/")
def index():
    users = User.query.all()
    print(users)
    return render_template("register.html", users=users)


@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    new_user = User(
        name=name,
        surname=surname,
        email=email,
        username=username,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")


@app.route("/image/<filename>")
def get_image(filename):
    image_path = f"images/{filename}"
    return send_file(image_path, mimetype="image/png")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаем таблицу в контексте приложения
    app.run(debug=True)
