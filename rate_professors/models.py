from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


# module instance
class Module(models.Model):
    code = models.CharField(max_length=3, default="")
    name = models.CharField(max_length=60)
    year = models.IntegerField(validators=[MinValueValidator(1970), MaxValueValidator(2100)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])

    professor = models.ManyToManyField(Professor)

    def __str__(self):
        output = "{name}: {year}: S{semester}".format(name=self.name,
                                                      year=self.year,
                                                      semester=self.semester)
        return output


class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        output = "Prf. {professor}: {module}: Rating: {rating}".format(professor=self.professor,
                                                                       module=self.module,
                                                                       rating=self.rating)

        return output
