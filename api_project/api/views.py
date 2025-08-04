from django.shortcuts import render
# from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import BookSerializer
from .models import Book

# Create your views here.

# class BookList(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]