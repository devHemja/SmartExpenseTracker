from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required # Add this
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required # This forces users to log in first
def dashboard(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user # This links the expense to the logged-in person
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    # .filter(user=request.user) ensures privacy
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses, 
        'total_spent': total_spent,
        'form': form 
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log them in after signup
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/signup.html', {'form': form})