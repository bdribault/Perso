from django.contrib import admin

from .models import Experience, Cv, Skill, SkillCategory, Formation, Company, MissionFunction, MissionTechnical


class FormationInline(admin.TabularInline):
    model = Formation
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    show_change_link = True


class CompanyInline(admin.StackedInline):
    model = Company
    verbose_name = u"Company"
    verbose_name_plural = u"Companies"
    extra = 1
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['begin', 'end'], 'classes': ['collapse']}),
    ]
    show_change_link = True


class SkillInline(admin.TabularInline):
    model = Skill


class CvAdmin(admin.ModelAdmin):
    inlines = [FormationInline, SkillInline, CompanyInline]


class CompanyAdmin(admin.ModelAdmin):
    inlines = (ExperienceInline,)


class MissionFunctionInline(admin.TabularInline):
    model = MissionFunction


class MissionTechnicalInline(admin.TabularInline):
    model = MissionTechnical


class ExperienceAdmin(admin.ModelAdmin):
    inlines = [MissionFunctionInline, MissionTechnicalInline]


admin.site.register(Cv, CvAdmin)
admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(Formation)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(MissionFunction)
admin.site.register(MissionTechnical)
