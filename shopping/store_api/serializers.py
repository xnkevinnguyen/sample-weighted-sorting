from rest_framework import serializers

from . import models


class StoreUserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our store user profile objects."""
    store_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.StoreUserProfile
        fields = ('id', 'email', 'store_name', 'phone_number',
                  'password', 'store_items')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.StoreUserProfile(
            email=validated_data['email'],
            store_name=validated_data['store_name'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class StoreItemSerializer(serializers.ModelSerializer):
    """A serializer for store items"""

    class Meta:
        model = models.StoreItem
        fields = ('item_id', 'item_name','store_user', 'price','popularity', 'created_on')
        extra_kwargs = {'store_user': {'read_only': True}}
