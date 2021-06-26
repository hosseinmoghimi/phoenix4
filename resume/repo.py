from .models import ResumeIndex, ResumePortfolio, ResumeService
from authentication.repo import ProfileRepo

class ResumeIndexRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeIndex.objects.all()
    def resume_index(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            resume_index= self.objects.filter(profile_id=profile_id).first()
            if resume_index is None:
                resume_index=ResumeIndex(profile_id=profile_id)
                resume_index.save()
            return resume_index
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_index= self.objects.filter(pk=pk).first()
        return resume_index
class PortfolioRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumePortfolio.objects.all()
    def category_list(self,*args, **kwargs):
        category_list=[]
        try:
            category_list=(i[0] for i in self.objects.values('category').distinct('category'))
        except:
            for ii in self.objects.all():
                category=ii.category
                if not category in category_list:
                    category_list.append(category)

        return category_list
    def portfolio(self,*args, **kwargs):
        pk=0
        if 'portfolio_id' in kwargs:
            pk=kwargs['portfolio_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        portfolio= self.objects.filter(pk=pk).first()
        return portfolio
class ResumeServiceRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ResumeService.objects.all()
    
    def resume_service(self,*args, **kwargs):
        pk=0
        if 'resume_service_id' in kwargs:
            pk=kwargs['resume_service_id']           
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        resume_service= self.objects.filter(pk=pk).first()
        return resume_service