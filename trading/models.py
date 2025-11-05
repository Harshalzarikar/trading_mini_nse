from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile with wallet functionality
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    wallet_balance = models.FloatField(default=100000.00)  # Starting virtual money
    total_invested = models.FloatField(default=0.00)
    total_profit_loss = models.FloatField(default=0.00)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Represents a single stock available for trading
class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, unique=True)
    current_price = models.FloatField()
    purchase_price = models.FloatField(null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    day_high = models.FloatField(null=True, blank=True)
    day_low = models.FloatField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    change_percent = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

# Represents a user's holding of a particular stock
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    avg_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}'s portfolio for {self.stock.symbol}"

# Logs every transaction (buy or sell) made by a user
class Transaction(models.Model):
    TYPE_CHOICES = (('BUY', 'Buy'), ('SELL', 'Sell'))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} {self.quantity} of {self.stock.symbol} by {self.user.username}"

# Watchlist - Users can save stocks to watch
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'stock')
    
    def __str__(self):
        return f"{self.user.username} watching {self.stock.symbol}"

# Price Alerts - Get notified when stock reaches target price
class PriceAlert(models.Model):
    ALERT_TYPES = (
        ('ABOVE', 'Price Above'),
        ('BELOW', 'Price Below'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    target_price = models.FloatField()
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    is_active = models.BooleanField(default=True)
    triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Alert: {self.stock.symbol} {self.alert_type} ₹{self.target_price}"