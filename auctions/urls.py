from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing/', views.create_listing, name='create_listing'),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path('listing/', views.listing, name='listing'),
    path('categories/', views.categories_no_arg, name='categories_no_arg'),
    path('categories/<str:category>', views.categories_with_arg, name='categories_with_arg'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path("listing/<int:listing_id>", views.listing, name="listing")
]
