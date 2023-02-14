from django.contrib import admin 
from django.contrib.auth.models import User , Permission
from django.contrib.auth.admin import UserAdmin
from .models import TestModel
# Register your models here.

# from typing import Set



admin.site.register(TestModel)
#just doing some stuff with user model in admin panel
#code here dosn't really realte to the project Qabasat for now
#it dosnt affect the work flow of the project


admin.site.unregister(User)

@admin.register(User)
class CustomUser (UserAdmin):
    
    def get_form(self, request, obj,  **kwargs):
            
        form=super().get_form(request, obj, **kwargs)
        
        if obj is not None:
            print(request.user.username)
            
            if not request.user.is_superuser:
                form.base_fields["username"].disabled=True
            
            print(f"User: {request.user} , Obj: {obj}")
            if request.user == obj :
                print(True)
                for f in form.base_fields:
                    print(f)
                    form.base_fields[f].disabled=True
            
            else:
                print(False)
            form.base_fields["username"].disabled=False
        else:
            print("Object is None -> Create New User")
        return form
    
    # def has_delete_permission(self, request, obj=None) -> bool:
    #     return False
    
    # def has_change_permission(self, request, obj=None) -> bool:
    #     return False
    
    #Not-RealCase Function
    #override the view that lets the user add another user
    #and redirect the form to admin page 
    def add_view(self, request, form_url=None, extra_context=None):
        
        if not request.user.is_superuser:
            form_url="/admin/"
        
        view= super().add_view(request, form_url, extra_context)
        
        return view
    
    def has_delete_permission(self, request,obj=None):
        #allow all non-superuser users to delete user 
        #and prevent superusers from deleteing users
        
        if request.user.is_superuser:
            return False
        else :
            return True
