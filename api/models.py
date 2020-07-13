from django.db import models


class Staff(models.Model):
	name = models.CharField(max_length=250)
	birth_date = models.DateTimeField()
	sex = models.BooleanField(null=True)
	slack_id = models.CharField(max_length=250)
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Team(models.Model):
	teamlead = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='teamlead')
	teammate = models.ManyToManyField(Staff, related_name='teammate')

	def __str__(self):
		return f'комманда: {self.teamlead}'


class Gift(models.Model):
	name = models.CharField(max_length=250)


class Wishlist(models.Model):
	employee_name = models.ForeignKey(Staff, on_delete=models.CASCADE)
	gift = models.ManyToManyField(Gift)

	def __str__(self):
		return f'{self.employee_name} не отказался бы от {self.gift}'


