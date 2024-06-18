import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(BASE_DIR, 'books')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
START_SENTENCE_ID = 1
START_PARAGRAPH_ID = 1
VISIBLE_SENTENCE_ENDINGS = ['.', '?', '!', ':']
INVISIBLE_SENTENCE_ENDINGS = ['@', '#']
