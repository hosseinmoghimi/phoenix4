from django import forms

class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=50, required=True)
class AddSchoolForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
class AddClassRoomForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
    school_id=forms.IntegerField( required=True)
class AddMajorForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
class AddTeacherForm(forms.Form):
    profile_id=forms.IntegerField( required=True)
class AddStudentForm(forms.Form):
    profile_id=forms.IntegerField( required=True)
class AddSessionForm(forms.Form):
    active_course_id=forms.IntegerField( required=True)
class AddAttendanceForm(forms.Form):
    student_id=forms.IntegerField( required=True)
    session_id=forms.IntegerField( required=True)
    status=forms.CharField( max_length=50, required=True)
    description=forms.CharField( max_length=500, required=False)
    time=forms.CharField( max_length=50, required=False)
class AddDocumentForm(forms.Form):
    book_id=forms.IntegerField( required=True)
    title=forms.CharField( max_length=50, required=True)