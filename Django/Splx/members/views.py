from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from members.forms import MemberForm, EmailForm
from members.models import Member

# Create your views here.

def member_form_view(request):
    """
    Creates a new Member from form page
    """
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
        #send mail to member
    form = MemberForm()
    context = {
        'form': form
    }
    return render(request, 'members/form.html', context=context)

def scan(request, data):
    """
    Receives data from QR scanners and sends back response
    """
    member = Member.objects.get(qr_token=data)
    response = {
        'state': 'Membre Actif',
        'email': member.email
    }
    # return HttpResponse(data)
    return JsonResponse(response, safe=False)

def member_retrieve(request):
    """
    Retrieves a member based on email and sends them a copy of existing QR
    """
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                member = Member.objects.get(email=email)
                #send mail and replace template by 'mail sent'
                return render(request, 'members/card.html', context={'member': member})
            except Member.DoesNotExist:
                return render(request, 'members/invalid_email.html')
    form = EmailForm()
    context = {
        'form': form
    }
    return render(request, 'members/retrieve.html', context=context)
