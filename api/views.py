from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Organization, User, Individual, Tag, Partner, Resource, Event
from .serializers import OrganizationSerializer, UserSerializer, UserAdminSerializer, TagSerializer, TagPartnerSerializer, PartnerSerializer, PartnerEventSerializer, EventSerializer, EventDashboardSerializer
from rest_framework.views import APIView
import bcrypt
from django.core.files.base import ContentFile
import base64
import random
from .utils import is_valid_email, is_valid_phone_number, format_phone_number
import datetime
from django.utils.dateparse import parse_date, parse_time

colours = [(241, 91, 181), (254, 228, 64), (17, 138, 178), (6, 214, 160), (155, 93, 229), (0, 187, 249), (231, 29, 54), (255, 159, 28)]

# Create your views here.
# class UserListCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserData(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserList(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if user.role != 0 and user.role != 1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.filter(organization=user.organization)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAuthentication(APIView):
    def post(self, request, format=None):
        username = request.query_params.get("username", "")
        password = request.query_params.get("password", "")

        print(username)
        print(password)

        if not (username and password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user = User.objects.prefetch_related('organization').get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if not bcrypt.checkpw(bytes(password, "utf-8"), bytes(user.password, "utf-8")):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreation(APIView):
    def post(self, request, format=None):
        # User.objects.create(username="test", password=str(bcrypt.hashpw(bytes("test", "utf-8"), bcrypt.gensalt(rounds=15)))[2:-1], email="test@test.com", first_name="Test", last_name="Ter", role=0, organization=Organization.objects.get(pk=1))
        user_hash = request.query_params.get("user_hash", "")
        username = request.query_params.get("username", "")
        password = request.query_params.get("password", "")
        email = request.query_params.get("email", "")
        first_name = request.query_params.get("first_name", "")
        last_name = request.query_params.get("last_name", "")
        role = request.query_params.get("role", "")

        if not (user_hash and username and password and email and first_name and last_name and role):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not is_valid_email(email):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if user.role != 0 and user.role != 1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        salt = bcrypt.gensalt(rounds=15)
        new_user = User.objects.create(username=username, password=str(bcrypt.hashpw(bytes(password, "utf-8"), salt))[2:-1], email=email, first_name=first_name, last_name=last_name, role=int(role), organization=user.organization.pk)
        
        serializer = UserAdminSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserModification(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        username = request.query_params.get("username", "")
        email = request.query_params.get("email", "")
        first_name = request.query_params.get("first_name", "")
        last_name = request.query_params.get("last_name", "")
        role = request.query_params.get("role", "")

        if not (user_hash and username and email and first_name and last_name and role):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            new_user = User.objects.prefetch_related('organization').get(username=username, organization=user.organization)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not is_valid_email(email):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if user.role != 0 or user.role != 1 or user.role > new_user.role:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        new_user.username=username
        new_user.email=email
        new_user.first_name=first_name
        new_user.last_name=last_name
        new_user.role=int(role)
        new_user.save()
        
        serializer = UserAdminSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserPasswordModification(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        old_password = request.query_params.get("old_password", "")
        new_password = request.query_params.get("new_password", "")

        if not (user_hash and old_password and new_password):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not bcrypt.checkpw(bytes(old_password, "utf-8"), bytes(user.password, "utf-8")):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        salt = bcrypt.gensalt(rounds=15)
        user.password = str(bcrypt.hashpw(bytes(new_password, "utf-8"), salt))[2:-1]
        user.save()
        
        serializer = UserAdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeletion(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        username = request.query_params.get("username", "")

        if not (user_hash and username):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            new_user = User.objects.prefetch_related('organization').get(username=username, organization=user.organization)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if user.role != 0 or user.role != 1 or user.role > new_user.role:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        new_user.delete()

        return Response(status=status.HTTP_200_OK)

######################################################################################################

class PartnerList(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        partners = Partner.objects.filter(organization=user.organization)
        
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartnerCreation(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        name = request.query_params.get("name", "")
        description = request.query_params.get("description", "")
        type = request.query_params.get("type", "")
        email = request.query_params.get("email", "")
        phone = request.query_params.get("phone", "")
        image = request.query_params.get("image", "")
        individual_first_name = request.query_params.get("individual_first_name", "")
        individual_last_name = request.query_params.get("individual_last_name", "")
        individual_email = request.query_params.get("individual_email", "")
        individual_phone = request.query_params.get("individual_phone", "")
        tags = request.query_params.get("tags", "")
        resource_types = request.query_params.get("resource_types", "")
        resource_names = request.query_params.get("resource_names", "")
        resource_amounts = request.query_params.get("resource_amounts", "")

        if not (user_hash and name and description and type and email and phone and individual_first_name and individual_last_name and individual_email and individual_phone):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not is_valid_email(email) or not is_valid_email(individual_email):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if not is_valid_phone_number(phone) or not is_valid_phone_number(individual_phone):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Derived from https://stackoverflow.com/a/39587386
        image_data = None
        if image:
            format, imgstr = image.split(';base64,') 
            ext = format.split('/')[-1] 

            image_data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        
        tags_data = None
        tags_split = tags.split(", ")
        if tags_split:
            tags_data = Tag.objects.filter(organization=user.organization, name__in=tags_split)
            if len(tags_data) != len(tags_split):
                old_tags = list(tags_data.values_list('name', flat=True))
                new_tags_split = [x for x in tags_split if x not in old_tags]

                count = Tag.objects.count()
                new_tags = []
                for tag in new_tags_split:
                    colour = None
                    if count > len(colours):
                        colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                    else:
                        colour = colours[count]
                    new_tags.append(Tag(name=tag, color_red=colour[0], color_green=colour[1], color_blue=colour[2], organization=user.organization))
                    count += 1
                
                Tag.objects.bulk_create(new_tags)
                
                tags_data = Tag.objects.filter(organization=user.organization, name__in=tags_split)
        
        new_individual = Individual.objects.create(first_name=individual_first_name, last_name=individual_last_name, email=individual_email, phone=format_phone_number(individual_phone))
        new_partner = Partner.objects.create(name=name, description=description, type=int(type), email=email, phone=format_phone_number(phone), image=image_data, individual=new_individual, organization=user.organization)
        new_partner.tags.set(tags_data)
        new_partner.save()

        resources_data = None
        resource_types_split = resource_types.split(", ")
        resource_names_split = resource_names.split(", ")
        resource_amounts_split = resource_amounts.split(", ")

        if resource_types_split and resource_names_split and resource_amounts_split and len(resource_types_split) == len(resource_names_split) and len(resource_names_split) == len(resource_amounts_split):
            new_resources = []
            for i in range(len(resource_amounts_split)):
                new_resources.append(Resource(type=int(resource_types_split[i]), name=resource_names_split[i], amount=int(resource_amounts_split[i]), partner=new_partner))
            Resource.objects.bulk_create(new_resources)
        
        new_partner.refresh_from_db()
        
        serializer = PartnerSerializer(new_partner)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartnerModification(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        partner_id = request.query_params.get("partner_id", "")
        name = request.query_params.get("name", "")
        description = request.query_params.get("description", "")
        type = request.query_params.get("type", "")
        email = request.query_params.get("email", "")
        phone = request.query_params.get("phone", "")
        image = request.query_params.get("image", "")
        individual_first_name = request.query_params.get("individual_first_name", "")
        individual_last_name = request.query_params.get("individual_last_name", "")
        individual_email = request.query_params.get("individual_email", "")
        individual_phone = request.query_params.get("individual_phone", "")
        tags = request.query_params.get("tags", "")
        resource_types = request.query_params.get("resource_types", "")
        resource_names = request.query_params.get("resource_names", "")
        resource_amounts = request.query_params.get("resource_amounts", "")

        if not (user_hash and partner_id and name and description and type and email and phone and individual_first_name and individual_last_name and individual_email and individual_phone):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            partner = Partner.objects.prefetch_related('individual').prefetch_related('tags').prefetch_related('resources').get(pk=partner_id, organization=user.organization)
        except Partner.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not is_valid_email(email) or not is_valid_email(individual_email):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if not is_valid_phone_number(phone) or not is_valid_phone_number(individual_phone):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Derived from https://stackoverflow.com/a/39587386
        image_data = None
        if image:
            format, imgstr = image.split(';base64,') 
            ext = format.split('/')[-1] 

            image_data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        
        tags_data = None
        tags_split = tags.split(", ")
        if tags_split:
            tags_data = Tag.objects.filter(organization=user.organization, name__in=tags_split)
            if len(tags_data) != len(tags_split):
                old_tags = list(tags_data.values_list('name', flat=True))
                new_tags_split = [x for x in tags_split if x not in old_tags]

                count = Tag.objects.count()
                new_tags = []
                for tag in new_tags_split:
                    colour = None
                    if count > len(colours):
                        colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                    else:
                        colour = colours[count]
                    new_tags.append(Tag(name=tag, color_red=colour[0], color_green=colour[1], color_blue=colour[2], organization=user.organization))
                    count += 1
                
                Tag.objects.bulk_create(new_tags)
                
                tags_data = Tag.objects.filter(organization=user.organization, name__in=tags_split)
        
        resources_data = None
        resource_types_split = resource_types.split(", ")
        resource_names_split = resource_names.split(", ")
        resource_amounts_split = resource_amounts.split(", ")

        Resource.objects.filter(partner=partner).delete()

        if resource_types_split and resource_names_split and resource_amounts_split and len(resource_types_split) == len(resource_names_split) and len(resource_names_split) == len(resource_amounts_split):
            new_resources = []
            for i in range(len(resource_amounts_split)):
                new_resources.append(Resource(type=int(resource_types_split[i]), name=resource_names_split[i], amount=int(resource_amounts_split[i]), partner=partner))
            Resource.objects.bulk_create(new_resources)

        partner.individual.first_name =  individual_first_name
        partner.individual.last_name = individual_last_name
        partner.individual.email = individual_email
        partner.individual.phone = format_phone_number(individual_phone)
        partner.individual.save()

        partner.name = name
        partner.description = description
        partner.type = int(type)
        partner.email = email
        partner.phone = format_phone_number(phone)
        partner.image = image_data
        partner.save()

        partner.tags.clear()
        partner.tags.set(tags_data)
        partner.save()

        partner.refresh_from_db()
        
        serializer = PartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartnerDeletion(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        partner_id = request.query_params.get("partner_id", "")

        if not (user_hash and partner_id):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            partner = Partner.objects.prefetch_related('individual').prefetch_related('tags').prefetch_related('resources').get(pk=partner_id, organization=user.organization)
        except Partner.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        partner.individual.delete()
        
        return Response(status=status.HTTP_200_OK)

######################################################################################################

class EventList(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        events = Event.objects.filter(organization=user.organization)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventCreation(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        name = request.query_params.get("name", "")
        description = request.query_params.get("description", "")
        date = request.query_params.get("date", "")
        start_time = request.query_params.get("start_time", "")
        end_time = request.query_params.get("end_time", "")
        partners = request.query_params.get("partners", "")

        if not (user_hash and name and description and date and start_time and end_time):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            date_object = parse_date(date)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        try:
            start_time_object = parse_time(start_time)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        try:
            end_time_object = parse_time(end_time)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        if date_object == None or start_time_object == None or end_time_object == None:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        
        partners_data = None
        partners_split = partners.split(", ")
        
        if partners_split:
            partners_data = Partner.objects.filter(organization=user.organization, pk__in=partners_split)
        
        new_event = Event.objects.create(name=name, description=description, date=date, start_time=start_time, end_time=end_time, organization=user.organization)
        new_event.partners.set(partners_data)
        new_event.save()
        
        serializer = EventSerializer(new_event)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventModification(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        event_id = request.query_params.get("event_id", "")
        name = request.query_params.get("name", "")
        description = request.query_params.get("description", "")
        date = request.query_params.get("date", "")
        start_time = request.query_params.get("start_time", "")
        end_time = request.query_params.get("end_time", "")
        partners = request.query_params.get("partners", "")

        if not (user_hash and event_id and name and description and date and start_time and end_time):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            event = Event.objects.prefetch_related('partners').get(pk=event_id, organization=user.organization)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            date_object = parse_date(date)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        try:
            start_time_object = parse_time(start_time)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        try:
            end_time_object = parse_time(end_time)
        except ValueError:
            return Response(status=status.HTTP_409_CONFLICT)
        
        if date_object == None or start_time_object == None or end_time_object == None:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        
        partners_data = None
        partners_split = partners.split(", ")
        
        if partners_split:
            partners_data = Partner.objects.filter(organization=user.organization, pk__in=partners_split)
        
        event.name = name
        event.description = description
        event.date = date
        event.start_time = start_time
        event.end_time = end_time
        event.partners.clear()
        event.partners.set(partners_data)
        event.save()
        
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventDeletion(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        event_id = request.query_params.get("event_id", "")

        if not (user_hash and event_id):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            event = Event.objects.prefetch_related('partners').get(pk=event_id, organization=user.organization)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        event.delete()

        return Response(status=status.HTTP_200_OK)

######################################################################################################

class OrganizationModification(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")
        name = request.query_params.get("name", "")
        message = request.query_params.get("message", "")
        message_icon = request.query_params.get("message_icon", "")

        if not (user_hash and name):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if user.role != 0 and user.role != 1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        if not message:
            message = None
        
        if not message_icon:
            messag_icon = None
        
        user.organization.name = name
        user.organization.message = message
        user.organization.message_icon = int(message_icon)
        user.organization.save()
        
        serializer = OrganizationSerializer(user.organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

######################################################################################################

class DashboardList(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        events = Event.objects.filter(organization=user.organization)
        
        event_serializer = EventDashboardSerializer(events, many=True)
        organization_serializer = OrganizationSerializer(user.organization)
        return Response([event_serializer.data, organization_serializer.data], status=status.HTTP_200_OK)

######################################################################################################

class AdminList(APIView):
    def post(self, request, format=None):
        user_hash = request.query_params.get("user_hash", "")

        if not user_hash:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            user = User.objects.prefetch_related('organization').get(user_hash=user_hash)
        except User.DoesNotExist:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if user.role != 0 and user.role != 1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        users = User.objects.filter(organization=user.organization)
        
        user_serializer = UserAdminSerializer(users, many=True)
        organization_serializer = OrganizationSerializer(user.organization)
        return Response([user_serializer.data, organization_serializer.data], status=status.HTTP_200_OK)