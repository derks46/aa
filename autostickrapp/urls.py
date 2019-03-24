from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('marca/<pk>/', views.detalle_marca, name='detalle_marca'),
    path('email/', views.emailView, name='email'),
    path('success/', views.successView, name='success'),
    path('usuario/nuevo',views.register_user, name='register_user'),
    path('usuario/nuevo/confirmar/<activation_key>',views.register_confirm, name='register_confirm'),
    path('usuario/nuevo/confirmar',views.register_confirm, name='register_confirm'),
    path('exito/',views.exito, name='exito'),
    path('logout/',views.logout_view, name='logout'),
    path('usuario/',views.detalle_usuario, name='detalle_usuario'),
    url(r'^login/$',auth_views.login,
    	{
    		'template_name': 'auth/login.html',
    		'redirect_authenticated_user': True,
    	},
    	name='auth_login',
    	),
    url(
    r'^dashboard/$',
    views.DashboardView.as_view(),
    name='dashboard',
),
    
]

