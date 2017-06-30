from __future__ import unicode_literals
import time
import hashlib
from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


def _createHash():
	hash = hashlib.sha1()
	hash.update(str(time.time()))
	return hash.hexdigest()[:-10]
# Create your models here.

class Email(models.Model):
	subject = models.CharField(max_length=250)
	body = models.TextField()
	rec_one = models.CharField(max_length=50)
	rec_two = models.CharField(max_length=50, blank=True)
	rec_three = models.CharField(max_length=50, blank=True)
	rec_four = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.rec_one + self.rec_two + self.rec_three + self.rec_four + self.subject

class PDF(models.Model):
	file = models.FileField()
	user = models.ForeignKey(User)
	ivv_id = models.CharField(max_length=10, default="null")

	def __str__(self):
		return str(self.user) + self.ivv_id

class Entire(models.Model):
	user = models.ForeignKey(User)
	state_id = models.CharField(max_length=10)
	submitter_id = models.CharField(max_length=10)
	ivv_id = models.CharField(max_length=10)

	def __str__(self):
		return str(self.user)

class State(models.Model):
	state_id = models.AutoField(primary_key=True)
	# phone_regex = RegexValidator(regex=r'^?1?\d{9,15}$', message="Phone number must be entered in the format: '1234567890'. Up to 15 digits allowed. ")
	state_name = models.CharField(max_length=100, default="None")
	POC_name = models.CharField(max_length=100, default="None")
	POC_email = models.CharField(max_length=100, default="None")
	update_date = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return "State: " + self.state_name + " POC: " + self.POC_name

	# @classmethod
	# def create(state_name, poc_name, poc_email):
	# 	state = State.object.create(state_name, poc_name, poc_email)
	# 	state.save()
	# 	return state

class Submitter(models.Model):
	submitter_id = models.AutoField(primary_key=True)
	phone_regex = RegexValidator(regex=r'^?1?\d{9,15}$', message="Phone number must be entered in the format: '1234567890'. Up to 15 digits allowed. ")
	submitter_name = models.CharField(max_length=100, default="None")
	submitter_phone = models.CharField(max_length=10, default="None")
	submitter_title = models.CharField(max_length=10, default="None")
	submitter_email = models.CharField(max_length=50, default="None")

	def __str__(self):
		return self.submitter_name + self.submitter_title

class LifeCycle(models.Model):
	lc_id = models.AutoField(primary_key=True)
	status_choices = (
					  ('No plans for developement', 'No plans for development'),
					  ('Pre-R1', 'Pre-R1'),
					  ('R1', 'R1'),
					  ('R2', 'R2'),
					  ('R3', 'R3')
					  )
	status = models.CharField(max_length=40, choices=status_choices, blank=True)
	module_choices_business = (
		('Business Relationship Management', 'Business Relationship Management'),
		('Care Management', 'Care Management'),
		('Contractor Management', 'Contractor Management'),
		('Eligibility & Enrollment', 'Eligibility & Enrollment'),
		('Financial Management', 'Financial Management'),
		('Member Management', 'Member Management'),
		('Operations Management', 'Operations Management'),
		('Performance Management', 'Performance Management'),
		('Plan Management', 'Plan Management'),
		('Provider Management', 'Provider Management')
		)
	module_choices_functional = (
		('Member Eligibility', 'Member Eligibility'),
		('Member Enrollment', 'Member Enrollment'),
		('FFS Claims and Adjudication', 'FFS Claims and Adjudication'),
		('Pharmacy', 'Pharmacy'),
		('Third Party Liability', 'Third Party Liability'),
		('Care Management', 'Care Management'),
		('Program Integrity', 'Program Integrity'),
		('Decision Support System', 'Decision Support System'),
		('Reference Data Management', 'Reference Data Management'),
		('Provider Management', 'Provider Management'),
		('Registries', 'Registries')
		)
	module_business = models.CharField(max_length=50, choices=module_choices_business)
	module_functional = models.CharField(max_length=50, choices=module_choices_functional)
	target_approval_date = models.CharField(blank=True, help_text='Enter all dates in format MM-DD-YY', max_length=8)
	target_development_date = models.CharField(blank=True, max_length=8)
	target_R1 = models.CharField(blank=True, max_length=8)
	target_R2 = models.CharField(blank=True, max_length=8)
	target_go_live = models.CharField(blank=True, max_length=8)
	target_R3 = models.CharField(blank=True, max_length=8)
	ivv_id = models.CharField(max_length=10)

	def __str__(self):
		return self.module_functional + self.module_business + self.status

class Recommendations(models.Model):
	rec_id = models.AutoField(primary_key=True)
	ivv_id = models.CharField(max_length=10)
	recommendation_number = models.CharField(max_length=1, blank=True)
	recommendation_date = models.CharField(max_length=8)
	recommendation = models.TextField(default="None")
	resolved = models.CharField(max_length=5, blank=True)
	comments = models.TextField(default="None")

	def __str__(self):
		return self.recommendation + self.resolved + self.comments

class Risk(models.Model):
	risk_id = models.AutoField(primary_key=True)
	ivv_id = models.CharField(max_length=10)
	risk_ID_number = models.CharField(max_length=10, blank=True)
	title = models.CharField(max_length=20, blank=True)
	description = models.TextField(default="None")
	prob_choices = (
		('1', '1'),
		('2', '2'),
		('3', '3')
		)
	probability = models.CharField(max_length=1, choices=prob_choices, blank=True)
	impact = models.CharField(max_length=10, blank=True)
	score = models.CharField(max_length=1, blank=True)
	target_resolution_date = models.CharField(max_length=8)
	status = models.CharField(max_length=10, blank="True")

	def __str__(self):
		return self.risk_ID_number + self.title + self.description + self.probability

class IVV(models.Model):
	ivv_id = models.AutoField(primary_key=True)
	state_id = models.CharField(max_length=10)
	submitter_id = models.CharField(max_length=10)
	project_name = models.CharField(max_length=20)
	prog_choices = (
		('MMIS', 'MMIS'),
		('E&E', 'E&E'),
		('HIT', 'HIT')
		)
	program_name = models.CharField(max_length=10, choices=prog_choices)
	progress_report_date = models.CharField(max_length=8)
	activity_one_consult_date = models.CharField(max_length=8)
	target_RFP_release_date = models.CharField(max_length=8)
	next_progress_report_date = models.CharField(max_length=8)
	target_IVV_on_board_date = models.CharField(max_length=8)
	executive_summary = models.TextField(default="None")
	total_budget = models.CharField(max_length=10, blank=True)
	earned_value = models.CharField(max_length=10, blank=True)
	budget_variance = models.CharField(max_length=10, blank=True)
	schedule_variance = models.CharField(max_length=10, blank=True)
	other = models.CharField(max_length=10, blank=True)


	def __str__(self):
		return self.project_name + self.program_name

# class TodoList(models.Model):
#     name = models.CharField(max_length=100)

#     def __unicode__(self):
#         return self.name


# class TodoItem(models.Model):
#     name = models.CharField(max_length=150,
#                help_text="e.g. Buy milk, wash dog etc")
#     list = models.ForeignKey(TodoList)

#     def __unicode__(self):
#         return self.name + " (" + str(self.list) + ")"





