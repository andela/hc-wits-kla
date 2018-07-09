from django.conf.urls import url

from hc.api import views

urlpatterns = [
    url(r'^ping/([\w-]+)/$', views.ping, name="hc-ping-slash"),
    url(r'^ping/([\w-]+)$', views.ping, name="hc-ping"),
    url(r'^api/v1/checks/$', views.checks),
    url(r'^api/v1/checks/([\w-]+)/pause$', views.pause, name="hc-api-pause"),
    url(r'^badge/([\w-]+)/([\w-]{8})/([\w-]+).svg$', views.badge, name="hc-badge"),
    url(r'^allocate_jobs/$', views.allocate_jobs, name = "allocate-jobs"),
    url(r'^view_assigned_jobs/$', views.view_assigned_jobs, name="hc-view-assigned-jobs"),
]
