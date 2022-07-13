from rest_framework import serializers
from cinemas.models import Cinema
from addresses.models import Address, City, Country, District, State
from addresses.serializers import (
    AddressSerializer,
    CitySerializer,
    DistrictSerializer,
    StateSerializer,
    CountrySerializer,
)

# from addresses.serializers import
# import ipdb

from users.models import User


class CreateCinemaSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Cinema
        fields = "__all__"
        read_only_fields = ["id", "owner"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }

    def create(self, validated_data: dict):
        print("teste")
        address = validated_data.pop("address")
        city = address.pop("city")
        district = address.pop("district")
        state = address.pop("state")
        country = address.pop("country")

        objCity = City.objects.get_or_create(**city)[0]
        objCountry = Country.objects.get_or_create(**country)[0]
        objDistrict = District.objects.get_or_create(**district)[0]
        objState = State.objects.get_or_create(**state)[0]

        objAddress = Address.objects.create(
            **address,
            country=objCountry,
            state=objState,
            district=objDistrict,
            city=objCity
        )
        return Cinema.objects.create(**validated_data, address=objAddress)

    def update(self, instance: Cinema, validated_data: dict):
        address = validated_data.pop("address", None)
        city = validated_data.pop("city", None)
        district = validated_data.pop("district", None)
        state = validated_data.pop("state", None)
        country = validated_data.pop("country", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if city:
            instance.city = City.objects.get_or_create(**city)[0]
        if district:
            instance.district = District.objects.get_or_create(**district)[0]
        if state:
            instance.state = State.objects.get_or_create(**state)[0]
        if country:
            instance.country = Country.objects.get_or_create(**country)[0]

        instance.save()
        return instance


class ListCinemaSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cinema
        fields = "__all__"
        read_only_fields = [
            "description",
            "id",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
