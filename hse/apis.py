from typing import ContextManager
from utility.persian import PersianCalendar
from .serializers import BlogSerializer
from core.constants import SUCCEED, FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import BlogRepo
from .forms import *


class BlogApi(APIView):
    def add_blog(self, request):
        log = 1
        context = {}
        context['result'] = FAILED

        user = request.user
        if request.method == 'POST':
            log = 2
            add_blog_form = AddBlogForm(request.POST)
            if add_blog_form.is_valid():
                log = 3 
                title = add_blog_form.cleaned_data['title'] 
                blog = BlogRepo(request=request).add_blog(
                    title=title,
                  
                )

                if blog is not None:
                    log = 4
                    print(blog)
                    blog = BlogSerializer(blog).data
                    context['blog'] = blog
                    context['result'] = SUCCEED
        return JsonResponse(context)

    