import os
from .utils import write_json

class TOCProcessor:
    def __init__(self, content, output_dir, chapter_id):
        self.content = content
        self.output_dir = output_dir
        self.chapter_id = chapter_id
        self.toc = []

    def process_toc(self):
        lines = self.content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                level = line.count('#')
                title = line.replace('#', '').strip()
                self.toc.append({
                    'sentenceId': i + 1,
                    'title': title,
                    'paragraphs': {'start': i, 'end': i + 1},
                    'level': level,
                    'subheadings': []
                })
        self.write_toc_json()

    def write_toc_json(self):
        toc_json_path = os.path.join(self.output_dir, '{}-toc.json'.format(self.chapter_id))
        write_json({'toc': self.toc}, toc_json_path)
