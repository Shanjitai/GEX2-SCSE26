from admin import (
    load_library,
    save_library,
    find_book,
    display_books,
    display_loans,
    library_statistics,
)


def books_in_category(books, category):
    """Return list of book IDs matching category (case-insensitive)."""
    if not category:
        return []
    category_lower = category.strip().lower()
    result = []
    for book_id, book in books.items():
        if book.get('category', '').lower() == category_lower:
            result.append(book_id)
    return result


def search_by_title(books, search_text):
    """Return list of book IDs whose title contains search_text (case-insensitive)."""
    if not search_text:
        return []
    search_lower = search_text.strip().lower()
    result = []
    for book_id, book in books.items():
        if search_lower in book.get('title', '').lower():
            result.append(book_id)
    return result


def borrow_book(books, loans, search_text, borrower):
    """Borrow a book. Returns OK, EMPTY_NAME, BOOK_NOT_FOUND, NOT_AVAILABLE."""
    if not borrower or not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not books[book_id].get('available', False):
        return "NOT_AVAILABLE"

    books[book_id]['available'] = False
    loans.append({
        'book_id': book_id,
        'borrower': borrower.strip()
    })
    return "OK"


def return_book(books, loans, book_title, borrower):
    """Return a book. Returns OK, EMPTY_NAME, BOOK_NOT_FOUND, NOT_ON_LOAN."""
    if not borrower or not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    borrower_lower = borrower.strip().lower()
    for i, loan in enumerate(loans):
        if (loan.get('book_id') == book_id and
                loan.get('borrower', '').strip().lower() == borrower_lower):
            loans.pop(i)
            books[book_id]['available'] = True
            return "OK"

    return "NOT_ON_LOAN"


def main():
    """User interface for the library system."""
    filename = "library.json"
    data = load_library(filename)
    books = data.get('books', {})
    loans = data.get('loans', [])

    while True:
        print("\nLIBRARY USER SYSTEM")
        print("=" * 60)
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_text = input("Enter title (or part): ").strip()
            results = search_by_title(books, search_text)
            if results:
                print("Matching book IDs:", ", ".join(results))
            else:
                print("No books found.")
        elif choice == "2":
            category = input("Enter category: ").strip()
            results = books_in_category(books, category)
            if results:
                print("Matching book IDs:", ", ".join(results))
            else:
                print("No books found.")
        elif choice == "3":
            search_text = input("Enter book ID, title, or author: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = borrow_book(books, loans, search_text, borrower)
            print(f"Result: {result}")
        elif choice == "4":
            search_text = input("Enter book ID, title, or author: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = return_book(books, loans, search_text, borrower)
            print(f"Result: {result}")
        elif choice == "5":
            save_library(data, filename)
            print("Library data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()