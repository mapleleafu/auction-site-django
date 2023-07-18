# eBay-like E-Commerce Auction Site

This project is an **eBay-like e-commerce auction site** developed as Project 2 of HarvardX's *"CS50’s Web Programming with Python and JavaScript"* course. The site allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a watchlist. The project was built using **Python, Django, CSS, and HTML**.

## Specification

This project was built against the following specification:

### Models

The application includes the following models in addition to the User model:

- **Auction Listings**: Represents the auction listings with fields like *title*, *description*, *starting bid*, *image URL*, and *category*.
- **Bids**: Represents the bids made on auction listings.
- **Comments**: Represents the comments made on auction listings.


### Create Listing

Users can visit a page to create a new listing. The create listing page allows users to specify a *title*, a *text-based description*, and the *starting bid* for the listing. Optionally, users can provide an *image URL* and select a *category* for the listing, such as *Fashion, Sports, Electronics, Art*, etc.

### Active Listings Page

The default route of the web application displays all currently active auction listings. For each active listing, the page should display the *title*, *description*, *current price*, and a *photo* (if available).

### Listing Page

Clicking on a listing takes users to a page dedicated to that listing. On this page, users can view all details about the listing, including the *current price*. 

- If the user is signed in, they can *add the item to their watchlist*. If the item is already on the watchlist, the user can *remove it*.
- If the user is signed in, they can *place a bid on the item*. The bid must be at least as large as the starting bid and greater than any previous bids. Otherwise, an error is presented.
- If the user is signed in and is the *creator of the listing*, they can *"close" the auction*, declaring the highest bidder as the winner and making the listing inactive.
- On a closed listing page, if the signed-in user has *won the auction*, the page indicates so.

Users who are signed in can *add comments* to the listing page. The listing page should display all comments made on the listing.

### Watchlist

Signed-in users have access to a Watchlist page that displays all listings they have added to their watchlist. Clicking on any of the listings takes the user to the specific listing page.

### Categories

Users can visit a page displaying a list of all listing categories. Clicking on a category name takes the user to a page showing all active listings in that category.

### Django Admin Interface

The Django admin interface provides site administrators with the ability to view, add, edit, and delete listings, comments, and bids on the site.

## Installation and Usage

To run the project locally, follow these steps:

1. Clone the repository.
2. Install Python and Django if not already installed.
3. Set up a virtual environment (recommended).
4. Run the database migrations.
5. Start the Django development server.
6. Access the application through the provided URL.