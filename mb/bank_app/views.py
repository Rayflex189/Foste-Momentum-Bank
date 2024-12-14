from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout

from .decorators import *
from .models import *
from .utilis import *
from .forms import *

# Create your views here.

def verify(request):
    return render(request, 'bank_app/verify.html')

def home(request):
    return render(request, 'bank_app/landing.html')

def about(request):
    return render(request, 'bank_app/about.html')

def contact(request):
    return render(request, 'bank_app/contact.html')

def services(request):
    return render(request, 'bank_app/services.html')

def blog(request):
    return render(request, 'bank_app/blog.html')

def client(request):
    return render(request, 'bank_app/client.html')

@login_required(login_url='LoginPage')
def dashboard(request):
    user_profile = request.user.userprofile  # Retrieve user profile associated with the current user

    if not user_profile.is_linked:
        show_alert = request.session.get('show_alert', True)
        if show_alert:
            last_refresh_str = request.session.get('last_refresh', None)
            if last_refresh_str:
                last_refresh = timezone.datetime.fromisoformat(last_refresh_str)
            else:
                last_refresh = None

            if last_refresh is None or (timezone.now() - last_refresh) > timedelta(minutes=5):
                request.session['last_refresh'] = timezone.now().isoformat()
                request.session['show_alert'] = True
                alert_message = "Link account with the payment system for secure transfer"
            else:
                alert_message = None
        else:
            alert_message = None
    else:
        alert_message = None
        request.session['show_alert'] = False

    if request.method == 'POST':
        form = DepositForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            try:
                if not user_profile.is_linked:
                    form.add_error(None, "Please link your account before making a deposit.")
                else:
                    form.save()
                    return redirect('imf')
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = DepositForm(user_profile=user_profile)

    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10] # Fetch recent transactions
    context = {
        'user_profile': user_profile,
        'alert_message': alert_message,
        'form': form,
        'transactions': transactions,
    }
    return render(request, 'bank_app/dashboard.html', context)





@unauthenticated_user
def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('LoginPage')

    context = {'form': form}
    return render(request, 'bank_app/register.html', context)

@login_required(login_url='LoginPage')
def Upgrade_Account(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    # Check if the account is upgraded
    if user_profile.is_upgraded:
        message = 'Account upgraded successfully'
    else:
        message = 'Account upgrade processing contact support for more information'

    context = {
        'user_profile': user_profile,
        'message': message,
    }
    return render(request, 'bank_app/account_upgrade.html', context)


@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('reset_setting')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'bank_app/login.html')

@login_required(login_url='LoginPage')
def profile_setting(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/profile_settings.html', context)

@login_required(login_url='LoginPage')
def aml(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    # Check if the user is authenticated and try to get the user's profile
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Handle the case where the UserProfile does not exist
            userprofile = None

    if request.method == 'POST':
        form = AMLForm(request.POST)
        if form.is_valid():
            aml_code_input = form.cleaned_data['aml']
            # Validate the OTP here (e.g., check if it matches the expected value)
            if validate_aml(aml_code_input, user_profile):  # Define this function based on your validation logic
                # Redirect to success page or dashboard
                return redirect('tac')
            else:
                form.add_error(None, 'Invalid AML code')
    else:
        form = AMLForm()

    context = {
        'userprofile': userprofile,
        'form': form
    }
    return render(request, 'bank_app/aml.html', context)

@login_required(login_url='LoginPage')
def imf(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    # Check if the user is authenticated and try to get the user's profile
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Handle the case where the UserProfile does not exist
            userprofile = None

    if request.method == 'POST':
        form = IMFForm(request.POST)
        if form.is_valid():
            imf_code_input = form.cleaned_data['imf']
            # Validate the OTP here (e.g., check if it matches the expected value)
            if validate_imf(imf_code_input, user_profile):  # Define this function based on your validation logic
                # Redirect to success page or dashboard
                return redirect('aml')
            else:
                form.add_error(None, 'Invalid IMF code')
    else:
        form = IMFForm()

    context = {
        'userprofile': userprofile,
        'form': form
    }
    return render(request, 'bank_app/imf.html', context)

@login_required(login_url='LoginPage')
def tac(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)

    # Check if the user is authenticated and try to get the user's profile
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Handle the case where the UserProfile does not exist
            userprofile = None

    if request.method == 'POST':
        form = TACForm(request.POST)
        if form.is_valid():
            tac_code_input = form.cleaned_data['tac']
            # Validate the OTP here (e.g., check if it matches the expected value)
            if validate_tac(tac_code_input, user_profile):  # Define this function based on your validation logic
                # Redirect to success page or dashboard
                return redirect('pending')
            else:
                form.add_error(None, 'Invalid TAC code')
    else:
        form = TACForm()

    context = {
        'userprofile': userprofile,
        'form': form
    }
    return render(request, 'bank_app/tac.html', context)

@login_required(login_url='LoginPage')
def kyc(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/kyc.html', context)

@login_required(login_url='LoginPage')
def statistics(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/statistics.html', context)

@login_required(login_url='LoginPage')
def alert(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/alert.html', context)

@login_required(login_url='LoginPage')
def transaction_details(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10]
    context = {'user_profile':user_profile, 'transactions':transactions}
    return render(request, 'bank_app/transaction_details.html', context)

@login_required(login_url='LoginPage')
def pending(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/pending.html')

@login_required(login_url='LoginPage')
def loans(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        # You can create a new UserProfile or redirect to a different page
        user_profile = UserProfile.objects.create(user=request.user)
    balance = user_profile.balance
    context = {'user_profile':user_profile}
    return render(request, 'bank_app/loans.html', context)

@login_required(login_url='LoginPage')
@transaction.atomic
def reset_setting(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
            form = UserProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')  # Redirect to the same page after successful update
            else:
                form = UserProfileForm(instance=request.user.userprofile)

    context = {
                'form': form
            }
    return render(request, 'bank_app/reset_setting.html', context)

@login_required(login_url='LoginPage')
@transaction.atomic
def linking_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    if request.method == 'POST':
        form = LinkingCodeForm(request.POST)
        if form.is_valid():
            # Check if the linking code matches
            entered_code = form.cleaned_data['linking_code']
            if entered_code == profile.linking_code:
                messages.success(request, 'Account successfully linked.')
                # Handle linking logic here, e.g., set a flag in UserProfile
                profile.is_linked = True
                profile.save()
                return redirect('dashboard')  # Redirect to dashboard or another view
            else:
                messages.error(request, 'Invalid linking code. Please try again.')
        else:
            messages.error(request, 'Form validation failed. Please check the input.')

    else:
        form = LinkingCodeForm()

    context = {
        'form': form,
        'user_profile': profile
    }
    return render(request, 'bank_app/linking_page.html', context)


@login_required(login_url='LoginPage')
def LogOut(request):
    logout(request)
    return redirect('LoginPage')