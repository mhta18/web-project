from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.timezone import now


class User(AbstractUser):
    pass   

def get_default_user():
    """Return the ID of the default user, creating one if needed."""
    user, created = User.objects.get_or_create(username="default_user")
    return user.id
    
class Listing(models.Model):    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100,default="other")
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    list_num = models.PositiveIntegerField(unique=True, blank=True)
    is_closed = models.BooleanField(default=False)  
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default= get_default_user) 
    
    def save(self, *args, **kwargs):
        if not self.list_num:
            existing_numbers = set(Listing.objects.values_list('list_num', flat=True))
            new_number = 1
            while new_number in existing_numbers:
                new_number += 1  # Find the lowest available number
            self.list_num = new_number  # Assign the lowest available number
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.list_num}: {self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, related_name='watchlisted_by')
    added_at = models.DateTimeField(default=timezone.now) 

        

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Bidder
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField(default="text")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Bidder
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_by")