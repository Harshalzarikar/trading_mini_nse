# 🚀 Quick Start Guide - NSE Trading Platform

## For Windows Users

### Option 1: Automated Setup (Recommended)

1. **Run Setup Script**
   ```bash
   setup.bat
   ```
   This will:
   - Create virtual environment
   - Install all dependencies
   - Setup database
   - Create superuser account

2. **Start the Server**
   ```bash
   start.bat
   ```
   Server will run at: http://localhost:8000

### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**
   ```bash
   cd nse_project
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Server**
   ```bash
   daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
   ```

## First Steps After Installation

### 1. Login as Admin
- Go to http://localhost:8000/admin
- Login with superuser credentials
- Verify everything is working

### 2. Add Your First Stock
- Navigate to "Add Custom Stock" from the menu
- Enter a stock symbol (e.g., `RELIANCE.NS`)
- Enter stock name (e.g., `Reliance Industries`)
- Click "Add Stock"

### 3. Start Trading
- Go to Dashboard/Market page
- Click "Buy" on any stock
- Enter quantity and confirm
- Check your Portfolio to see holdings

### 4. Test Real-Time Updates
- Keep Dashboard page open
- Watch for live price updates (every 5-10 seconds)
- See the connection status indicator (green = connected)

## Popular NSE Stock Symbols

Add these stocks to get started:

| Symbol | Company Name |
|--------|-------------|
| RELIANCE.NS | Reliance Industries |
| TCS.NS | Tata Consultancy Services |
| INFY.NS | Infosys |
| HDFCBANK.NS | HDFC Bank |
| ICICIBANK.NS | ICICI Bank |
| SBIN.NS | State Bank of India |
| BHARTIARTL.NS | Bharti Airtel |
| ITC.NS | ITC Limited |
| HINDUNILVR.NS | Hindustan Unilever |
| KOTAKBANK.NS | Kotak Mahindra Bank |

## Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F
```

### WebSocket Not Connecting
- Make sure you're using Daphne (not runserver)
- Check browser console for errors
- Verify ASGI configuration in settings.py

### Stock Prices Not Updating
- Check internet connection
- yfinance API might be rate-limited
- Try adding stocks with .NS suffix for NSE

### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
python manage.py flush
python manage.py migrate
```

## Testing the Application

### Test Real-Time Updates
1. Open Dashboard in two browser windows
2. Watch both windows update simultaneously
3. Verify WebSocket connection status

### Test Buy/Sell Flow
1. Buy a stock from Dashboard
2. Check Portfolio for the purchase
3. Verify transaction in Transaction History
4. Sell some quantity from Portfolio
5. Confirm updated holdings

### Test P&L Calculations
1. Buy a stock at current price
2. Wait for price to change
3. Check Portfolio for P&L updates
4. Verify color coding (green/red)

## Next Steps

- Explore the Live Prices page
- Try the Market Explorer
- Add more stocks to your portfolio
- Monitor your transaction history
- Experiment with different trading strategies

## Need Help?

- Check the main README.md for detailed documentation
- Review the troubleshooting section
- Check Django logs for errors
- Verify all dependencies are installed

---

**Happy Trading! 📈**
