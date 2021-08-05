from django import forms
from django.forms import ModelForm
from togobi.models import Content, ContentFile

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = (
            'title',
            'description',
            'tags',
            'target_date',
            'is_active'
            )
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':5, 'cols':20}),
        }
        labels = {
            'is_active': 'Active'
        }

class ContentFileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContentFileForm, self).__init__(*args, **kwargs)
        self.fields['source'].required = False

    class Meta:
        model = ContentFile
        fields = (
            "source",
        )
        widgets = {
            'source': forms.FileInput(attrs={'type': 'file'})
        }