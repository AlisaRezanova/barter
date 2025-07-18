from django.urls import path
from . import views

urlpatterns = [
    path('edit_ad/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete_ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('search_by_title_and_description/', views.search_by_title_and_description, name='search_by_title_and_description'),
    path('filter_by_/', views.filter_by_, name='filter_by_'),
    path('add_exchange_proposal/', views.add_exchange_proposal, name='add_exchange_proposal'),
    path('update_status/<int:proposal_id>/', views.update_status, name='update_status'),
    path('filter_proposal_by/', views.filter_proposal_by, name='filter_proposal_by'),
    path('show_ads/', views.show_ads, name='show_ads'),
    path('add_ad/', views.add_ad, name='add_ad'),
]