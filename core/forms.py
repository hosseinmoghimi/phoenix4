from django import forms

class AddPageForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageLinkForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    url=forms.CharField(max_length=1000, required=True)
    

class AddPageDocumentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    comment=forms.CharField(max_length=200, required=True)
    

class DeletePageCommentForm(forms.Form):
    page_comment_id=forms.IntegerField(required=True)