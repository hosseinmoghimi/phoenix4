from rest_framework import serializers
from .models import Book, Lend, Member
from authentication.serializers import ProfileSerializer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model=Book
        fields=['id','title','shelf','row','col','get_edit_url','get_absolute_url']


class MemberSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Member
        fields=['id','profile','level','color','persian_membership_ended','persian_membership_started','get_edit_url','get_absolute_url']


class LendSerializer(serializers.ModelSerializer):
    member=MemberSerializer()
    book=BookSerializer()
    class Meta:
        model=Lend
        fields=['id','member','book','persian_date_lended','persian_date_returned','get_edit_url','get_absolute_url']

