from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import now
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
import datetime
import braintree

# from community.extras import transact, generate_client_token, find_transaction
from community.extras import generate_order_id
from django.conf import settings
from .forms import *
from .models import *

def primaryhome(request):
    if request.user.username:
        return redirect('userprofile')
    else:
       return redirect('home')

def home(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'community/home.html', {'userprofile': UserProfile, 'user':user})
    else:
        subject = request.POST['Subject']
        message = request.POST['Message']
        email_from = request.POST['Email']
        recipient_list = [settings.EMAIL_HOST_USER,]
        send_mail( subject, message, email_from, recipient_list )
 
        user = request.user
        tymessage = True
        return render(request, 'community/home.html', {'tymessage':tymessage,'userprofile': UserProfile, 'user':user})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'community/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('userprofile')
            except IntegrityError:
                return render(request, 'community/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'community/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'community/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'community/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('userprofile')

def fullcommunity(request): 
    if 'search' in request.GET:
        search_term = request.GET['search']
        accounts  = UserProfile.objects.filter(name__icontains=search_term).order_by('-authentic', '?').exclude(image__exact='')[0:100]
        trades = Trade.objects.all()
        active_users = User.objects.filter(last_login__gt=datetime.datetime.now() - datetime.timedelta(days=60))
        return render(request, 'community/fullCommunity.html', {'active_users':active_users, 'accounts':accounts, 'trades':trades})
    if not 'search' in request.GET:
        account_list = UserProfile.objects.all().order_by('-authentic','?').exclude(image__exact='')
        paginator = Paginator(account_list, 50)
        page_number = request.GET.get('page')
        accounts = paginator.get_page(page_number)
        active_users = User.objects.filter(last_login__gt=datetime.datetime.now() - datetime.timedelta(days=60))
        trades = Trade.objects.all()
        return render(request, 'community/fullCommunity.html', {'active_users':active_users, 'accounts':accounts, 'trades':trades})

def feed(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
        if search_term.isdigit():
            trades = Trade.objects.filter(openedpositionon__icontains=search_term, openedpositionon__gt=datetime.datetime.today()-datetime.timedelta(days=364))[0:100]
            accounts = UserProfile.objects.all()
            return render(request, 'community/feed.html', {'accounts':accounts, 'trades':trades})
        else:
            trades = Trade.objects.filter(pair__icontains=search_term).order_by('-openedpositionon')[0:100]
            accounts = UserProfile.objects.all()
            return render(request, 'community/feed.html', {'accounts':accounts, 'trades':trades})  

    if not 'search' in request.GET:
        trade_list = Trade.objects.all().order_by('-openedpositionon')
        paginator = Paginator(trade_list, 50) 
        page_number = request.GET.get('page')
        trades = paginator.get_page(page_number)
        accounts = UserProfile.objects.all()
        return render(request, 'community/feed.html', {'accounts':accounts, 'trades':trades})

def viewuser(request, user_pk):
    userprofile = get_object_or_404(UserProfile, pk=user_pk)
    trades = Trade.objects.filter(user=userprofile.user).order_by('-openedpositionon')[0:50]
    return render(request, 'community/viewuser.html', {'trades':trades,'userprofile':userprofile})

def viewusertrade(request, trade_pk, user_pk):
    if user_pk == request.user.id:
        return redirect('viewyourtrade', trade_pk)
    else:
        trade = get_object_or_404(Trade, pk=trade_pk)
        userprofile = get_object_or_404(UserProfile, pk=user_pk)
        trades = Trade.objects.filter(user=trade.user)
        if request.method == 'GET':
            return render(request, 'community/viewusertrade.html', {'trades':trades, 'trade':trade, 'userprofile':userprofile})

def education(request):
    return render(request, 'community/education.html')

@login_required
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')

@login_required
def userprofile(request):
    trades = Trade.objects.filter(user=request.user).order_by('-openedpositionon')[0:50]
    userprofile = UserProfile.objects.filter(user=request.user)
    return render(request, 'community/userprofile.html', {'trades':trades, 'userprofile':userprofile})

@login_required
def posttrade(request):
    if request.method == 'GET':
        return render(request, 'community/posttrade.html', {'form':TradeForm()})
    else:
        try:
            form = TradeForm(request.POST, request.FILES)
            newtrade = form.save(commit=False)
            newtrade.user = request.user
            newtrade.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'community/posttrade.html', {'form':TradeForm(), 'error':'Error. Some fields were filled in incorrectly. Try again'})
 
@login_required
def viewyourtrade(request, trade_pk):
    trade = get_object_or_404(Trade, pk=trade_pk, user=request.user)
    userprofile = UserProfile.objects.filter(user=request.user)
    if request.method == 'GET':
        form = TradeForm(instance=trade)
        return render(request, 'community/viewyourtrade.html', {'trade':trade, 'form':form, 'userprofile':userprofile})
    else:
        try:
            form = TradeForm(request.POST, request.FILES, instance=trade)
            newtrade = form.save(commit=False)
            newtrade.user = request.user
            newtrade.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'community/viewyourtrade.html', {'trade':trade, 'form':form, 'userprofile':userprofile, 'error':'Error. Some fields were filled in incorrectly. Try again'})

@login_required
def edituserprofile(request):
    if request.method == 'GET':
        userprofile = UserProfile.objects.filter(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.userprofile)
        return render(request, 'community/edituserprofile.html', {'p_form':p_form, 'u_form':u_form, 'userprofile':userprofile})
    else:
        try:
            p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            u_form = UserUpdateForm(data=request.POST, instance=request.user)
            updateuser = u_form.save(commit=False)
            updateuser.user = request.user
            updateuser.save()
            newuserinfo = p_form.save(commit=False)
            newuserinfo.user = request.user
            newuserinfo.save()
            return redirect('userprofile')
        except ValueError:
            return render(request, 'community/edituserprofile.html', {'p_form':p_form, 'u_form':u_form, 'error':'Error. Some fields were filled in incorrectly. Try again'})

@login_required
def change_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        return render(request, 'community/changepassword.html', {'form':form})
    else:
        try:
            if request.POST['new_password1'] == request.POST['new_password2']:
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    return redirect('userprofile')
                else:
                    form = PasswordChangeForm(user=request.user)
                    return render(request, 'community/changepassword.html', {'form':form, 'error':'Incorrect Password'})
            else:
                form = PasswordChangeForm(user=request.user)
                return render(request, 'community/changepassword.html', {'form':form, 'error':'Passwords did not match'})
        except ValueError:
            return render(request, 'community/changepassword.html', {'form':form, 'error':'Bad data passed in. Try again.'})

@login_required
def alltradeshtml(request):
    return render(request, 'community/deletealltrades.html')

@login_required
def accounthtml(request):
    return render(request, 'community/deleteaccount.html')

@login_required
def deletetrade(request, trade_pk):
    trade = get_object_or_404(Trade, pk=trade_pk)
    trade.delete()
    return redirect('userprofile')

@login_required
def deletealltrades(request, user_pk):
    theuser = get_object_or_404(User, pk=user_pk)
    trades = Trade.objects.filter(user=theuser)
    trades.delete()
    return redirect('userprofile')

@login_required
def deleteaccount(request, user_pk):
    theuser = get_object_or_404(User, pk=user_pk)
    trades = Trade.objects.filter(user=theuser)
    trades.delete()
    theuser.delete()
    return redirect('userprofile')

# TRANSACTION_SUCCESS_STATUSES = [
#     braintree.Transaction.Status.Authorized,
#     braintree.Transaction.Status.Authorizing,
#     braintree.Transaction.Status.Settled,
#     braintree.Transaction.Status.SettlementConfirmed,
#     braintree.Transaction.Status.SettlementPending,
#     braintree.Transaction.Status.Settling,
#     braintree.Transaction.Status.SubmittedForSettlement
# ]

# def new_checkout(request):
#     client_token = generate_client_token()
#     return render(request, 'community/payments/new.html', {'client_token':client_token})

# def show_checkout(request, transaction_id):
#     transaction = find_transaction(transaction_id)
#     result = {}
#     if transaction.status in TRANSACTION_SUCCESS_STATUSES:
#         result = {
#             'header': 'Success!',
#             'message': 'Your transaction has been successfully processed.'
#         }
#         if request.user.email:
#             subject = 'Thank you for supporting this site'
#             message = 'Without you there would be no Forex_Flow_'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [request.user.email,]
#             send_mail( subject, message, email_from, recipient_list )
#         else:
#             pass
            
#     else:
#         result = {
#             'header': 'Transaction Failed',
#             'icon': 'fail',
#             'message': 'Your transaction has a status of ' + transaction.status + '. Please try again.'
#         }

#     return render(request, 'community/payments/show.html', {'transaction':transaction, 'result':result})

# def create_checkout(request):
#     result = transact({
#         'amount': request.POST['amount'],
#         'payment_method_nonce': request.POST['payment_method_nonce'],
#         'options': {
#             "submit_for_settlement": True
#         }
#     })
#     if result.is_success or result.transaction:
#         return redirect('show_checkout',transaction_id=result.transaction.id)
#     else:
#         for x in result.errors.deep_errors: 
#             messages.info(request, x)
#         return redirect('new_checkout')


 
def process_payment(request):
    order = generate_order_id()
    host = settings.HOSTNAME
    if settings.DEBUG:
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'item_name': 'Donation',
            'invoice': order,
            'currency_code': 'USD',
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),  #PayPal redirects the user after they make the payment.
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),  #PayPal redirects the user if they cancel the payment.
        }
    else:
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'item_name': 'Donation',
            'invoice': order,
            'currency_code': 'USD',
            'return_url': 'https://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'https://{}{}'.format(host, reverse('payment_cancelled')),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'community/payments/process_payment.html', {'order': order, 'form': form})

def payment_done(request):
    return render(request, 'community/payments/payment_done.html')

def payment_canceled(request):
    return render(request, 'community/payments/payment_cancelled.html')