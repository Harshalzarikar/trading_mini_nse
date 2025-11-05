import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Stock
import asyncio
import yfinance as yf
import random

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to Real-Time Stock Updates'
        }))
        
        # Start sending stock updates
        self.is_running = True
        self.update_task = asyncio.create_task(self.send_stock_updates())
    
    async def disconnect(self, close_code):
        self.is_running = False
        if hasattr(self, 'update_task'):
            self.update_task.cancel()
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        
        if message == 'get_stocks':
            stocks = await self.get_all_stocks()
            await self.send(text_data=json.dumps({
                'type': 'stock_list',
                'stocks': stocks
            }))
    
    @database_sync_to_async
    def get_all_stocks(self):
        stocks = Stock.objects.all()
        return [{'id': stock.id, 'symbol': stock.symbol, 'name': stock.name, 'price': float(stock.current_price)} 
                for stock in stocks]
    
    @database_sync_to_async
    def update_stock_price_from_yfinance(self, stock_id, symbol):
        """Fetch real price from yfinance and update database"""
        try:
            stock = Stock.objects.get(id=stock_id)
            ticker = yf.Ticker(symbol)
            
            # Try to get real-time data
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty:
                new_price = float(hist['Close'].iloc[-1])
            else:
                # Fallback to simulation if no data
                price_change = stock.current_price * (random.uniform(-0.01, 0.01))
                new_price = max(0.01, stock.current_price + price_change)
            
            stock.current_price = new_price
            stock.save()
            
            return {
                'id': stock.id, 
                'symbol': stock.symbol, 
                'name': stock.name, 
                'price': float(stock.current_price),
                'purchase_price': float(stock.purchase_price) if stock.purchase_price else float(stock.current_price)
            }
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    async def send_stock_updates(self):
        """Send real-time stock price updates using yfinance"""
        while self.is_running:
            try:
                # Get all stocks
                stocks = await self.get_all_stocks()
                
                if stocks:
                    # Update a random stock with real data
                    stock = random.choice(stocks)
                    updated_stock = await self.update_stock_price_from_yfinance(stock['id'], stock['symbol'])
                    
                    if updated_stock:
                        # Send update to client
                        await self.send(text_data=json.dumps({
                            'type': 'stock_update',
                            'stock': updated_stock
                        }))
                
            except Exception as e:
                print(f"Error in send_stock_updates: {e}")
            
            # Wait before next update (5-10 seconds for real API calls)
            await asyncio.sleep(random.uniform(5, 10))