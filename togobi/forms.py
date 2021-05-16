from django import forms
from django.forms import ModelForm
from togobi.models import Content, ContentFile

class DateInput(forms.DateInput):
    input_type = 'date'

class FileInput(forms.FileInput):
    input_type = 'file'

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = (
            "title",
            "description",
            "tags",
            "target_date",
            "is_active"
            )
        widgets = {
            'target_date': DateInput(),
        }
        labels = {
            "is_active": "Active"
        }
    def __init__(self, *args, **kwargs):
        edit_check = kwargs.pop('edit_check', False)
        super(ContentForm, self).__init__(*args, **kwargs)
        if not edit_check:
            del self.fields['is_active']

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
            'source': FileInput()
        }