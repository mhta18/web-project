from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Listing, Watchlist,Bid,Comment
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import User


def index(request):
    listings = Listing.objects.filter(is_active = True)
    return render(request, "auctions/index.html",{'listings' : listings})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invallist_num username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def  create_new_list(request):
        if request.method == "POST":
            # Attempt to sign user in
            title = request.POST.get("title")
            category = request.POST.get("category")
            description = request.POST.get("description")
            starting_blist_num = request.POST.get("cost")
            image_url = request.POST.get("image")
            today = date.today()


            new_listing = Listing(
                title=title,
                category=category,
                description=description,
                current_price=starting_blist_num,
                image_url=image_url,
                created_at = today,
            )
            new_listing.save()
            
           
            return redirect('index') 
        return render(request, "auctions/create_new_list.html") 
        

def watchlist_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    watchlist = Watchlist.objects.filter(user=request.user).first()

    if not watchlist:
        messages.info(request, "You don't have any items in your watchlist yet.")
        return render(request, "auctions/watchlist.html", {"watchlist": None})
    
    return render(request, 'auctions/watchlist.html', {'listings': watchlist.listings.all()})

def add_to_watchlist(request, listing_list_num):
    listing = Listing.objects.get(list_num=listing_list_num)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)
    return render(request,'auctions/watchlist.html', {'listings': watchlist.listings.all()})

def listing_detail(request, listing_list_num):
    item_bids = None
    item = get_object_or_404(Listing, list_num=listing_list_num)
    if request.user == item.owner:
        item_bids = Bid.objects.filter(listing=item) 
    return render(request, "auctions/page_list.html", {"item": item, "item_bids": item_bids })

def remove_item(request, listing_list_num):
    listing = get_object_or_404(Listing, list_num=listing_list_num)
    # Get the user's watchlist
    watchlist = Watchlist.objects.get_or_create(user=request.user)[0]  # Ensure watchlist exists  
    # Remove the listing from the watchlist
    watchlist.listings.remove(listing)
    return redirect('index')  # Redirect after removal
    
def save_bid(request,listing_list_num):
        # Check if user is authenticated
        if request.method == "POST":
            if not request.user.is_authenticated:
                return redirect("login")  # Redirect to login page if user is not logged in

            # Check if the user exists in the database
            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                 return render(request, "auctions/error.html", {
                "message": "User does not exist."
            })
                
            item = get_object_or_404(Listing, list_num=listing_list_num)
            bid_amount = request.POST.get("bid_suggestion")

            if not bid_amount:
                return render(request, "auctions/error.html", {
                    "message": "Text box is empty",
                    "item": item
                })

            try:
                bid = float(bid_amount)
            except ValueError:
                return render(request, "auctions/error.html", {
                    "message": "Invalid bid",
                    "item": item
                })
                
            

            if bid <= item.current_price:
                return render(request, "auctions/error.html", {
                    "message": "Bid must be higher than the current price.",
                    "item": item
                })
                

        # Save the blist_num
        new_bid = Bid(user=user, listing=item, amount=bid)
        new_bid.save()

        # Update the listing's current price
        messages.success(request, "Your bid was placed successfully!")
        return redirect("page_list", listing_list_num=item.list_num)

def filter_by_category(request, category_name) :
    listings = Listing.objects.filter(category = category_name)
    return render(request, "auctions/index.html",{'listings' : listings, "category": category_name})
  
def close_the_list(request,listing_list_num):
    # Get the listing
    listing = get_object_or_404(Listing, list_num=listing_list_num)

    # Ensure the logged-in user is the owner of the listing
    if request.user != listing.owner:
        return redirect("index")  # Prevent unauthorized access

    # Find the highest bid for this listing
    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()

    if highest_bid and listing.is_closed == False:  # If there were bids
        listing.winner = highest_bid.user  # Assign winner
        listing.is_closed = True  # Mark as closed
    
        listing.current_price = highest_bid.amount
        listing.save()  # Save the updated listing


        return render(request, "auctions/page_list.html", {
                    "item": listing,
                    "highest_bid": highest_bid
                })
    return redirect("page_list", listing_list_num= listing.list_num)

def submit_comment(request,listing_list_num):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return redirect("login")  # Redirect to login page if user is not logged in
            
            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                return render(request, "auctions/error.html", {
                    "message": "User does not exist.",
                })

            item = get_object_or_404(Listing, list_num=listing_list_num)
            comment = request.POST.get("comment")
        if comment:
            new_comment = Comment(content = comment,user=user,listing = item)
            new_comment.save()
        return redirect("page_list", listing_list_num= item.list_num)