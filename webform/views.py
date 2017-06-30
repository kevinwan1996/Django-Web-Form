from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from webform.forms import SignUpForm, StateForm, SubmitterForm, IVVGeneralForm, LCForm, LCForm2, RiskForm, RecForm, EntireForm, EmailForm
from .models import *
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext  # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
# from weasyprint import HTML
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from functools import partial
from reportlab.graphics.shapes import Drawing, Group, Line
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from StringIO import StringIO
from django.core.files.base import ContentFile
import os

def email(request):
	if request.method == 'POST':
		email_form = EmailForm(request.POST, instance=Email())
		if email_form.is_valid():
			email_instance = email_form.save()
			entire_results = Entire.objects.filter(user=request.user).latest('ivv_id')
			if int(entire_results.ivv_id) == int(IVV.objects.latest('ivv_id').ivv_id):
				ivv_results = IVV.objects.latest('ivv_id')
			# ivv_results = IVV.objects.latest('ivv_id')
			lc_results = LifeCycle.objects.filter(ivv_id=ivv_results.ivv_id)
			state_results = State.objects.get(state_id=ivv_results.state_id)
			submitter_results = Submitter.objects.get(submitter_id=ivv_results.submitter_id)
			rec_results = Recommendations.objects.filter(ivv_id=ivv_results.ivv_id)
			risk_results = Risk.objects.filter(ivv_id=ivv_results.ivv_id)

			#Set up ReportLab doc
			styles = getSampleStyleSheet()
			styleH = styles['Heading1']
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="IV&V_REPORT.pdf"'
			buffer = StringIO()
			doc = SimpleDocTemplate(buffer)
			elements = []
			styles = getSampleStyleSheet()

			#Title Section

			title = 'Independent Verification and Validation Report'
			ptext = '<font size=20>%s </font>' % title
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2, 20))

			
			d = Drawing(100,1)
			d.add(Line(-100,0,1000,0))
			elements.append(d)
			elements.append(Spacer(2,20))

			general_info = 'General Information'
			ptext = '<font size=16>%s </font>' % general_info
			elements.append(Paragraph(ptext, styles["Normal"]))

			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,130,0))
			elements.append(d)

			elements.append(Spacer(2,20))
			# General Information Section

			line_one = [['State', 'Project Name', 'Program Name', 'Progress Report Date', 'POC Name'],['----------------------','----------------------','----------------------','----------------------','----------------------'], [state_results.state_name, ivv_results.project_name, ivv_results.program_name, ivv_results.progress_report_date, state_results.POC_name]]
			t_one = Table(line_one, 5*[1.5*inch], 3*[0.2*inch])
			line_two = [['POC Email', 'Submitter Name', 'Submitter Role', 'Submitter Email', 'Submitter Phone'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [state_results.POC_email, submitter_results.submitter_name, submitter_results.submitter_title, submitter_results.submitter_email, submitter_results.submitter_phone]]
			t_two = Table(line_two, 5* [1.5*inch], 3*[0.2*inch])
			line_three = [['Activity 1 Consult Date', 'RFP Release Date', 'IV&V Onboard Date', 'Next Progress Report Date'], ['----------------------','----------------------','----------------------','----------------------'], [ivv_results.activity_one_consult_date, ivv_results.target_RFP_release_date, ivv_results.target_IVV_on_board_date, ivv_results.next_progress_report_date]]
			t_three = Table(line_three, 4 * [1.5*inch], 3*[0.2*inch])


			elements.append(t_one)
			elements.append(Spacer(1,20))
			elements.append(t_two)
			elements.append(Spacer(1,20))
			elements.append(t_three)

			elements.append(Spacer(2,20))

			#Executive Summary
			executive_summary = 'Executive Summary'
			ptext = '<font size=16>%s</font>'%executive_summary
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,130,0))
			elements.append(d)

			elements.append(Spacer(2,20))

			e_s = ivv_results.executive_summary
			ptext = '<font size=10>%s </font>'%e_s
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,20))

			#Project status
			project_status = 'Project Management Office Status'
			ptext = '<font size=16>%s</font>'%project_status
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,215,0))
			elements.append(d)
			elements.append(Spacer(2,20))

			ps_data = [['Total Budget', 'Earned Value(EV)', 'Budget Variance(%)', 'Schedule Variance(%)', 'Other'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [ivv_results.total_budget, ivv_results.earned_value, ivv_results.budget_variance, ivv_results.schedule_variance, ivv_results.other]]
			t_ps = Table(ps_data, 5*[1.5*inch], 3*[0.2*inch])
			elements.append(t_ps)
			elements.append(Spacer(2,20))

			#Life Cycle Status
			life_cycle = 'Life Cycle Status and Schedule'
			ptext = '<font size=16>%s</font>'%life_cycle
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,200,0))
			elements.append(d)
			elements.append(Spacer(2,15))

			for lc in lc_results:
				if lc.module_business:
					module_name = lc.module_business
				if lc.module_functional:
					module_name = lc.module_functional
				ptext = '<font size=12>%s (Status: %s)</font>'%(module_name, lc.status)
				elements.append(Paragraph(ptext, styles["Normal"]))
				elements.append(Spacer(2,5))

				d = Drawing(100,1)
				d.add(Line(0,0,200,0))
				elements.append(d)
				elements.append(Spacer(2,15))

				data = [['Target App. Date','Target Dev. Start', 'Target R1', 'Target R2', 'Target Go Live', 'Target R3'], ['----------------------','----------------------','----------------------','----------------------','----------------------','----------------------'], [lc.target_approval_date, lc.target_development_date, lc.target_R1, lc.target_R2, lc.target_go_live, lc.target_R3]]
				table = Table(data, 6*[1.3*inch], 3*[0.2*inch])
				elements.append(table)
				elements.append(Spacer(2,15))

			elements.append(Spacer(2,10))
			#Risks
			risk = 'Risks'
			ptext = '<font size=16>%s</font>'%risk
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,45,0))
			elements.append(d)
			elements.append(Spacer(2,15))

			for risk in risk_results:
				ptext = '<font size=14>%s (ID: %s)</font>'%(risk.title, risk.risk_ID_number)
				elements.append(Paragraph(ptext, styles["Normal"]))
				elements.append(Spacer(2,5))

				d = Drawing(100,1)
				d.add(Line(0,0,90,0))
				elements.append(d)
				elements.append(Spacer(2,15))

				ptext = '<font size=12>Description: %s</font>'%risk.description
				elements.append(Paragraph(ptext, styles["Normal"]))
				elements.append(Spacer(2,15))

				risk_info = [['Probability', 'Impact', 'Risk Score', 'Target Resolution Date', 'Status'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [risk.probability, risk.impact, risk.score, risk.target_resolution_date, risk.status]]
				risk_table = Table(risk_info, 5*[1.5*inch], 3*[0.2*inch])
				elements.append(risk_table)
				elements.append(Spacer(2,20))

			#Recommendations
			recs = 'Recommendations'
			ptext = '<font size=16>%s</font>'%recs
			elements.append(Paragraph(ptext, styles["Normal"]))
			elements.append(Spacer(2,5))

			d = Drawing(100,1)
			d.add(Line(0,0,135,0))
			elements.append(d)
			elements.append(Spacer(2,15))
			for rec in rec_results:
				ptext = '<font size=12>Recommendation #: %s (Date of Recommendation: %s, Resolved?: %s)</font>'%(rec.recommendation_number, rec.recommendation_date, rec.resolved)
				elements.append(Paragraph(ptext, styles["Normal"]))
				elements.append(Spacer(2,15))

				ptext = '<font size=12> Recommendation: %s</font>' %rec.recommendation
				elements.append(Paragraph(ptext, styles["Normal"]))

				elements.append(Spacer(2,20))
				ptext = '<font size=12> Comments: %s</font>'%rec.comments
				elements.append(Paragraph(ptext, styles["Normal"]))
			doc.build(elements)
			to_list = []
			to_list.append(email_instance.rec_one)
			to_list.append(email_instance.rec_two)
			to_list.append(email_instance.rec_three)
			to_list.append(email_instance.rec_four)
			email = EmailMessage(email_instance.subject, email_instance.body, to=to_list)
			email.attach('IV&V_REPORT.pdf',buffer.getvalue(), 'application/pdf' )
			email.send()
			buffer.close()
			return redirect("../email_sent")
	else:
		email_form = EmailForm(instance=Email())
	
	context = {'form': email_form}
	context.update(csrf(request))

	return render(request, 'webform/email_contact.html', context)
# Create your views here.
def email_sent(request):
	return render(request, "webform/email_sent.html", {})
def practice(request):

    doc = SimpleDocTemplate("/tmp/somefilename.pdf")
    styles = getSampleStyleSheet()
    Story = [Spacer(1,1*inch)]
    style = styles["Normal"]
    for i in range(100):
       bogustext = ("This is Paragraph number %s.  " % i) * 20
       p = Paragraph(bogustext, style)
       Story.append(p)
       Story.append(Spacer(1,0.2*inch))
    doc.build(Story)

    fs = FileSystemStorage("/tmp")
    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
        return response

    return response

def landing(request):
	return render(request, 'webform/landing.html', {})

@login_required
def general(request):
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = False

	RecFormSet = formset_factory(RecForm, max_num=15, formset=RequiredFormSet)
	RiskFormSet = formset_factory(RiskForm, max_num=15, formset=RequiredFormSet)
	LCFormSet = formset_factory(LCForm, max_num=15, formset=RequiredFormSet)
	LCFormSet2 = formset_factory(LCForm2, max_num=15, formset=RequiredFormSet)
	if request.method == 'POST':
		entire_form = EntireForm(request.POST, instance=Entire())
		state_form = StateForm(request.POST, instance=State())
		submitter_form = SubmitterForm(request.POST, instance=Submitter())
		ivv_gen_form = IVVGeneralForm(request.POST, instance=IVV())
		lc_formset = LCFormSet(request.POST, request.FILES, prefix='lc')
		lc_formset2 = LCFormSet2(request.POST, request.FILES, prefix='lc2')
		risk_formset = RiskFormSet(request.POST, request.FILES, prefix='risk')
		rec_formset = RecFormSet(request.POST, request.FILES, prefix='rec')	
		user = request.user
		if state_form.is_valid() and submitter_form.is_valid() and ivv_gen_form.is_valid() and lc_formset.is_valid() and lc_formset2.is_valid() and risk_formset.is_valid() and rec_formset.is_valid():
			entire_instance = entire_form.save(commit=False)
			state_instance = state_form.save()
			submitter_instance = submitter_form.save()
			ivv_instance = ivv_gen_form.save(commit=False)
			ivv_instance.state_id = state_instance.state_id
			ivv_instance.submitter_id = submitter_instance.submitter_id
			ivv_instance.save()
			for form in lc_formset.forms:
				lc = form.save(commit=False)
				lc.ivv_id = ivv_instance.ivv_id
				lc.save()
			for form in lc_formset2.forms:
				lc2 = form.save(commit=False)
				lc2.ivv_id = ivv_instance.ivv_id
				lc2.save()
			for form in risk_formset.forms:
				risk = form.save(commit=False)
				risk.ivv_id = ivv_instance.ivv_id
				risk.save()
			for form in rec_formset.forms:
				rec = form.save(commit=False)
				rec.ivv_id = ivv_instance.ivv_id
				rec.save()
			entire_instance.user = user
			entire_instance.state_id = state_instance.state_id
			entire_instance.submitter_id = submitter_instance.submitter_id
			entire_instance.ivv_id = ivv_instance.ivv_id
			entire_instance.save()
			return redirect('../display')
	else:
		entire_form = EntireForm(instance=Entire())
		state_form = StateForm(instance=State())
		submitter_form = SubmitterForm(instance=Submitter())
		ivv_gen_form = IVVGeneralForm(instance=IVV())
		lc_formset = LCFormSet(prefix='lc')
		lc_formset2 = LCFormSet2(prefix='lc2')
		risk_formset = RiskFormSet(prefix='risk')
		rec_formset = RecFormSet(prefix='rec')

	context = {'state_form': state_form,
			   'submitter_form' :submitter_form,
			   'ivv_form':ivv_gen_form,
			   'lc_formset': lc_formset,
			   'lc_formset2': lc_formset2,
			   'risk_formset': risk_formset,
			   'rec_formset': rec_formset
	}

	context.update(csrf(request))

	return render(request, 'webform/general.html', context)

def display(request):
	entire_results = Entire.objects.filter(user=request.user).latest('ivv_id')
	if int(entire_results.ivv_id) == int(IVV.objects.latest('ivv_id').ivv_id):
		ivv_results = IVV.objects.latest('ivv_id')
	lc_results = LifeCycle.objects.filter(ivv_id=ivv_results.ivv_id)
	state_results = State.objects.get(state_id=ivv_results.state_id)
	submitter_results = Submitter.objects.get(submitter_id=ivv_results.submitter_id)
	rec_results = Recommendations.objects.filter(ivv_id=ivv_results.ivv_id)
	risk_results = Risk.objects.filter(ivv_id=ivv_results.ivv_id)
	context = {'ivv_results':ivv_results,
			   'lc_results': lc_results,
			   'state_results': state_results,
			   'submitter_results':submitter_results,
			   'rec_results':rec_results,
			   'risk_results':risk_results
	}
	return render(request, 'webform/display.html', context)

def pdf(request):
	entire_results = Entire.objects.filter(user=request.user).latest('ivv_id')
	if int(entire_results.ivv_id) == int(IVV.objects.latest('ivv_id').ivv_id):
		ivv_results = IVV.objects.latest('ivv_id')
	lc_results = LifeCycle.objects.filter(ivv_id=ivv_results.ivv_id)
	state_results = State.objects.get(state_id=ivv_results.state_id)
	submitter_results = Submitter.objects.get(submitter_id=ivv_results.submitter_id)
	rec_results = Recommendations.objects.filter(ivv_id=ivv_results.ivv_id)
	risk_results = Risk.objects.filter(ivv_id=ivv_results.ivv_id)

	#Set up ReportLab doc
	styles = getSampleStyleSheet()
	styleH = styles['Heading1']
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="IV&V_REPORT.pdf"'
	buffer = StringIO()
	doc = SimpleDocTemplate(buffer)
	elements = []
	styles = getSampleStyleSheet()

	#Title Section

	title = 'Independent Verification and Validation Report'
	ptext = '<font size=20>%s </font>' % title
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2, 20))

	
	d = Drawing(100,1)
	d.add(Line(-100,0,1000,0))
	elements.append(d)
	elements.append(Spacer(2,20))

	general_info = 'General Information'
	ptext = '<font size=16>%s </font>' % general_info
	elements.append(Paragraph(ptext, styles["Normal"]))

	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,130,0))
	elements.append(d)

	elements.append(Spacer(2,20))
	# General Information Section

	line_one = [['State', 'Project Name', 'Program Name', 'Progress Report Date', 'POC Name'],['----------------------','----------------------','----------------------','----------------------','----------------------'], [state_results.state_name, ivv_results.project_name, ivv_results.program_name, ivv_results.progress_report_date, state_results.POC_name]]
	t_one = Table(line_one, 5*[1.5*inch], 3*[0.2*inch])
	line_two = [['POC Email', 'Submitter Name', 'Submitter Role', 'Submitter Email', 'Submitter Phone'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [state_results.POC_email, submitter_results.submitter_name, submitter_results.submitter_title, submitter_results.submitter_email, submitter_results.submitter_phone]]
	t_two = Table(line_two, 5* [1.5*inch], 3*[0.2*inch])
	line_three = [['Activity 1 Consult Date', 'RFP Release Date', 'IV&V Onboard Date', 'Next Progress Report Date'], ['----------------------','----------------------','----------------------','----------------------'], [ivv_results.activity_one_consult_date, ivv_results.target_RFP_release_date, ivv_results.target_IVV_on_board_date, ivv_results.next_progress_report_date]]
	t_three = Table(line_three, 4 * [1.5*inch], 3*[0.2*inch])


	elements.append(t_one)
	elements.append(Spacer(1,20))
	elements.append(t_two)
	elements.append(Spacer(1,20))
	elements.append(t_three)

	elements.append(Spacer(2,20))

	#Executive Summary
	executive_summary = 'Executive Summary'
	ptext = '<font size=16>%s</font>'%executive_summary
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,130,0))
	elements.append(d)

	elements.append(Spacer(2,20))

	e_s = ivv_results.executive_summary
	ptext = '<font size=10>%s </font>'%e_s
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,20))

	#Project status
	project_status = 'Project Management Office Status'
	ptext = '<font size=16>%s</font>'%project_status
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,215,0))
	elements.append(d)
	elements.append(Spacer(2,20))

	ps_data = [['Total Budget', 'Earned Value(EV)', 'Budget Variance(%)', 'Schedule Variance(%)', 'Other'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [ivv_results.total_budget, ivv_results.earned_value, ivv_results.budget_variance, ivv_results.schedule_variance, ivv_results.other]]
	t_ps = Table(ps_data, 5*[1.5*inch], 3*[0.2*inch])
	elements.append(t_ps)
	elements.append(Spacer(2,20))

	#Life Cycle Status
	life_cycle = 'Life Cycle Status and Schedule'
	ptext = '<font size=16>%s</font>'%life_cycle
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,200,0))
	elements.append(d)
	elements.append(Spacer(2,15))

	for lc in lc_results:
		if lc.module_business:
			module_name = lc.module_business
		if lc.module_functional:
			module_name = lc.module_functional
		ptext = '<font size=12>%s (Status: %s)</font>'%(module_name, lc.status)
		elements.append(Paragraph(ptext, styles["Normal"]))
		elements.append(Spacer(2,5))

		d = Drawing(100,1)
		d.add(Line(0,0,200,0))
		elements.append(d)
		elements.append(Spacer(2,15))

		data = [['Target App. Date','Target Dev. Start', 'Target R1', 'Target R2', 'Target Go Live', 'Target R3'], ['----------------------','----------------------','----------------------','----------------------','----------------------','----------------------'], [lc.target_approval_date, lc.target_development_date, lc.target_R1, lc.target_R2, lc.target_go_live, lc.target_R3]]
		table = Table(data, 6*[1.3*inch], 3*[0.2*inch])
		elements.append(table)
		elements.append(Spacer(2,15))

	elements.append(Spacer(2,10))
	#Risks
	risk = 'Risks'
	ptext = '<font size=16>%s</font>'%risk
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,45,0))
	elements.append(d)
	elements.append(Spacer(2,15))

	for risk in risk_results:
		ptext = '<font size=14>%s (ID: %s)</font>'%(risk.title, risk.risk_ID_number)
		elements.append(Paragraph(ptext, styles["Normal"]))
		elements.append(Spacer(2,5))

		d = Drawing(100,1)
		d.add(Line(0,0,90,0))
		elements.append(d)
		elements.append(Spacer(2,15))

		ptext = '<font size=12>Description: %s</font>'%risk.description
		elements.append(Paragraph(ptext, styles["Normal"]))
		elements.append(Spacer(2,15))

		risk_info = [['Probability', 'Impact', 'Risk Score', 'Target Resolution Date', 'Status'], ['----------------------','----------------------','----------------------','----------------------','----------------------'], [risk.probability, risk.impact, risk.score, risk.target_resolution_date, risk.status]]
		risk_table = Table(risk_info, 5*[1.5*inch], 3*[0.2*inch])
		elements.append(risk_table)
		elements.append(Spacer(2,20))

	#Recommendations
	recs = 'Recommendations'
	ptext = '<font size=16>%s</font>'%recs
	elements.append(Paragraph(ptext, styles["Normal"]))
	elements.append(Spacer(2,5))

	d = Drawing(100,1)
	d.add(Line(0,0,135,0))
	elements.append(d)
	elements.append(Spacer(2,15))
	for rec in rec_results:
		ptext = '<font size=12>Recommendation #: %s (Date of Recommendation: %s, Resolved?: %s)</font>'%(rec.recommendation_number, rec.recommendation_date, rec.resolved)
		elements.append(Paragraph(ptext, styles["Normal"]))
		elements.append(Spacer(2,15))

		ptext = '<font size=12> Recommendation: %s</font>' %rec.recommendation
		elements.append(Paragraph(ptext, styles["Normal"]))

		elements.append(Spacer(2,20))
		ptext = '<font size=12> Comments: %s</font>'%rec.comments
		elements.append(Paragraph(ptext, styles["Normal"]))
	doc.build(elements)
	pdf = buffer.getvalue()
	response.write(buffer.getvalue())
	buffer.close()

	myfile = ContentFile(pdf)
	m = PDF()
	m.user = request.user
	m.ivv_id = ivv_results.ivv_id
	m.save()
	m.file.save('test.pdf', myfile)


	return response

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../')
    else:
        form = SignUpForm()
    return render(request, 'webform/signup.html', {'form': form})

def login(request):
	def errorHandler(error):
		return render(request, 'webform/login.html', {'error': error})

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				fullName = user.get_full_name
				return redirect('../', {'user': user})
			else:
				error = 'Account disabled'
			return errorHandler(error)
		else:
			error = 'Invalid details entered.'
		return errorHandler(error)
	return render(request,'webform/login.html')

