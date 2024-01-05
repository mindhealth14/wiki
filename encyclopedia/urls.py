from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.detail_page, name='title'),
    path("addpage/", views.create_entry, name='addpage'),
    path('randompage/', views.random_page, name='randompage'),
    path('edit/<str:title>/', views.edit_page, name='editpage'),
    path('delete/<str:title>', views.delete_entry, name='delete'),
    path('pagenotfound/', views.page_not_found, name='error_page'),
    path('search/', views.search_v, name='search'),
    
]
