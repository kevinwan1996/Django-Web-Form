from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import IVV, Submitter, Recommendations, Risk, LifeCycle, State, Entire, Email

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class EmailForm(forms.ModelForm):
	class Meta:
		model = Email
		fields = ('subject', 'rec_one', 'rec_two', 'rec_three', 'rec_four', 'body')

class EntireForm(forms.ModelForm):
	class Meta:
		model = Entire
		exclude = ('user', 'risk_id', 'state_id', 'submitter_id', 'lc_id', 'rec_id', 'ivv_id')

class StateForm(forms.ModelForm):
	# state_name = forms.CharField(max_length=30, required=True)
	# poc_name = forms.CharField(max_length=30, required=True)
	# poc_email = forms.CharField(max_length=50, required=True)
	def __init__(self, *args, **kwargs):
		super(StateForm, self).__init__(*args, **kwargs)
		self.fields['POC_email'].widget.attrs.update({
			'id': 'state_POC_email'
		})

	class Meta:
		model = State
		exclude = ('state_id', 'update_date')

class SubmitterForm(forms.ModelForm):
	# submitter_name = forms.CharField(max_length=30, required=True)
	# submitter_phone = forms.CharField(max_length=10, required=True)
	# submitter_title = forms.CharField(max_length=15, required=True)
	class Meta:
		model = Submitter
		exclude = ('submitter_id',)

class IVVGeneralForm(forms.ModelForm):
	# executive_summary = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '<Input Executive Summary Here>', 'max_length': '2000', 'size': '1000' }))
	class Meta:
		model = IVV
		fields = ('project_name', 'program_name', 'progress_report_date', 'activity_one_consult_date','target_RFP_release_date', 'target_IVV_on_board_date', 'next_progress_report_date', 'total_budget', 'earned_value', 'budget_variance', 'schedule_variance', 'other','executive_summary')

class LCForm(forms.ModelForm):

	class Meta:
		model = LifeCycle
		exclude = ('ivv_id', 'lc_id', 'module_functional',)

class LCForm2(forms.ModelForm):

	class Meta:
		model = LifeCycle
		exclude = ('ivv_id', 'lc_id', 'module_business',)

class RiskForm(forms.ModelForm):
	class Meta:
		model = Risk
		exclude = ('risk_id', 'ivv_id',)

class RecForm(forms.ModelForm):
	class Meta:
		model = Recommendations
		exclude = ('rec_id', 'ivv_id',)
class GeneralInfoForm(forms.Form):
	state_name = forms.CharField(max_length=15)
	project_name = forms.CharField(max_length=15)
	program_name = forms.CharField(max_length=15)
class ExecAndBudgetForm(forms.Form):
	executive_summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Executive Summary'}), required=False)
	total_budget = forms.CharField(max_length=4)
	earned_value = forms.CharField(max_length=4)
	budget_variance = forms.CharField(max_length=4)
	schedule_variance = forms.CharField(max_length=4)

# class TodoListForm(forms.ModelForm):
#   class Meta:
#     model = TodoList
#     fields = ('name',)


# class TodoItemForm(forms.ModelForm):
#   class Meta:
#     model = TodoItem
#     exclude = ('list',)

