from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import MeteoriteClass, MeteoriteLanding


class MeteoriteClassForm(forms.ModelForm):
	class Meta:
		model = MeteoriteClass
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))

class MeteoriteLandingForm(forms.ModelForm):
	class Meta:
		model = MeteoriteLanding
		fields = ('meteorite_count', 'average_mass', 'max_mass', 'min_mass')
		labels = {
			'average_mass': "Average mass (g)",
			'max_mass': "Max mass (g)",
			'min_mass': "Min mass (g)"
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))
