from django.db import models


class Staff(models.Model):
	name = models.CharField(max_length=250)
	birth_date = models.DateTimeField()
	sex = models.BooleanField(null=True)
	slack_id = models.CharField(max_length=250, null=False, blank=False)

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


class Channel(models.Model):
	slack_id = models.CharField(max_length=250, null=False, blank=False)
	time_to_join = models.DateTimeField(auto_now_add=True)


INTERACTION_CHOICES = (
	('create_user', 'create_user'),
)


class Interaction(models.Model):
	slack_ts = models.CharField(max_length=250, null=False, blank=False)
	kind = models.CharField(max_length=15, choices=INTERACTION_CHOICES, default='create_user')
