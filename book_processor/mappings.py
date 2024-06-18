import os
from .utils import write_json

class MappingsProcessor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.book_chapters = {}
        self.chapter_paragraphs = {}
        self.paragraph_sentences = {}
        self.pages_paragraphs = {}

    def add_book_chapter(self, book_id, chapter_id):
        if book_id not in self.book_chapters:
            self.book_chapters[book_id] = []
        self.book_chapters[book_id].append(chapter_id)

    def add_chapter_paragraph(self, chapter_id, start, end):
        self.chapter_paragraphs[chapter_id] = {'start': start, 'end': end}

    def add_paragraph_sentence(self, paragraph_id, start, end):
        self.paragraph_sentences[paragraph_id] = {'start': start, 'end': end}

    def add_page_paragraph(self, book_id, page_type, page_number, start, end):
        if book_id not in self.pages_paragraphs:
            self.pages_paragraphs[book_id] = {'old': {}, 'new': {}}
        if page_type not in self.pages_paragraphs[book_id]:
            self.pages_paragraphs[book_id][page_type] = {}
        self.pages_paragraphs[book_id][page_type][page_number] = {'start': start, 'end': end}

    def update_page_paragraph(self, book_id, page_type, page_number, start, end):
        if book_id in self.pages_paragraphs and page_type in self.pages_paragraphs[book_id] and page_number in self.pages_paragraphs[book_id][page_type]:
            self.pages_paragraphs[book_id][page_type][page_number]['end'] = end

    def write_mappings_json(self):
        os.makedirs(os.path.join(self.output_dir, 'maps'), exist_ok=True)
        write_json({'bookChapters': self.book_chapters}, os.path.join(self.output_dir, 'maps', 'books-to-chapters.json'))
        write_json({'chapterParagraphs': self.chapter_paragraphs}, os.path.join(self.output_dir, 'maps', 'chapters-to-paragraphs.json'))
        write_json({'paragraphSentences': self.paragraph_sentences}, os.path.join(self.output_dir, 'maps', 'paragraphs-to-sentences.json'))
        write_json({'books': self.pages_paragraphs}, os.path.join(self.output_dir, 'maps', 'pages-to-paragraphs.json'))
