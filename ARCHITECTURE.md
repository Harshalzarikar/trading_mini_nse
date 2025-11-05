# 🏗️ NSE Trading Platform - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │  Portfolio   │  │ Transactions │         │
│  │   (HTML/JS)  │  │   (HTML/JS)  │  │   (HTML/JS)  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │   HTTP/HTTPS    │
                    │   WebSocket     │
                    └────────┬────────┘
                             │
┌────────────────────────────┼─────────────────────────────────────┐
│                    DJANGO SERVER (ASGI)                          │
│                            │                                     │
│  ┌─────────────────────────┴──────────────────────────────┐    │
│  │              DAPHNE (ASGI Server)                       │    │
│  └─────────────────────────┬──────────────────────────────┘    │
│                            │                                     │
│         ┌──────────────────┴──────────────────┐                │
│         │                                      │                │
│  ┌──────▼──────┐                    ┌─────────▼────────┐       │
│  │   HTTP      │                    │   WebSocket      │       │
│  │  Requests   │                    │   Connection     │       │
│  └──────┬──────┘                    └─────────┬────────┘       │
│         │                                      │                │
│  ┌──────▼──────────────┐            ┌─────────▼────────────┐   │
│  │   Django Views      │            │  Async Consumer      │   │
│  │  - dashboard_view   │            │  - StockConsumer     │   │
│  │  - buy_stock_view   │            │  - send_updates()    │   │
│  │  - sell_stock_view  │            │  - fetch_yfinance()  │   │
│  │  - portfolio_view   │            └─────────┬────────────┘   │
│  │  - transactions     │                      │                │
│  └──────┬──────────────┘                      │                │
│         │                                      │                │
│         └──────────────────┬───────────────────┘                │
│                            │                                     │
│                   ┌────────▼────────┐                           │
│                   │  Django Models  │                           │
│                   │  - Stock        │                           │
│                   │  - Portfolio    │                           │
│                   │  - Transaction  │                           │
│                   └────────┬────────┘                           │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   DATABASE      │
                    │   (SQLite/      │
                    │   PostgreSQL)   │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│  ┌──────────────┐                    ┌──────────────┐          │
│  │   yfinance   │◄───────────────────┤  Yahoo       │          │
│  │   API        │                    │  Finance     │          │
│  └──────────────┘                    └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Frontend Layer

#### Pages
```
Home Page (/)
    │
    ├── Register (/register/)
    │       │
    │       └── Success → Dashboard
    │
    ├── Login (/login/)
    │       │
    │       └── Success → Dashboard
    │
    └── Dashboard (/dashboard/)
            │
            ├── Buy Stock (/buy/<id>/)
            │       │
            │       └── Success → Portfolio
            │
            ├── Portfolio (/portfolio/)
            │       │
            │       └── Sell Stock (/sell/<id>/)
            │               │
            │               └── Success → Portfolio
            │
            ├── Transactions (/transactions/)
            │
            ├── Live Prices (/live-prices/)
            │
            └── Add Custom Stock (/add-custom-stock/)
```

### 2. Backend Layer

#### URL Routing
```python
# Public URLs
/                           → home_view
/register/                  → register_view
/login/                     → login_view
/logout/                    → logout_view

# Trading URLs (Login Required)
/dashboard/                 → dashboard_view
/portfolio/                 → portfolio_view
/buy/<stock_id>/           → buy_stock_view
/sell/<portfolio_id>/      → sell_stock_view
/transactions/             → transactions_view

# Stock Management
/add-custom-stock/         → add_custom_stock
/add_stock/                → add_stock (Superuser)

# API Endpoints
/api/live-prices/          → live_prices_api
/api/market-explorer/      → market_explorer_api
/api/stock-updates/        → stock_updates_api

# WebSocket
ws://host/ws/stocks/       → StockConsumer
```

#### Models Schema
```python
Stock
├── id (PK)
├── name (CharField)
├── symbol (CharField, Unique)
├── current_price (FloatField)
└── purchase_price (FloatField, Nullable)

Portfolio
├── id (PK)
├── user (FK → User)
├── stock (FK → Stock)
├── quantity (IntegerField)
└── avg_price (FloatField)

Transaction
├── id (PK)
├── user (FK → User)
├── stock (FK → Stock)
├── quantity (IntegerField)
├── price (FloatField)
├── type (CharField: BUY/SELL)
└── timestamp (DateTimeField)
```

### 3. WebSocket Flow

```
Client Connection
    │
    ├─► WebSocket Handshake
    │       │
    │       └─► Accept Connection
    │               │
    │               └─► Send "connection_established"
    │
    ├─► Start Update Loop
    │       │
    │       ├─► Fetch Stock from DB
    │       │
    │       ├─► Call yfinance API
    │       │       │
    │       │       ├─► Success → Real Price
    │       │       └─► Failure → Simulated Price
    │       │
    │       ├─► Update Database
    │       │
    │       ├─► Send Update to Client
    │       │       │
    │       │       └─► {type: "stock_update", stock: {...}}
    │       │
    │       └─► Wait 5-10 seconds → Loop
    │
    └─► Disconnect
            │
            └─► Cleanup & Close
```

### 4. Trading Flow

#### Buy Stock Flow
```
User Clicks "Buy"
    │
    ├─► Navigate to /buy/<stock_id>/
    │
    ├─► Display Stock Info
    │   ├─► Current Price
    │   └─► Input Quantity
    │
    ├─► User Submits Form
    │
    ├─► Validate Quantity
    │
    ├─► Create Transaction (BUY)
    │
    ├─► Update/Create Portfolio
    │   ├─► Calculate New Avg Price
    │   └─► Update Quantity
    │
    ├─► Save to Database
    │
    └─► Redirect to Portfolio
```

#### Sell Stock Flow
```
User Clicks "Sell" in Portfolio
    │
    ├─► Navigate to /sell/<portfolio_id>/
    │
    ├─► Display Holding Info
    │   ├─► Current Price
    │   ├─► Quantity Owned
    │   ├─► Avg Purchase Price
    │   └─► Expected P&L
    │
    ├─► User Enters Quantity
    │
    ├─► Validate (quantity <= owned)
    │
    ├─► Create Transaction (SELL)
    │
    ├─► Update Portfolio
    │   ├─► Reduce Quantity
    │   └─► Delete if quantity = 0
    │
    ├─► Save to Database
    │
    └─► Redirect to Portfolio
```

### 5. Real-Time Update Flow

```
Dashboard Page Loaded
    │
    ├─► Initialize WebSocket
    │       │
    │       └─► ws://localhost:8000/ws/stocks/
    │
    ├─► Connection Established
    │       │
    │       └─► Update Status: "● Live"
    │
    ├─► Receive Stock Update
    │       │
    │       ├─► Parse JSON Data
    │       │
    │       ├─► Find Stock Card
    │       │
    │       ├─► Update Price Display
    │       │
    │       ├─► Show Price Change Indicator
    │       │   ├─► ▲ Green (Price Up)
    │       │   └─► ▼ Red (Price Down)
    │       │
    │       ├─► Flash Animation
    │       │
    │       └─► Recalculate P&L
    │
    └─► Connection Lost
            │
            ├─► Update Status: "Reconnecting..."
            │
            └─► Attempt Reconnection (max 5 times)
```

### 6. Data Flow Diagram

```
┌──────────────┐
│   User       │
│   Action     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Frontend   │
│   (Browser)  │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   HTTP       │  │  WebSocket   │
│   Request    │  │  Message     │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Django     │  │   Async      │
│   View       │  │   Consumer   │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ├─────────────────┤
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│   Django     │  │   yfinance   │
│   ORM        │  │   API        │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 │
┌──────────────┐         │
│   Database   │◄────────┘
└──────────────┘
```

## Technology Stack Details

### Backend Technologies
```
Django 5.1.5
├── Web Framework
├── ORM (Database)
├── Authentication
├── Admin Panel
└── Template Engine

Django Channels 4.2.0
├── WebSocket Support
├── Async Operations
├── Channel Layers
└── ASGI Protocol

Daphne 4.1.2
├── ASGI Server
├── WebSocket Handler
└── HTTP/2 Support
```

### Frontend Technologies
```
HTML5
├── Semantic Markup
├── Forms
└── Templates

TailwindCSS
├── Utility Classes
├── Responsive Design
└── Modern Styling

JavaScript (ES6+)
├── WebSocket API
├── DOM Manipulation
├── Event Handling
└── Async/Await
```

### Data Sources
```
yfinance
├── Real-time Prices
├── Historical Data
└── Stock Information

nsepy
├── NSE Data
└── Indian Stocks
```

## Security Architecture

```
┌─────────────────────────────────────┐
│         Security Layers             │
├─────────────────────────────────────┤
│  1. HTTPS/WSS (Transport Layer)     │
├─────────────────────────────────────┤
│  2. Django Authentication           │
│     - Session Management            │
│     - Password Hashing              │
├─────────────────────────────────────┤
│  3. CSRF Protection                 │
│     - Token Validation              │
├─────────────────────────────────────┤
│  4. Input Validation                │
│     - Form Validation               │
│     - Type Checking                 │
├─────────────────────────────────────┤
│  5. SQL Injection Prevention        │
│     - Django ORM                    │
│     - Parameterized Queries         │
├─────────────────────────────────────┤
│  6. XSS Protection                  │
│     - Template Escaping             │
│     - Content Security Policy       │
└─────────────────────────────────────┘
```

## Deployment Architecture

### Development
```
Local Machine
├── SQLite Database
├── Django Dev Server / Daphne
├── In-Memory Channel Layer
└── Debug Mode ON
```

### Production
```
Server (VPS/Cloud)
├── PostgreSQL Database
├── Gunicorn (HTTP) + Daphne (WebSocket)
├── Redis (Channel Layer)
├── Nginx (Reverse Proxy)
├── SSL/TLS Certificate
└── Debug Mode OFF
```

## Performance Optimization

```
┌─────────────────────────────────────┐
│     Performance Strategies          │
├─────────────────────────────────────┤
│  1. Async WebSocket Consumer        │
│     - Non-blocking operations       │
├─────────────────────────────────────┤
│  2. Database Optimization           │
│     - select_related()              │
│     - Indexes on foreign keys       │
├─────────────────────────────────────┤
│  3. WebSocket vs Polling            │
│     - Reduced server load           │
│     - Lower latency                 │
├─────────────────────────────────────┤
│  4. Efficient Queries               │
│     - Minimize DB hits              │
│     - Batch operations              │
├─────────────────────────────────────┤
│  5. Frontend Optimization           │
│     - Minimal re-renders            │
│     - Efficient DOM updates         │
└─────────────────────────────────────┘
```

## Scalability Considerations

```
Horizontal Scaling
├── Multiple Gunicorn Workers
├── Multiple Daphne Instances
├── Load Balancer (Nginx/HAProxy)
└── Redis Channel Layer (shared state)

Vertical Scaling
├── Increase Server Resources
├── Database Optimization
└── Connection Pooling

Caching Strategy
├── Redis for Session Storage
├── Cache Stock Prices (1-2 min)
└── CDN for Static Files
```

---

**This architecture supports real-time, scalable, and secure stock trading operations! 🏗️**
