from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_list_num>/", views.listing_detail, name="page_list"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("create_new_list", views.create_new_list, name="create_new_list"),
    path("add_to_watchlist/<int:listing_list_num>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_item/<int:listing_list_num>/",views.remove_item,name="remove_item"),
    path("save_bid/<int:listing_list_num>/", views.save_bid, name="save_bid"),
    path("category/<str:category_name>/", views.filter_by_category, name="filter_by_category"),
    path("list_closed/<int:listing_list_num>/", views.close_the_list, name="list_closed"),
    path("submit_comment/<int:listing_list_num>/", views.submit_comment, name="submit_comment"),
    
]
