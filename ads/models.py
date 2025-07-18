from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    conditional_choices = [
        ('new', 'Новый'),
        ('used', 'Б/У')
    ]
    category_choices = [
        ('home_supplies', 'Товары для дома'),
        ('electronic', 'Электроника'),
        ('pet_supplies', 'Зоотовары')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=150)
    description = models.TextField(max_length=300)
    image_url = models.TextField(null=True, blank=True)
    category = models.TextField(choices=category_choices)
    condition = models.TextField(choices=conditional_choices)
    created_at = models.DateTimeField(auto_now_add=True)


class ExchangeProposal(models.Model):
    status_choices = [
        ('waiting', 'ожидает'),
        ('accepted', 'принята'),
        ('decline', 'отклонена')
    ]
    ad_sender = models.ForeignKey(Ad, related_name='ad_sender', on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(Ad, related_name='ad_receiver', on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    status = models.TextField(choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
