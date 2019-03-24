from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from .models import *
from django.utils import timezone
from .forms import ContactForm, SignUpForm
from django.contrib.auth.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.template import RequestContext
import hashlib, datetime, random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from cart.forms import CartAddProductForm

def index(request):
	marcas = Marca.objects.all().order_by('nombre');
	return render(request, 'autostickrapp/index.html', {'marcas': marcas})
	

def detalle_usuario(request):
	return render(request, 'autostickrapp/detalle_usuario.html')

def detalle_marca(request, pk):
	post = Emblema.objects.filter(marca=pk)
	cart_product_form = CartAddProductForm()
	context = {
        'post': post,
        'cart_product_form': cart_product_form
    }
	return render(request, 'autostickrapp/detalle_marca.html', context)


def emailView(request):
	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			from_email = form.cleaned_data['Correo']
			message = form.cleaned_data['Mensaje']+" Responda a este mensaje al correo "+from_email
			try:
				send_mail('Requiero informacion', message,from_email,['diegoarturogonmon@gmail.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('success')
	return render(request, "autostickrapp/email.html", {'form': form})

def successView(request):
	return render(request, "autostickrapp/gracias.html")

def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			usuario = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			usuario = authenticate(username=usuario, password=password)
			login(self.request, usuario)
			return redirect('/')
		else:
			return render(request,'autostickrapp/nuevousuario.html',{'formulario':formulario})
	else:
		formulario = SignUpForm()
	return render(request,'autostickrapp/nuevousuario.html',{'formulario':formulario})

def register_user(request):
	args = {}
	args.update(csrf(request))
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		args['form'] = form
		if form.is_valid(): 
			form.save()  # guardar el usuario en la base de datos si es válido
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			salt = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()[:5]
			activation_key = hashlib.sha256((email).encode('utf-8')).hexdigest()            
			key_expires = datetime.datetime.today() + datetime.timedelta(2)

			#Obtener el nombre de usuario
			user=User.objects.get(username=username)

			# Crear el perfil del usuario                                                                                                                                 
			new_profile = Perfil(user=user, activation_key=activation_key)
			new_profile.save()

			# Enviar un email de confirmación
			email_subject = 'Confirmacion de la cuenta'
			email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da click en este link en menos de 48 horas: http://autostickrweb.pythonanywhere.com/usuario/nuevo/confirmar/%s" % (username, activation_key)

			send_mail(email_subject, email_body, 'autostickr@gmail.com',
				[email], fail_silently=False)

			return HttpResponseRedirect('/exito')
	else:
		args['form'] = SignUpForm()

	return render_to_response('autostickrapp/nuevousuario.html', args, request)

def register_confirm(request, activation_key):
	# Verifica que el usuario ya está logeado
	if request.user.is_authenticated:
		HttpResponseRedirect('/')

	# Verifica que el token de activación sea válido y sino retorna un 404
	user_profile = get_object_or_404(Perfil, activation_key=activation_key)

	# Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
	user = user_profile.user
	user.is_active = True
	user.save()
	return render_to_response('autostickrapp/confirmar.html')

def inicio_screen(request):
	return render(request, 'autostickrapp/cuentas/inicio.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'autostickrapp/dashboard.html'

def exito(request):
	return render(request, 'autostickrapp/exito.html')
	
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')