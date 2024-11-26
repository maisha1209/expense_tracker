
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.http import JsonResponse
from plaid import Configuration, ApiClient, Environment
from plaid.api.plaid_api import PlaidApi
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import datetime, timedelta
#from .models import UserProfile
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Transaction, Account
from django.shortcuts import render, get_object_or_404, redirect
from .models import Budget, Category, BudgetCategoryAmount, PlaidItem
from .forms import BudgetForm, CategoryForm, BudgetCategoryAmountForm
from plaid.model.accounts_get_request import AccountsGetRequest
from django.urls import reverse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import plaid
from plaid import ApiClient, Configuration
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from datetime import datetime, timedelta, date

import os
import json
from .settings import PLAID_CLIENT_ID, PLAID_ENV, PLAID_SECRET
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Sum, Q
import collections
from .utils import categorize_transactions
from plaid.api import plaid_api
from plaid.model.auth_get_request import AuthGetRequest
from plaid.exceptions import ApiException
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid import ApiClient, Configuration
from django.views.decorators.http import require_POST
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_response import TransactionsGetResponse
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.account_base import AccountBase
from datetime import datetime, timedelta
from .forms import SavingsGoalForm
from .models import SavingsGoal
from decimal import Decimal

import json
import certifi

configuration=Configuration(
    host="https://sandbox.plaid.com",  # Change to the appropriate environment if needed
    api_key={
        "clientId": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SECRET,
    }
)
api_client= plaid.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

logged_in = False


def create_savings_goal(request):
    if request.method == "POST":
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            savings_goal = form.save(commit=False)
            savings_goal.user = request.user
            savings_goal.save()
            return redirect('view_savings_goals')
    else:
        form = SavingsGoalForm()
    return render(request, 'expense_tracker/create_savings_goal.html', {'form': form})

"""def view_savings_goals(request):
    user = request.user
    savings_goals = SavingsGoal.objects.filter(user=user)
    return render(request, 'expense_tracker/view_savings_goals.html', {'savings_goals': savings_goals})"""

def view_savings_goals(request):
    user = request.user
    if user.is_authenticated:
        savings_goals = SavingsGoal.objects.filter(user=user)
        return render(request, 'expense_tracker/view_savings_goals.html', {'savings_goals': savings_goals})
    else:
        return redirect('log_in')


@login_required
def update_savings_goal(request, goal_id):
    user = request.user
    if user.is_authenticated and request.method == "POST":
        amount_saved = request.POST.get("amount_saved", 0)
        try:
            savings_goal = SavingsGoal.objects.get(id=goal_id, user=user)
            savings_goal.current_savings += Decimal(amount_saved)
            savings_goal.save()
            return redirect('view_savings_goals')
        except SavingsGoal.DoesNotExist:
            return redirect('view_savings_goals')
    return redirect('log_in')




def base(request):
    return render(request, 'expense_tracker/base.html',{
        'hide_header': False,  # Show the full header
        'hide_header_links': False,  # Show all links
        'is_homepage': True,  # Show the welcome message

    }) # Render a template named 'base.html'

def login_view(request):
    return render(request, 'expense_tracker/log_in.html', {'hide_header': False,  # Show the header but selectively hide links
        'hide_header_links': True,  # Hide the login and signup links
														   })



def signup_view(request):
    return render(request, 'expense_tracker/signup.html', {'hide_header': False,  # Show the header but selectively hide links
        'hide_header_links': True, 
														   })








def index(request):
	
	latest_budgets = username = latest_transactions = accounts = None
	user = request.user
	global logged_in

	if user.is_authenticated:
		latest_budgets = user.budget_set.order_by('-date'[:5])
		latest_transactions = user.transaction_set.order_by('-date')[:5]
		logged_in = user.is_authenticated
		accounts = user.account_set.order_by('name')
		username = user.username

	data = {
		'latest_budgets': latest_budgets,
		'latest_transactions': latest_transactions,
		'logged_in': logged_in,
		'accounts': accounts,
		'username': username
	}
	return render(request, 'expense_tracker/index.html', data)


def transactions(request):
	global logged_in

	username = all_transactions = None
	user = request.user

	if user.is_authenticated:
		all_transactions = user.transaction_set.order_by('-date')
		paginator = Paginator(all_transactions, 100)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		logged_in = user.is_authenticated
		username = user.username

		builtin_categories = Category.objects.filter(custom=False).order_by('description')

	data = {
		'all_transactions': all_transactions,
		'logged_in': logged_in,
		'username': username,
		'page_obj': page_obj,
		'builtin_categories': builtin_categories
	}
	return render(request, 'expense_tracker/transactions.html', data)

def budget(request, budget_id):
	user = request.user

	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)

		categories = Category.objects.order_by('description')
		bcas = None

		bca_set = budget.budgetcategoryamount_set
		if bca_set.exists():
			bcas = {bca.category.id: bca.amount for bca in bca_set.filter(budget=budget_id)}
		budgeted_amts = []

		for cat in categories:
			if bcas and cat.id in bcas:
				child_cat_ids = [ c.id for c in cat.category_set.all() ] 
				
				month = budget.date.month
				year = budget.date.year

				if len(child_cat_ids) > 1:
					# QuerySet of dictionaries
					trans_sum_by_cat = Transaction.objects.filter(date__month=month) \
						.filter(date__year=year) \
						.filter(Q(builtin_category_id=cat.id) | Q(builtin_category_id__in=child_cat_ids)) \
						.values('builtin_category') \
						.annotate(Sum('amount')) \
						.order_by('-amount__sum')
				else:
					trans_sum_by_cat = Transaction.objects.filter(date__month=month) \
						.filter(date__year=year) \
						.filter(builtin_category_id=cat.id) \
						.values('builtin_category') \
						.annotate(Sum('amount')) \
						.order_by('-amount__sum')
					
				cat_dict, cat_sum = {}, 0

				if trans_sum_by_cat.count() > 0:
					cat_sum = 0
					for cat_dict in trans_sum_by_cat:
						cat_sum += cat_dict['amount__sum']

				budgeted_amts.append({ 'category': cat.description, 'amt': bcas[cat.id], 'cat_sum': cat_sum, 'id': cat.id })

	context = {
		'budget': budget,
		'categories': categories,
		'budgeted_amts': budgeted_amts
	}

	return render(request, 'expense_tracker/budget.html', context)


def budget_new(request):
	# Default to last month's budgeted amounts for each category
	#
	user = request.user
	budgets = user.budget_set

	if user.is_authenticated:
		last_month_budget = budgets.latest('date') if budgets.exists() else None
		last_month_bcas = []

		if last_month_budget:
			bca_set = last_month_budget.budgetcategoryamount_set
			if bca_set.exists():
				last_month_bcas = bca_set.filter(budget_id = last_month_budget.id)

		if request.method == 'POST':
			request_copy = request.POST.copy()
			form = BudgetForm(request_copy)
			form.data['date'] = form.data['date'] + '-01'
			form.data['user'] = user

			if form.is_valid():
				new_budget = form.save()

				for bca in last_month_bcas:
					new_bca = BudgetCategoryAmount(
						category=bca.category,
						budget=new_budget,
						amount=bca.amount
					)
					new_bca.save()

				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

def budget_delete(request):
	id = request.POST["pk"]
	budget = get_object_or_404(Budget,pk=id)
	budget.delete()

	return HttpResponseRedirect(reverse('index'))


def category_new(request, budget_id):
	user = request.user

	if user.is_authenticated:
		form = CategoryForm(request.POST)

		budget = user.budget_set.get(id=budget_id)

		new_category = Category(description=request.POST['description'], user=user)
		new_category.save()
		new_budg_cat_amt = BudgetCategoryAmount(
			category=new_category,
			budget=budget,
			amount=0
			)
		new_budg_cat_amt.save()

		return HttpResponseRedirect(reverse('budget', args=[budget.id]))
	else:
		return HttpResponseRedirect(reverse('index'))

     
def bca_new(request, budget_id):
	user = request.user

	if user.is_authenticated:
		category_id = int(request.POST['category_id'])
		all_budgets = user.budget_set.all()
		if all_budgets.count() > 1:
			last_budget_id=all_budgets[all_budgets.count() - 2].id
			try:
				last_month_bca = get_object_or_404(BudgetCategoryAmount,budget=last_budget_id, category=category_id)
			except:
				last_month_bca = None

		budget = user.budget_set.get(id=budget_id)
		category = Category.objects.get(id=category_id)
		amount = last_month_bca.amount if last_month_bca else 0

		bca = BudgetCategoryAmount(budget=budget, category=category, amount=amount)
		bca.save()

		return HttpResponseRedirect(reverse('budget', args=[budget_id]))
	else:
		return HttpResponseRedirect(reverse('index'))


def bca_delete(request, budget_id, category_id):
	user = request.user
	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)
		category = user.category_set.get(id=category_id)
		bca = get_object_or_404(BudgetCategoryAmount,budget=budget, category=category)
		bca.delete()

		return HttpResponseRedirect(reverse('expense_tracker:budget', args=[budget.id]))
	else:
		return HttpResponseRedirect(reverse('expense_tracker:index'))


def category_edit(request, budget_id, category_id):
	user = request.user
	context = {}

	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)
		category = Category.objects.get(id=category_id)
		amount = BudgetCategoryAmount.objects.filter(budget=budget_id, category=category_id).first().amount

		context = {
			'budget': budget,
			'category': category,
			'amount': amount
		}
	return render(request, 'expense_tracker/category-edit.html', context)

def category_update(request, budget_id, category_id):
	user = request.user
	
	if user.is_authenticated:
		form = BudgetCategoryAmountForm(request.POST)
		amount = request.POST["amount"]
		description = request.POST["description"]
		category = Category.objects.get(id=category_id)
		category.description = description

		bca = BudgetCategoryAmount.objects.filter(budget=budget_id, category=category_id).first()
		bca.amount = amount
	
		if form.is_valid():
			bca.save(update_fields=['amount'])
			category.save(update_fields=['description'])

		return HttpResponseRedirect(reverse('expense_tracker:budget', args=[budget_id]))
	else:
		return HttpResponseRedirect(reverse('expense_tracker:index'))

      
#@csrf_protect
@ensure_csrf_cookie
def link_account(request):
	context = {}
	return render(request, 'expense_tracker/link-account.html', context)


#@ensure_csrf_cookie
@csrf_exempt
def create_link_token(request):
    user=request.user
    print(user.is_authenticated)
	
    if user.is_authenticated:
		
        # Define the request data for the link token
        request_data=LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=str(user.id)),
            client_name="expense_tracker",
            #products=["transactions"],
            #country_codes=["US"],
			products=[Products("transactions")], 
			country_codes=[CountryCode("US")],
            language="en"
        )
        try:
            # Call Plaid API to create the link token
            response=plaid_client.link_token_create(request_data)
            link_token=response.link_token # Access link token from response
            
            return JsonResponse({'link_token':link_token})
        except Exception as e:
            # Return an error message if something goes wrong
            return JsonResponse({"error": str(e)}, status=400)
    else:
        # Redirect to home if user is not authenticated
     return redirect('index')
	    
#@require_POST
@csrf_exempt
def get_access_token(request):
    user = request.user
    plaid_item = None  # Initialize plaid_item to None

    if user.is_authenticated and request.method == "POST":
        try:
            body_data = json.loads(request.body.decode())
            public_token = body_data["public_token"]
            accounts = body_data.get("accounts", [])  # Use .get() to avoid KeyErrors

            # Exchange the public token for an access token
            exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
            exchange_response = plaid_client.item_public_token_exchange(exchange_request)
            access_token = exchange_response.access_token
            item_id = exchange_response.item_id

            # Retrieve or create PlaidItem
            plaid_item, created = PlaidItem.objects.get_or_create(
                user=user, item_id=item_id,
                defaults={"access_token": access_token}
            )

            # Process each account in accounts
            for account in accounts:
                account_id = account.get("account_id")
                if not account_id:
                    continue  # Skip accounts without an account_id

                # Check if the account already exists, or create a new one
                existing_acct = Account.objects.filter(user=user, plaid_account_id=account_id).first()
                if existing_acct is None:
                    new_acct = Account(
                        plaid_account_id=account_id,
                        balances=account.get("balances", {}),
                        mask=account.get("mask", ""),
                        name=account.get("name", ""),
                        official_name=account.get("official_name", ""),
                        subtype=account.get("subtype", ""),
                        account_type=account.get("type", ""),
                        user=user
                    )
                    new_acct.save()

            return JsonResponse({"status": "success"})

        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Unauthorized or invalid request"}, status=403)



def get_auth(request):
    user = request.user

    if user.is_authenticated:
        try:
            # Retrieve the access token for the user's linked item
            plaid_item = user.plaiditem_set.first()
            access_token = plaid_item.access_token if plaid_item else None

            if not access_token:
                return JsonResponse({"error": "No access token available for this user."}, status=400)

            # Create an AuthGetRequest using the access token
            auth_request = AuthGetRequest(access_token=access_token)

            # Call Plaid's auth_get endpoint to retrieve authentication data
            auth_response = plaid_client.auth_get(auth_request)

            # Pretty-print the auth response in development
            print(json.dumps(auth_response.to_dict(), sort_keys=True, indent=4))

            return JsonResponse({'error': None, 'auth': auth_response.to_dict()})
        except ApiException as e:
            # Handle Plaid API exceptions
            error_json = json.loads(e.body) if hasattr(e, 'body') else str(e)
            return JsonResponse({'error': {'display_message': error_json.get('display_message', 'An error occurred'), 'error_code': error_json.get('error_code', ''), 'error_type': error_json.get('error_type', '')}}, status=400)
    else:
        return JsonResponse({"error": "User not authenticated."}, status=401)









def get_transactions(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    transactions = []
    plaid_items = user.plaiditem_set.all()

    # Define date range (up to 24 months for Plaid) as date objects
    timespan_weeks = 4 * 24
    start_date = (datetime.now() - timedelta(weeks=timespan_weeks)).date()  # Convert to date directly
    end_date = datetime.now().date()  # Convert to date directly

    for item in plaid_items:
        try:
            access_token = item.access_token

            # Define the transaction request
            transaction_request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,  # Already a date object
                end_date=end_date,      # Already a date object
                options=TransactionsGetRequestOptions(count=100)
            )

            # Call the Plaid API to fetch transactions
            response = plaid_client.transactions_get(transaction_request)
            transactions_data = response.to_dict()
            transactions.extend(transactions_data['transactions'])
            accounts = transactions_data['accounts']

            # Process each account
            for account in accounts:
                try:
                    existing_acct = user.account_set.get(plaid_account_id=account['account_id'])
                except Account.DoesNotExist:
                    # Create a new account if it doesn't exist
                    new_acct = Account(
                        plaid_account_id=account['account_id'],
                        balances=account['balances'],
                        mask=account['mask'],
                        name=account['name'],
                        official_name=account.get('official_name', ''),
                        subtype=account['subtype'],
                        account_type=account['type'],
                        user=user
                    )
                    new_acct.save()

            # Handle pagination if more than 500 transactions
            while len(transactions) < transactions_data['total_transactions']:
                transaction_request = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=start_date,
                    end_date=end_date,
                    options=TransactionsGetRequestOptions(offset=len(transactions))
                )
                response = plaid_client.transactions_get(transaction_request)
                transactions.extend(response.to_dict()['transactions'])

            # Process each transaction
            for transaction in transactions:
                try:
                    existing_trans = user.transaction_set.get(transaction_id=transaction['transaction_id'])
                except Transaction.DoesNotExist:
                    # Create a new transaction if it doesn't exist
                    new_trans = Transaction(
                        account=user.account_set.get(plaid_account_id=transaction['account_id']),
                        account_owner=transaction.get('account_owner', ''),
                        amount=transaction['amount'],
                        authorized_date=transaction.get('authorized_date', None),
                        category=transaction['category'],
                        category_id=transaction['category_id'],
                        date=transaction['date'],  # No need to convert; directly assign the date
                        iso_currency_code=transaction['iso_currency_code'],
                        location=transaction.get('location', {}),
                        merchant_name=transaction.get('merchant_name', ''),
                        name=transaction['name'],
                        payment_meta=transaction.get('payment_meta', {}),
                        payment_channel=transaction['payment_channel'],
                        pending=transaction['pending'],
                        pending_transaction_id=transaction.get('pending_transaction_id', ''),
                        transaction_code=transaction.get('transaction_code', ''),
                        transaction_id=transaction['transaction_id'],
                        transaction_type=transaction['transaction_type'],
                        unofficial_currency_code=transaction.get('unofficial_currency_code', ''),
                        user=user
                    )
                    new_trans.save()

        except Exception as e:
            print(e)
            # Optionally log the error or display a message
            return JsonResponse({"error": str(e)}, status=500)

    # Send transaction data as JSON response
    return JsonResponse({"transactions": [t for t in transactions]})





#Create your views here.
#def login_view(request):
 #  if request.method == "POST":
 #      username = request.POST.get("username")
 #      password = request.POST.get("password")
 #      user = authenticate(request, username=username, password=password)
 #      if user is not None:
  #          login(request, user)
  #          messages.success(request, "Logged in successfully!")
  #          return redirect("link")  # Redirect to link.html after successful login
  #     else:
 #           messages.error(request, "Invalid username or password")
  # return render(request, "login.html")


#def signup_view(request):
 #   if request.method == "POST":
  #      form = SignUpForm(request.POST)
  #      if form.is_valid():
 #          form.save()  # Save the new user

            # Redirect the user to the login page after successful signup
 #           messages.success(request, "Account created successfully! Please log in.")
  #          return redirect("login")
  #      else:
   #         messages.error(request, "Error in form submission. Please check your details.")
 #   else:
 #       form = SignUpForm()
  #  return render(request, "signup.html", {"form": form})

#@login_required
#def home_view(request):
 #   return render(request, 'dashboard.html')


def signup(request):
	
	return render(request, 'expense_tracker/signup.html',)


def create_user(request):
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username, email, password)

	
	user.save()
	print('User created successfully')
	return HttpResponseRedirect('/log_in_form')

def log_in_form(request):
	return render(request, 'expense_tracker/log_in.html',)


"""def log_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		print('invalid credentials')
	return HttpResponseRedirect('/', {'username': username})"""


def log_in(request):
    if request.method == "POST":
        # Process the form submission
        username = request.POST.get('username')  # Safely get 'username'
        password = request.POST.get('password')  # Safely get 'password'

        if username and password:  # Ensure both fields are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))  # Redirect on successful login
            else:
                # Handle invalid credentials
                return render(request, 'expense_tracker/log_in.html', {'error_message': 'Invalid credentials'})
        else:
            # Handle missing fields
            return render(request, 'expense_tracker/log_in.html', {'error_message': 'Please enter both username and password'})

    # Render the login page for GET requests
    return render(request, 'expense_tracker/log_in.html')


def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('log_in'))


"""def refresh_accounts(request):
    user = request.user
    items = user.plaiditem_set.all()

    for item in items:
        access_token = item.access_token
        try:
            # Create an AccountsGetRequest with the access token
            request_data = AccountsGetRequest(access_token=access_token)
            # Use the client to fetch accounts
            response = plaid_client.accounts_get(request_data)

            # Parse the response and update account information in the database
            accounts = response['accounts']
            for account in accounts:
                try:
                    # Attempt to retrieve an existing account
                    acc = Account.objects.get(plaid_account_id=account['account_id'])
                except Account.DoesNotExist:
                    # If account does not exist, create a new Account instance
                    acc = Account(plaid_account_id=account['account_id'], user=user)

                # Convert balances to a dictionary to make it JSON serializable
                acc.balances = {
                    'available': account['balances'].available,
                    'current': account['balances'].current,
                    'iso_currency_code': account['balances'].iso_currency_code,
                    'unofficial_currency_code': account['balances'].unofficial_currency_code,
                }
                acc.mask = account['mask']
                acc.name = account['name']
                acc.official_name = account['official_name']
                acc.subtype = account['subtype']
                acc.account_type = account['type']
                #acc.balances = account['balances']
                # Save the account with updated information
                acc.save()

        except Exception as e:
            print(f"Error refreshing accounts for item {item.item_id}: {e}")
			
    # Redirect to the index page after refreshing accounts
    return HttpResponseRedirect(reverse('index'))"""





@login_required  
def refresh_accounts(request):
    user = request.user
    items = user.plaiditem_set.all()

    for item in items:
        access_token = item.access_token
        try:
            request_data = AccountsGetRequest(access_token=access_token)
            response = plaid_client.accounts_get(request_data)

            accounts = response['accounts']
            for account in accounts:
                try:
                    acc = Account.objects.get(plaid_account_id=account['account_id'])
                except Account.DoesNotExist:
                    acc = Account(plaid_account_id=account['account_id'], user=user)

                acc.balances = {
                    'available': account['balances'].available,
                    'current': account['balances'].current,
                    'iso_currency_code': account['balances'].iso_currency_code,
                    'unofficial_currency_code': account['balances'].unofficial_currency_code,
                }
                acc.mask = account['mask']
                acc.name = account['name']
                acc.official_name = account['official_name']
                acc.subtype = str(account['subtype']) if account['subtype'] else None
                acc.account_type = str(account['type']) if account['type'] else None
                
                acc.save()

        except Exception as e:
            print(f"Error refreshing accounts for item {item.item_id}: {e}")

    # Redirect to the index page after refreshing accounts
    return HttpResponseRedirect(reverse('index'))





def trans_category_update(request):
	user = request.user
	
	if user.is_authenticated:
		body_data = json.loads(request.body.decode())
		trans_id = body_data["trans_id"]
		category_id = body_data["cat_id"]

		category = Category.objects.get(id=category_id)
		trans = Transaction.objects.filter(pk=trans_id).first()
		trans.builtin_category = category
	
		trans.save(update_fields=['builtin_category'])

		return HttpResponseRedirect(reverse('transactions'))
	else:
		return HttpResponseRedirect(reverse('index'))

	
# Private helper methods

def get_top10_popular_categories():
	past_duration = datetime.now() - timedelta(weeks=12)
	top_cats = Transaction.objects.filter(date__gt=past_duration).values('category').annotate(Sum('amount')).order_by('-amount__sum')
	return top_cats






