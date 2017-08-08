from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from forms import *
# from views import ContactWizard

urlpatterns = [
	url(r'^$', views.landing, name='landing'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^state/$', login_required(views.general), name='general'),
	url(r'^signup/webform/landing', views.landing, name='landing'),
	url(r'^state/webform/landing', views.landing, name='landing'),
	url(r'^practice/$', views.practice, name = 'temp'),
	url(r'^display/$', login_required(views.display), name = 'display'),

	url(r'^pdf/$', login_required(views.pdf), name='pdf'),
	url(r'^excel/$', login_required(views.excel), name='excel'),
	url(r'^email/$', login_required(views.email), name='email'),
	# url(r'^email_contact/$', login_required(views.email), name='email_contact'),
	url(r'email_sent/$', login_required(views.email_sent), name='email_sent'),

	#Multi-Step form
	# url(r'^multi/$', ContactWizard.as_view(GeneralInfoForm, ExecAndBudgetForm)),
	#login logout
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'webform/logged_out.html'}, name='logout')
]