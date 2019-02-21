from django import forms
from temp_sensor.models import tempSensor
from datetime import datetime




class TempForm(forms.Form):
    """Model Foo form"""
    class Meta:
        model = tempSensor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TempForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                HTML("""<a role="button" class="btn btn-default"
                        href="{% url "index" %}">Cancel</a>"""),
                Submit('save', 'Submit'),
        ))

#form model variations
class SearchForm(forms.Form):
	upperBound = forms.IntegerField()
	lowerBound = forms.IntegerField()
	set_Temp = forms.IntegerField()
	date_time = forms.DateTimeField(initial=datetime.now(), required=False)

class BoundForm(forms.ModelForm):
	class Meta:
		model = tempSensor
		fields = '__all__'