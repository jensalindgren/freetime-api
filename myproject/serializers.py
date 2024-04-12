from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serializer for the User model
    Adds three extra fields when returning a list of User instances
    """
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    is_staff = serializers.ReadOnlyField(source="profile.is_staff")

    def get_profile_image(self, obj):
        """
        Serializer method for profile image, to enable
        implementing a fix for cloudinary not serving images securely
        """
        # Fix for cloudinary not serving images securely is from
        # https://stackoverflow.com/questions/48508750/how-to-force-https-in-a-django-project-using-cloudinary
        obj.profile.image.url_options.update({'secure': True})
        return obj.profile.image.url

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id',
            'profile_image',
            'is_staff',
        )