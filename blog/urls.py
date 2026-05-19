from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('books/', views.BookViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('books/<int:pk>/', views.BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('borrowings/', views.BorrowingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('borrowings/<int:pk>/', views.BorrowingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('borrowings/borrow/', views.BorrowingViewSet.as_view({'post': 'borrow'})),
    path('borrowings/<int:pk>/return_book/', views.BorrowingViewSet.as_view({'post': 'return_book'})),
]