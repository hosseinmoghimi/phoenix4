from typing import ContextManager
from utility.persian import PersianCalendar
from .serializers import TaxSerializer
from core.constants import SUCCEED, FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import TaxRepo
from .forms import *


class TaxApi(APIView):
    def add_tax(self, request):
        log = 1
        context = {}
        context['result'] = FAILED

        user = request.user
        if request.method == 'POST':
            log = 2
            add_tax_form = AddTaxForm(request.POST)
            if add_tax_form.is_valid():
                log = 3
                amount = add_tax_form.cleaned_data['amount']
                title = add_tax_form.cleaned_data['title']
                description = add_tax_form.cleaned_data['description']
                year = add_tax_form.cleaned_data['year']
                tax = TaxRepo(request=request).add_tax(
                    title=title,
                    amount=amount,
                    year=year,
                    description=description,
                )

                if tax is not None:
                    log = 4
                    tax = TaxSerializer(tax).data
                    context['tax'] = tax
                    context['result'] = SUCCEED
        return JsonResponse(context)

    