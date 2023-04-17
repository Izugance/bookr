# Bookr
This repository contains the code for a book review application (Bookr) and contains aspects that cover many concerns of Django
development. (The frontend is implemented in HTML, CSS, and JavaScript.)

Each folder contains a `description.txt` file that describes the main theme of files in such folder. And as such there's much to
learn through an exploration of the whole project.

The `book_management,` `bookr_test,` and `filter_demo` dirs are more for exploration, while the `bookr,`
`bookr_admin,` `media,` and `reviews` dirs are the heart of the project.

The code files are heavily commented, and intentionally so, to facilitate a broader coverage of aspects that aren't touched on 
with code alone. Hence, this repository is both referential and a demonstration of Django web development. 

# Requirements
In the root directory of this repository is a `requirements.txt` file that contains project dependencies. You can install them
from the command line (preferrably in a Python virtual environment) with the command
```
>>> pip install requirements.txt
```

# Seeding the database
You can seed the database (say sqlite3) with test data by running the command
```
>>> python manage.py loadcsv --csv reviews management/commands/WebDevWithDjangoData.csv
```
(The `loadcsv.py` (a custom management command) and `WebDevWithDjangoData.csv` files exist in the `reviews/management/commands` directory.)
