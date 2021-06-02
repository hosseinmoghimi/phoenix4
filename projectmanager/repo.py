from projectmanager.enums import MaterialRequestStatusEnum, SignatureStatusEnum
from authentication.repo import ProfileRepo
from authentication.models import Profile
from projectmanager.serializers import MaterialRequestSerializer, MaterialSerializer
from django.db.models.query_utils import Q
from .apps import APP_NAME
from .models import Employee, Employer, Material, MaterialRequest, MaterialRequestSignature, Project, OrganizationUnit


class ProjectRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Project.objects

    def project(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'project_id' in kwargs:
            return self.objects.filter(pk=kwargs['project_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_project(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_project"):
            return None
        new_project = Project()

        if 'title' in kwargs:
            new_project.title = kwargs['title']

        if 'parent_id' in kwargs:
            new_project.parent_id = kwargs['parent_id']

        new_project.save()
        return new_project


class OrganizationUnitRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OrganizationUnit.objects

    def organization_unit(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'new_organization_id' in kwargs:
            return self.objects.filter(pk=kwargs['new_organization_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_organization_unit(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_organizationunit"):
            return None
        new_organization = OrganizationUnit()

        if 'title' in kwargs:
            new_organization.title = kwargs['title']

        if 'parent_id' in kwargs:
            new_organization.parent_id = kwargs['parent_id']

        new_organization.save()
        return new_organization


class EmployeeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Employee.objects

    def employee(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'employee_id' in kwargs:
            return self.objects.filter(pk=kwargs['employee_id']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_employee(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_employee"):
            return None
        new_employee = Employee()

        if 'profile_id' in kwargs:
            new_employee.profile_id = kwargs['profile_id']

        if 'organization_unit_id' in kwargs:
            new_employee.organization_unit_id = kwargs['organization_unit_id']

        new_employee.save()
        return new_employee


class EmployerRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Employer.objects

    def employer(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'employer_id' in kwargs:
            return self.objects.filter(pk=kwargs['employee_id']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])

        return objects.all()

    def add_employer(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_employer"):
            return None
        new_employer = Employer()

        if 'title' in kwargs:
            new_employer.title = kwargs['title']
        if 'pre_title' in kwargs:
            new_employer.pre_title = kwargs['pre_title']

        new_employer.save()
        return new_employer


class MaterialRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Material.objects

    def material(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'material_id' in kwargs:
            return self.objects.filter(pk=kwargs['material_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def material_request(self, *args, **kwargs):
        objects = MaterialRequest.objects
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
        if 'material_id' in kwargs:
            return objects.filter(pk=kwargs['material_id']).first()
        if 'title' in kwargs:
            return objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_material_request(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_materialrequest"):
            return None
        new_material_request = MaterialRequest(status=MaterialRequestStatusEnum.REQUESTED)
        if 'project_id' in kwargs:
            new_material_request.project_id = kwargs['project_id']
        if 'material_id' in kwargs:
            new_material_request.material_id = kwargs['material_id']
        if 'quantity' in kwargs:
            new_material_request.quantity = kwargs['quantity']
        if 'unit_name' in kwargs:
            new_material_request.unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            new_material_request.unit_price = kwargs['unit_price']
        if 'description' in kwargs:
            new_material_request.description = kwargs['description']
        if 'status' in kwargs:
            new_material_request.status = kwargs['status']
        if 'status' in kwargs:
            new_material_request.status = kwargs['status']
        profile = ProfileRepo(user=self.user).me
        new_material_request.profile = profile
        if new_material_request.quantity > 0 and new_material_request.unit_price > 0:
            new_material_request.save()
            new_material_request.material.unit_price = new_material_request.unit_price
            new_material_request.material.unit_name = new_material_request.unit_name
            new_material_request.material.save()
            material_request_signature=MaterialRequestSignature(profile=profile,material_request=new_material_request,status=SignatureStatusEnum.REQUESTED)
            material_request_signature.save()
            return new_material_request

    def add_material(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_material"):
            return None
        new_material = Material()

        if 'parent_id' in kwargs:
            new_material.parent_id = kwargs['parent_id']

        if 'title' in kwargs:
            new_material.title = kwargs['title']
        if new_material.parent_id == 0:
            new_material.parent = None
        new_material.save()
        return new_material
