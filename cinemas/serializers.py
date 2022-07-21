from addresses.models import Address, City, Country, District, State
from addresses.serializers import AddressSerializer
from financial_controls.models import CinemaFinancialControl
from rest_framework import serializers
from users.serializers import UserSerializer
from utils.exceptions import IdenticalAddressError

from cinemas.models import Cinema


class CreateCinemaSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Cinema
        fields = "__all__"

    def create(self, validated_data: dict):
        address = validated_data.pop("address")
        city = address.pop("city")
        district = address.pop("district")
        state = address.pop("state")
        country = address.pop("country")

        objCity = City.objects.get_or_create(**city)[0]
        objCountry = Country.objects.get_or_create(**country)[0]
        objDistrict = District.objects.get_or_create(**district)[0]
        objState = State.objects.get_or_create(**state)[0]

        address_data = {
            **address,
            "country": objCountry,
            "state": objState,
            "district": objDistrict,
            "city": objCity,
        }

        objAddress, created = Address.objects.get_or_create(**address_data)
        if not created:
            raise IdenticalAddressError

        cinema = Cinema.objects.create(**validated_data, address=objAddress)
        CinemaFinancialControl.objects.create(cinema=cinema)
        return cinema

    def update(self, instance: Cinema, validated_data: dict):
        address = validated_data.pop("address", None)

        if address:
            city = address.pop("city", None)
            district = address.pop("district", None)
            state = address.pop("state", None)
            country = address.pop("country", None)

            street = address.pop("street", None)
            number = address.pop("number", None)
            details = address.pop("details", None)

            if city:
                instance.address.city = City.objects.get_or_create(**city)[0]
            if district:
                instance.address.district = District.objects.get_or_create(**district)[
                    0
                ]
            if state:
                instance.address.state = State.objects.get_or_create(**state)[0]
            if country:
                instance.address.country = Country.objects.get_or_create(**country)[0]

            if street:
                instance.address.street = street
            if number:
                instance.address.number = number
            if details:
                instance.address.details = details

            if (
                Cinema.objects.filter(
                    address__city=instance.address.city,
                    address__district=instance.address.district,
                    address__state=instance.address.state,
                    address__country=instance.address.country,
                    address__street=instance.address.street,
                    address__number=instance.address.number,
                    address__details=instance.address.details,
                )
                .exclude(pk=instance.id)
                .exists()
            ):
                raise IdenticalAddressError

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class ListCinemaSerializer(serializers.ModelSerializer):
    total_rooms = serializers.SerializerMethodField()
    address = AddressSerializer()

    class Meta:
        model = Cinema
        fields = "__all__"

    def get_total_rooms(self, obj: Cinema):
        return obj.rooms.count()
