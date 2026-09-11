class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year


class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = []

    def add_book(self, book):
        """
        Ajoute un livre à la bibliothèque.

        Args:
            book: Le livre à ajouter.
        """
        self.books.append(book)

    def remove_book(self, book_title):
        """
        Supprime un livre de la bibliothèque.

        Args:
            book_title : Le titre du livre à supprimer.
        """
        for book in self.books:
            if book.title == book_title:
                self.books.remove(book)
                return
        print(f"Le livre '{book_title}' n'est pas dans la bibliothèque.")

    def borrow_book(self, book_title):
        """
        Emprunte un livre disponible de la bibliothèque.

        Args:
            book_title : Le titre du livre à emprunter.
        """
        for book in self.books:
            if book.title == book_title:
                self.books.remove(book)
                self.borrowed_books.append(book)
                return
        print(f"Le livre '{book_title}' n'est pas disponible.")

    def return_book(self, book_title):
        """
        Rend un livre emprunté à la bibliothèque.

        Args:
            book_title : Le titre du livre à rendre.
        """
        for book in self.borrowed_books:
            if book.title == book_title:
                self.borrowed_books.remove(book)
                self.books.append(book)
                return
        print(f"Le livre '{book_title}' n'a pas été emprunté ici.")

    def available_books_titles(self):
        """
        Renvoie la liste des titres des livres disponibles.

        Returns:
            list: Liste des titres des livres disponibles.
        """
        return [book.title for book in self.books]

    def borrowed_books_titles(self):
        """
        Renvoie la liste des titres des livres empruntés.

        Returns:
            list: Liste des titres des livres empruntés.
        """
        return [book.title for book in self.borrowed_books]
