# 🔄 NSE Trading Platform - Complete Project Flow

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [User Registration Flow](#user-registration-flow)
3. [Trading Flow](#trading-flow)
4. [Data Flow](#data-flow)
5. [WebSocket Real-Time Updates](#websocket-real-time-updates)
6. [Request-Response Flow](#request-response-flow)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│  (HTML/CSS/JavaScript - Templates with Tailwind CSS)        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP/HTTPS Requests
                 │ WebSocket Connection
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    DAPHNE SERVER (ASGI)                      │
│              (Handles HTTP + WebSocket)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO APPLICATION                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   URLS.PY    │→ │   VIEWS.PY   │→ │  MODELS.PY   │     │
│  │  (Routing)   │  │  (Logic)     │  │  (Database)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ CONSUMERS.PY │  │ TEMPLATES/   │                        │
│  │ (WebSocket)  │  │ (HTML Pages) │                        │
│  └──────────────┘  └──────────────┘                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    SQLite DATABASE                           │
│  (Users, Stocks, Portfolio, Transactions, Watchlist)        │
└─────────────────────────────────────────────────────────────┘
```

---

## 👤 User Registration Flow

```
START
  │
  ↓
┌─────────────────────────┐
│ User visits /register/  │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ Fill Registration Form              │
│ - Username                          │
│ - Email                             │
│ - Password                          │
└───────────┬─────────────────────────┘
            │
            ↓ Submit Form (POST)
┌─────────────────────────────────────┐
│ views.register_view()               │
│ 1. Validate form data               │
│ 2. Create User object               │
│ 3. Save to database                 │
└───────────┬─────────────────────────┘
            │
            ↓ Signal Triggered
┌─────────────────────────────────────┐
│ models.create_user_profile()        │
│ (Post-save signal)                  │
│                                     │
│ 1. Auto-create UserProfile          │
│ 2. Set wallet_balance = ₹100,000   │
│ 3. Save profile                     │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ User logged in automatically        │
│ Redirect to /dashboard/             │
└───────────┬─────────────────────────┘
            │
            ↓
          END
```

**Database Changes:**
```sql
-- User table (Django built-in)
INSERT INTO auth_user (username, email, password)

-- UserProfile table (Auto-created by signal)
INSERT INTO trading_userprofile (user_id, wallet_balance, total_invested)
VALUES (new_user_id, 100000.00, 0.00)
```

---

## 💰 Trading Flow (Buy Stock)

```
START: User on Dashboard
  │
  ↓
┌─────────────────────────────────────┐
│ User clicks "Buy" on a stock        │
└───────────┬─────────────────────────┘
            │
            ↓ GET /buy/<stock_id>/
┌─────────────────────────────────────┐
│ views.buy_stock_view()              │
│ 1. Get stock from database          │
│ 2. Get user's wallet balance        │
│ 3. Render buy.html with data        │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ Buy Page Displayed                  │
│ - Stock name & price                │
│ - Wallet balance shown              │
│ - Quantity input field              │
└───────────┬─────────────────────────┘
            │
            ↓ User enters quantity & submits
┌─────────────────────────────────────┐
│ POST /buy/<stock_id>/               │
│ Form data: quantity = 10            │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ views.buy_stock_view() [POST]       │
│                                     │
│ STEP 1: Validate Quantity           │
│   - Check if positive number        │
│   - Check if valid integer          │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ STEP 2: Calculate Total Cost        │
│   total_cost = price × quantity     │
│   Example: ₹500 × 10 = ₹5,000      │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ STEP 3: Check Wallet Balance        │
│   if wallet_balance < total_cost:   │
│     Show error message              │
│     Return to buy page              │
└───────────┬─────────────────────────┘
            │ Balance OK
            ↓
┌─────────────────────────────────────┐
│ STEP 4: Deduct from Wallet          │
│   wallet_balance -= total_cost      │
│   total_invested += total_cost      │
│   Save UserProfile                  │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ STEP 5: Create Transaction Record   │
│   Transaction.create(               │
│     user = current_user             │
│     stock = selected_stock          │
│     quantity = 10                   │
│     price = 500                     │
│     type = "BUY"                    │
│     timestamp = now()               │
│   )                                 │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ STEP 6: Update Portfolio            │
│                                     │
│ If user already owns this stock:    │
│   - Calculate new average price     │
│   - Add to existing quantity        │
│                                     │
│ If new stock:                       │
│   - Create new portfolio entry      │
│   - Set quantity & avg_price        │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ STEP 7: Show Success Message        │
│ "Successfully purchased 10 shares   │
│  of RELIANCE for ₹5,000"           │
└───────────┬─────────────────────────┘
            │
            ↓
┌─────────────────────────────────────┐
│ Redirect to /portfolio/             │
└───────────┬─────────────────────────┘
            │
            ↓
          END
```

**Database Changes:**
```sql
-- Update wallet
UPDATE trading_userprofile 
SET wallet_balance = wallet_balance - 5000,
    total_invested = total_invested + 5000
WHERE user_id = current_user_id

-- Create transaction
INSERT INTO trading_transaction 
(user_id, stock_id, quantity, price, type, timestamp)
VALUES (user_id, stock_id, 10, 500, 'BUY', NOW())

-- Update portfolio
-- If exists:
UPDATE trading_portfolio 
SET quantity = quantity + 10,
    avg_price = (avg_price * old_qty + price * new_qty) / total_qty
WHERE user_id = user_id AND stock_id = stock_id

-- If new:
INSERT INTO trading_portfolio (user_id, stock_id, quantity, avg_price)
VALUES (user_id, stock_id, 10, 500)
```

---

## 📊 Data Flow (Complete Cycle)

```
┌─────────────────────────────────────────────────────────────┐
│                    1. USER INTERACTION                       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    2. HTTP REQUEST                           │
│  Browser → Django (via Daphne)                              │
│  Example: GET /dashboard/                                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    3. URL ROUTING                            │
│  urls.py matches pattern                                     │
│  path('dashboard/', views.dashboard_view)                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    4. VIEW FUNCTION                          │
│  views.dashboard_view(request)                              │
│                                                              │
│  def dashboard_view(request):                               │
│      # Get data from database                               │
│      stocks = Stock.objects.all()                           │
│                                                              │
│      # Prepare context                                      │
│      context = {'stocks': stocks}                           │
│                                                              │
│      # Render template                                      │
│      return render(request, 'dashboard.html', context)      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    5. DATABASE QUERY                         │
│  ORM translates to SQL                                       │
│  SELECT * FROM trading_stock                                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    6. TEMPLATE RENDERING                     │
│  dashboard.html receives context                            │
│                                                              │
│  {% for stock in stocks %}                                  │
│      <div>{{ stock.name }} - ₹{{ stock.price }}</div>      │
│  {% endfor %}                                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    7. HTTP RESPONSE                          │
│  HTML sent back to browser                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    8. BROWSER RENDERS                        │
│  User sees the dashboard page                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 WebSocket Real-Time Updates Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (JavaScript)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓ Open WebSocket Connection
┌─────────────────────────────────────────────────────────────┐
│  const socket = new WebSocket('ws://localhost:8000/ws/..') │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    DAPHNE SERVER                             │
│  Routes WebSocket to appropriate consumer                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    ROUTING.PY                                │
│  websocket_urlpatterns = [                                  │
│      path('ws/stocks/', StockConsumer.as_asgi())           │
│  ]                                                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    CONSUMER.PY                               │
│  class StockConsumer(AsyncWebsocketConsumer):              │
│                                                              │
│      async def connect(self):                               │
│          # Accept connection                                │
│          await self.accept()                                │
│          # Start sending updates                            │
│          await self.send_stock_updates()                    │
│                                                              │
│      async def send_stock_updates(self):                    │
│          while True:                                        │
│              # Get stock data                               │
│              stock = get_random_stock()                     │
│              # Simulate price change                        │
│              new_price = update_price(stock)                │
│              # Send to browser                              │
│              await self.send(json.dumps({                   │
│                  'stock': {                                 │
│                      'id': stock.id,                        │
│                      'price': new_price                     │
│                  }                                          │
│              }))                                            │
│              await asyncio.sleep(5)  # Every 5 seconds     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓ Send JSON data
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (JavaScript)                      │
│                                                              │
│  socket.onmessage = function(event) {                       │
│      const data = JSON.parse(event.data);                   │
│      updateStockPrice(data.stock);                          │
│      // Update DOM with new price                           │
│      document.getElementById('stock-' + data.stock.id)      │
│          .textContent = '₹' + data.stock.price;            │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

**Flow Summary:**
1. Browser opens WebSocket connection
2. Server accepts and keeps connection alive
3. Server sends price updates every 5 seconds
4. Browser receives updates and updates UI
5. No page refresh needed!

---

## 🔍 Complete Request-Response Example

### Example: User Buys 10 Shares of RELIANCE

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: User Action                                          │
│ User clicks "Buy" button on RELIANCE stock card             │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 2: Browser Request                                      │
│ GET http://localhost:8000/buy/1/                            │
│ Headers: Cookie (session ID)                                │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 3: Django Receives Request                              │
│ - Middleware processes request                               │
│ - Authentication checks session                              │
│ - CSRF protection validates                                  │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 4: URL Routing                                          │
│ urls.py: path('buy/<int:stock_id>/', views.buy_stock_view) │
│ Matches: stock_id = 1                                       │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 5: View Execution                                       │
│ views.buy_stock_view(request, stock_id=1)                   │
│                                                              │
│ # Get stock                                                 │
│ stock = Stock.objects.get(id=1)                             │
│ # Result: RELIANCE, price=₹2500                            │
│                                                              │
│ # Get user profile                                          │
│ profile = UserProfile.objects.get(user=request.user)        │
│ # Result: wallet_balance=₹100,000                          │
│                                                              │
│ # Render template                                           │
│ return render(request, 'buy.html', {                        │
│     'stock': stock,                                         │
│     'wallet_balance': profile.wallet_balance                │
│ })                                                          │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 6: Template Rendering                                   │
│ buy.html displays:                                           │
│ - Stock: RELIANCE                                           │
│ - Price: ₹2,500                                             │
│ - Your Balance: ₹100,000                                    │
│ - Quantity input field                                      │
│ - Buy button                                                │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 7: User Enters Quantity                                 │
│ User types: 10                                              │
│ Clicks: "Confirm Purchase"                                  │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 8: Form Submission                                      │
│ POST http://localhost:8000/buy/1/                           │
│ Body: quantity=10                                           │
│ Headers: CSRF Token, Cookie                                 │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 9: View Processes Purchase                              │
│ views.buy_stock_view(request, stock_id=1) [POST method]    │
│                                                              │
│ quantity = 10                                               │
│ price = ₹2,500                                              │
│ total_cost = 10 × ₹2,500 = ₹25,000                        │
│                                                              │
│ # Check balance                                             │
│ if wallet_balance (₹100,000) >= total_cost (₹25,000):     │
│     ✅ Proceed                                              │
│                                                              │
│ # Deduct money                                              │
│ wallet_balance = ₹100,000 - ₹25,000 = ₹75,000            │
│                                                              │
│ # Create transaction                                        │
│ Transaction.create(BUY, RELIANCE, 10, ₹2,500)             │
│                                                              │
│ # Update portfolio                                          │
│ Portfolio.create(user, RELIANCE, qty=10, avg=₹2,500)      │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 10: Database Updates                                    │
│                                                              │
│ UPDATE trading_userprofile                                  │
│ SET wallet_balance = 75000                                  │
│ WHERE user_id = 1                                           │
│                                                              │
│ INSERT INTO trading_transaction                             │
│ VALUES (1, 1, 10, 2500, 'BUY', NOW())                      │
│                                                              │
│ INSERT INTO trading_portfolio                               │
│ VALUES (1, 1, 10, 2500)                                     │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 11: Success Response                                    │
│ messages.success("Successfully purchased 10 shares...")     │
│ redirect('/portfolio/')                                     │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 12: Browser Redirects                                   │
│ GET http://localhost:8000/portfolio/                        │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────────────────────┐
│ STEP 13: Portfolio Page Displayed                            │
│ Shows:                                                       │
│ - RELIANCE: 10 shares @ ₹2,500                             │
│ - Current value: ₹25,000                                    │
│ - P&L: ₹0 (just bought)                                     │
│ - Success message displayed                                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure & Flow

```
nse_project/
│
├── nse_project/              # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── asgi.py              # ASGI config (WebSocket)
│   └── wsgi.py              # WSGI config (HTTP)
│
├── trading/                  # Main app
│   │
│   ├── models.py            # Database models
│   │   ├── UserProfile      # Wallet & user data
│   │   ├── Stock            # Stock information
│   │   ├── Portfolio        # User holdings
│   │   ├── Transaction      # Buy/sell records
│   │   ├── Watchlist        # Favorite stocks
│   │   └── PriceAlert       # Price notifications
│   │
│   ├── views.py             # Business logic
│   │   ├── register_view    # User registration
│   │   ├── login_view       # User login
│   │   ├── dashboard_view   # Market watch
│   │   ├── buy_stock_view   # Buy stocks
│   │   ├── sell_stock_view  # Sell stocks
│   │   ├── portfolio_view   # View holdings
│   │   ├── watchlist_view   # View watchlist
│   │   ├── profile_view     # User profile
│   │   └── wallet_view      # Wallet management
│   │
│   ├── urls.py              # App URL routing
│   │   └── Maps URLs to views
│   │
│   ├── consumers.py         # WebSocket handlers
│   │   └── StockConsumer    # Real-time updates
│   │
│   ├── routing.py           # WebSocket routing
│   │   └── websocket_urlpatterns
│   │
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── home.html        # Homepage
│       ├── dashboard.html   # Market watch
│       ├── buy.html         # Buy page
│       ├── sell.html        # Sell page
│       ├── portfolio.html   # Portfolio page
│       ├── transactions.html # Transaction history
│       ├── watchlist.html   # Watchlist page
│       ├── profile.html     # User profile
│       └── wallet.html      # Wallet page
│
└── db.sqlite3               # Database file
```

---

## 🎯 Key Concepts

### 1. **MVC Pattern (Django MVT)**
```
Model (models.py)     → Database structure
View (views.py)       → Business logic
Template (HTML)       → User interface
```

### 2. **Request-Response Cycle**
```
Browser → URL → View → Model → Database
                ↓
Database → Model → View → Template → Browser
```

### 3. **Authentication Flow**
```
Login → Session Created → Cookie Stored → 
Subsequent Requests Include Cookie → 
Django Validates Session → User Authenticated
```

### 4. **Database Relationships**
```
User ←→ UserProfile (One-to-One)
User ←→ Portfolio (One-to-Many)
User ←→ Transaction (One-to-Many)
User ←→ Watchlist (One-to-Many)
Stock ←→ Portfolio (One-to-Many)
Stock ←→ Transaction (One-to-Many)
```

---

## 🚀 Summary

### Complete Flow in One Picture:
```
User Registers
    ↓
Profile Created (₹100K wallet)
    ↓
Browse Dashboard (WebSocket updates prices)
    ↓
Search/Filter Stocks
    ↓
View Stock Details
    ↓
Add to Watchlist (optional)
    ↓
Click Buy
    ↓
Enter Quantity
    ↓
System Checks Balance
    ↓
Deduct Money from Wallet
    ↓
Create Transaction Record
    ↓
Update Portfolio
    ↓
Show Success Message
    ↓
View Portfolio (Real-time P&L)
    ↓
Monitor Prices (WebSocket)
    ↓
Click Sell
    ↓
Enter Quantity
    ↓
Add Money to Wallet
    ↓
Update Portfolio
    ↓
Create Transaction Record
    ↓
View Transaction History
    ↓
Check Wallet Balance
    ↓
View Profile & Total Assets
```

**This is your complete end-to-end NSE Trading Platform flow! 🎉**
