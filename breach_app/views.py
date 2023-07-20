from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from .models import UserProfile, RedeemCode



# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

def indexx(request):
    if request.method == 'POST':
        email = request.POST['email']
        results = []

        if request.user.is_authenticated:
            user_profile = get_or_create_user_profile(request.user)
            if not user_profile.is_premium and user_profile.search_count >= 3:
                messages.info(request, 'Free user limit exceeded. Upgrade to premium for unlimited requests.')
                return redirect('index')
            if not user_profile.is_premium:
                if user_profile.search_count < 3:
                    user_profile.search_count += 1
                    user_profile.save()

        url = "https://breachdirectory.p.rapidapi.com/"
        querystring = {"func": "auto", "term": email}
        headers = {
            "X-RapidAPI-Key": "245e3c9548msh3e717e9f123778ep1fb142jsn0f39f7811042",
            "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        print(user_profile.search_count)
        print(data)

        if "message" in data and data["message"] == "You have exceeded the MONTHLY quota for Requests on your current plan, BASIC. Upgrade your plan at https://rapidapi.com/rohan-patra/api/breachdirectory":
            messages.info(request, 'Contact the admin. Monthly quota has been exceeded.')
            return redirect('index')
        elif data.get('result') and len(data['result']) > 0:
            if request.user.is_authenticated and user_profile.is_premium:
                for result in data['result']:
                    line = result.get("line")
                    if line and ':' in line:
                        password = line.split(':')[1]
                        source = result["sources"][0]
                        result_string = {
                            "email": email,
                            "password": password,  # Non-masked full password for premium users
                            "source": source
                        }
                        results.append(result_string)
            else:
                for result in data['result']:
                    line = result.get("line")
                    if line and ':' in line:
                        password = line.split(':')[1]
                        source = result["sources"][0]
                        masked_password = mask_password(password)
                        result_string = {
                            "email": email,
                            "password": masked_password,
                            "source": source
                        }
                        results.append(result_string)

            # Store the email in a text file for successful requests
            with open('suc.html', 'a') as file:
                file.write(email + '\n')

            # Count the number of lines in the text file for available requests count
            with open('suc.html', 'r') as file:
                available_requests_count = int(10 - sum(1 for line in file))

            context = {
                'email': email,
                'results': results,
                'available_requests_count': available_requests_count
            }

            return render(request, 'index.html', context)
        else:
            messages.info(request, 'No data found for the given email address.')
            if request.user.is_authenticated and not user_profile.is_premium and user_profile.search_count < 3:
                user_profile.search_count += 1
                user_profile.save()
                if user_profile.search_count >= 3:
                    messages.info(request, 'Free user limit exceeded. Upgrade to premium for unlimited requests.')
            return redirect('index')
    else:
        # Count the number of lines in the text file for available requests count
        with open('successful_requests.txt', 'r') as file:
            available_requests_count = int(10 - sum(1 for line in file))

        context = {
            'available_requests_count': available_requests_count
        }
        return render(request, 'index.html', context)















def has_redeemed_code(user):
    return user.userprofile.redeemed_codes.exists()

def mask_password(password):
    # Masks the last 1/4 of the password
    masked_length = len(password) // 4
    return password[:-masked_length] + '*' * masked_length



def get_or_create_user_profile(user):
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    return user_profile

# Rest of the code...



def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']
        user = None

        # Check if the identifier is an email
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass
        else:  # Assume it's a username
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            if user.check_password(password):
                login(request, user)
                return redirect('index')

        messages.error(request, 'Invalid email/username or password.')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if the username is already taken
        existing_user = User.objects.filter(email=email).exists()
        if existing_user:
            messages.error(request, "Email is already taken.")
            return redirect('register')
        
        existing_user = User.objects.filter(username=username).exists()
        if existing_user:
            messages.error(request, "Username is already taken.")
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(email=email,username=username, password=password)
        user.save()

        # Create a user profile
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()

        # Log in the user automatically after registration
        authenticated_user = authenticate(request, username=username, password=password)
        login(request, authenticated_user)

        # Redirect the user to the desired page after successful registration
        return redirect('index')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render
from django.contrib import messages
from .models import UserProfile

def dashboard_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    search_count = user_profile.search_count
    premium_search_count = user_profile.premium_search_count
    is_premium = user_profile.is_premium
    search_limit = user_profile.search_limit

    # Calculate search left for free user
    if not is_premium:
        search_left = max(0, search_limit - search_count)
    else:
        search_left = premium_search_count

    # Decrease search count if user makes a search
    if request.method == 'POST':
        if search_left > 0:
            search_left -= 1
            if is_premium:
                premium_search_count -= 1
            else:
                search_count += 1
                if search_count >= search_limit:
                    is_premium = True  # Upgrade to premium if search limit reached
                    premium_search_count = 0
                    messages.success(request, "Congratulations! You have been upgraded to premium.")
        else:
            messages.error(request, "You have reached your search limit.")

    # Check if user redeemed a code
    redeem_code = request.POST.get('redeem_code')
    if redeem_code:
        # Process redeem code and update search limit accordingly
        if redeem_code == "SOME_REDEEM_CODE":
            search_limit = 3  # Update search limit to 3 after redeeming the code
            premium_search_count = 3  # Set premium search count to 3 after redeeming the code
            is_premium = True  # Upgrade to premium after redeeming the code
            messages.success(request, "Code redeemed successfully. Your search limit has been reset.")

    # Update the user profile with the new search count, search limit, and membership status
    user_profile.search_count = search_count
    user_profile.premium_search_count = premium_search_count
    user_profile.is_premium = is_premium
    user_profile.search_limit = search_limit
    user_profile.save()

    context = {
        'search_left': search_left,
        'premium_search_count': premium_search_count,
        'is_premium': is_premium,
    }

    return render(request, 'dashboard.html', context)









def redeem_code(request):
    if request.method == 'POST':
        redeem_code = request.POST['redeem_code']
        try:
            code = RedeemCode.objects.get(code=redeem_code, is_redeemed=False)
            user_profile = UserProfile.objects.get(user=request.user)
            if code.code_type == '5':
                user_profile.search_limit += 5
                user_profile.is_premium = True  # Consider the user as premium after redeeming any code
            elif code.code_type == '10':
                user_profile.search_limit += 10
                user_profile.is_premium = True
            elif code.code_type == '15':
                user_profile.search_limit += 15
                user_profile.is_premium = True

            code.is_redeemed = True
            code.save()
            user_profile.save()

            messages.success(request, 'Code redeemed successfully.')
        except RedeemCode.DoesNotExist:
            messages.error(request, 'Invalid redeem code or code already redeemed.')

    return redirect('dashboard')



def aboutus(request):

    return render(request, 'aboutus.html')
