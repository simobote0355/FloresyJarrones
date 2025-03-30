from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from django.contrib import messages 
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Flowers

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

class Register(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        authenticate(self.request, username=user.username, password=form.cleaned_data['password1'])
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Cuenta creada con éxito. Bienvenido, {user.username}!')
        else:
            messages.error(self.request, 'Hubo un problema al iniciar sesión automáticamente.')

        return redirect(self.success_url)

class LogIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Sesión iniciada correctamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

class LogOut(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)

class Shop(ListView):
    model = Flowers
    template_name = "shop/index.html"
    context_object_name = "flowers"

class DetailFlower(DetailView):
    model = Flowers
    template_name = "shop/flower.html"
    context_object_name = "flower"

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para realizar esta acción.")
            # Redirigir al login y luego volver a esta página
            login_url = reverse_lazy('login')  # Asegúrate que 'login' esté definido en tus URLs
            return redirect(f'{login_url}?next={request.path}')

        self.object = self.get_object()
        action = request.POST.get('action')
        cantidad = int(request.POST.get('cantidad', 1))
        mensaje = request.POST.get('mensaje', '')

        item = {
            'id': self.object.pk,
            'nombre': self.object.nombre,
            'precio': float(self.object.precio),
            'cantidad': cantidad,
            'mensaje': mensaje,
            'imagen': self.object.imagen.url if self.object.imagen else '',
        }

        carrito = request.session.get('carrito', [])

        if action == 'carrito':
            carrito.append(item)
            request.session['carrito'] = carrito
            messages.success(request, f'{self.object.nombre} se añadió al carrito.')
            return redirect('cart')

        '''
        elif action == 'comprar':
            request.session['carrito'] = [item]
            messages.info(request, f'Procesando compra de {self.object.nombre}.')
            return redirect('checkout')
            '''
        return redirect('shop')
    
class ShoppingCart(TemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carrito'] = self.request.session.get('carrito', [])
        carrito = context['carrito']

        for item in carrito:
            item["subtotal"] = item['precio'] * item['cantidad']

        context['carrito'] = carrito
        context['total'] = sum(item['subtotal'] for item in carrito)

        return context

class DeleteFlower(View):
    def post(self, request, *args, **kwargs):
        producto_id = int(kwargs.get('producto_id'))
        carrito = request.session.get('carrito', [])
        nuevo_carrito = [item for item in carrito if item.get('id') != producto_id]
        
        if len(carrito) != len(nuevo_carrito):
            request.session['carrito'] = nuevo_carrito
            request.session.modified = True
            messages.success(request, "Producto eliminado del carrito.")
        else:
            messages.warning(request, "El producto no se encontró en el carrito.")
        
        request.session['carrito'] = nuevo_carrito
        return redirect('cart')

class AboutUs(TemplateView):
    template_name = "about/about.html"