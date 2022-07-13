from django.db import models

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=2)
    details = models.TextField(max_length=300)

    cities = models.ForeignKey(
        "addresses.City", on_delete=models.CASCADE, related_name="addresses"
    )
    districts = models.ForeignKey(
        "addresses.District", on_delete=models.CASCADE, related_name="addresses"
    )
    states = models.ForeignKey(
        "addresses.State", on_delete=models.CASCADE, related_name="addresses"
    )
    countries = models.ForeignKey(
        "addresses.Country", on_delete=models.CASCADE, related_name="addresses"
    )


class City(models.Model):
    name = models.CharField(max_length=50)


class District(models.Model):
    name = models.CharField(max_length=50)


class State(models.Model):
    name = models.CharField(max_length=50)


class Country(models.Model):
    name = models.CharField(max_length=50)
