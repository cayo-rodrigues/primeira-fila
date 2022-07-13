from rest_framework import serializers
from cinemas.models import Cinema
from addresses.models import Address

# import ipdb

# from users.serializers import AccountSerializer
from users.models import User


class CreateCinemaSerializer(serializers.ModelSerializer):

    # seller = AccountSerializer(read_only=True)
    # address =

    class Meta:
        model = Cinema
        fields = ["id", "owner", "address"]
        read_only_fields = ["id", "owner"]
        # extra_kwargs = {
        #     "is_active": {"default": True},
        #     "quantity": {"min_value": 0},
        # }

    def create(self, validated_data):
        print("teste")
        address = validated_data.pop("address")
        objAddress = Address.objects.create(**address)
        address_id = objAddress.id
        cinema = Cinema.objects.create(**validated_data, address=address_id)
        return cinema


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
