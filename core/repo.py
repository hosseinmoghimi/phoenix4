from .models import *
from .constants import *
from authentication.repo import ProfileRepo
from django.db.models import Q
from .enums import ParametersEnum
from authentication.repo import ProfileRepo
class BasicPageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=BasicPage.objects
    def add_page(self,title,*args, **kwargs):
        new_page=BasicPage(title=title)
        new_page.title=title
        if 'parent_id' in kwargs:
            new_page.parent_id=kwargs['parent_id']
        new_page.save()
        new_page.app_name=new_page.parent.app_name
        new_page.class_name=new_page.parent.class_name
        new_page.save()
        return new_page

    def page(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'project_id' in kwargs:
            return self.objects.filter(pk=kwargs['project_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])        
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects.all()
class PageCommentRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageComment.objects
    def add_comment(self,comment,page_id,*args, **kwargs):
        profile=ProfileRepo(self.user).me
        page_comment=PageComment(comment=comment,page_id=page_id,profile=profile)
        
        page_comment.save()
        return page_comment

    def delete_comment(self,page_comment_id,*args, **kwargs):
        profile=ProfileRepo(self.user).me
        page_comment=PageComment.objects.filter(pk=page_comment_id).first()

        if page_comment is not None and page_comment.profile==profile:
            page_comment.delete()
            return True
        return False

    def page_link(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_link_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_link_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class PageLinkRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageLink.objects
    def add_page_link(self,title,url,page_id,*args, **kwargs):
        new_page_link=PageLink(title=title,page_id=page_id,url=url,icon_fa="fa fa-tag")
        
        new_page_link.save()
        return new_page_link

    def page_link(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_link_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_link_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

class PageImageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageImage.objects
    def add_page_image(self,title,image,page_id,*args, **kwargs):
        image=Image(title=title,image_main_origin=image)
        image.save()
        new_page_image=PageImage(image=image,page_id=page_id)
        
        new_page_image.save()
        return new_page_image

   

class ParameterRepo:
    def __init__(self,app_name,user=None):
        self.objects=Parameter.objects.filter(Q(app_name=None)|Q(app_name=app_name))
        self.user=user
        self.app_name=app_name
    
    def change_parameter(self,parameter_id,parameter_value):
        if self.user.has_perm(APP_NAME+'.change_parameter'):
            try:
                parameter=Parameter.objects.get(pk=parameter_id)
            except:
                return None
            parameter.value_origin=parameter_value
            parameter.save()
            return parameter

    
    def set(self,name,value=None):
        # if name==ParametersEnum.LOCATION:
        #     value=value.replace('width="600"','width="100%"')
        #     value=value.replace('height="450"','height="400"') 
        if value is None:
            value=name
        olds=self.objects.filter(name=name).filter(app_name=self.app_name)
        if len(olds)>1:
            value=olds.first().value
        olds.delete()
        Parameter(name=name,value_origin=value,app_name=self.app_name).save()
    
    

    def get(self,name):
        try:
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        except:
            self.set(name=name)
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        return parameter

class DocumentRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Document.objects.order_by('priority')

    def document(self,document_id):
        try:
            return self.objects.get(pk=document_id)
        except:
            return None

    def add_page_document(self,title,file,priority=1000,page_id=None):
        
        page=BasicPage.objects.get(pk=page_id)
        if page is None:
            return None

        document=PageDocument(icon_material="get_app",title=title,file=file,priority=priority,page=page,profile=self.profile)
        document.save()
        return document


class PictureRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Picture.objects.all()
    def get(self,*args, **kwargs):
        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None and not name=="":
                picture=self.objects.create(app_name=self.app_name,name=name)
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(app_name=self.app_name).filter(pk=pk).first()
        return picture


class LinkRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Link.objects.all()
    def get(self,*args, **kwargs):
        pk=0
        name=""
        link=None
        if 'name' in kwargs:
            name=kwargs['name']
            link= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if link in None:
                link=self.objects.create(app_name=self.app_name,name=name)
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'link_id' in kwargs:
            pk=kwargs['link_id']
        if pk>0:
            link= self.objects.filter(app_name=self.app_name).filter(pk=pk).first()
        return link

