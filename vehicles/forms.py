from django import forms
from django.forms.fields import IntegerField


class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=50, required=True)


class AddTripPathForm(forms.Form):
    source_id=forms.IntegerField(  required=True)
    destination_id=forms.IntegerField(  required=True)
    cost=forms.IntegerField(required=False)
    duration=forms.IntegerField(required=False)
    distance=forms.IntegerField(required=False)


class AddDriverForm(forms.Form):
    profile_id=forms.IntegerField(  required=True)


class AddAreaForm(forms.Form):
    name=forms.CharField( max_length=50, required=True)
    code=forms.CharField( max_length=50, required=False)


class VehicleReportForm(forms.Form):
    vehicle_id=forms.IntegerField(  required=True)
    month=forms.IntegerField(  required=True)
    year=forms.IntegerField(  required=True)


class AddPassengerForm(forms.Form):
    profile_id=forms.IntegerField(  required=True)


class AddServiceManForm(forms.Form):
    profile_id=forms.IntegerField(  required=True)
    name=forms.CharField( max_length=50, required=True)
    tel=forms.CharField( max_length=50, required=False)
    address=forms.CharField( max_length=50, required=False)


class FilterTripForm(forms.Form):
    title=forms.CharField( max_length=50, required=False)
    vehicle_id=forms.IntegerField(required=False)
    driver_id=forms.IntegerField( required=False)
    trip_path_id=forms.IntegerField( required=False)
    start_date=forms.CharField( max_length=50, required=False)
    end_date=forms.CharField( max_length=50, required=False)


class AddWorkShiftForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    start_datetime=forms.CharField( max_length=50, required=True)
    end_datetime=forms.CharField( max_length=50, required=True)
    driver_id=forms.IntegerField( required=True)
    area_id=forms.IntegerField( required=True)
    income=forms.IntegerField( required=True)
    outcome=forms.IntegerField( required=True)
    description=forms.CharField( max_length=5000, required=False)


class AddMaintenanceForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    service_man_id=forms.IntegerField(required=False)
    event_datetime=forms.CharField( max_length=25, required=True)
    title=forms.CharField( max_length=100, required=True)
    description=forms.CharField( max_length=5000, required=False)
    paid=forms.IntegerField(required=True)
    maintenance_type=forms.CharField( max_length=100, required=False)
    kilometer=forms.IntegerField( required=False)


class AddVehicleForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)


class AddPassengerToTripForm(forms.Form):
    passenger_id=forms.IntegerField( required=True)
    trip_id=forms.IntegerField( required=True)


class FilterTripsForm(forms.Form):
    title=forms.CharField( max_length=100, required=False)
    start_report_datetime=forms.CharField( max_length=100, required=False)
    end_report_datetime=forms.CharField( max_length=100, required=False)
    driver_id=forms.IntegerField( required=False)
    vehicle_id=forms.IntegerField( required=False)
    driver_id=forms.IntegerField( required=False)


class AddTripForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    passengers=forms.CharField( max_length=5500, required=False)
    paths=forms.CharField( max_length=5500, required=False)
    start_datetime=forms.CharField( max_length=50, required=False)
    end_datetime=forms.CharField( max_length=50, required=False)
    vehicle_id=forms.IntegerField(required=False)
    driver_id=forms.IntegerField(required=False)
    delay=forms.IntegerField(required=False)
    cost=forms.IntegerField(required=True)
    delay=forms.IntegerField(required=False)


class AddVehicleWorkEventForm(forms.Form):
    work_shift_id=forms.IntegerField(required=True)
    event_type=forms.CharField( max_length=50, required=True)
    vehicle_id=forms.IntegerField(required=True)
    event_datetime=forms.CharField( max_length=50, required=True)
    kilometer=forms.IntegerField( required=True)
     
    description=forms.CharField( max_length=5000, required=False)

