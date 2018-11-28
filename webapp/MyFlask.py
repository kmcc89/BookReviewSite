from flask import Flask, render_template, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)
nav = Nav(app)

@nav.navigation()
def mynavbar():
    return Navbar(
        'mysite',
        View('Home', 'show_index'),
        View('Book Reviews', 'show_book_reviews'),
        View('About L&M', 'show_about'),
        View('Account', 'show_account'),
    )

@app.route('/')
def show_index() -> 'html':
    return render_template('index.html')

@app.route('/bookReviews')
def show_book_reviews() -> 'html':
    return render_template('bookReviews.html')

@app.route('/writeReview')
def shoe_write_review() -> 'html':
    return render_template('writeReview.html')

@app.route('/about')
def show_about() -> 'html':
    return render_template('about.html')

@app.route('/account')
def show_account() -> 'html':
    return render_template('account.html')

def log_review(req: 'flask_request', res: str) -> None:
    dbconfig = {'host':'127.0.0.1',
                'user':'bill',
                'password':'pass',
                'database':'vsearchlogDB',}



nav.init_app(app)
app.run(debug=True)
