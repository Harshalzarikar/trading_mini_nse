# 📈 Add All NSE Stocks - Complete Guide

## 🚀 Quick Start (One Command)

```bash
add_nse_stocks.bat
```

This will add **50 popular NSE stocks** to your database with live prices!

---

## 📋 What Stocks Will Be Added?

### Top 50 NSE Stocks (Nifty 50)

#### Banking & Finance (8 stocks)
- HDFC Bank
- ICICI Bank
- State Bank of India
- Kotak Mahindra Bank
- Axis Bank
- Bajaj Finance
- Bajaj Finserv
- IndusInd Bank

#### IT & Technology (5 stocks)
- TCS (Tata Consultancy Services)
- Infosys
- HCL Technologies
- Wipro
- Tech Mahindra

#### FMCG & Consumer (6 stocks)
- Hindustan Unilever
- ITC
- Nestle India
- Britannia Industries
- Tata Consumer Products
- Asian Paints

#### Automobile (6 stocks)
- Maruti Suzuki
- Tata Motors
- Mahindra & Mahindra
- Eicher Motors
- Hero MotoCorp
- Bajaj Auto

#### Energy & Oil (3 stocks)
- Reliance Industries
- ONGC
- Bharat Petroleum

#### Pharma & Healthcare (5 stocks)
- Sun Pharmaceutical
- Dr. Reddy's Laboratories
- Cipla
- Divi's Laboratories
- Apollo Hospitals

#### Infrastructure & Cement (6 stocks)
- Larsen & Toubro
- UltraTech Cement
- Shree Cement
- Grasim Industries
- Adani Ports
- Adani Enterprises

#### Metals & Mining (4 stocks)
- Tata Steel
- JSW Steel
- Hindalco Industries
- Coal India

#### Power & Utilities (2 stocks)
- NTPC
- Power Grid Corporation

#### Others (5 stocks)
- Titan Company (Jewellery)
- SBI Life Insurance
- HDFC Life Insurance
- UPL (Chemicals)
- Bharti Airtel (Telecom)

---

## 🎯 What Data Gets Added?

For each stock, the system fetches:

```
✓ Stock Name          (e.g., "Reliance Industries Ltd")
✓ Symbol              (e.g., "RELIANCE.NS")
✓ Current Price       (Live from yfinance)
✓ Sector              (e.g., "Energy", "IT", "Banking")
✓ Market Cap          (Company valuation)
✓ Day High            (Today's highest price)
✓ Day Low             (Today's lowest price)
✓ Volume              (Trading volume)
```

---

## 📝 Step-by-Step Instructions

### Method 1: Using Batch Script (Easiest)

```bash
# Just double-click or run:
add_nse_stocks.bat
```

### Method 2: Manual Command

```bash
# Activate virtual environment
venv\Scripts\activate

# Navigate to project
cd nse_project

# Run the command
python manage.py add_nse_stocks
```

---

## ⏱️ How Long Does It Take?

- **Time**: 2-3 minutes
- **Why**: Fetches live prices from yfinance for each stock
- **Progress**: Shows real-time progress for each stock

---

## 📊 What You'll See

### During Execution:
```
Starting to add NSE stocks...
Fetching price for RELIANCE.NS...
  ✓ Added: Reliance Industries Ltd (RELIANCE.NS) - ₹2,450.50
Fetching price for TCS.NS...
  ✓ Added: Tata Consultancy Services Ltd (TCS.NS) - ₹3,520.75
...
```

### After Completion:
```
============================================================
✓ Successfully added: 50 stocks
✓ Successfully updated: 0 stocks
============================================================
Total stocks in database: 50
```

---

## 🔄 Running Again (Update Prices)

If you run the command again:
- **Existing stocks** → Prices updated
- **New stocks** → Added to database

```bash
# Run anytime to update prices
add_nse_stocks.bat
```

---

## 🛠️ Advanced Usage

### Add More Stocks

Edit the file:
```
nse_project\trading\management\commands\add_nse_stocks.py
```

Add to the `nse_stocks` list:
```python
{'symbol': 'NEWSTOCK.NS', 'name': 'New Stock Ltd', 'sector': 'Technology'},
```

### Custom Stock List

Create your own command:
```bash
cd nse_project
python manage.py shell
```

```python
from trading.models import Stock

# Add custom stock
Stock.objects.create(
    name='My Custom Stock',
    symbol='CUSTOM.NS',
    current_price=100.0,
    sector='Technology'
)
```

---

## 🔍 Verify Stocks Were Added

### Method 1: Django Admin
```
1. Start server: start.bat
2. Go to: http://localhost:8000/admin/
3. Login as superuser
4. Click "Stocks" → See all 50 stocks
```

### Method 2: Django Shell
```bash
cd nse_project
python manage.py shell
```

```python
from trading.models import Stock

# Count stocks
print(f"Total stocks: {Stock.objects.count()}")

# List all stocks
for stock in Stock.objects.all():
    print(f"{stock.symbol} - {stock.name} - ₹{stock.current_price}")

# Filter by sector
it_stocks = Stock.objects.filter(sector='IT')
print(f"IT stocks: {it_stocks.count()}")
```

### Method 3: Dashboard
```
1. Start server: start.bat
2. Go to: http://localhost:8000/dashboard/
3. See all stocks displayed
```

---

## ❌ Troubleshooting

### Issue: "No module named 'yfinance'"
**Solution:**
```bash
pip install yfinance
```

### Issue: "No price data for symbol"
**Reason:** Stock symbol might be delisted or incorrect
**Solution:** Stock will be added with default price ₹100

### Issue: "Connection timeout"
**Reason:** Internet connection issue
**Solution:** 
- Check internet connection
- Try again
- Or add stocks manually with default prices

### Issue: Command not found
**Solution:**
```bash
# Make sure you're in the right directory
cd nse_project

# Run with full path
python manage.py add_nse_stocks
```

---

## 📈 After Adding Stocks

### What You Can Do:

1. **Browse Dashboard**
   ```
   http://localhost:8000/dashboard/
   See all 50 stocks with live prices
   ```

2. **Start Trading**
   ```
   - Click "Buy" on any stock
   - Enter quantity
   - Purchase with your ₹100,000 wallet
   ```

3. **Search Stocks**
   ```
   http://localhost:8000/search/
   Search by name or symbol
   ```

4. **Add to Watchlist**
   ```
   Click "Add to Watchlist" on any stock
   Track your favorites
   ```

5. **View Stock Details**
   ```
   Click on any stock
   See detailed information
   ```

---

## 🎯 Stock Categories

### By Sector:
```python
# View stocks by sector
from trading.models import Stock

banking = Stock.objects.filter(sector='Banking')
it = Stock.objects.filter(sector='IT')
pharma = Stock.objects.filter(sector='Pharma')
automobile = Stock.objects.filter(sector='Automobile')
```

### By Price Range:
```python
# Stocks under ₹1000
cheap = Stock.objects.filter(current_price__lt=1000)

# Stocks over ₹2000
expensive = Stock.objects.filter(current_price__gt=2000)
```

---

## 📝 Database Schema

After adding stocks, your database will have:

```sql
trading_stock table:
┌────┬─────────────┬──────────────────────┬───────────┬──────────┬────────────┐
│ ID │   Symbol    │        Name          │   Price   │  Sector  │ Market Cap │
├────┼─────────────┼──────────────────────┼───────────┼──────────┼────────────┤
│ 1  │ RELIANCE.NS │ Reliance Industries  │  2450.50  │  Energy  │  16500000  │
│ 2  │ TCS.NS      │ Tata Consultancy     │  3520.75  │  IT      │  12800000  │
│ 3  │ HDFCBANK.NS │ HDFC Bank            │  1650.25  │  Banking │  9200000   │
│... │ ...         │ ...                  │  ...      │  ...     │  ...       │
└────┴─────────────┴──────────────────────┴───────────┴──────────┴────────────┘
```

---

## 🚀 Quick Commands Summary

```bash
# Add all NSE stocks
add_nse_stocks.bat

# Update prices (run again)
add_nse_stocks.bat

# View stocks in shell
cd nse_project
python manage.py shell
>>> from trading.models import Stock
>>> Stock.objects.count()

# Start trading
start.bat
```

---

## ✨ What's Next?

After adding stocks:

1. ✅ **Start Server**
   ```bash
   start.bat
   ```

2. ✅ **Register/Login**
   ```
   http://localhost:8000/register/
   ```

3. ✅ **Browse 50 Stocks**
   ```
   http://localhost:8000/dashboard/
   ```

4. ✅ **Start Trading**
   ```
   Buy stocks with your ₹100,000 wallet
   ```

5. ✅ **Build Portfolio**
   ```
   Track your investments
   Monitor P&L in real-time
   ```

---

## 🎉 Summary

**One command adds 50 NSE stocks:**
```bash
add_nse_stocks.bat
```

**Includes:**
- ✅ 50 popular NSE stocks
- ✅ Live prices from yfinance
- ✅ Sector information
- ✅ Market data
- ✅ Ready to trade

**Your trading platform is now fully stocked! 📈💰**
