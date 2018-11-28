#Imports
from flask import Flask, render_template, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

from DBcm import UseDatabase



app = Flask(__name__)
nav = Nav(app)

app.config['dbconfig'] = {  'host':'127.0.0.1',
                            'user':'kevin',
                            'password':'pass',
                            'database':'bookreviews',}

#Function to set navigation menu - will show on each page by including in base.html template
@nav.navigation()
def mynavbar():
    return Navbar(
        'mysite',
        View('Home', 'show_index'),
        View('Book Reviews', 'show_book_reviews'),
        View('About L&M', 'show_about'),
        View('Account', 'show_account'),
    )

#Decorator for index.html (Home Page)
@app.route('/')
def show_index() -> 'html':
    return render_template('index.html')

@app.route('/bookReviews')
def show_book_reviews() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT author, book, rating FROM reviews"""

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Author', 'Book', 'Rating')

    return render_template('bookReviews.html',
                           the_title='View Reviews',
                           the_row_titles=titles,
                           the_data=contents,)

@app.route('/writeReview')
def shoe_write_review() -> 'html':
    return render_template('writeReview.html')

@app.route('/about')
def show_about() -> 'html':
    return render_template('about.html')

@app.route('/account')
def show_account() -> 'html':
    return render_template('account.html')

#Function to get data from form that user fills in
@app.route('/log_request', methods=['POST'])
def prepare_log():

    #get values from HTML form and save in variables
    author_name = request.form['bookAuthor']
    book_name = request.form['bookTitle']
    book_rating = request.form['bookRating']

    title = 'Your review review:'

    #call method to store info in DB - pass values
    log_review(author_name, book_name, book_rating)

    #Render confirmation page -**MUST BE AFTER ANY OTHER METHOD CALLS OR THEY WILL BE IGNORED**
    return render_template('reviewConfirm.html',
                           the_title = title,
                           the_author = author_name,
                           the_book = book_name,
                           the_rating = book_rating)
    #Send data to log_review method which will then store in DB
    #**This happens automatically now but will cahnge to only send when user clicks Confirm


#Function to run when user clicks to confirm review
@app.route('/confirm_review')
def confirm_review() -> None:
    return render_template('index.html')

#Background runner function to store data in DB
def log_review(author:str, book:str, rating:str) -> None:

    with UseDatabase(app.config['dbconfig']) as cursor:
        # Create SQL Statement - dynamic placeholders for values
        _SQL = """INSERT INTO reviews
                        (author, book, rating)
                        values
                        (%s, %s, %s)"""

        cursor.execute(_SQL, (author,
                              book,
                              rating))

nav.init_app(app)
app.run(debug=True)
