from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# To link categories with items
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

# Listing database model
class Listings(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    creation = models.DateTimeField(auto_now_add=True)  
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title} auctioned by {self.owner} going for {self.price.amount}"   



class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="commenter")
    time = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, related_name="item")
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.commenter} commented on {self.time}"