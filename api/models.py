from django.db import models


class Channel(models.Model):
	slack_id = models.CharField(max_length=250, null=False, blank=False)
	time_to_join = models.DateTimeField(auto_now_add=True)


class Staff(models.Model):
	name = models.CharField(max_length=250)
	birth_date = models.DateTimeField(null=True, blank=True)
	sex = models.BooleanField(null=True)
	slack_id = models.CharField(max_length=250, null=False, blank=False)
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Team(models.Model):
	teamlead = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='teamlead')
	teammate = models.ManyToManyField(Staff, related_name='teammate')

	def __str__(self):
		return f'{self.teamlead} и его команда'


class Gift(models.Model):
	name = models.CharField(max_length=250)


class Wishlist(models.Model):
	employee_name = models.ForeignKey(Staff, on_delete=models.CASCADE)
	gift = models.ManyToManyField(Gift)

	def __str__(self):
		return f'{self.employee_name} не отказался бы от {self.gift}'


class Interaction(models.Model):
	INTERACTION_CHOICES = (
		('UJF', 'user_join_form'),
	)
	message_ts = models.CharField(max_length=250, null=False, blank=False)
	kind = models.CharField(max_length=15, choices=INTERACTION_CHOICES, default='UJF', unique=True)
	value = models.CharField(max_length=250, null=False, blank=False)
	user = models.ForeignKey(Staff, on_delete=models.CASCADE)
