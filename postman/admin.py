from django.contrib import admin

from postman.models import Letter, LetterPosition, LetterSignature

# Register your models here.
admin.site.register(Letter)
admin.site.register(LetterSignature)
admin.site.register(LetterPosition)