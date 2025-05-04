from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def tracker_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user 
            transaction.save()
            return redirect('tracker')  
    else:
        form = TransactionForm()

  
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    profit_loss = total_income - total_expense

    return render(request, 'tracker.html', {
        'form': form,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'profit_loss': profit_loss,
    })
