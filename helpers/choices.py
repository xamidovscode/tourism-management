from django.db import models


class TourConceptChoice(models.TextChoices):
    STANDARD = "standard", "Standard"
    INDIVIDUAL = "individual", "Individual"
    FREE = "free", "Free"
    GROUP = "group", "Group"

