import os
import re
from .utils import read_md_file, write_json
from .sentence import SentenceProcessor
from .toc import TOCProcessor

class ChapterProcessor:
    def __init__(self, book_dir, output_dir, mappings_processor, book_id, start_sentence_id, start_paragraph_id):
        self.book_dir = book_dir
        self.output_dir = output_dir
        self.mappings_processor = mappings_processor
        self.book_id = book_id
        self.start_sentence_id = start_sentence_id
        self.start_paragraph_id = start_paragraph_id
        self.current_sentence_id = start_sentence_id
        self.current_paragraph_id = start_paragraph_id
        self.chapters_meta = []

    def process_chapters(self):
        for chapter_file in os.listdir(self.book_dir):
            if chapter_file.endswith('.md'):
                chapter_meta = self.get_chapter_meta(chapter_file)
                if chapter_meta:
                    self.chapters_meta.append(chapter_meta)
                    self.process_chapter(chapter_file, chapter_meta)
        self.write_chapters_json()
        return self.current_sentence_id, self.current_paragraph_id

    def get_chapter_meta(self, chapter_file):
        content = read_md_file(os.path.join(self.book_dir, chapter_file))
        frontmatter = self.extract_front_matter(content)
        if frontmatter:
            return {
                'id': frontmatter.get('id'),
                'title': frontmatter.get('title'),
                'slug': frontmatter.get('slug'),
                'description': frontmatter.get('description')
            }
        return None

    def extract_front_matter(self, content):
        match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            return dict(re.findall(r'(\w+):\s*(.*)', frontmatter))
        return None

    def process_chapter(self, chapter_file, chapter_meta):
        chapter_output_dir = os.path.join(self.output_dir, "{}-sentences.json".format(chapter_meta['id']))
        content = read_md_file(os.path.join(self.book_dir, chapter_file))
        sentences = SentenceProcessor(
            content,
            self.mappings_processor,
            chapter_meta['id'],
            self.current_sentence_id,
            self.current_paragraph_id
        ).process_sentences()
        write_json({'sentences': sentences}, chapter_output_dir)

        toc_processor = TOCProcessor(content, self.output_dir, chapter_meta['id'])
        toc_processor.process_toc()

        self.mappings_processor.add_book_chapter(self.book_id, chapter_meta['id'])
        self.current_sentence_id = sentences[-1]['id']
        self.current_paragraph_id = sentences[-1]['paragraph']

    def write_chapters_json(self):
        chapters_json_path = os.path.join(self.output_dir, 'chapters.json')
        write_json({'chapters': self.chapters_meta}, chapters_json_path)
