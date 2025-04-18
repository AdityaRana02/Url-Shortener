from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10), unique=True)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short = ''.join(random.choices(characters, k=6))
    while URL.query.filter_by(short_url=short).first():
        short = ''.join(random.choices(characters, k=6))
    return short

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        existing = URL.query.filter_by(long_url=long_url).first()
        if existing:
            return render_template('result.html', short_url=existing.short_url)
        short_url = generate_short_url()
        new_url = URL(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('result.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short>')
def redirect_short_url(short):
    url = URL.query.filter_by(short_url=short).first_or_404()
    return redirect(url.long_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

