from django.contrib import admin
from .models import User, Review, Title, Comment, Genre, Category


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
