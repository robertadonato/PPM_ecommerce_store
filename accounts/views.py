from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm 
from shop.models import Order 
from .forms import CustomLoginForm 

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('shop:product-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    next_page = 'shop:product_list'

class CustomLogoutView(LogoutView):
    next_page = 'account:login'

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('account:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_update.html', {'form': form})

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('date_created')
    return render(request, 'accounts/orders.html', {'orders': orders})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('account:profile')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout effettuato con successo.')
        return redirect('account:login')
    else:
        return redirect('account:profile')
