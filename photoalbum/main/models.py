from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=70, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.description