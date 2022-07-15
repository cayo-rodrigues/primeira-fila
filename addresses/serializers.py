from rest_framework import serializers
from addresses.models import Address, City, Country, State, District


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
        read_only_fields = ["id"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"
        read_only_fields = ["id"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"
        read_only_fields = ["id"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
        read_only_fields = ["id"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    district = DistrictSerializer()
    country = CountrySerializer()
    state = StateSerializer()

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }
