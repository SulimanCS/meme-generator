"""Flask application to provide an interface to our application on the web."""
import random
import os
import requests
import traceback
from flask import Flask, render_template, abort, request
from QuoteEngine import Ingestor
from MemeEngine import MemeEngine


app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    for root, _, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    path = None
    try:
        # get data from request form
        img_url = request.form.get('image_url')
        body = request.form.get('body')
        author  = request.form.get('author')
        if len(body) > 150 or len(author) > 150:
            raise ValueError('Body/Author length must udner 150')
        r = requests.get(img_url, allow_redirects=True)
        if not r.ok:
            raise Exception("Couldn't load image from url")
        directory = './tmp'
        tmp_file = f'{directory}/{random.randint(0, 100000000)}.png'
        if not os.path.isdir(directory):
            os.mkdir(directory)
        with open(tmp_file, 'wb') as outfile:
            outfile.write(r.content)

        path = meme.make_meme(tmp_file, body, author)
    except Exception as e:
        print('[ERROR] Failed to make a meme from image url.')
        print(traceback.format_exc())

    if path is not None:
        os.remove(tmp_file)
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
