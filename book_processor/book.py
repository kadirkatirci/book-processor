import os
from .utils import get_book_meta, write_json
from .chapter import ChapterProcessor
from .mappings import MappingsProcessor

class BookProcessor:
    def __init__(self, books_dir, output_dir):
        self.books_dir = books_dir
        self.output_dir = output_dir
        self.books_meta = []
        self.mappings_processor = MappingsProcessor(output_dir)
        self.current_sentence_id = 1
        self.current_paragraph_id = 1

    def process_books(self):
        for book_folder in os.listdir(self.books_dir):
            book_meta = get_book_meta(book_folder)
            if book_meta:
                self.books_meta.append(book_meta)
                self.process_book(book_folder, book_meta)
        self.write_books_json()
        self.mappings_processor.write_mappings_json()

    def process_book(self, book_folder, book_meta):
        book_output_dir = os.path.join(self.output_dir, "{}-{}".format(book_meta['id'], book_meta['slug']))
        os.makedirs(book_output_dir, exist_ok=True)
        chapters = ChapterProcessor(
            os.path.join(self.books_dir, book_folder),
            book_output_dir,
            self.mappings_processor,
            book_meta['id'],
            self.current_sentence_id,
            self.current_paragraph_id
        )
        last_sentence_id, last_paragraph_id = chapters.process_chapters()
        self.current_sentence_id = last_sentence_id + 1
        self.current_paragraph_id = last_paragraph_id + 1

    def write_books_json(self):
        books_json_path = os.path.join(self.output_dir, 'books.json')
        write_json({'books': self.books_meta}, books_json_path)
