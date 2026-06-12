from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegisterView, LoginView

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'borrowings', views.BorrowingViewSet, basename='borrowing')

urlpatterns = [

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/borrowings/borrow/', views.BorrowingViewSet.as_view({'post': 'borrow'}), name='borrowing-borrow'),
    path('api/borrowings/<int:pk>/return_book/', views.BorrowingViewSet.as_view({'post': 'return_book'}), name='borrowing-return-book'),
    path('api/', include(router.urls)),


]

