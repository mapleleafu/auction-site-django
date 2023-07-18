from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

from .models import User, AuctionListings, Bids, Comments


def index(request):
    auctions = AuctionListings.objects.filter(is_active=True).annotate(highest_bid=Max('bids__bid'))
    if not auctions:
        messages.info(request, "No Active Listings.")

    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })

def categories_no_arg(request):
    categories = AuctionListings.CATEGORY_CHOICES
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)


def categories_with_arg(request, category):
    auctions = AuctionListings.objects.filter(category=category, is_active=True)
    if not auctions:
        messages.info(request, "No auctions found in this category.")
    return render(request, "auctions/categories.html", {
        "auctions": auctions,
        "category": category
    })



def create_listing(request):
    categories = AuctionListings.CATEGORY_CHOICES
    context = {'categories': categories}

    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please log in.")
            return HttpResponseRedirect(reverse('login'))

        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]

        listing = AuctionListings(
            title=title,
            description=description,
            image_url=image_url,
            starting_bid=starting_bid,
            category=category,
            user=user
        )
        listing.save()

        return HttpResponseRedirect(reverse('listing', args=[listing.pk]))

    return render(request, 'auctions/create_listing.html', context)


def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please log in.")
            return HttpResponseRedirect(reverse('login'))
        description = request.POST["description"]

        if not description:
            return render(request, "auctions/comment.html", {"auction": AuctionListings.objects.get(id=listing_id)})


        Comments.objects.create(
            description=description,
            user=request.user,
            auction=AuctionListings.objects.get(id=listing_id)
        )

        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, "auctions/comment.html", {"auction": AuctionListings.objects.get(id=listing_id)})

def watchlist(request):
    user = request.user
    watchlist_items = None
    can_bid = {}

    if request.method == "POST":
        if not user.is_authenticated:
            messages.error(request, "Please log in.")
            return HttpResponseRedirect(reverse('login'))

        listing_id = request.POST.get('listing_id')
        listing = AuctionListings.objects.get(pk=listing_id)
        action = request.POST.get('action')

        if action == 'add':
            user.watchlist.add(listing)  
        elif action == 'remove':
            user.watchlist.remove(listing)  

        is_in_watchlist = user.watchlist.filter(pk=listing_id).exists()

        return HttpResponseRedirect(reverse('listing', args=[listing.pk]), {'is_in_watchlist': is_in_watchlist})

    else: 
        if user.is_authenticated:
            watchlist_items = user.watchlist.all().annotate(highest_bid=Max('bids__bid'))
            
            if not watchlist_items:
                messages.info(request, "Your watchlist is empty.")

            for item in watchlist_items:
                item.can_bid = item.is_active and user.is_authenticated
                try:
                    last_bid = item.bids.order_by('-bid').first() 
                    if last_bid and last_bid.user == user and not item.is_active:
                        item.won_auction = True
                    else:
                        item.won_auction = False
                except:
                    item.won_auction = False
                
    return render(request, "auctions/watchlist.html", {'watchlist_items': watchlist_items, 'can_bid': can_bid})

def listing(request, listing_id):
    auction = get_object_or_404(AuctionListings, id=listing_id)
    user = request.user
    is_in_watchlist = False 
    message = None

    if user.is_authenticated:
        is_in_watchlist = user.watchlist.filter(pk=listing_id).exists()


    auction_active = auction.is_active 
    can_bid = auction.is_active and user.is_authenticated
    log_to_bid = auction.is_active and not user.is_authenticated
    highest_bid = auction.bids.order_by('-bid').first()

    if highest_bid and highest_bid.user == user and not auction.is_active:
        messages.success(request, "You won this auction!")
    elif not auction.is_active:
        messages.info(request, "This auction has finished.")


    try:
        if request.method == "POST":
            if 'close_auction' in request.POST:
                if request.user == auction.user:
                    auction.is_active = False
                    auction.save()
                    messages.success(request, "You've successfully closed this auction!")
                else:
                    messages.error(request, "Only the owner of the auction can close it.")
                return HttpResponseRedirect(reverse('listing', args=[auction.id]))

            if not can_bid:
                messages.error(request, "Bidding is not allowed on this auction.")
                return HttpResponseRedirect(reverse('listing', args=[auction.id]))
                
            bid = float(request.POST["bid"])
            starting_bid = auction.starting_bid

            if not highest_bid:
                if bid >= starting_bid:
                    new_bid = Bids.objects.create(bid=bid, user=request.user, listing=auction)
                    new_bid.save()
                    messages.success(request, "You've placed your bid!")
                else:
                    messages.error(request, "Your bid should be at least the starting bid.")
            else:
                if bid > highest_bid.bid:
                    new_bid = Bids.objects.create(bid=bid, user=request.user, listing=auction)
                    new_bid.save()
                    messages.success(request, "You've placed your bid!")
                else:
                    messages.error(request, "Your bid should be higher than the current bid.")   
                    
            return HttpResponseRedirect(reverse('listing', args=[auction.id]))

    except ValueError:
        messages.error(request, "Enter your bid please.")
        return HttpResponseRedirect(reverse('listing', args=[auction.id]))
    else:
        return render(request, "auctions/listing.html",{
            "auction": auction,
            "highest_bid": highest_bid,
            "comments": Comments.objects.filter(auction_id=listing_id),
            "comments_count": Comments.objects.filter(auction_id=listing_id).count(),
            "is_in_watchlist": is_in_watchlist,
            "can_bid": can_bid,
            "auction_active": auction_active,
            "log_to_bid": log_to_bid,
        }) 


def login_view(request):
    if request.method == "POST":    
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return HttpResponseRedirect(reverse('register'))
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return HttpResponseRedirect(reverse('register'))
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")