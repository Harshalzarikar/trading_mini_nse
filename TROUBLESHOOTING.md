# 🔧 Troubleshooting Guide

## Issue 1: WebSocket Not Connecting

### Problem
WebSocket connection fails with error or shows "Disconnected" status.

### Solutions

#### Solution 1: Use Daphne (ASGI Server)
WebSockets require an ASGI server. Django's `runserver` has limited WebSocket support.

**Stop the current server and run:**
```bash
cd nse_project
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

Or use the provided script:
```bash
start.bat
```

#### Solution 2: Check if Daphne is Installed
```bash
pip install daphne
```

#### Solution 3: Verify ASGI Configuration
Check `nse_project/settings.py`:
```python
ASGI_APPLICATION = 'nse_project.asgi.application'
```

#### Solution 4: Check Browser Console
Open browser DevTools (F12) → Console tab
Look for WebSocket errors like:
- `WebSocket connection failed`
- `Error in connection establishment`

#### Solution 5: Fallback to AJAX Polling
If WebSocket still doesn't work, you can use AJAX polling instead.

**Update `dashboard.html`** - Replace WebSocket code with:
```javascript
// AJAX Polling (Fallback)
function fetchStockUpdates() {
    fetch('/api/stock-updates/')
        .then(response => response.json())
        .then(data => {
            if (data.stock) {
                updateStockPrice(data.stock);
                calculateAllProfitLoss();
            }
            setTimeout(fetchStockUpdates, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
            setTimeout(fetchStockUpdates, 10000);
        });
}
fetchStockUpdates();
```

## Issue 2: Template Tag Library Error

### Problem
```
TemplateSyntaxError: 'custom_filters' is not a registered tag library
```

### Solution (Already Fixed)
The transactions template has been updated to calculate totals in the view instead of using template filters.

**If you still see this error:**

1. **Restart the server** (important!)
```bash
# Stop server (Ctrl+C)
# Start again
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

2. **Clear Python cache**
```bash
# Delete __pycache__ folders
cd nse_project
python manage.py clean_pyc  # if available
# Or manually delete __pycache__ folders
```

3. **Verify the fix**
Check `transactions.html` - it should NOT have:
```django
{% load custom_filters %}  # This line should be removed
```

## Issue 3: Module Import Errors

### Problem
```
ModuleNotFoundError: No module named 'channels'
```

### Solution
Install missing dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install channels==4.2.0
pip install daphne==4.1.2
pip install yfinance==0.2.50
```

## Issue 4: Database Errors

### Problem
```
django.db.utils.OperationalError: no such table
```

### Solution
Run migrations:
```bash
cd nse_project
python manage.py makemigrations
python manage.py migrate
```

## Issue 5: Port Already in Use

### Problem
```
Error: [Errno 10048] Only one usage of each socket address is normally permitted
```

### Solution

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Alternative: Use different port**
```bash
daphne -b 0.0.0.0 -p 8001 nse_project.asgi:application
```

## Issue 6: Static Files Not Loading

### Problem
CSS/JS files not loading (404 errors)

### Solution
```bash
cd nse_project
python manage.py collectstatic --noinput
```

## Issue 7: yfinance API Errors

### Problem
```
No price data available for symbol
```

### Solutions

1. **Check symbol format**
   - NSE stocks need `.NS` suffix
   - Example: `RELIANCE.NS`, `TCS.NS`

2. **Check internet connection**

3. **Try different stock**
   - Some stocks may not have real-time data

4. **The app will fallback to simulated prices** if yfinance fails

## Issue 8: CSRF Token Errors

### Problem
```
CSRF verification failed
```

### Solution
Ensure forms have CSRF token:
```django
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

## Common Commands

### Start Server (ASGI with WebSocket)
```bash
cd nse_project
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

### Start Server (Django runserver - Limited WebSocket)
```bash
cd nse_project
python manage.py runserver
```

### Create Superuser
```bash
cd nse_project
python manage.py createsuperuser
```

### Reset Database (WARNING: Deletes all data)
```bash
cd nse_project
python manage.py flush
python manage.py migrate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Quick Fixes Checklist

- [ ] Restart server after code changes
- [ ] Use Daphne for WebSocket support
- [ ] Check browser console for errors
- [ ] Verify all dependencies installed
- [ ] Run migrations if database errors
- [ ] Clear browser cache
- [ ] Check Python version (3.8+)
- [ ] Verify virtual environment is activated

## Still Having Issues?

1. **Check server logs** - Look at terminal output for errors
2. **Check browser console** - F12 → Console tab
3. **Verify file paths** - Ensure all files are in correct locations
4. **Check Python version** - Should be 3.8 or higher
5. **Reinstall dependencies** - `pip install -r requirements.txt --force-reinstall`

## Getting Help

If issues persist:
1. Note the exact error message
2. Check which URL is failing
3. Review server terminal output
4. Check browser console errors
5. Verify all setup steps were completed

---

**Most Common Fix: Use Daphne instead of runserver for WebSocket support!**
