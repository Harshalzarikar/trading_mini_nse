from django.urls import path
from . import views

# Maps URL patterns to their corresponding view functions
urlpatterns = [
    # Public and authentication URLs
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Core application URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('buy/<int:stock_id>/', views.buy_stock_view, name='buy_stock'),
    path('sell/<int:portfolio_id>/', views.sell_stock_view, name='sell_stock'),
    path('transactions/', views.transactions_view, name='transactions'),
    
    # Superuser URLs
    path('add_stock/', views.add_stock, name='add_stock'),
    path('live-prices/', views.live_prices, name='live_prices'),
    path('api/live-prices/', views.live_prices_api, name='live_prices_api'),
    
    # User stock management
    path('add-custom-stock/', views.add_custom_stock, name='add_custom_stock'),
    
    # Profile & Wallet
    path('profile/', views.profile_view, name='profile'),
    path('wallet/', views.wallet_view, name='wallet'),
    
    # Watchlist
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/add/<int:stock_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:watchlist_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    
    # Stock Details & Search
    path('stock/<int:stock_id>/', views.stock_detail_view, name='stock_detail'),
    path('search/', views.search_stocks, name='search_stocks'),
    
    # Market Explorer
    path('market-explorer/', views.market_explorer_view, name='market_explorer'),
    
    # API endpoints
    path('api/market-explorer/', views.market_explorer_api, name='market_explorer_api'),
    path('api/stock-updates/', views.stock_updates_api, name='stock_updates_api'),
    path('api/top-gainers/', views.top_gainers_api, name='top_gainers_api'),
    path('api/top-losers/', views.top_losers_api, name='top_losers_api'),
]

