from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
from django.template.defaultfilters import slugify



class Responsible(models.Model):
    class Meta:
        abstract=True
    
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    MARTIAL_STATUS_CHOICES = [
        ("S", "Single"),
        ("M", "maried"),
        ("D", 'Devorced'),
        ("W", "widowed"),
        ("O", "Others")
    ]
    PROVINCE_CHOICES = [
        ("tana", "Antananarivo"),
        ("diego", "Antsiranana"),
        ("fianara", "Fianarantsoa"),
        ("majunga", "Mahajanga"),
        ("tamaga", "Toamasina"),
        ("tulear", "Toliara")
    ]
    identifiant = models.CharField(blank=True, null=True, max_length=100)
    slug = models.SlugField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(choices=SEX_CHOICES, max_length=100)
    martial_status = models.CharField(choices=MARTIAL_STATUS_CHOICES, default="S", max_length=100, blank=True, null=True)
    province = models.CharField(max_length=50, choices = PROVINCE_CHOICES)
    picture = models.ImageField("Picture profile", upload_to='responsible/pictures', default='responsible/unknown.jpg')
    confirmed_email = models.BooleanField(default=False, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    adress = models.CharField(blank=True, null=True, max_length=100)
    adress2 = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    mobile_number = models.CharField(blank=True, null=True, max_length=20)
    fixe_number = models.CharField(blank=True, null=True, max_length=20)
    last_update = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.slug} | {self.user.username}"
    
    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"slug": self.slug})
    
    
    def save(self, *args, **kwargs):
        if self.identifiant is None:
            self.identifiant = str(uuid4()).split("-")[-1]
        
        self.slug = slugify(f"{self.user.username} {self.user.first_name} {self.user.last_name} {self.identifiant}")
        self.last_update = timezone.now()
        return super(Responsible, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})
class Candidate(Responsible):
    cover_letter = models.FileField(upload_to="responsible/cover_letters", blank=True, null=True)
    cv = models.FileField(upload_to="responsible/cv", blank=True, null=True)