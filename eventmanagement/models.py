
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Event(models.Model):

    CATEGORY_CHOICES = [
        ("WEBINAR", "Webinar"),
        ("SEMINAR", "Seminar"),
        ("CONFERENCE", "Conference"),
        ("WORKSHOP", "Workshop"),
        ("MEETUP", "Meetup"),
    ]

    FORMAT_CHOICES = [
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
        ("HYBRID", "Hybrid"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PUBLISHED", "Published"),
    ]

    # Admin who creates the event
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="events_created"
    )

    # Event information
    event_name = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    event_format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES
    )

    # Event date and time
    event_date = models.DateField()

    registration_deadline = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    # Location
    venue = models.CharField(
        max_length=255,
        blank=True
    )

    # Seats and ticket details
    total_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    is_free = models.BooleanField(default=True)

    ticket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    # Event banner
    event_image = models.ImageField(
        upload_to="events/banners/",
        blank=True,
        null=True
    )

    # Event status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if (
            self.registration_deadline
            and self.event_date
            and self.registration_deadline > self.event_date
        ):
            raise ValidationError({
                "registration_deadline":
                    "Registration deadline cannot be after the event date."
            })

        if (
            self.start_time
            and self.end_time
            and self.end_time <= self.start_time
        ):
            raise ValidationError({
                "end_time":
                    "End time must be later than start time."
            })

        if self.is_free:
            self.ticket_price = 0

        if self.event_format == "OFFLINE" and not self.venue:
            raise ValidationError({
                "venue":
                    "A venue is required for offline events."
            })

    def __str__(self):
        return self.event_name
