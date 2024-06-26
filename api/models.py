from django.db import models
from .utils import generate_random_string

# Create your models here.
class Organization(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=False, blank=False, unique=True, max_length=64)
    message = models.TextField(null=True)
    message_icon = models.IntegerField(null=True) # 0 = red/warning

    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    def generate_hash():
        # Derived from https://stackoverflow.com/a/67546412
        not_unique = True
        unique_hash = ""

        while not_unique:
            unique_hash = generate_random_string(64)
            if not User.objects.filter(user_hash=unique_hash):
                not_unique = False

        return unique_hash
    
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    user_hash = models.CharField(null=False, blank=False, unique=True, max_length=64, default=generate_hash)
    username = models.CharField(null=False, blank=False, unique=True, max_length=64)
    password = models.CharField(null=False, blank=False, max_length=64)
    email = models.CharField(null=False, blank=False, max_length=64)
    first_name = models.CharField(null=False, blank=False, max_length=64)
    last_name = models.CharField(null=False, blank=False, max_length=64)
    role = models.IntegerField(null=False, blank=False, default=2) # 0 = owner, 1 = admin, 2 = user
    profile_picture = models.ImageField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)


    def __str__(self):
        return f"{self.username} | {self.first_name} {self.last_name} | {self.organization.name}"

class Individual(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(null=False, blank=False, max_length=64)
    last_name = models.CharField(null=False, blank=False, max_length=64)
    email = models.CharField(null=False, blank=False, max_length=64)
    phone = models.CharField(null=False, blank=False, max_length=64)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.partner.name}"

class Tag(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=False, blank=False, max_length=64)
    color_red = models.IntegerField(null=False, blank=False)
    color_blue = models.IntegerField(null=False, blank=False)
    color_green = models.IntegerField(null=False, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.name} | ({self.color_red}, {self.color_green}, {self.color_blue})"

class Partner(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=False, blank=False, max_length=64)
    description = models.TextField(null=False, blank=False)
    type = models.IntegerField(null=False, blank=False) # 0 = business, 1 = community, 2 = education, 3 = other
    email = models.CharField(null=False, blank=False, max_length=64)
    phone = models.CharField(null=False, blank=False, max_length=64)
    image = models.ImageField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)
    individual = models.OneToOneField(Individual, on_delete=models.CASCADE, null=False, blank=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        tags = ""

        for tag in self.tags.all():
            tags += tag.name + ", "

        if tags:
            tags = tags[:-2]

        return f"{self.name} | {tags if tags else 'No Tags'}"

class Resource(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(null=False, blank=False) # 0 = financial, 1 = human, 2 = physical, 3 = other
    name = models.CharField(null=False, blank=False, max_length=64)
    amount = models.IntegerField(null=False, blank=False)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=False, blank=False, related_name="resources")

    def __str__(self):
        return f"{self.name} | {self.partner.name}"

class Event(models.Model):
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=False, blank=False, unique=True, max_length=64)
    description = models.TextField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)
    partners = models.ManyToManyField(Partner)

    def __str__(self):
        partners = ""

        for partner in self.partners.all():
            partners += partner.name + ", "

        if partners:
            partners = partners[:-2]

        return f"{self.name} | {partners if partners else 'No Partners'}"