from book_processor.book import BookProcessor
from config import BOOKS_DIR, OUTPUT_DIR

def main():
    processor = BookProcessor(BOOKS_DIR, OUTPUT_DIR)
    processor.process_books()

if __name__ == "__main__":
    main()
