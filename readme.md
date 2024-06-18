# Book Processor

Book Processor is a Python project designed to process books stored in Markdown files. This project identifies sentences and paragraphs in each book chapter, generates metadata, and creates JSON files with the processed data. The project also includes functionality to map books to chapters, chapters to paragraphs, paragraphs to sentences, and pages to paragraphs.

## Project Structure

```
book_processor/
├── main.py
├── book_processor/
│   ├── __init__.py
│   ├── book.py
│   ├── chapter.py
│   ├── sentence.py
│   ├── toc.py
│   ├── mappings.py
│   ├── utils.py
├── config.py
books/
│   ├── 01-(Book Title 1)/
│   │   ├── 01-(Chapter Title 1).md
│   │   ├── 02-(Chapter Title 2).md
│   ├── 02-(Book Title 2)/
│   │   ├── 01-(Chapter Title 1).md
│   │   ├── 02-(Chapter Title 2).md
output/
    ├── 01-book-title-1/
    │   ├── chapters.json
    │   ├── 01-sentences.json
    │   ├── 02-sentences.json
    │   ├── 01-toc.json
    ├── books.json
    ├── maps/
        ├── books-to-chapters.json
        ├── chapters-to-paragraphs.json
        ├── paragraphs-to-sentences.json
        ├── pages-to-paragraphs.json
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kadirkatirci/book-processor.git
   cd book-processor
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install slugify
   ```

## Configuration

Edit `config.py` to set up your configurations for visible and invisible sentence-ending characters.

## Usage

To process the books and generate the output files, run:

```bash
python3 main.py
```

## How It Works

1. **Books Directory**: Each book is stored in a folder within the `books` directory. The folder name structure is `number-(Book Title)`. Each folder contains Markdown files representing the chapters of the book.

2. **Output Directory**: The processed data will be saved in the `output` directory. This includes JSON files for books, chapters, sentences, table of contents (TOC), and various mappings.

3. **Metadata Extraction**: The script extracts metadata from the folder and file names as well as from the front matter within the Markdown files.

4. **Sentence and Paragraph Extraction**: Sentences and paragraphs are extracted based on visible and invisible sentence-ending characters. Unique IDs are assigned to each sentence and paragraph.

5. **Mappings**: The script generates various mappings:
   - `books-to-chapters.json`: Maps books to their chapters.
   - `chapters-to-paragraphs.json`: Maps chapters to their paragraphs.
   - `paragraphs-to-sentences.json`: Maps paragraphs to their sentences.
   - `pages-to-paragraphs.json`: Maps pages to paragraphs based on special markers in the text.

## Example

Given a book folder `01-(Book Title 1)` with a chapter file `01-(Chapter Title 1).md` containing:

```markdown
---
id: 1
title: Chapter Title 1
slug: chapter-title-1
description: Chapter Description
---

<3>
{2}
This is an example for Table of Content.

# Heading 1 Title

Heading 1 content. Second sentence of heading 1 content.
Second paragraph of heading 1 content.

## Heading 2 Title of first heading 1

Heading 2 content
```

The script will generate corresponding JSON files in the `output` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## Contact

For any questions or comments, please contact [Kadir Katırcı](mailto:katircikadir@gmail.com).

---

Make sure to update the contact information and the repository URL with your actual details before publishing the README file.