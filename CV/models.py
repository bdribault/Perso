from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError


class SkillCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Cv(models.Model):
    AVAILABILITY_TYPE_NOW = "NOW"
    AVAILABILITY_TYPE_OFFSET = "OFFSET"
    AVAILABILITY_TYPE_AT = "AT"
    AVAILABILITY_TYPE = (
        (AVAILABILITY_TYPE_NOW, 'now'),
        (AVAILABILITY_TYPE_OFFSET, 'offset'),
        (AVAILABILITY_TYPE_AT, 'at'),
    )

    AVAILABILITY_OFFSET_MONTH = "MONTH"
    AVAILABILITY_OFFSET_DAY = "DAY"
    
    AVAILABILITY_OFFSET = (
        (AVAILABILITY_OFFSET_DAY, 'day'),
        (AVAILABILITY_OFFSET_MONTH, 'month'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    begin = models.DateField(null=True, blank=True)  # to compute experience

    availability_type = models.CharField(max_length=64, choices=AVAILABILITY_TYPE, default=AVAILABILITY_TYPE_NOW)
    availability_date = models.DateField(null=True, blank=True, help_text="if 'Availability type' is 'at'")
    availability_offset_number = models.IntegerField(null=True, blank=True, help_text="if 'Availability type' is 'offset'")
    availability_offset_quantity = models.CharField(max_length=64, choices=AVAILABILITY_OFFSET, default=AVAILABILITY_OFFSET_MONTH, help_text="if 'Availability type' is 'offset'")
    

    @classmethod
    def is_availability_valide(cls, availability_type, availability_date, availability_offset_number, availability_offset_quantity):
        if availability_type == cls.AVAILABILITY_TYPE_OFFSET:
            if not availability_offset_number or not availability_offset_quantity:
                return "availability offset expected"

        if availability_type == cls.AVAILABILITY_TYPE_AT:
            if not availability_date:
                return "availability date expected"
        return None

    def get_experience(self):
        delta = date.today() - self.begin
        return int(delta.days/365.25)

    def get_skills(self):
        skills = self.skill_set.all()
        ordered_skills = {}
        for skill in skills:
            if skill.category.name in ordered_skills:
                ordered_skills[skill.category.name].append(skill.name)
            else:
                ordered_skills[skill.category.name] = [skill.name]
        return ordered_skills

    def __str__(self):
        return self.user.username

    def clean(self):
        error = self.is_availability_valide(self.availability_type, self.availability_date, self.availability_offset_number, self.availability_offset_quantity)
        if error:
            raise ValidationError(error)


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(Cv, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.name + " (" + self.category.name + ")"


class Formation(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.content


class Company(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    website_link = models.CharField(max_length=512, blank=True)
    begin = models.DateField()
    end = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Experience(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    duration = models.CharField(max_length=255)
    begin = models.DateField()
    end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-begin', ]

    def __str__(self):
        return self.title


class MissionFunction(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.content


class MissionTechnical(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return self.content
