import json


def load_library(filename):
    """Load library data from JSON file and return it."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_library(data, filename):
    """Save library data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def find_book(books, search_text):
    """Find book by ID, title, or author. Return book ID or None."""
    if not search_text:
        return None
    search_lower = search_text.strip().lower()
    for book_id, book in books.items():
        if (search_lower == book_id.lower() or
                search_lower in book.get('title', '').lower() or
                search_lower in book.get('author', '').lower()):
            return book_id
    return None


def display_books(books):
    """Display book catalogue."""
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        title = book.get('title', '')
        category = book.get('category', '')
        available = book.get('available', False)
        status = "AVAILABLE" if available else "ON LOAN"
        print(f"{book_id} | {title} | {category} | {status}")


def display_loans(loans, books):
    """Display current loans."""
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan.get('book_id')
        borrower = loan.get('borrower', '')
        if book_id in books:
            title = books[book_id].get('title', '')
            print(f"{book_id} | {title} | Borrower: {borrower}")


def library_statistics(books):
    """Return total, available, borrowed counts as a tuple."""
    total = len(books)
    available = sum(1 for book in books.values() if book.get('available', False))
    borrowed = total - available
    return total, available, borrowed


def main():
    """Display the full library administration interface."""
    data = load_library("library.json")
    library_info = data.get('library', {})
    categories = data.get('categories', [])
    books = data.get('books', {})
    loans = data.get('loans', [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library_info.get('name', '')}")
    print(f"Branch: {library_info.get('branch', '')}")
    print(f"Year: {library_info.get('year', '')}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()
    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)
    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()