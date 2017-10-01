from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login_view),
    url(r'^success/$', views.success),
    url(r'^logout/$', views.logout),
    url(r'^home/$', views.home),
    url(r'^items/$', views.items),
    url(r'^items/add/$', views.add_item),
    url(r'^show/(?P<id>\d+)/$', views.show),
    url(r'^delete/(?P<item_id>\d+)/$', views.delete),
    url(r'^add_to_wishlist/(?P<item_id>\d+)/$', views.add_to_wishlist),
    url(r'^remove/(?P<item_id>\d+)/$', views.remove),



]
