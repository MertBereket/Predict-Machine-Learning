from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms import TextField
from machinelearning import pred

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "adm123qwe_"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'


def authentication(username, password):
    _check = username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD
    if _check:
        return True

    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


# Simple form handling using raw HTML forms
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    error = None
    if request.method == 'POST':
        # Form being submitted; grab data from form.
        first_name = request.form['Name']
        last_name = request.form['Password']

        _user = authentication(first_name, last_name)

        # Validate form data
        if _user:
            return redirect(url_for('predict'))

        error = "Wrong Password!"

    # Render the sign-up page
    return render_template('sign-in.html', message=error)


# More powerful approach using WTForms
class RegistrationForm(Form):
    first_name = TextField('Name')
    last_name = TextField('Surname')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = "Please supply both first and last name"
        else:
            return redirect(url_for('thank_you'))

    return render_template('register.html', form=form, message=error)


@app.route('/pred', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        yil = request.form['Yıl']
        km = request.form['Km']
        motor = request.form['Motor Hacmi']
        hp = request.form['Motor Gücü']

        _pred = pred(int(yil), float(motor), int(hp), float(km))

        return render_template('pred.html', context={
            'result': "%.3f" % _pred
        })

    return render_template('pred.html', context=None)
    # return redirect(url_for('thank_you'))


# Run the application
app.run(debug=True)
