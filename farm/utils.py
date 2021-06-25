from core.settings import ADMIN_URL,SITE_URL,MEDIA_URL
from .apps import APP_NAME
from django.shortcuts import reverse
class AdminUtility():
    
    def __init__(self,app_name,user,*args, **kwargs):
        self.user=user
        self.app_name=app_name
    def get_link(self,child_class,class_title):
        app_name=APP_NAME
        url=f'{ADMIN_URL}{app_name}/{child_class}/add/'
        if self.user.has_perm(APP_NAME+".add_"+child_class):
            pass
        else:
            return ""
        template= f"""
            <a class="btn btn-info rtl" target="_blank" href="{url}" title="افزودن {class_title}" >
                        <i class="material-icons">add_circle</i>
            <span class="farsi">
            افزودن 
            {class_title}
            </span>
                    </a>
            """
        return template
        
    
    def add_doctor_btn(self):
        return self.get_link(child_class='doctor',class_title='دکتر')
    
   
    def add_farm_btn(self):
        return self.get_link(child_class='farm',class_title='مزرعه')
    
   
    def add_drug_btn(self):
        return self.get_link(child_class='drug',class_title='دارو')
    
   
   
    def add_saloon_btn(self):
        return self.get_link(child_class='saloon',class_title='سالن')
    
   
    def add_emplyee_btn(self):
        return self.get_link(child_class='employee',class_title='کارمند')
    
   
    def add_animal_btn(self):
        return self.get_link(child_class='animal',class_title='دام')
    
   