from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt       

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class _Bases_(DeclarativeBase):
    pass
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(model_class=_Bases_)
db.init_app(app)

class Books(db.Model):
    __tablename__="Books"
    id: Mapped[int] = mapped_column("Id",Integer,primary_key=True)
    title: Mapped[str] = mapped_column("Title",String(250),unique=True,nullable=False)
    author: Mapped[str] = mapped_column("Author",String(250),nullable=False)
    rating: Mapped[float] = mapped_column("Rating",Float,nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    results = db.session.execute(db.select(Books).order_by(Books.title))
    all_books=results.scalars()
    return render_template("index.html",books=all_books)

@app.route("/a  dd",methods=["POST","GET"])
def add():
    if request.method=="POST":
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=float(request.form["rating"])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return  render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

