import re
from config import VISIBLE_SENTENCE_ENDINGS, INVISIBLE_SENTENCE_ENDINGS

class SentenceProcessor:
    def __init__(self, content, mappings_processor, chapter_id, start_sentence_id, start_paragraph_id):
        self.content = content
        self.sentences = []
        self.sentence_id = start_sentence_id
        self.paragraph_id = start_paragraph_id
        self.page_number_old = 0
        self.page_number_new = 0
        self.mappings_processor = mappings_processor
        self.chapter_id = chapter_id
        self.start_sentence_id = start_sentence_id
        self.start_paragraph_id = start_paragraph_id

    def process_sentences(self):
        self.content = self.remove_brackets(self.content)
        self.content = self.remove_front_matter(self.content)
        lines = self.content.split('\n')
        for line in lines:
            if line.strip():  # Ignore empty lines
                self.extract_sentences(line.strip())
        self.mappings_processor.add_chapter_paragraph(
            self.chapter_id,
            self.start_paragraph_id,
            self.paragraph_id - 1
        )
        return self.sentences

    def remove_brackets(self, text):
        text = re.sub(r'<(\d+)>', self.handle_old_brackets, text)
        text = re.sub(r'\{(\d+)\}', self.handle_new_brackets, text)
        return text

    def handle_old_brackets(self, match):
        self.page_number_old += 1
        self.mappings_processor.add_page_paragraph(
            self.chapter_id,
            'old',
            self.page_number_old,
            self.paragraph_id,
            self.paragraph_id
        )
        return ''

    def handle_new_brackets(self, match):
        self.page_number_new += 1
        self.mappings_processor.add_page_paragraph(
            self.chapter_id,
            'new',
            self.page_number_new,
            self.paragraph_id,
            self.paragraph_id
        )
        return ''

    def remove_front_matter(self, text):
        return re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)

    def extract_sentences(self, line):
        sentence = ''
        start_sentence_id = self.sentence_id
        start_paragraph_id = self.paragraph_id
        for char in line:
            if char in VISIBLE_SENTENCE_ENDINGS + INVISIBLE_SENTENCE_ENDINGS:
                if char in INVISIBLE_SENTENCE_ENDINGS:
                    sentence = sentence.strip()
                else:
                    sentence += char
                if sentence:  # Ignore empty sentences
                    self.sentences.append({'id': self.sentence_id, 'text': sentence.strip(), 'paragraph': self.paragraph_id})
                    self.sentence_id += 1
                sentence = ''
            else:
                sentence += char
        if sentence.strip():  # Ignore empty sentences
            self.sentences.append({'id': self.sentence_id, 'text': sentence.strip(), 'paragraph': self.paragraph_id})
            self.sentence_id += 1
        end_sentence_id = self.sentence_id - 1
        self.mappings_processor.add_paragraph_sentence(self.paragraph_id, start_sentence_id, end_sentence_id)
        self.paragraph_id += 1
        self.mappings_processor.update_page_paragraph(
            self.chapter_id,
            'old' if self.page_number_old > 0 else 'new',
            self.page_number_old if self.page_number_old > 0 else self.page_number_new,
            start_paragraph_id,
            self.paragraph_id - 1
        )
