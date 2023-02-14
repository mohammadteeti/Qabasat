from django.db import models

# Create your models here.

#a test model to test users permission 
#doenst affect the project flow 
class TestModel (models.Model):
    name=models.CharField(("Name:"), max_length=50)
    age=models.PositiveIntegerField(("Age:"),default=25)
    
    def __str__(self) -> str:
        return f"{self.name} is {self.age}"
    
    