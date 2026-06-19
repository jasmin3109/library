from django.db import transaction
from datetime import timedelta
from django.utils import timezone
from .models import Book, Borrowing


def borrow_book(data):
    with transaction.atomic():
        book = Book.objects.select_for_update().get(id=data["book"])

        if book.available_copies <= 0:
            return {"error": "Book not available"}

        borrowing = Borrowing.objects.create(
            user_id=data["user"],
            book=book,
            due_date=data.get(
                "due_date",
                timezone.now().date() + timedelta(days=14)
            ),
            status="ACTIVE"
        )

        book.available_copies -= 1
        book.save()

        return {"success": True, "id": borrowing.id}