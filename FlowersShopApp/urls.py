from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("sobre_nosotros/", AboutUs.as_view(), name="about"),
    path("registro/", Register.as_view(), name="register"),
    path("inicia_sesion/", LogIn.as_view(), name="login"),
    path("tienda/", Shop.as_view(), name="shop"),
    path("cerrar_sesion/", LogOut.as_view(), name="logout"),
    path("flor/<int:pk>/", DetailFlower.as_view(), name="detail_flower"),
    path("carrito/", ShoppingCart.as_view(), name="cart"),
    path("carrito/eliminar/<int:producto_id>", DeleteFlower.as_view(), name="eliminar")
]