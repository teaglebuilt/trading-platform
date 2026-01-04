# Intraday Master Indicator - Complete Guide

## Overview
This is an all-in-one intraday trading indicator for TradingView that combines multiple proven strategies into a single comprehensive system.

---

## How to Install

### Step 1: Open TradingView
1. Go to [TradingView.com](https://www.tradingview.com)
2. Open any chart (stocks, futures, forex, crypto)

### Step 2: Add the Indicator
1. Click on **Pine Editor** at the bottom of the screen
2. Click **"New"** → **"New blank indicator"**
3. Delete all the default code
4. Copy and paste the entire code from `intraday_master_indicator.pine`
5. Click **"Save"** and name it **"Intraday Master"**
6. Click **"Add to Chart"**

---

## Features Included

### 1. Opening Range Breakout (ORB)
- **What it does**: Identifies the high/low range in the first 15 minutes (customizable)
- **Strategy**: Breakouts above/below this range often indicate strong directional moves
- **Best for**: First 30-60 minutes of market open
- **Green line** = ORB High | **Red line** = ORB Low

### 2. VWAP with Standard Deviation Bands
- **What it does**: Shows the volume-weighted average price with statistical bands
- **Strategy**:
  - Price bouncing off lower bands = potential long
  - Price rejecting upper bands = potential short
  - Price above VWAP = bullish bias
- **Blue line** = VWAP
- **Green/Red bands** = 1σ and 2σ deviation zones

### 3. Volume Analysis
- **What it does**: Detects abnormal volume spikes
- **Strategy**: High volume confirms breakouts and trend changes
- **Purple bars** = Volume spike (1.5x+ average)
- **Blue bars** = Above average volume
- **Gray bars** = Normal volume

### 4. Momentum Indicators (RSI + MACD)
- **RSI**: Identifies overbought (>70) and oversold (<30) conditions
- **MACD**: Confirms trend changes with crossovers
- **Strategy**: Combined signals provide higher probability setups

### 5. Trend Detection (EMA Crossover)
- **Fast EMA (9)** and **Slow EMA (21)**
- **Bullish trend**: Fast EMA > Slow EMA
- **Bearish trend**: Fast EMA < Slow EMA

### 6. Smart Entry Signals
The indicator generates LONG/SHORT signals when multiple conditions align:

**LONG Signal Triggers:**
- ORB breakout above high + volume spike, OR
- Price bouncing from lower VWAP band + RSI oversold + bullish trend, OR
- MACD bullish crossover + price above VWAP + bullish trend

**SHORT Signal Triggers:**
- ORB breakdown below low + volume spike, OR
- Price rejecting from upper VWAP band + RSI overbought + bearish trend, OR
- MACD bearish crossover + price below VWAP + bearish trend

### 7. Auto Risk Management
- **Stop Loss**: Calculated using ATR (Average True Range) × multiplier
- **Target 1**: 50% of full risk-reward target
- **Target 2**: Full risk-reward target (default 1:2)
- All levels displayed automatically when signal triggers

### 8. Real-time Dashboard
Top-right corner shows:
- Current trend direction
- RSI value and status
- MACD direction
- Volume status
- VWAP position
- ORB status
- Active trade status
- Current signal

---

## How to Use for Today's Trading

### Pre-Market Setup (Before 9:15 AM for NSE / 9:30 AM for US)
1. Open TradingView and add the indicator
2. Set your preferred timeframe: **5-min** or **15-min** charts work best
3. Customize settings if needed (default settings work well)
4. Enable alerts (see Alert Setup below)

### Market Open Strategy (First Hour)
1. **Wait for ORB formation** (dashboard shows "FORMING" → "ACTIVE")
2. **Watch for volume confirmation** (purple bars = spike)
3. **Look for signals**:
   - Green triangle below bar = **LONG** opportunity
   - Red triangle above bar = **SHORT** opportunity
4. **Check the label** for:
   - Entry price
   - Stop loss level
   - Target price
   - Current RSI

### During Trading Hours
1. **Monitor dashboard** for:
   - Trend confirmation
   - Volume spikes
   - VWAP position
2. **Take signals that align with**:
   - Overall market trend
   - High volume confirmation
   - Multiple indicator confluence
3. **Exit when**:
   - Orange circle appears (exit signal)
   - Price hits Target 2
   - Price hits Stop Loss

---

## Alert Setup (Important!)

### To receive notifications when signals appear:

1. Click on the **alarm clock icon** on the right panel
2. Select **"Intraday Master"** from the indicator list
3. Choose alert type:
   - **"Long Signal"** = Buy opportunities
   - **"Short Signal"** = Sell opportunities
   - **"ORB Breakout Long"** = Opening range breakout
   - **"Volume Spike"** = Unusual volume detected
4. Set notification method:
   - Popup alert
   - App notification (download TradingView mobile app)
   - Email
   - Webhook (for automated trading)
5. Click **"Create"**

### Recommended Alerts to Set:
1. Long Signal
2. Short Signal
3. ORB Breakout Long
4. ORB Breakdown Short

---

## Settings Customization

### Opening Range Breakout
- **ORB Period**: Default 15 min (adjust to 5/10/30 based on preference)
- **Show ORB Levels**: Toggle high/low lines

### VWAP
- **Standard Deviation 1**: 1.0σ band (first support/resistance)
- **Standard Deviation 2**: 2.0σ band (extreme zones)

### Volume
- **Volume MA Length**: 20 periods (average calculation)
- **Volume Spike Threshold**: 1.5x (1.5x average = spike)

### Momentum
- **RSI Length**: 14 (standard)
- **RSI Oversold**: 30 (buy zone)
- **RSI Overbought**: 70 (sell zone)

### Risk Management
- **Risk:Reward Ratio**: 2.0 (1:2 ratio - risk $100 to make $200)
- **ATR Length**: 14 periods
- **ATR Stop Loss Multiplier**: 1.5 (distance from entry)

---

## Trading Examples

### Example 1: ORB Breakout Long
```
Time: 9:30 AM
ORB High: 150.50
ORB Low: 149.80

Price breaks above 150.50 at 10:00 AM with volume spike
→ GREEN TRIANGLE appears
→ Label shows:
   Entry: 150.55
   Stop Loss: 149.80
   Target: 151.80
   RSI: 58

Action: Enter long at 150.55, SL at 149.80, Target 151.80
```

### Example 2: VWAP Bounce
```
Time: 11:15 AM
VWAP: 2500
Lower Band 1σ: 2490
Price: 2488

Price touches 2488, forms bullish candle, RSI = 28, volume spike
→ GREEN TRIANGLE appears
→ Trend = Bullish (EMA 9 > EMA 21)

Action: Enter long at 2490, SL at 2483, Target based on R:R
```

### Example 3: MACD Reversal Short
```
Time: 2:00 PM
Price: 45,200
VWAP: 45,180
MACD crosses down, RSI = 72

→ RED TRIANGLE appears
→ Dashboard shows "BEARISH" trend
→ Volume = HIGH

Action: Enter short at 45,200, SL at 45,350, Target 45,050
```

---

## Best Practices

### DO:
✅ Wait for volume confirmation (purple/blue bars)
✅ Trade in direction of overall trend (check dashboard)
✅ Use 5-min or 15-min timeframes for intraday
✅ Set alerts to avoid missing signals
✅ Follow the stop loss strictly
✅ Book partial profits at Target 1
✅ Move stop to breakeven after Target 1 hits
✅ Trade liquid stocks/instruments only

### DON'T:
❌ Trade signals without volume confirmation
❌ Ignore the dashboard trend indicator
❌ Use on 1-hour+ timeframes (meant for intraday)
❌ Override stop loss levels
❌ Trade in choppy/sideways markets (low volume)
❌ Take every signal blindly
❌ Trade illiquid stocks with wide spreads

---

## Timeframe Recommendations

| Timeframe | Best For | Signals/Day |
|-----------|----------|-------------|
| 3-min | Scalping | 10-20 |
| 5-min | **Intraday (Recommended)** | 5-10 |
| 15-min | **Swing Intraday (Recommended)** | 3-5 |
| 30-min | Position intraday | 1-3 |

---

## Markets Supported

### Indian Markets (NSE/BSE)
- **Market hours**: 9:15 AM - 3:30 PM IST
- **ORB period**: First 15 minutes (9:15-9:30)
- **Best stocks**: Nifty 50, Bank Nifty, liquid stocks
- **Timeframe**: 5-min or 15-min

### US Markets (NYSE/NASDAQ)
- **Market hours**: 9:30 AM - 4:00 PM EST
- **ORB period**: First 15-30 minutes (9:30-10:00)
- **Best stocks**: S&P 500, NASDAQ 100, high volume stocks
- **Timeframe**: 5-min or 15-min

### Futures & Forex
- Works on all liquid futures contracts
- 24-hour forex markets (adjust ORB to session open)

---

## Troubleshooting

### "No signals appearing"
- Check if volume is sufficient (purple/blue bars)
- Verify trend is clear (not choppy/sideways)
- Ensure ORB period has completed ("ACTIVE" in dashboard)
- Try lower timeframe (5-min instead of 15-min)

### "Too many signals"
- Increase volume threshold (1.5 → 2.0)
- Trade only with trend (ignore counter-trend signals)
- Wait for ORB completion before taking signals
- Use higher timeframe (15-min instead of 5-min)

### "Signals are late"
- This is normal - indicator waits for confirmation
- Enable alerts to get notified immediately
- Consider using lower timeframe for faster signals

### "Dashboard not showing"
- Ensure "Show Price Labels" is enabled in settings
- Try reloading the chart
- Check if you're on mobile (might be too small)

---

## Performance Tips

1. **Best trading hours** (highest volume/volatility):
   - NSE: 9:15-11:00 AM, 2:00-3:30 PM
   - US: 9:30-11:00 AM, 2:00-4:00 PM EST

2. **Combine with market context**:
   - Check overall market trend (Nifty/SPY direction)
   - Avoid trading against strong market moves
   - Higher success rate when stock and market align

3. **Risk management**:
   - Never risk more than 1-2% per trade
   - Use position sizing based on stop loss distance
   - Book partial profits at Target 1 (50%)
   - Trail stop loss after Target 1 hits

4. **Filter signals**:
   - Only trade when dashboard shows clear trend
   - Avoid signals during lunch hours (low volume)
   - Higher success with ORB and VWAP confluence

---

## Advanced: Customization for Your Strategy

### For Aggressive Traders
- Reduce RSI oversold to 25, overbought to 75
- Decrease volume threshold to 1.2
- Use 3-min or 5-min charts
- Set R:R to 1.5:1

### For Conservative Traders
- Increase volume threshold to 2.0
- Only trade ORB breakouts (disable other signals)
- Use 15-min or 30-min charts
- Set R:R to 3:1
- Wait for multiple confirmations

### For Scalpers
- Use 1-min or 3-min charts
- Reduce ATR multiplier to 1.0
- Set R:R to 1:1 or 1.5:1
- Take quick profits, don't wait for Target 2

---

## Support & Updates

### File Location
- Indicator code: `strategies/intraday_master_indicator.pine`
- This guide: `strategies/INTRADAY_INDICATOR_GUIDE.md`

### Need Help?
- Review TradingView's Pine Script documentation
- Join TradingView community forums
- Test on paper trading first before live trading

### Backtesting
- Use TradingView's strategy tester (requires converting to strategy)
- Test on historical data for your preferred timeframe
- Optimize settings based on your trading instrument

---

## Disclaimer

⚠️ **IMPORTANT**: This indicator is for educational purposes only. Trading involves substantial risk of loss. Past performance does not guarantee future results. Always:

- Paper trade first to understand how it works
- Use proper risk management (1-2% per trade max)
- Never trade with money you can't afford to lose
- Consult with a licensed financial advisor
- Understand that no indicator is 100% accurate

---

## Quick Reference Card

### Signal Types
| Signal | Meaning | Action |
|--------|---------|--------|
| 🟢 Green Triangle | LONG opportunity | Consider buying |
| 🔴 Red Triangle | SHORT opportunity | Consider selling |
| ⚪ Orange Circle | EXIT signal | Close position |

### Dashboard Indicators
| Indicator | Status | Meaning |
|-----------|--------|---------|
| Trend | 🟢 BULLISH | Uptrend - favor longs |
| Trend | 🔴 BEARISH | Downtrend - favor shorts |
| RSI | <30 | Oversold - potential bounce |
| RSI | >70 | Overbought - potential reversal |
| Volume | 🔥 SPIKE | Strong move - high conviction |
| VWAP | 🟢 ABOVE | Bullish bias |
| VWAP | 🔴 BELOW | Bearish bias |

### Chart Elements
- **Blue line**: VWAP (average price)
- **Green lines**: ORB high, VWAP upper bands
- **Red lines**: ORB low, VWAP lower bands
- **Yellow line**: Fast EMA (9)
- **Orange line**: Slow EMA (21)
- **White cross**: Entry price
- **Red circles**: Stop loss
- **Green circles**: Targets

---
**Good luck with your trading! Trade safe and stick to your risk management plan.** 🚀
