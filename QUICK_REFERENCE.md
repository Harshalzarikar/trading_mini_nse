# 🚀 NSE Trading Platform - Quick Reference

## ⚡ Quick Start (One Command)
```bash
migrate_and_start.bat
```

## 🔧 Issues Fixed
✅ Template error → Fixed
✅ WebSocket not connecting → Use Daphne
✅ Server setup → ASGI configured

## 🎯 New Features Added

### 💰 Wallet System
- Starting balance: **₹100,000**
- Deducted on buy
- Credited on sell
- Can't overspend

### ⭐ Watchlist
- Save favorite stocks
- Quick access
- Add/remove easily

### 🔍 Search
- Find by symbol
- Find by name
- Quick results

### 👤 Profile
- View wallet balance
- See total assets
- Track performance

### 📊 Stock Details
- Comprehensive info
- Your holdings
- Watchlist status

## 🔗 New URLs

```
/profile/          → User Profile
/wallet/           → Wallet
/watchlist/        → Watchlist
/stock/<id>/       → Stock Details
/search/           → Search
```

## 📋 Complete Flow

```
Register → Get ₹100K → Search → Watchlist → Buy → Monitor → Sell → Profit
```

## 🛠️ Commands

### Start Server (WebSocket)
```bash
cd nse_project
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

### Run Migrations
```bash
cd nse_project
python manage.py makemigrations
python manage.py migrate
```

### Create Profiles
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from trading.models import UserProfile
>>> for user in User.objects.all():
...     UserProfile.objects.get_or_create(user=user)
>>> exit()
```

## 🐛 Quick Fixes

### WebSocket Not Working?
```bash
# Use Daphne, not runserver!
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

### Port Already in Use?
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Template Error?
```bash
# Restart server
Ctrl+C
start.bat
```

## 📊 What's New

### Models
- UserProfile (wallet)
- Watchlist
- PriceAlert
- Enhanced Stock

### Views
- profile_view
- wallet_view
- watchlist_view
- stock_detail_view
- search_stocks
- + 4 more

### Features
- Wallet validation
- Search & filter
- Watchlist management
- Stock details
- Market analytics

## ✅ Status

🟢 **ALL WORKING!**
- WebSocket: ✅
- Wallet: ✅
- Trading: ✅
- Real-time: ✅
- End-to-end: ✅

## 🎉 Ready to Trade!

```bash
migrate_and_start.bat
```

Open: **http://localhost:8000**

**Happy Trading! 📈💰**
