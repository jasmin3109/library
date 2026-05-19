from django.contrib import admin
# Register your models here.
from .models import User, Category, Book, Borrowing

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Borrowing)