# Meme Generator
A Python-based meme generator that generates a meme composed of a random image with a random quote drawn on it unless the user specifies otherwise.

## Installation
------------
Make a virtual environment:
```sh
$ virtualenv venv
```

Activate the virtual environment:
```sh
$ . venv/Script/activate
```

Install dependencies in a virtual environment:
```sh
$ pip install -r requirements.txt
```

## Project Structure - Roles and Responsibilities
------------

    ├── README.md          <- Top-level README for developers using this project.
    |
    ├── pdftotext.exe      <- PDF to text CLI utility tool
    |
    ├── .gitignore         <- Standard .gitignore file
    |
    ├── requirements.txt   <- The requirements file for reproducing the environment
    |
    ├── _data              <- Data directory, houses pre-loaded quotes and images.
    │   ├── DogQuotes
    │   ├── photos
    │   └── SimpleLines
    │
    ├── templates          <- Templates directory, houses pre-loaded html templates for flask to render.
    │   ├── base.html
    │   ├── meme_format.html
    │   └── meme.html
    |
    ├── MemeEngine         <- MemeEngine module, responsible for generating memes given a quote and an image
    │   ├── __init__.py
    │   ├── meme_engine.py
    |
    ├── QuoteEngine        <- QuoteEngine module, responsible for ingesting different file types and generates quote objects out of them.
    │   ├── __init__.py
    │   ├── ingestor.py
    │   ├── quote.py
    |
    ├── meme.py            <- Responsible for generating memes using command line arguments.
    │
    ├── app.py             <- Responsible for providing a web interface to generate memes using flask.

## Dependencies
------------
* **python-docx**: Used to read from .docx files.
* **pandas**: Used to read from .csv files as dataframes.
* **Pillow**: Used to read and manipulate images, used to draw quotes on memes.
* **requests**: Used to download custom images from the web.
* **flask**: Used to provide MemeEngine and QuoteEngine functionalities as a web service.

## General Usage
------------
Run the project on local host:
```sh
$ flask run --host 0.0.0.0 --port 3000 --reload
```

Generate a meme using the command line:
```sh
$ python meme.py --body <insert quote body> --author <insert quote author> --path <insert image path>
```

## Module Usage
------------
Using the ingestor to generate quotes model objects (body, author) from .txt, .docx, .pdf and .csv files:
```py
file_paths = ['<path to .txt> file',
                '<path to .docx> file',
                '<path to .pdf> file',
                '<path to .csv> file']
from QuoteEngine import Ingestor
quotes = []
for f in file_paths:
    quotes.extend(Ingestor.parse(f))
```

Using the MemeEngine to generate a meme in a specific path:
```py
from MemeEngine import MemeEngine
meme = MemeEngine('<path where the generated memes will be saved>')
img = '<path to image>'
quote_body = '<body of quote>'
quote_author = '<author of quote>'
path = meme.make_meme(img, quote_body, quote_author)
```
