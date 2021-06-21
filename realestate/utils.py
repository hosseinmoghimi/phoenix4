from .settings import *
from .apps import APP_NAME
class AdminUtility():
    def __init__(self,user=None):
        self.user=user

    def get_link(self,class_name,class_title,*args, **kwargs):
        url=f'{CoreSettings.ADMIN_URL}{APP_NAME}/{class_name}/add/'
        return f"""
         <a target="_blank" href="{url}" title="افزودن {class_title}" >
                     <i class="material-icons text-info">add_circle</i>
                 </a>
        """

    def get_add_property(self):
        return self.get_link(class_name='property',class_title='ملک',color="success")

