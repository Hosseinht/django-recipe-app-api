from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        """
            these are the fields that are gonna be converted to and,
            from json when we make HTTP Post, simply these are
            fields that we want to make accessible in the API wither
            to read or write
        """
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        # it adds extra restriction or argument for the password field

    def create(self, validation_data):
        """
        Create a news user with encrypted password and return it.
         it's a function that's called when we create a new object,
        and specify all the available functions that we can override
        """
        return get_user_model().objects.create_user(**validation_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        """
            instance is model instance.
            validated_data: fields = ('email', 'password', 'name')
        """
        password = validated_data.pop('password', None)
        # remove password from validation
        user = super().update(instance, validated_data)
        # super will call ModelSerializer update function

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
