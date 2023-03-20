from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, Comment, Bid

# can reduce the size of code if we could declare "categories":Category.objects.all() as global

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(is_active=True),
        "categories": Category.objects.all(), # this required everywhere to display list of category 
        "message": "Active Listings"
        })


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
                "message": "Invalid username and/or password."
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

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/createListing.html", {
            "categories": Category.objects.all()
            })
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        imageURL = request.POST.get("imageurl")
        initialPrice = request.POST.get("bid")
        category_name = request.POST.get("category")
        category = Category.objects.get(category_name=category_name)
        currentUser = request.user

        # uploading the bid(price)
        bid = Bid(
            bidder = currentUser,
            amount = initialPrice
        )
        bid.save()

        # uploading the listing       
        newListing = Listings(
            title = title,
            description = description,
            image = imageURL,
            price = bid,
            category = category,
            owner = currentUser
        )

        newListing.save()

        return HttpResponseRedirect(reverse("index"))

def listings(request, id):
    # flight = Flight.objects.get(id=flight_id)
    # passengers = flight.passengers.all()
    # a lot of things going on checks for winner, checks for highest bidder to handle the get requests
    listing = Listings.objects.get(pk=id) # get the listing
    users_in_watchlist = listing.watchlist.all() # knowing which user is in the watchlist
    user_in_watchlist = request.user in users_in_watchlist # returns true or false
    allComment = Comment.objects.filter(item=listing).order_by('-time') # .order_by(-time) sorting the comments in descending(recent first) order
    current_user = request.user
    winner = ""
    if current_user == listing.price.bidder:
        alert = "You have the current bid."
    elif listing.price.bidder == listing.owner:
        alert="No bids yet."
    else:
        alert = f"{listing.price.bidder} has the current bid."

    is_owner = False
    if current_user == listing.owner:
        is_owner = True
    
    if not listing.is_active and current_user == listing.winner:
        winner = f"Congratulations you have won this auction with the bid of ${listing.price.amount}"

    return render(request, "auctions/listings.html", {
        "listing": listing,
        "categories": Category.objects.all(),
        "user_watchlist": user_in_watchlist,
        "allComment": allComment,
        "message":alert,
        "is_owner":is_owner,
        "winner": winner
    })

def closeAuction(request, id):
    # closes the auctions and inactivates the product
    if request.method=="POST":
        listing = Listings.objects.get(pk=id)
        highest_bidder = listing.price.bidder
        listing.is_active = False
        listing.winner = highest_bidder
        listing.save()
    return HttpResponseRedirect(reverse("index"))

def closed(request):
    # returns all closed listings
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(is_active=False),
        "categories": Category.objects.all(),
        "message": "Closed Listings"
        })

def addWatchlist(request, id):
    # adds to watchlist
    listing = Listings.objects.get(pk=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listings", args=(id, )))

def removeWatchlist(request, id):
    # removes form watchlist
    listing = Listings.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listings", args=(id, )))

def addComment(request, id):
    # ez comments
    listing = Listings.objects.get(pk=id)
    message = request.POST.get("comment")
    user = request.user
    newComment = Comment(
        commenter=user,
        comment=message,
        item=listing
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listings", args=(id, )))

def addBid(request, id):
    # ez bids
    listing = Listings.objects.get(pk=id)
    current_user = request.user
    if request.method == "POST":
        bid_price = request.POST.get("bidPrice")
        current_price = listing.price.amount
        
        if float(bid_price) > float(current_price):
            new_bid = Bid(
                bidder=current_user,
                amount=bid_price
            )
            new_bid.save()

            listing.price = new_bid
            listing.save()
            # message="Your is the current bid."
            alert="Bid successfully placed."
        else:
            alert="Bid could not be placed."
            # message=f"{listing.price.bidder} has the current bid. Make a bid to surpass it!!"
        return render(request, "auctions/listings.html", {
                "message": alert,
                "categories": Category.objects.all(),
                "listing": listing
            })
        

def seeWatchlist(request):
    # returns the watchlist in index.html
    listing = Listings.objects.filter(is_active=True, watchlist=request.user)
    return render(request, "auctions/index.html", {
        "listings": listing,
        "message": "Watchlist",
        "categories": Category.objects.all()
    })

def display_category(request, category):
    # displays the selected category listings when a certain is clicked from the drop down
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(is_active=True, category=Category.objects.get(category_name=category)),
        "message": "Active Listings",
        "categories": Category.objects.all()
    })