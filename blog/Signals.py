from .models import Course
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver




@receiver(post_save, sender=Course)
def object_post_save(sender, **kwargs):
    #cache.delete('s_course')
    pass

