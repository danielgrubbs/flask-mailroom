import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b'\n\xcfr\xdd\x12O\xa9\x00c\xe1h\xcd\xd97\x00\xc1\x1c?\x0c\x844[\x9a\xd9'
# app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
@app.route('/home/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['name']).get()
        except Donor.DoesNotExist:
            donor = Donor(name=request.form['name'])
            donor.save()

        amount = request.form['value']
        if amount == '':
            amount = 0
        donation = Donation(value=amount, donor=donor)
        donation.save()
        return redirect(url_for('home'))
    
    else:
        return render_template('create.jinja2')

    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

