# 🎯 NSE Trading Platform - Simple Flow Guide

## 🌟 The Big Picture (30 Seconds)

```
User → Register → Get ₹100K → Browse Stocks → Buy → Portfolio → Sell → Profit!
```

---

## 👤 1. User Journey (What User Sees)

### Step 1: Registration
```
Visit Homepage → Click Register → Fill Form → Submit
    ↓
✅ Account Created + ₹100,000 in Wallet
```

### Step 2: Browse Stocks
```
Dashboard Page → See All Stocks → Prices Update Live (WebSocket)
```

### Step 3: Buy Stock
```
Click "Buy" → Enter Quantity → Confirm
    ↓
✅ Money Deducted from Wallet
✅ Stock Added to Portfolio
```

### Step 4: Monitor
```
Portfolio Page → See Your Stocks → Watch P&L Change in Real-Time
```

### Step 5: Sell Stock
```
Click "Sell" → Enter Quantity → Confirm
    ↓
✅ Money Added to Wallet
✅ Portfolio Updated
```

---

## 🔧 2. Technical Flow (What Happens Behind)

### When User Registers:
```
1. Browser sends form data
2. Django creates User
3. Signal auto-creates UserProfile with ₹100K
4. User logged in
5. Redirect to dashboard
```

### When User Buys Stock:
```
1. User clicks Buy button
2. Django shows buy page with wallet balance
3. User enters quantity
4. Django checks: Do they have enough money?
   ├─ YES → Proceed
   └─ NO → Show error
5. Deduct money from wallet
6. Create transaction record
7. Add to portfolio
8. Show success message
```

### When Prices Update (WebSocket):
```
1. Browser opens WebSocket connection
2. Server sends price updates every 5 seconds
3. JavaScript updates prices on page
4. No page refresh needed!
```

---

## 📊 3. Database Flow (What Gets Saved)

### Registration:
```
auth_user table:
  ├─ username
  ├─ email
  └─ password (hashed)

trading_userprofile table:
  ├─ user_id (links to auth_user)
  ├─ wallet_balance = 100000
  └─ total_invested = 0
```

### Buying Stock:
```
trading_userprofile:
  └─ wallet_balance: 100000 → 75000 (deducted 25000)

trading_transaction:
  ├─ user_id
  ├─ stock_id
  ├─ quantity = 10
  ├─ price = 2500
  ├─ type = "BUY"
  └─ timestamp

trading_portfolio:
  ├─ user_id
  ├─ stock_id
  ├─ quantity = 10
  └─ avg_price = 2500
```

---

## 🔄 4. Request Flow (Browser ↔ Server)

### Simple Example: Viewing Dashboard

```
BROWSER                          SERVER
   │                               │
   │  GET /dashboard/              │
   ├──────────────────────────────>│
   │                               │
   │                          urls.py finds route
   │                               │
   │                          views.dashboard_view()
   │                               │
   │                          Gets stocks from database
   │                               │
   │                          Renders dashboard.html
   │                               │
   │  HTML with stock data         │
   │<──────────────────────────────┤
   │                               │
   Display page                    │
```

### With WebSocket:

```
BROWSER                          SERVER
   │                               │
   │  Open WebSocket               │
   ├──────────────────────────────>│
   │                               │
   │  Connection Accepted          │
   │<──────────────────────────────┤
   │                               │
   │                          Every 5 seconds:
   │                          - Update stock price
   │                          - Send to browser
   │                               │
   │  Price Update                 │
   │<──────────────────────────────┤
   │                               │
   Update UI (no refresh!)         │
```

---

## 📁 5. File Organization (Where Code Lives)

```
models.py        → Database structure (tables)
views.py         → Business logic (what happens)
urls.py          → URL routing (which page)
templates/       → HTML pages (what user sees)
consumers.py     → WebSocket handlers (real-time)
```

### Example: Buy Stock

```
1. urls.py:        path('buy/<id>/', views.buy_stock_view)
                   ↓
2. views.py:       def buy_stock_view(request, stock_id):
                       # Check balance
                       # Deduct money
                       # Update portfolio
                   ↓
3. models.py:      UserProfile.wallet_balance -= cost
                   Portfolio.quantity += qty
                   Transaction.create(...)
                   ↓
4. templates/:     buy.html shows success message
```

---

## 💡 6. Key Concepts Explained

### What is a Model?
```
A model = A database table

class Stock(models.Model):
    name = CharField()
    price = FloatField()

This creates a table:
┌────────┬───────────┬─────────┐
│   ID   │   Name    │  Price  │
├────────┼───────────┼─────────┤
│   1    │ RELIANCE  │  2500   │
│   2    │ TCS       │  3200   │
└────────┴───────────┴─────────┘
```

### What is a View?
```
A view = A function that handles requests

def buy_stock_view(request):
    # Get data
    # Process logic
    # Return response
```

### What is a Template?
```
A template = HTML with dynamic data

<h1>{{ stock.name }}</h1>
<p>Price: ₹{{ stock.price }}</p>

Becomes:
<h1>RELIANCE</h1>
<p>Price: ₹2500</p>
```

### What is WebSocket?
```
Normal HTTP:
  Browser asks → Server responds → Connection closes

WebSocket:
  Browser connects → Connection stays open → 
  Server can send updates anytime → Real-time!
```

---

## 🎯 7. Complete Example: Buy 10 Shares

### User's Perspective:
```
1. I see RELIANCE at ₹2,500
2. I click "Buy"
3. I enter quantity: 10
4. I click "Confirm"
5. I see success message
6. My portfolio shows 10 shares
7. My wallet shows ₹75,000 (was ₹100,000)
```

### What Happens in Code:
```python
# 1. User clicks Buy
# Browser: GET /buy/1/

# 2. Django shows buy page
def buy_stock_view(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    return render(request, 'buy.html', {'stock': stock})

# 3. User submits form
# Browser: POST /buy/1/ with quantity=10

# 4. Django processes purchase
def buy_stock_view(request, stock_id):
    quantity = 10
    stock = Stock.objects.get(id=stock_id)
    total_cost = stock.price * quantity  # 2500 * 10 = 25000
    
    # Check balance
    profile = UserProfile.objects.get(user=request.user)
    if profile.wallet_balance < total_cost:
        return "Insufficient funds!"
    
    # Deduct money
    profile.wallet_balance -= total_cost  # 100000 - 25000 = 75000
    profile.save()
    
    # Create transaction
    Transaction.objects.create(
        user=request.user,
        stock=stock,
        quantity=10,
        price=2500,
        type="BUY"
    )
    
    # Update portfolio
    Portfolio.objects.create(
        user=request.user,
        stock=stock,
        quantity=10,
        avg_price=2500
    )
    
    return redirect('portfolio')
```

### What Gets Saved:
```sql
-- Wallet updated
UPDATE trading_userprofile 
SET wallet_balance = 75000 
WHERE user_id = 1

-- Transaction recorded
INSERT INTO trading_transaction 
VALUES (1, 1, 10, 2500, 'BUY', NOW())

-- Portfolio updated
INSERT INTO trading_portfolio 
VALUES (1, 1, 10, 2500)
```

---

## 🚀 Quick Reference

### Main Components:
```
Models     → Database tables
Views      → Business logic
Templates  → HTML pages
URLs       → Route mapping
Consumers  → WebSocket handlers
```

### Main Flow:
```
URL → View → Model → Database
         ↓
    Template → Browser
```

### Data Flow:
```
User Input → Form → View → Model → Database
Database → Model → View → Template → User Sees Result
```

---

## 📚 Where to Learn More

1. **PROJECT_FLOW.md** - Detailed technical flow
2. **FINAL_SUMMARY.md** - Complete feature list
3. **WHAT_WAS_DONE.md** - All changes made
4. **QUICK_REFERENCE.md** - Quick commands

---

## ✨ Summary

Your NSE Trading Platform works like this:

1. **User interacts** with browser (HTML/JavaScript)
2. **Browser sends request** to Django server
3. **Django processes** the request (views.py)
4. **Database updated** (models.py)
5. **Response sent back** to browser (templates)
6. **WebSocket keeps** connection alive for real-time updates

**It's that simple! 🎉**
