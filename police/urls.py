from django.urls import path,include
from police import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.login, name='policelogin'),
    path('/home',views.policehome,name='policehome'),
    path('/logout',views.logout,name='policelogout'),
    path('/register',views.register,name='register'),
    path('/dashboard',views.dashboard,name='dashboard'),
    path('/search',views.search,name='search'),
    path('/notifications',views.notifications,name='search'),
    path('/posts/<str:slug>',views.posts,name='posts'),
    path('/dashDetail/<str:slug>',views.dashDetail,name='dashDetail'),
    path('/pdf/<str:slug>',views.reportPDF,name='reportPDF'),
    path('/update_status/<str:slug>',views.update_status, name='update_status'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)