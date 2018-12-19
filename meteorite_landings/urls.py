from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),

    # meteorite landing listview
    path('meteorite_landing/', views.MeteoriteLandingListView.as_view(), name='meteorite_landings'),
    path('meteorite_landing/<int:pk>/', views.MeteoriteLandingDetailView.as_view(), name='meteorite_landing_detail'),

    # meteorite class listview
    path('meteorite_class/', views.MeteoriteClassListView.as_view(), name='meteorite_classes'),
    path('meteorite_class/<int:pk>/', views.MeteoriteClassDetailView.as_view(), name='meteorite_class_detail'),

    # country area listview
    path('country_area/', views.CountryAreaListView.as_view(), name='country_area'),
    path('country_area/<int:pk>/', views.CountryAreaDetailView.as_view(), name='country_area_detail'),

    #meteorite landing forms
    path('meteorite_landing/<int:pk>/update/', views.MeteoriteLandingUpdateView.as_view(), name='meteorite_landing_update'),

    # meteorite class forms
    path('meteorite_class/new/', views.MeteoriteClassCreateView.as_view(), name='meteorite_class_new'),
    path('meteorite_class/<int:pk>/delete/', views.MeteoriteClassDeleteView.as_view(), name='meteorite_class_delete'),
    path('meteorite_class/<int:pk>/update/', views.MeteoriteClassUpdateView.as_view(), name='meteorite_class_update'),

    # adding path for filter
    path('meteorite_class/filter/', views.MeteoriteClassFilterView.as_view(), name='meteorite_class_filter')
]
