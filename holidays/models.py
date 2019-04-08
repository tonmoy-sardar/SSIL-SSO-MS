from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HolidaysList(models.Model):
    holiday_name = models.CharField(max_length=100, blank=False,null=False)
    holiday_date = models.DateField(blank=False,null=False)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='h_l_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='h_l_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='h_l_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'holidays_list'