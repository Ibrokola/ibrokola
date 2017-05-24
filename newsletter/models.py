from django.conf import settings
from django.db import models
from .signals import signed_up
from .utils import get_client_city_data, get_client_ip


class JoinManager(models.Manager):
	def create_new(self, user, session_key=None, ip_address=None, city_data=None):
		session_new = self.model()
		session_new.email = email
		session_new.session_key = session_key
		if ip_address is not None:
			session_new.ip_address = ip_address
			if city_data:
				session_new.city_data = city_data
				try:
					city = city_data['city']
				except:
					city = None
				session_new.city = city
				try:
					country = city_data['country_name']
				except:
					country = None
			session_new.country = country
			session_new.save()
			return session_new
		return None



class Join(models.Model):
	email 	   = models.EmailField()
	session_key= models.CharField(max_length=60, null=True, blank=True)
	ip_address = models.GenericIPAddressField(null=True, blank=True)
	city_data  = models.TextField(null=True, blank=True)
	city       = models.CharField(max_length=120, null=True, blank=True)
	country    = models.CharField(max_length=120, null=True, blank=True)
	timestamp  = models.DateTimeField(auto_now_add=True)

	objects = JoinManager()


	def __str__(self):
		city = self.city
		country = self.country
		if city and country:
			return f"{city}, {country}"
		elif city and not country:
			return f"{city}"
		elif country and not city:
			return f"{country}"
		return self.email





def signed_up_receiver(sender, request, *args, **kwargs):
	email = sender
	ip_address = get_client_ip(request)
	city_data = get_client_city_data(ip_address)
	request.session['CITY'] = str(city_data.get('city', 'Edmonton'))
	session_key = request.session.session_key

	Join.objects.create_new(
					email = email,
					session_key = session_key,
					ip_address=ip_address,
					city_data=city_data,
		)


signed_up.connect(signed_up_receiver)