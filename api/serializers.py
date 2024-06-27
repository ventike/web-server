from rest_framework import serializers
from .models import Organization, User, Individual, Tag, Partner, Resource, Event

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "message", "message_icon"]

######################################################################################################

class UserSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(required=False)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["user_hash", "username", "email", "first_name", "last_name", "role", "creation_date", "profile_picture", "organization"]

class UserAdminSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "role", "creation_date", "profile_picture"]

######################################################################################################

class TagSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ["name", "color_red", "color_blue", "color_green", "organization"]

class TagPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "color_red", "color_blue", "color_green"]

######################################################################################################

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["type", "name", "amount", "partner"]

class ResourcePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["type", "name", "amount"]

######################################################################################################

class IndividualSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Individual
        fields = ["pk", "first_name", "last_name", "email", "phone"]

class IndividualPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ["first_name", "last_name", "email", "phone"]

######################################################################################################

class PartnerSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=False)
    organization = OrganizationSerializer(read_only=True)
    tags = TagPartnerSerializer(read_only=True, many=True)
    resources = ResourcePartnerSerializer(read_only=True, many=True)
    individual = IndividualPartnerSerializer(read_only=True)

    class Meta:
        model = Partner
        fields = ["pk", "name", "description", "type", "email", "phone", "image", "organization", "individual", "tags", "resources"]

class PartnerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["name"]

class PartnerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["pk", "name"]

######################################################################################################

class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    partners = PartnerEventSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ["pk", "name", "description", "date", "start_time", "end_time", "organization", "partners"]

class EventDashboardSerializer(serializers.ModelSerializer):
    partners = PartnerEventSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ["pk", "name", "description", "date", "start_time", "end_time", "partners"]