
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from functions import reverse_complement
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="strobi1925",
    password="Dercolo1_",
    hostname="strobi1925.mysql.pythonanywhere-services.com",
    databasename="strobi1925$sequences",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Sequence(db.Model):
    __tablename__ = "sequences"
    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.String(4096))
    rev_com = db.Column(db.String(4096))
    gc = db.Column(db.Float())
    date = db.Column(db.DateTime())


errormessage = [""]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", sequences=Sequence.query.all(), errormessage = errormessage)
    else:
        if reverse_complement(request.form["sequence"]) == "Q":
            errormessage[0] = "NOT A SEQUENCE!"
            return redirect(url_for("index"))
        else:
            errormessage[0] = ""
            result = reverse_complement(request.form["sequence"])
            sequence = Sequence(sequence=result[0], rev_com=result[1], gc=result[2], date=result[3])
            db.session.add(sequence)
            db.session.commit()
            return redirect(url_for("index"))



