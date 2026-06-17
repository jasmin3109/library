from rest_framework import serializers
from django.db import models
from .models import User, Category, Book, Borrowing
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan. Boshqa raqam kiritin")
        return value
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        if not validated_data.get('role'):
            validated_data['role'] = 'student'
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        phone = data.get("phone").strip()
        password = data.get("password")
        if not phone.startswith('+'):
            phone_with_plus = f"+{phone}"
        else:
            phone_with_plus = phone
            phone = phone.replace('+', '')
        user = User.objects.filter(models.Q(phone=phone) | models.Q(phone=phone_with_plus)).first()
        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi yoki telefon raqam xato!")
        if not check_password(password, user.password):
            raise serializers.ValidationError("Parol noto'g'ri!")
        data["user"] = user
        return data
