from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from forms import ContactForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(25))

    def __repr__(self):
        return '<Contact %r>' % self.name


db.create_all()
db.session.commit()


@app.route('/')
def index():
    records = Contact.query.all()
    return render_template('index.html', records=records)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ContactForm(request.form)
    if form.validate_on_submit():
        contact = Contact()
        form.populate_obj(contact)
        db.session.add(contact)
        db.session.commit()
        return 'ok'
    return render_template('_form.html', form=form)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get(id)
    form = ContactForm(request.form, obj=contact)
    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.commit()
        return 'ok'
    return render_template('_form.html', form=form)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return 'ok'


if __name__ == "__main__":
    app.run(debug=True)