from django.contrib import admin
from .models import Listing , Watchlist,User,Bid,Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Bid) 
admin.site.register(Comment) 