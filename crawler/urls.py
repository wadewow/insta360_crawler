from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sales_status/$', views.sales_status, name='sales_status'),
    url(r'^electronic_sales/$', views.electronic_sales, name='electronic_sales'),
    url(r'^get_sales_status/$', views.get_sales_status, name='get_sales_status'),
    url(r'^get_electronic_sales/$', views.get_electronic_sales, name='get_electronic_sales'),
    url(r'^user_distribution/$', views.user_distribution, name='user_distribution'),
    url(r'^user_area/$', views.user_area, name='user_area'),
    url(r'^use_condition/$', views.use_condition, name='use_condition'),
    url(r'^search_index/$', views.search_index, name='search_index'),
    url(r'^error_condition/$', views.error_condition, name='error_condition'),
    url(r'^market_environment/$', views.market_environment, name='market_environment'),
    url(r'^competitor_data/$', views.competitor_data, name='competitor_data'),
    url(r'^login/$', views.login, name='login'),
    url(r'^test/$', views.test, name='test'),

]