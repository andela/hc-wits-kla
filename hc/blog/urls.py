from django.conf.urls import url
from hc.blog import views

urlpatterns = [
    url(r'^my-blogs/$', views.my_posts, name="hc-my-posts"),
    url(r'^add-post/$', views.add_post, name='hc-add-post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='hc-edit-post'),
    url(r'^post/(?P<post_id>\d+)/remove/$',
        views.remove_post, name='hc-remove-post'),
    url(r'^category/add/$', views.add_category, name="hc-add-category"),
    url(r'^blog/$', views.articles_list, name="hc-blog"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)$',
        views.article_detail, name='hc-view-post')
]
