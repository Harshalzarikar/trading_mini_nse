from django.core.management.base import BaseCommand
from trading.models import Stock
import yfinance as yf

class Command(BaseCommand):
    help = 'Add popular NSE stocks to the database'

    def handle(self, *args, **kwargs):
        # Top 50 NSE stocks with their details
        nse_stocks = [
            # Nifty 50 Major Stocks
            {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries Ltd', 'sector': 'Energy'},
            {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services Ltd', 'sector': 'IT'},
            {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank Ltd', 'sector': 'Banking'},
            {'symbol': 'INFY.NS', 'name': 'Infosys Ltd', 'sector': 'IT'},
            {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank Ltd', 'sector': 'Banking'},
            {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever Ltd', 'sector': 'FMCG'},
            {'symbol': 'ITC.NS', 'name': 'ITC Ltd', 'sector': 'FMCG'},
            {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'sector': 'Banking'},
            {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel Ltd', 'sector': 'Telecom'},
            {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank Ltd', 'sector': 'Banking'},
            
            {'symbol': 'LT.NS', 'name': 'Larsen & Toubro Ltd', 'sector': 'Infrastructure'},
            {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank Ltd', 'sector': 'Banking'},
            {'symbol': 'BAJFINANCE.NS', 'name': 'Bajaj Finance Ltd', 'sector': 'Finance'},
            {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints Ltd', 'sector': 'Paints'},
            {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India Ltd', 'sector': 'Automobile'},
            {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies Ltd', 'sector': 'IT'},
            {'symbol': 'WIPRO.NS', 'name': 'Wipro Ltd', 'sector': 'IT'},
            {'symbol': 'ULTRACEMCO.NS', 'name': 'UltraTech Cement Ltd', 'sector': 'Cement'},
            {'symbol': 'TITAN.NS', 'name': 'Titan Company Ltd', 'sector': 'Jewellery'},
            {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical Industries Ltd', 'sector': 'Pharma'},
            
            {'symbol': 'NESTLEIND.NS', 'name': 'Nestle India Ltd', 'sector': 'FMCG'},
            {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors Ltd', 'sector': 'Automobile'},
            {'symbol': 'TATASTEEL.NS', 'name': 'Tata Steel Ltd', 'sector': 'Steel'},
            {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra Ltd', 'sector': 'IT'},
            {'symbol': 'POWERGRID.NS', 'name': 'Power Grid Corporation of India Ltd', 'sector': 'Power'},
            {'symbol': 'NTPC.NS', 'name': 'NTPC Ltd', 'sector': 'Power'},
            {'symbol': 'ONGC.NS', 'name': 'Oil and Natural Gas Corporation Ltd', 'sector': 'Energy'},
            {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra Ltd', 'sector': 'Automobile'},
            {'symbol': 'BAJAJFINSV.NS', 'name': 'Bajaj Finserv Ltd', 'sector': 'Finance'},
            {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddys Laboratories Ltd', 'sector': 'Pharma'},
            
            {'symbol': 'CIPLA.NS', 'name': 'Cipla Ltd', 'sector': 'Pharma'},
            {'symbol': 'DIVISLAB.NS', 'name': 'Divis Laboratories Ltd', 'sector': 'Pharma'},
            {'symbol': 'EICHERMOT.NS', 'name': 'Eicher Motors Ltd', 'sector': 'Automobile'},
            {'symbol': 'GRASIM.NS', 'name': 'Grasim Industries Ltd', 'sector': 'Cement'},
            {'symbol': 'HEROMOTOCO.NS', 'name': 'Hero MotoCorp Ltd', 'sector': 'Automobile'},
            {'symbol': 'HINDALCO.NS', 'name': 'Hindalco Industries Ltd', 'sector': 'Metals'},
            {'symbol': 'INDUSINDBK.NS', 'name': 'IndusInd Bank Ltd', 'sector': 'Banking'},
            {'symbol': 'JSWSTEEL.NS', 'name': 'JSW Steel Ltd', 'sector': 'Steel'},
            {'symbol': 'BRITANNIA.NS', 'name': 'Britannia Industries Ltd', 'sector': 'FMCG'},
            {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports and Special Economic Zone Ltd', 'sector': 'Infrastructure'},
            
            {'symbol': 'COALINDIA.NS', 'name': 'Coal India Ltd', 'sector': 'Mining'},
            {'symbol': 'BPCL.NS', 'name': 'Bharat Petroleum Corporation Ltd', 'sector': 'Energy'},
            {'symbol': 'SHREECEM.NS', 'name': 'Shree Cement Ltd', 'sector': 'Cement'},
            {'symbol': 'TATACONSUM.NS', 'name': 'Tata Consumer Products Ltd', 'sector': 'FMCG'},
            {'symbol': 'APOLLOHOSP.NS', 'name': 'Apollo Hospitals Enterprise Ltd', 'sector': 'Healthcare'},
            {'symbol': 'ADANIENT.NS', 'name': 'Adani Enterprises Ltd', 'sector': 'Infrastructure'},
            {'symbol': 'BAJAJ-AUTO.NS', 'name': 'Bajaj Auto Ltd', 'sector': 'Automobile'},
            {'symbol': 'SBILIFE.NS', 'name': 'SBI Life Insurance Company Ltd', 'sector': 'Insurance'},
            {'symbol': 'HDFCLIFE.NS', 'name': 'HDFC Life Insurance Company Ltd', 'sector': 'Insurance'},
            {'symbol': 'UPL.NS', 'name': 'UPL Ltd', 'sector': 'Chemicals'},
        ]

        self.stdout.write(self.style.WARNING('Starting to add NSE stocks...'))
        self.stdout.write(self.style.WARNING('This may take a few minutes as we fetch live prices from yfinance...'))
        
        added_count = 0
        updated_count = 0
        failed_count = 0
        
        for stock_data in nse_stocks:
            symbol = stock_data['symbol']
            name = stock_data['name']
            sector = stock_data['sector']
            
            try:
                # Check if stock already exists
                existing_stock = Stock.objects.filter(symbol=symbol).first()
                
                # Fetch current price from yfinance
                self.stdout.write(f'Fetching price for {symbol}...')
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d")
                
                if hist.empty:
                    self.stdout.write(self.style.WARNING(f'  ⚠ No price data for {symbol}, using default price'))
                    current_price = 100.0  # Default price
                else:
                    current_price = float(hist['Close'].iloc[-1])
                
                # Try to get additional data
                try:
                    info = ticker.info
                    market_cap = info.get('marketCap', None)
                    day_high = float(hist['High'].iloc[-1]) if not hist.empty else None
                    day_low = float(hist['Low'].iloc[-1]) if not hist.empty else None
                    volume = int(hist['Volume'].iloc[-1]) if not hist.empty else None
                except:
                    market_cap = None
                    day_high = None
                    day_low = None
                    volume = None
                
                if existing_stock:
                    # Update existing stock
                    existing_stock.name = name
                    existing_stock.current_price = current_price
                    existing_stock.sector = sector
                    existing_stock.market_cap = market_cap
                    existing_stock.day_high = day_high
                    existing_stock.day_low = day_low
                    existing_stock.volume = volume
                    existing_stock.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Updated: {name} ({symbol}) - ₹{current_price:.2f}'))
                else:
                    # Create new stock
                    Stock.objects.create(
                        name=name,
                        symbol=symbol,
                        current_price=current_price,
                        sector=sector,
                        market_cap=market_cap,
                        day_high=day_high,
                        day_low=day_low,
                        volume=volume
                    )
                    added_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Added: {name} ({symbol}) - ₹{current_price:.2f}'))
                
            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to add {symbol}: {str(e)}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully added: {added_count} stocks'))
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully updated: {updated_count} stocks'))
        if failed_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Failed: {failed_count} stocks'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'Total stocks in database: {Stock.objects.count()}'))
