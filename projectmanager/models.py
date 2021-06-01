from django.db import models
from core.models import BasicPage as CoreBasicPage
from .apps import APP_NAME
from django.utils.translation import gettext as _



class ProjectManagerPage(CoreBasicPage):   

    class Meta:
        verbose_name = _("ProjectManagerPage")
        verbose_name_plural = _("ProjectManagerPage")
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ProjectManagerPage,self).save(*args, **kwargs)

class Project(ProjectManagerPage):
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    def save(self,*args, **kwargs):
        self.class_name="project"
        return super(Project,self).save(*args, **kwargs)


class OrganizationUnit(ProjectManagerPage):
    
    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")
    def save(self,*args, **kwargs):
        self.class_name="organizationunit"
        return super(OrganizationUnit,self).save(*args, **kwargs)



