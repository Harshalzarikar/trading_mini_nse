# 🏦 NSE Trading Platform - Real-Time Stock Trading Simulator

A comprehensive, real-time stock trading simulation platform built with Django, Django Channels, and WebSocket technology. This application provides live stock price updates from Yahoo Finance (yfinance) and allows users to practice trading without real money.

## ✨ Features

### 🔴 Real-Time Updates
- **WebSocket Integration**: Live stock price updates using Django Channels
- **yfinance API**: Real-time stock data from Yahoo Finance
- **Auto-Reconnection**: Automatic WebSocket reconnection on connection loss
- **Live Dashboard**: Real-time price changes with visual indicators

### 📊 Trading Features
- **Buy Stocks**: Purchase stocks at current market prices
- **Sell Stocks**: Sell holdings from your portfolio
- **Portfolio Management**: Track your investments with profit/loss calculations
- **Transaction History**: Complete record of all buy/sell transactions
- **Market Explorer**: Browse and discover top NSE stocks

### 💼 Portfolio Analytics
- **Real-Time P&L**: Live profit/loss calculations
- **Average Price Tracking**: Monitor your average purchase price
- **Performance Metrics**: Detailed portfolio performance analysis
- **Visual Indicators**: Color-coded gains and losses

### 🔐 User Management
- **User Registration & Authentication**
- **Secure Login/Logout**
- **Personal Portfolio Tracking**
- **Transaction History per User**

### 🛠️ Admin Features
- **Add Stocks**: Superusers can add new stocks to the platform
- **Custom Stock Addition**: Users can add custom stock symbols
- **Live Price Management**: Automatic price updates from yfinance

## 🚀 Technology Stack

- **Backend**: Django 5.1.5
- **WebSocket**: Django Channels 4.2.0
- **ASGI Server**: Daphne 4.1.2
- **Stock Data**: yfinance, nsepy
- **Frontend**: HTML, TailwindCSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: Django REST Framework

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
cd nse-app
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
cd nse_project
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
# Using Daphne (ASGI server for WebSocket support)
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application

# OR using Django's runserver (limited WebSocket support)
python manage.py runserver
```

### 7. Access the Application
Open your browser and navigate to:
- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📱 Usage Guide

### For Regular Users

1. **Register an Account**
   - Click "Register" on the homepage
   - Create your account with username and password

2. **Add Stocks to Trade**
   - Navigate to "Add Custom Stock"
   - Enter stock symbol (e.g., RELIANCE.NS, TCS.NS)
   - Stock price will be fetched automatically from yfinance

3. **View Market Dashboard**
   - Browse available stocks with real-time prices
   - See live price updates via WebSocket
   - Monitor profit/loss for each stock

4. **Buy Stocks**
   - Click "Buy" on any stock card
   - Enter the quantity you want to purchase
   - Confirm the transaction

5. **Manage Portfolio**
   - View your holdings in the Portfolio page
   - See real-time profit/loss calculations
   - Track average purchase price vs current price

6. **Sell Stocks**
   - Go to Portfolio page
   - Click "Sell" on any holding
   - Enter quantity to sell
   - View expected profit/loss before confirming

7. **Transaction History**
   - View all your buy/sell transactions
   - Filter by date and type
   - Track your trading activity

### For Superusers (Admin)

1. **Add Stocks Manually**
   - Navigate to "Add Stock" (admin only)
   - Enter stock name, symbol, and initial price
   - Stock will be available for all users

2. **Manage Users**
   - Access Django admin panel
   - View and manage user accounts
   - Monitor system-wide transactions

## 🌐 API Endpoints

### Stock APIs
- `GET /api/live-prices/` - Fetch live prices for all stocks
- `GET /api/market-explorer/` - Get top NSE stocks with live data
- `GET /api/stock-updates/` - Get random stock price update

### WebSocket Endpoint
- `ws://localhost:8000/ws/stocks/` - Real-time stock price updates

## 📊 Stock Symbol Format

For NSE (National Stock Exchange) stocks, use the format:
- **RELIANCE.NS** - Reliance Industries
- **TCS.NS** - Tata Consultancy Services
- **INFY.NS** - Infosys
- **HDFCBANK.NS** - HDFC Bank
- **ICICIBANK.NS** - ICICI Bank

## 🔒 Security Features

- CSRF Protection enabled
- User authentication required for trading
- Secure password hashing
- Session management
- SQL injection protection via Django ORM

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Built with TailwindCSS
- **Real-time Indicators**: Visual feedback for price changes
- **Color-coded P&L**: Green for profit, red for loss
- **Smooth Animations**: Enhanced user experience
- **Toast Notifications**: Success/error messages

## 📈 Performance Optimization

- **Async WebSocket**: Non-blocking real-time updates
- **Database Indexing**: Optimized queries
- **Caching**: Reduced API calls
- **Lazy Loading**: Efficient data fetching

## 🐛 Troubleshooting

### WebSocket Connection Issues
```bash
# Make sure you're using Daphne or another ASGI server
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
```

### yfinance API Errors
- Check your internet connection
- Some stocks may not have real-time data
- Falls back to simulated prices if API fails

### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
python manage.py flush
python manage.py migrate
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up environment variables
5. Configure static files with WhiteNoise or CDN
6. Use Redis for channel layers
7. Set up HTTPS for secure WebSocket (wss://)
8. Configure Gunicorn + Daphne for production

### Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📝 Project Structure

```
nse-app/
├── nse_project/
│   ├── trading/
│   │   ├── models.py          # Stock, Portfolio, Transaction models
│   │   ├── views.py           # View functions
│   │   ├── consumers.py       # WebSocket consumers
│   │   ├── routing.py         # WebSocket routing
│   │   ├── urls.py            # URL patterns
│   │   └── templates/         # HTML templates
│   ├── nse_project/
│   │   ├── settings.py        # Django settings
│   │   ├── asgi.py            # ASGI configuration
│   │   └── urls.py            # Main URL configuration
│   └── manage.py
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ for learning and practicing stock trading concepts.

## 🙏 Acknowledgments

- **yfinance**: For providing free stock market data
- **Django**: For the robust web framework
- **Django Channels**: For WebSocket support
- **TailwindCSS**: For beautiful UI components

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🔮 Future Enhancements

- [ ] Real-time charts and graphs
- [ ] Stock watchlist feature
- [ ] Price alerts and notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Paper trading competitions
- [ ] Social trading features
- [ ] Technical indicators
- [ ] News integration
- [ ] Multi-currency support

---

**Happy Trading! 📈💰**

*Remember: This is a simulation platform for learning purposes. Always do thorough research before investing real money in the stock market.*
#   t r a d i n g _ m i n i _ n s e  
 