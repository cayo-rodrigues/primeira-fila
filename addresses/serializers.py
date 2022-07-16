from rest_framework import serializers

from addresses.models import Address, City, Country, District, State


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
        read_only_fields = ["id"]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"
        read_only_fields = ["id"]


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"
        read_only_fields = ["id"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
        read_only_fields = ["id"]


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    district = DistrictSerializer()
    country = CountrySerializer()
    state = StateSerializer()

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id"]
