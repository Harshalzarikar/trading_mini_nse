import asyncio
import json
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Stock

def update_stock_prices():
    """
    Update stock prices periodically and broadcast to connected clients
    This can be called from a management command or scheduler
    """
    stocks = Stock.objects.all()
    if not stocks:
        return
    
    # Select a random stock to update
    stock = random.choice(stocks)
    
    # Simulate price change (±5%)
    price_change = stock.current_price * random.uniform(-0.05, 0.05)
    new_price = max(0.01, stock.current_price + price_change)
    
    # Update in database
    stock.current_price = new_price
    stock.save()
    
    # Prepare data for broadcast
    stock_data = {
        'id': stock.id,
        'symbol': stock.symbol,
        'name': stock.name,
        'price': stock.current_price
    }
    
    # Send to channel layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stock_updates",
        {
            'type': 'stock_update',
            'stock': stock_data
        }
    )
    
    return stock_data