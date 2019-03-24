from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib, datetime, random


class Marca(models.Model):
	nombre = models.CharField(max_length=200, unique=True)
	logo = models.ImageField(upload_to='logo/')

	def __str__(self):
		return self.nombre

	#class Meta:
	 #   ordering = ['nombre']

class Emblema(models.Model):
	modelo = models.CharField(max_length=200)
	marca = models.ForeignKey(Marca, to_field='nombre', on_delete=models.CASCADE)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='img/')
	precio = models.DecimalField(decimal_places=2, max_digits=6)
	published_date = models.DateTimeField(
			blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.modelo

class Perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	activation_key = models.CharField(max_length=40, blank=True)

	class Meta:
		verbose_name_plural=u'Perfiles de Usuario'

	def __str__(self):
		return self.user.username
