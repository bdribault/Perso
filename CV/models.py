from datetime import date

from django.contrib.auth.models import User
from django.db import models


class SkillCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Cv(models.Model):
    AVAILABILITY_TYPE_DATE = "DATE"
    AVAILABILITY_TYPE_STRING = "STRING"
    AVAILABILITY_TYPE = (
        (AVAILABILITY_TYPE_DATE, 'date'),
        (AVAILABILITY_TYPE_STRING, 'string'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    begin = models.DateField(null=True, blank=True)  # to compute experience

    availability_type = models.CharField(max_length=64, choices=AVAILABILITY_TYPE, default=AVAILABILITY_TYPE_STRING)
    availability_date = models.DateField(null=True, blank=True)
    availability_string = models.CharField(max_length=255)

    def get_experience(self):
        delta = date.today() - self.begin
        return int(delta.days/365.25)

    def get_availability(self):
        if self.availability_type == self.AVAILABILITY_TYPE_DATE:
            return "le " + self.availability_date.strftime("%d-%m-%Y")
        else:
            return self.availability_string

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
