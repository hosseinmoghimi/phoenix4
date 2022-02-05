import json
from django.shortcuts import render
from hesabyar.forms import AddFinancialDocumentForm

from hesabyar.repo import FinancialDocumentCategoryRepo,FinancialDocumentRepo, ProfileFinancialAccountRepo, FinancialAccountRepo, TagRepo
from hesabyar.serializers import FinancialDocumentSerializer
from .apps import APP_NAME
from core.views import CoreContext
from django.views import View

# Create your views here.
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "hesabyar/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_accounts = FinancialAccountRepo(request=request).list()
        context['financial_accounts'] = financial_accounts
        return render(request, TEMPLATE_ROOT+"index.html", context)

    def tag(self, request, *args, **kwargs):
        context = getContext(request=request)
        tag = TagRepo(request=request).tag(*args, **kwargs)
        context['title'] = tag.name
        financial_accounts = FinancialAccountRepo(
            request=request).list(tag_id=tag.id)
        context['financial_accounts'] = financial_accounts
        return render(request, TEMPLATE_ROOT+"tag.html", context)


class ReportViews(View):
    def financial_document_category(self, request, *args, **kwargs):
        context = getContext(request=request)
        financial_document_category=FinancialDocumentCategoryRepo(request=request).financial_document_category(*args, **kwargs)
        financial_documents = FinancialDocumentRepo().list(
            category_id=financial_document_category.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['financial_document_category'] = financial_document_category
        context['rest']=0
        return render(request, TEMPLATE_ROOT+"financial-document-category.html", context)

    def profile_financial_account(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        profile_financial_account = ProfileFinancialAccountRepo(
            request=request).profile_financial_account(*args, **kwargs)
        context['profile_financial_account'] = profile_financial_account
        context['financial_account'] = profile_financial_account
        financial_documents = FinancialDocumentRepo().list(
            account_id=profile_financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['financial_documents'] = financial_documents
        return render(request, TEMPLATE_ROOT+"profile-financial-account.html", context)

    def financial_account(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_account = FinancialAccountRepo(
            request=request).financial_account(*args, **kwargs)
        context['financial_account'] = financial_account
        financial_documents = FinancialDocumentRepo().list(
            account_id=financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['rest']=financial_account.rest()
        if request.user.has_perm(APP_NAME+".add_financialdocumet"):
            document_categories=FinancialDocumentCategoryRepo(request=request).list()
            context['document_categories']=document_categories
            context['add_financial_document_form'] = AddFinancialDocumentForm()
        return render(request, TEMPLATE_ROOT+"financial-account.html", context)

    def financial_document(self, request, *args, **kwargs):
        context = getContext(request=request)
        financial_document = FinancialDocumentRepo().financial_document(*args, **kwargs)
        context['financial_document'] = financial_document
        return render(request, TEMPLATE_ROOT+"financial-document.html", context)
