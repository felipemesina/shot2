from __future__ import unicode_literals
from django.db import models
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(username = post_data['username'])) > 0:
            user = self.filter(username = post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Invalid Email/Password')
        else:
            errors.append('Invalid Email/Password')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        if len(post_data['name']) < 3:
            errors.append('Username must be at least 3 characters')
        if len(post_data['username']) < 3:
            errors.append('Username must be at least 3 characters')
        if len(post_data['password']) < 8:
            errors.append('password must be at least 8 characters long')
        if post_data['password'] != post_data['confirm_password']:
            errors.append('passwords do not match')

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name = post_data['name'],
                username = post_data['username'],
                password = hashed
            )
            return new_user
        return errors

class ItemManager(models.Manager):
    def validate_item(self, post_data):
        errors = []
        if len(post_data['item']) == 0:
            errors.append('Item is required.')
        if len(post_data['item']) < 3:
            errors.append('Item name must be at least 3 characters.')

        return errors


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_hired = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.username

class Item(models.Model):
    item = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, related_name="added_item")
    users = models.ManyToManyField(User, related_name="items")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
