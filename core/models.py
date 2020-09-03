from django.db import models


class Product(models.Model):
    class STORE_CHOICES(models.TextChoices):
        badr_group = 'BG', 'Badr Group',
        egypt_laptop = 'EL', 'Egypt Laptop',
        high_end = 'HE', 'High End',
        maximum = 'MX', 'Maximum',
        sigma_pc = 'SPC', 'Sigma PC',

    name = models.CharField(max_length=120)
    price = models.FloatField(max_length=10)
    image_path = models.URLField(
        default='http://placehold.it/500x500'
    )

    store = models.CharField(max_length=20, choices=STORE_CHOICES.choices, null=True, blank=True)
    seller_image = models.ImageField(default=None, null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
