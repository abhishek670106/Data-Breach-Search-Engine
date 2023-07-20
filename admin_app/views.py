from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import RedeemCode, UserProfile
from .forms import RedeemCodeForm, UserProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.models import User

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView


from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import RedeemCode

from django.shortcuts import render
from .forms import RedeemCodeForm
from .models import RedeemCode

from django.shortcuts import render, redirect
from .forms import RedeemCodeForm

from django.shortcuts import render
from .forms import RedeemCodeForm
from .utils import generate_unique_code

from django.shortcuts import render, redirect
from .forms import RedeemCodeForm

from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.decorators import login_required, user_passes_test



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login




from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    # Only staff members can access this view
    return HttpResponse("<h4> 403 Forbidden</h4 ")


def is_superuser(user):
    return user.is_superuser



def is_staff(user):
    return user.is_staff



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminapp:admin_home')
        else:
            # Invalid login credentials
            return render(request, 'admin_login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'admin_login.html')


@login_required(login_url='adminapp:admin_login')
def admin_home(request):
    return render(request, 'admin_home.html')


def is_superuser(user):
    return user.is_superuser



def generate_redeem_codes(request):
    if request.method == 'POST':
        form = RedeemCodeForm(request.POST)
        if form.is_valid():
            num_codes = form.cleaned_data.get('num_codes')
            if num_codes is not None and num_codes > 0:
                codes = generate_codes(num_codes)
                return render(request, 'generate_codes.html', {'form': form, 'codes': codes})
            else:
                form.add_error('num_codes', 'Number of codes must be a positive integer.')
    else:
        form = RedeemCodeForm()
    
    return render(request, 'generate_codes.html', {'form': form})


def generate_codes(num_codes):
    """
    Generate the specified number of unique codes.
    """
    codes = []
    for _ in range(num_codes):
        code = generate_unique_code()
        codes.append(code)
    return codes

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

user_list_view = UserListView.as_view()


class RedeemCodeListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = RedeemCode
    template_name = 'redeem_code_list.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


redeemcode_list_view=RedeemCodeListView.as_view()


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'user_edit.html'

class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('admin_app:user_list')

class RedeemCodeListView(ListView):
    model = RedeemCode
    template_name = 'redeem_code_list.html'

class RedeemCodeUpdateView(UpdateView):
    model = RedeemCode
    fields = ['code', 'code_type']
    template_name = 'redeem_code_edit.html'
    success_url = '/adminapp/redeem-codes/'  # Specify the URL to redirect to


class RedeemCodeDeleteView(DeleteView):
    model = RedeemCode
    template_name = 'redeem_code_delete.html'
    success_url = reverse_lazy('admin_app:redeem_code_list')


def RedeemCodeadd(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        value = request.POST.get('value')
        RedeemCode.objects.create(code=code, value=value)
        return redirect('/')
    return render(request, 'redeem_code_add.html')



def RedeemCodeadd(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        code_type = request.POST.get('code_type')
        RedeemCode.objects.create(code=code, code_type=code_type)
        return redirect('/adminapp/redeem-codes/')
    return render(request, 'redeem_code_add.html')