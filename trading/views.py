from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Stock, Portfolio, Transaction, UserProfile, Watchlist, PriceAlert
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import yfinance as yf
from django.core.cache import cache
from datetime import date
from nsepy import get_history
import json
from django.urls import reverse
from django.views.decorators.http import require_http_methods
# --- Custom Decorators ---
def superuser_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a superuser.
    """
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# --- Superuser Views ---
@superuser_required
def add_stock(request):
    """
    Allows superusers to add new stocks to the market.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        symbol = request.POST.get('symbol', '').upper()
        price = request.POST.get('price')

        if not all([name, symbol, price]):
            messages.error(request, "All fields are required.")
            return render(request, 'add_stock.html')
        
        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Please enter a valid positive price.")
            return render(request, 'add_stock.html')

        if Stock.objects.filter(symbol=symbol).exists():
            messages.error(request, f"Stock with symbol '{symbol}' already exists.")
        else:
            Stock.objects.create(name=name, symbol=symbol, current_price=price_float)
            messages.success(request, f"Stock '{name}' added successfully!")
            return redirect('dashboard')
            
    return render(request, 'add_stock.html')

# --- Public Views ---
def home_view(request):
    """
    Renders the homepage.
    """
    return render(request, 'home.html')

# --- Authentication Views ---
def register_view(request):
    """
    Handles user registration.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to your dashboard.")
            return redirect('dashboard')
        else:
            # Re-render form with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    """
    Logs the user out.
    """
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('login')

# --- Core Application Views ---
@login_required
def dashboard_view(request):
    """
    Displays all available stocks for trading.
    """
    stocks = Stock.objects.all()
    return render(request, 'dashboard.html', {'stocks': stocks})

@login_required
def portfolio_view(request):
    """
    Displays the logged-in user's stock portfolio with calculated values.
    """
    portfolio_items = Portfolio.objects.filter(user=request.user, quantity__gt=0).select_related('stock')
    
    total_invested = 0
    total_current_value = 0

    for item in portfolio_items:
        item.invested_value = item.quantity * item.avg_price
        item.current_value = item.quantity * item.stock.current_price
        item.profit_loss = item.current_value - item.invested_value
        item.profit_loss_percent = (item.profit_loss / item.invested_value) * 100 if item.invested_value > 0 else 0
        
        total_invested += item.invested_value
        total_current_value += item.current_value

    total_profit_loss = total_current_value - total_invested
    total_profit_loss_percent = (total_profit_loss / total_invested) * 100 if total_invested > 0 else 0

    context = {
        'portfolio': portfolio_items,
        'total_invested': total_invested,
        'total_current_value': total_current_value,
        'total_profit_loss': total_profit_loss,
        'total_profit_loss_percent': total_profit_loss_percent
    }
    return render(request, 'portfolio.html', context)

@login_required
def buy_stock_view(request, stock_id):
    """
    Handles the logic for a user buying a stock with wallet integration.
    """
    stock = get_object_or_404(Stock, id=stock_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            qty = int(request.POST['quantity'])
            if qty <= 0:
                raise ValueError
        except (KeyError, ValueError):
            messages.error(request, "Please enter a valid quantity.")
            return render(request, 'buy.html', {'stock': stock, 'wallet_balance': user_profile.wallet_balance})

        price = stock.current_price
        total_cost = price * qty
        user = request.user

        # Check if user has sufficient balance
        if user_profile.wallet_balance < total_cost:
            messages.error(request, f"Insufficient balance! You need ₹{total_cost:.2f} but have ₹{user_profile.wallet_balance:.2f}")
            return render(request, 'buy.html', {'stock': stock, 'wallet_balance': user_profile.wallet_balance})

        # Deduct from wallet
        user_profile.wallet_balance -= total_cost
        user_profile.total_invested += total_cost
        user_profile.save()

        # Create a transaction record
        Transaction.objects.create(user=user, stock=stock, quantity=qty, price=price, type="BUY")

        # Update or create the portfolio entry
        portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)
        
        if created:
            portfolio.quantity = qty
            portfolio.avg_price = price
        else:
            new_total_cost = (portfolio.avg_price * portfolio.quantity) + (price * qty)
            new_total_quantity = portfolio.quantity + qty
            portfolio.avg_price = new_total_cost / new_total_quantity
            portfolio.quantity = new_total_quantity
        
        portfolio.save()

        messages.success(request, f"Successfully purchased {qty} shares of {stock.symbol} for ₹{total_cost:.2f}")
        return redirect('portfolio')

    return render(request, 'buy.html', {'stock': stock, 'wallet_balance': user_profile.wallet_balance})

@login_required
def sell_stock_view(request, portfolio_id):
    """
    Handles the logic for a user selling a stock from their portfolio with wallet integration.
    """
    portfolio_item = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            qty = int(request.POST['quantity'])
            if qty <= 0:
                raise ValueError("Quantity must be positive")
            if qty > portfolio_item.quantity:
                raise ValueError("Cannot sell more than you own")
        except (KeyError, ValueError) as e:
            messages.error(request, f"Invalid quantity: {str(e)}")
            return render(request, 'sell.html', {'portfolio_item': portfolio_item})

        price = portfolio_item.stock.current_price
        total_sale = price * qty
        user = request.user

        # Add money to wallet
        user_profile.wallet_balance += total_sale
        user_profile.save()

        # Create a transaction record
        Transaction.objects.create(
            user=user, 
            stock=portfolio_item.stock, 
            quantity=qty, 
            price=price, 
            type="SELL"
        )

        # Update portfolio
        portfolio_item.quantity -= qty
        
        if portfolio_item.quantity == 0:
            portfolio_item.delete()
        else:
            portfolio_item.save()

        messages.success(request, f"Successfully sold {qty} shares of {portfolio_item.stock.symbol} for ₹{total_sale:.2f}")
        return redirect('portfolio')

    return render(request, 'sell.html', {'portfolio_item': portfolio_item})

@login_required
def transactions_view(request):
    """
    Displays the transaction history for the logged-in user.
    """
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp').select_related('stock')
    
    # Calculate total for each transaction
    for transaction in transactions:
        transaction.total = transaction.quantity * transaction.price
    
    context = {
        'transactions': transactions
    }
    return render(request, 'transactions.html', context)

def live_prices(request):
    return render(request, 'live_prices.html')


@login_required
def live_prices_api(request):
    """
    API endpoint to fetch latest stock prices using yfinance.
    This is called by the JavaScript on the live_prices page.
    """
    stocks = Stock.objects.all()
    if not stocks:
        return JsonResponse({'error': 'No stocks in the database'}, status=404)

    ticker_symbols = [stock.symbol for stock in stocks]
    
    try:
        latest_prices = {}
        for ticker in ticker_symbols:
            # Fetch the most recent intraday data for each ticker
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period="1d", interval="1m")
            
            if not hist.empty:
                latest_price = hist['Close'].iloc[-1]
                latest_prices[ticker] = round(latest_price, 2)

                # Update the price in the database
                stock_to_update = Stock.objects.filter(symbol=ticker).first()
                if stock_to_update:
                    stock_to_update.current_price = latest_price
                    stock_to_update.save()

        if not latest_prices:
             return JsonResponse({'error': 'Could not fetch data for any of the provided symbols.'}, status=400)

        return JsonResponse(latest_prices)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
TOP_NSE_STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 
    'SBIN.NS', 'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 'LICI.NS',
    'BAJFINANCE.NS', 'HCLTECH.NS', 'KOTAKBANK.NS', 'ASIANPAINT.NS', 'AXISBANK.NS'
]

@login_required
def market_explorer_view(request):
    """
    Renders the market explorer page and provides the necessary
    data to the template to correctly build the 'Buy' links.
    """
    # Create a map of {symbol: id} for stocks that are tradable in our app
    tradable_stocks = Stock.objects.all()
    stock_map = {stock.symbol: stock.id for stock in tradable_stocks}

    # Create a template URL for the buy link, with '0' as a placeholder for the ID
    buy_url_template = reverse('buy_stock', args=[0]) 

    context = {
        'stock_map_json': json.dumps(stock_map),
        'buy_url_template': buy_url_template
    }
    return render(request, 'market_explorer.html', context)


@login_required
def market_explorer_api(request):
    """
    API endpoint that fetches live prices for a pre-defined list of top NSE stocks using yfinance.
    This approach is faster and more reliable than discovering symbols dynamically.
    """
    try:
        # Fetch live data for the curated list of symbols in a single batch request
        tickers_data = yf.download(
            tickers=TOP_NSE_STOCKS, 
            period='1d', 
            interval='1m', 
            progress=False # Hides the download progress bar in the console
        )
        
        if tickers_data.empty:
            return JsonResponse({'error': 'Could not fetch live market data from yfinance.'}, status=500)

        live_prices = {}
        # The result from yf.download with multiple tickers has a multi-level column index
        close_prices = tickers_data['Close']

        for symbol in TOP_NSE_STOCKS:
            # Check if the symbol column exists and has non-empty, valid price data
            if symbol in close_prices and not close_prices[symbol].dropna().empty:
                # Get the last valid price from the series
                latest_price = close_prices[symbol].dropna().iloc[-1]
                live_prices[symbol] = round(latest_price, 2)
        
        if not live_prices:
            return JsonResponse({'error': 'Data was returned, but no valid prices were found.'}, status=500)

        return JsonResponse({'prices': live_prices})

    except Exception as e:
        # Generic error handler for any other issues during the process
        return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

# --- Real-time Stock Updates API ---
@login_required
def stock_updates_api(request):
    """API endpoint for real-time stock updates"""
    try:
        # Get all stocks
        stocks = Stock.objects.all()
        if stocks:
            # Update a random stock
            import random
            stock = random.choice(stocks)
            # Simulate price change (±0.5% for more realistic movement)
            price_change = stock.current_price * (random.uniform(-0.005, 0.005))
            new_price = max(0.01, stock.current_price + price_change)
            
            # Update in database
            stock.current_price = new_price
            stock.save()
            
            # Return updated stock
            return JsonResponse({
                'stock': {
                    'id': stock.id,
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.current_price,
                    'purchase_price': stock.purchase_price or stock.current_price
                }
            })
        else:
            return JsonResponse({'error': 'No stocks available'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def add_custom_stock(request):
    """
    Allows regular users to add custom stock symbols to trade.
    """
    if request.method == 'POST':
        symbol = request.POST.get('symbol', '').upper()
        name = request.POST.get('name')
        
        if not all([symbol, name]):
            messages.error(request, "Both symbol and name are required.")
            return render(request, 'add_custom_stock.html')
        
        # Check if stock already exists
        if Stock.objects.filter(symbol=symbol).exists():
            messages.error(request, f"Stock with symbol '{symbol}' already exists.")
            return render(request, 'add_custom_stock.html')
            
        try:
            # Try to get initial price data from yfinance
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            
            if hist.empty:
                messages.error(request, f"Could not find price data for symbol '{symbol}'. Please check the symbol and try again.")
                return render(request, 'add_custom_stock.html')
                
            current_price = float(hist['Close'].iloc[-1])
            
            # Create the stock
            Stock.objects.create(name=name, symbol=symbol, current_price=current_price)
            messages.success(request, f"Stock '{name}' ({symbol}) added successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error adding stock: {str(e)}")
            
    return render(request, 'add_custom_stock.html')

# --- User Profile & Wallet Views ---
@login_required
def profile_view(request):
    """User profile page with wallet information"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Calculate portfolio stats
    portfolio_items = Portfolio.objects.filter(user=request.user, quantity__gt=0).select_related('stock')
    total_current_value = sum(item.quantity * item.stock.current_price for item in portfolio_items)
    
    context = {
        'profile': user_profile,
        'total_portfolio_value': total_current_value,
        'total_assets': user_profile.wallet_balance + total_current_value
    }
    return render(request, 'profile.html', context)

@login_required
def wallet_view(request):
    """Wallet management page"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    context = {
        'profile': user_profile,
        'recent_transactions': transactions
    }
    return render(request, 'wallet.html', context)

# --- Watchlist Views ---
@login_required
def watchlist_view(request):
    """Display user's watchlist"""
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('stock')
    
    context = {
        'watchlist': watchlist_items
    }
    return render(request, 'watchlist.html', context)

@login_required
def add_to_watchlist(request, stock_id):
    """Add stock to watchlist"""
    stock = get_object_or_404(Stock, id=stock_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)
    
    if created:
        messages.success(request, f"{stock.symbol} added to watchlist!")
    else:
        messages.info(request, f"{stock.symbol} is already in your watchlist.")
    
    return redirect('watchlist')

@login_required
def remove_from_watchlist(request, watchlist_id):
    """Remove stock from watchlist"""
    watchlist_item = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
    stock_symbol = watchlist_item.stock.symbol
    watchlist_item.delete()
    messages.success(request, f"{stock_symbol} removed from watchlist.")
    return redirect('watchlist')

# --- Stock Details View ---
@login_required
def stock_detail_view(request, stock_id):
    """Detailed stock information page"""
    stock = get_object_or_404(Stock, id=stock_id)
    
    # Check if in watchlist
    in_watchlist = Watchlist.objects.filter(user=request.user, stock=stock).exists()
    
    # Get user's holdings
    try:
        portfolio_item = Portfolio.objects.get(user=request.user, stock=stock)
    except Portfolio.DoesNotExist:
        portfolio_item = None
    
    context = {
        'stock': stock,
        'in_watchlist': in_watchlist,
        'portfolio_item': portfolio_item
    }
    return render(request, 'stock_detail.html', context)

# --- Search & Filter Views ---
@login_required
def search_stocks(request):
    """Search stocks by symbol or name"""
    query = request.GET.get('q', '')
    
    if query:
        stocks = Stock.objects.filter(
            Q(symbol__icontains=query) | Q(name__icontains=query)
        )
    else:
        stocks = Stock.objects.all()
    
    context = {
        'stocks': stocks,
        'query': query
    }
    return render(request, 'search_results.html', context)

# --- API Views for Enhanced Features ---
@login_required
def top_gainers_api(request):
    """API endpoint for top gaining stocks"""
    stocks = Stock.objects.filter(change_percent__gt=0).order_by('-change_percent')[:10]
    
    data = [{
        'id': stock.id,
        'symbol': stock.symbol,
        'name': stock.name,
        'price': stock.current_price,
        'change_percent': stock.change_percent
    } for stock in stocks]
    
    return JsonResponse({'gainers': data})

@login_required
def top_losers_api(request):
    """API endpoint for top losing stocks"""
    stocks = Stock.objects.filter(change_percent__lt=0).order_by('change_percent')[:10]
    
    data = [{
        'id': stock.id,
        'symbol': stock.symbol,
        'name': stock.name,
        'price': stock.current_price,
        'change_percent': stock.change_percent
    } for stock in stocks]
    
    return JsonResponse({'losers': data})
