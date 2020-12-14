from django import forms
from django.forms import ModelForm
from togobi.models import Content, ContentFile

class DateInput(forms.DateInput):
    input_type = 'date'

class FileInput(forms.FileInput):
    input_type = 'file'

class ContentAddForm(ModelForm):
    class Meta:
        model = Content
        fields = (
            "title",
            "description",
            "tags",
            "target_date",
            )
        widgets = {
            'target_date': DateInput(),
        }

class ContentFileAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContentFileAddForm, self).__init__(*args, **kwargs)
        self.fields['source'].required = False

    class Meta:
        model = ContentFile
        fields = (
            "source",
        )
        widgets = {
            'source': FileInput()
        }