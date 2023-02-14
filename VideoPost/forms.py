from django import forms

class inputLink(forms.Form):
    link =forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "placeholder":"Video Link Here",
            "class":"link-input",
            "name":"link",
            "required":True,
            "maxlength":"200",
            "id":"link-input"
            }))
    
    
        
    
    