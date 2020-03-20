# LitGame

Online Demo: [https://litgame.pythonanywhere.com/](https://litgame.pythonanywhere.com/)

LitGame is a literature trivia game. To play, one must match the order of quotations and sources from classic literature. Originally started as a final project for fall 2018 session of [CCPS530](https://ce-online.ryerson.ca/ce/calendar/default.aspx?id=5&section=course&mode=course&ccode=CCPS+530) with instructor [Ghassem Tofighi](https://ghassem.com/).

![screenshot of game in progress](screenshot.jpg "Screenshot of game in progress")

## Featured Technologies

* [Flask](http://flask.pocoo.org/docs/1.0/) a Python micro web framework
* [WTForms](https://wtforms.readthedocs.io/en/stable/) and [Flask_WTF](https://flask-wtf.readthedocs.io/en/stable/) for form construction, validation, and CSRF protection.
* [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) CRUD database operations
* [passlib](https://passlib.readthedocs.io/en/stable/) to salt and hash user passwords
* [nltk](https://www.nltk.org/) for sentence tokenization 
* [jQuery](https://jquery.com/) for DOM manipulation
* [jQuery UI](https://jqueryui.com/) and [jQuery UI Touch Punch](http://touchpunch.furf.com/) for a touchscreen friendly sortable widget
* [Bootstrap](https://getbootstrap.com/) for mobile friendly styling
* [Featherlight](https://github.com/noelboss/featherlight) for modal image gallery

## Quick Start Guide

To get this Flask site running locally:

0. Make sure you have Python 3.6 available. `python --version`
1. Download this code.
2. While optional, it is highly recommended to create your virtual environment, and activate it as described [here](https://docs.python.org/3.6/library/venv.html).
3. Find a suitable replacement background image. The demo background image file "[paper-texture-1145467.jpg](https://www.freeimages.com/photo/paper-texture-1145467)" is not included in this repo. Place your replacement background image in static/img.
4. Find a suitable replacement favicon (.ico) file. The demo favicon "[favicon.ico](https://www.freefavicon.com/freefavicons/objects/iconinfo/stylized-book-152-171437.html)" is not included in this repo. Place your replacement favicon in static/.
5. Pip install all requirements in requirements.txt: `pip install -r requirements.txt`
6. To run locally run: `python routes.py`

Before deploying, be sure to change the `app.config['SECRET_KEY']` and turn off debugging by removing the optional arguments from `app.run()`.

## Customization
To serve quotations from authors of your choice, you must populate the database table `quote`. To start remove/rename quote_db.sqlite, and run `python db_init.py`. This will create a new quote_db.sqlite file. To populate the database run `python populate_db.py` and follow the interactive prompts.

## Limitations
This project can only support single author works.

## Supported Browsers
1. Latest: Chrome, Firefox, Opera, Edge, Safari
2. Internet Explorer 11

## Future Improvements
* [x] Change the number of quotations displayed in a quiz from 3 to 2. User testing suggests this will improve the game experience.

* [ ] Allow users to change their username, email address, and password.

* [ ] Allow users to opt-in to displaying their scores in a publicly accessible "high score" table.
