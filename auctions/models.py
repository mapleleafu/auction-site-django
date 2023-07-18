from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListings', blank=True, related_name='watchlisted_by')


class AuctionListings(models.Model):
    CATEGORY_CHOICES = sorted([
        ('art', 'Art'),
        ('automotive', 'Automotive'),
        ('beauty', 'Beauty'),
        ('books', 'Books'),
        ('collectibles', 'Collectibles'),
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('fitness', 'Fitness'),
        ('home', 'Home'),
        ('jewelry', 'Jewelry'),
        ('outdoor', 'Outdoor'),
        ('sports', 'Sports'),
        ('toys', 'Toys'),
    ], key=lambda x: x[1])

    title = models.CharField(max_length=200)    
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=600, null=True, blank=True, default=None)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_timestamp = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"[Bid is active: {self.is_active}] [Title: {self.title}] [Created at: {formatted_timestamp}]"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", default=1)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids", default=1)
    bid = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[User: {self.user.username}] [Bid: {self.bid}] [Auction Title: {self.listing.title}] [Created at: {formatted_timestamp}]"


class Comments(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)

    def __str__(self):
        return f"[User: {self.user.username}] [Description: {self.description}]"


