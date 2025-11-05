# 🚀 START HERE - Quick Fix & Launch Guide

## ⚡ Quick Fix (2 Minutes)

Your issues have been fixed! Follow these steps:

### Step 1: Stop Current Server
If server is running, press `Ctrl+C` to stop it.

### Step 2: Run Fix Script
```bash
fix_issues.bat
```

### Step 3: Start Server with Daphne
```bash
start.bat
```

**That's it!** Open http://localhost:8000

---

## 🔍 What Was Wrong?

### ❌ Problem 1: Template Error
**Error:** `'custom_filters' is not a registered tag library`

**✅ Fixed:** Removed custom filter, calculations now done in view

### ❌ Problem 2: WebSocket Not Connecting
**Error:** WebSocket connection fails

**✅ Solution:** Use Daphne (ASGI server) instead of runserver

---

## 📋 Startup Checklist

Follow this every time you start the application:

### First Time Setup
- [ ] Run `setup.bat` (one time only)
- [ ] Create superuser account

### Every Time You Start
- [ ] Activate virtual environment: `venv\Scripts\activate`
- [ ] Navigate to project: `cd nse_project`
- [ ] Start with Daphne: `daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application`
- [ ] Or simply run: `start.bat`

### Verify It's Working
- [ ] Open http://localhost:8000
- [ ] Dashboard shows green "● Live" status
- [ ] Transactions page loads without errors
- [ ] Can buy/sell stocks

---

## 🎯 Three Ways to Start

### Method 1: Easy Way (Recommended)
```bash
start.bat
```

### Method 2: Manual Way
```bash
venv\Scripts\activate
cd nse_project
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

### Method 3: Fallback (If WebSocket Doesn't Work)
```bash
# Switch to AJAX version
cd nse_project\trading\templates
ren dashboard.html dashboard_websocket.html
ren dashboard_ajax.html dashboard.html

# Start normally
cd ..
python manage.py runserver
```

---

## ✅ Verification Steps

After starting server, verify:

1. **Server Running**
   - Terminal shows: "Listening on TCP address 0.0.0.0:8000"

2. **Homepage Works**
   - Open: http://localhost:8000
   - Should see homepage

3. **Login Works**
   - Can login/register

4. **Dashboard Works**
   - Shows stocks
   - Status indicator is green: "● Live - Real-Time Updates"

5. **Transactions Page Works**
   - No template errors
   - Shows transaction history

6. **WebSocket Connected**
   - Open browser console (F12)
   - Should see: "WebSocket connected"

---

## 🐛 Still Having Issues?

### Issue: Template Error Still Appears
**Solution:**
```bash
# Restart server (Ctrl+C then start again)
start.bat
```

### Issue: WebSocket Not Connecting
**Check:**
1. Are you using Daphne? (not runserver)
2. Check browser console (F12) for errors
3. Try AJAX fallback (Method 3 above)

### Issue: Module Not Found
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port Already in Use
**Solution:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📚 Documentation Files

- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `FIXES_APPLIED.md` - What was fixed
- `TROUBLESHOOTING.md` - Detailed troubleshooting
- `DEPLOYMENT.md` - Production deployment

---

## 🎉 You're Ready!

**Your application is fixed and ready to use!**

Just run:
```bash
start.bat
```

Then open: **http://localhost:8000**

---

## 🔥 Quick Commands Reference

```bash
# Start server (WebSocket support)
start.bat

# Fix common issues
fix_issues.bat

# Create superuser
cd nse_project
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Install dependencies
pip install -r requirements.txt
```

---

**Happy Trading! 📈💰**
