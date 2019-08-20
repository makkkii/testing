from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Address, Company, Country, State, Timezone

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        exclude = ('password', )


class AddressSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField(many=False)
    country = serializers.StringRelatedField(many=False)

    class Meta:
        model = Address
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    registered_addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(many=False)

    class Meta:
        model = State
        fields = '__all__'


class TimezoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timezone
        fields = '__all__'

