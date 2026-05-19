from django.db import transaction
from .models import Book, Borrowing


def borrow_book(data):
    with transaction.atomic():
        book = Book.objects.select_for_update().get(id=data["book"])

        if book.available_copies <= 0:
            return {"error": "Book not available"}

        borrowing = Borrowing.objects.create(
            user_id=data["user"],
            book=book,
            due_date=data["due_date"],
            status = ["ACTIVE"]
        )

        book.available_copies -= 1
        book.save()

        return {"success": True, "id": borrowing.id}