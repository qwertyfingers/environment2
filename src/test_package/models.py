from django.db import models
from django.forms.models import ModelForm

# Create your models here.


class Test_db_1(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
       
class Test_db_1_form(ModelForm):
    class Meta:
        model = Test_db_1
          