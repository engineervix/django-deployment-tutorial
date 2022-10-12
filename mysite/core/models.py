from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property  # noqa: F401

import recurrence.fields
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel
from upload_validator import FileTypeValidator

from mysite.core.validators import validate_icon_size


class CommonInfo(StatusModel, TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True)
    description = models.TextField()
    STATUS = Choices("published", "draft")

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class WeeklyActivity(CommonInfo):
    start = models.TimeField()
    end = models.TimeField()
    recurrences = recurrence.fields.RecurrenceField()


class Belief(CommonInfo):
    icon = models.FileField(
        blank=True,
        help_text="Only SVG, JPEG and PNG Image files accepted",
        upload_to="images/icons/",
        validators=[
            FileTypeValidator(
                allowed_types=["image/svg+xml", "image/png", "image/jpeg"],
                allowed_extensions=[".svg", ".png", ".jpg", ".jpeg"],
            ),
            validate_icon_size,
        ],
    )


class OnlinePlatforms(SingletonModel):
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    sermon_audio = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook_livestream = models.BooleanField(help_text="Do you stream to Facebook?", default=False)
    youtube_livestream = models.BooleanField(help_text="Do you stream to YouTube?", default=False)


class Vision(CommonInfo, SingletonModel):
    pass


class Mission(CommonInfo, SingletonModel):
    pass


class Location(CommonInfo):
    street_address = models.CharField(max_length=255)
    postal_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    country = CountryField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)


class HomePage(CommonInfo, SingletonModel):
    """
    Homepage has the following sections:
    - Hero area, which is automatically populated with the latest sermon / article
    - Welcome message
    - Doctrine / Beliefs
    - Weekly activities
    - Online platforms
    - Verse of the day
    - Newsletter signup
    """

    # Welcome Message
    welcome_message = RichTextField()
    welcome_image = models.ImageField(blank=True, upload_to="images/")

    # Doctrine /Beliefs
    beliefs_heading = models.CharField(max_length=255, default="Our Beliefs")
    beliefs_subheading = RichTextField(blank=True)

    # Weekely Activities
    weekly_activities_heading = models.CharField(max_length=255, default="Weekly Activities")
    weekly_activities_subheading = RichTextField(blank=True)

    def get_absolute_url(self):
        return reverse("home")


class AboutPage(CommonInfo, SingletonModel):
    """
    About page has the following sections:
    - Introduction
    - Location
    - Vision
    - Mission
    - History
    - Doctrine / Beliefs
    - Church officers
    - Weekly activities
    - Online platforms
    """

    # Introduction
    introduction = RichTextField(blank=True)
    introduction_image = models.ImageField(blank=True, upload_to="images/")

    # History
    history = RichTextField(blank=True)
    history_image = models.ImageField(blank=True, upload_to="images/")

    # Doctrine / Beliefs
    doctrine = RichTextField(blank=True, help_text="A brief statement sumarizing our beliefs")
    doctrine_image = models.ImageField(blank=True, upload_to="images/")

    def get_absolute_url(self):
        return reverse("about")
