from .models import ResumeIndex
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