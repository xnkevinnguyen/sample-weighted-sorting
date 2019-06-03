from rest_framework import serializers

from . import models


class HelloSerializer(serializers.Serializer):
    """Serialize a name field to test our api"""

    first_name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class CandidateProfileSerializer(serializers.ModelSerializer):
    """Serializer for our candidate profile object"""
    user_profile = UserProfileSerializer()

    class Meta:
        model = models.CandidateProfile
        fields = ('user_profile', 'birth_date', 'formation', 'postal_code', 'instagram_url', 'specialities',
                  'schedule', 'availability_date')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user_profile_data = validated_data.pop('user_profile', None)
        if user_profile_data:
            user_profile = models.UserProfile.objects.create_user(**user_profile_data)

            validated_data['user_profile'] = user_profile

        user = models.CandidateProfile(
            user_profile=validated_data['user_profile'],
            birth_date=validated_data['birth_date'],
            formation=validated_data['formation'],
            postal_code=validated_data['postal_code'],
            instagram_url=validated_data['instagram_url'],
            specialities=validated_data['specialities'],
            schedule=validated_data['schedule'],
            availability_date=validated_data['availability_date']
        )

        user.save()
        return user


class EmployerProfileSerializer(serializers.ModelSerializer):
    """Serializer for our enteprise profile object"""
    user_profile = UserProfileSerializer()

    class Meta:
        model = models.EmployerProfile
        fields = ('user_profile', 'employer_name', 'address', 'office_number',
                  'commercial_category', 'specialty_demand', 'hiring_number', 'website_url')

    def create(self, validated_data):
        """Create and return a new user."""

        user_profile_data = validated_data.pop('user_profile', None)
        if user_profile_data:
            user_profile = models.UserProfile.objects.create_user(**user_profile_data)

            validated_data['user_profile'] = user_profile

        user = models.EmployerProfile(
            user_profile=validated_data['user_profile'],
            employer_name=validated_data['employer_name'],
            address=validated_data['address'],
            office_number=validated_data['office_number'],
            commercial_category=validated_data['commercial_category'],
            specialty_demand=validated_data['specialty_demand'],
            hiring_number=validated_data['hiring_number'],
            availability_date=validated_data['availability_date'],
            website_url=validated_data['website_url']
        )

        user.save()
        return user
