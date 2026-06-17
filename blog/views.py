from rest_framework import viewsets, status
from .models import User, Category, Book, Borrowing
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import render
from django.db import transaction
import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .serializers import (
    UserSerializer,
    CategorySerializer,
    BookSerializer,
    BorrowingSerializer
)
from .services import borrow_book


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz. Qoyil",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        data = request.data

        result = borrow_book(data)

        if "error" in result:
            return Response(
                {"error": result["error"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Book borrowed successfully", "id": result["id"]},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        try:
            with transaction.atomic():
                borrowing = Borrowing.objects.select_for_update().get(id=pk)

                if borrowing.status != "ACTIVE":
                    return Response(
                        {"error": "Already returned or not active"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                borrowing.status = "RETURNED"
                borrowing.return_date = timezone.now().date()
                borrowing.save()

                book = borrowing.book
                book.available_copies += 1
                book.save()

                return Response(
                    {"message": "Book returned successfully"}
                )

        except Borrowing.DoesNotExist:
            return Response(
                {"error": "Borrowing not found"},
                status=status.HTTP_404_NOT_FOUND

            )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("books")

        if cached_data:
            return Response(cached_data)

        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)

        cache.set("books", serializer.data, timeout=60 * 5)

        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token_key = str(uuid.uuid4())
            return Response({
                "status": "success",
                "message": "Muvaffaqiyatli tizimga kirdingiz!",
                "token": token_key,
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "role": user.role
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

