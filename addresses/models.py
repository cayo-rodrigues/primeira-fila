from django.db import models

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    details = models.TextField()

    city = models.ForeignKey(
        "addresses.City", on_delete=models.CASCADE, related_name="addresses"
    )
    district = models.ForeignKey(
        "addresses.District", on_delete=models.CASCADE, related_name="addresses"
    )
    state = models.ForeignKey(
        "addresses.State", on_delete=models.CASCADE, related_name="addresses"
    )
    country = models.ForeignKey(
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
