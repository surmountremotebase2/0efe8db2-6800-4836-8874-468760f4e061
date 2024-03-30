from surmount.base_class import Strategy, TargetAllocation#trading view 

from surmount.technical_indicators import EMA, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Example with Apple, can be modified
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        # The data interval; "1day" for daily data, can be adjusted based on need
        return "1day"  
    
    def run(self, data):
        # Define allocation dictionary
        allocation_dict = {ticker: 0 for ticker in self.tickers}  
        for ticker in self.tickers:
            # Calculating MACD and Signal Line
            macd_data = MACD(ticker=ticker, data=data["ohlcv"], fast=12, slow=26)
            # Short EMA term (12-day period by default)
            ema12 = EMA(ticker=ticker, data=data["ohlcv"], length=12)
            # Long EMA term (26-day period by default)
            ema26 = EMA(ticker=ticker, data=data["ohlcv"], length=26)
            
            if not all([macd_data, ema12, ema26]):
                log(f"Insufficient data for {ticker}")
                continue
            
            # Extract MACD and Signal values for the latest data points
            macd = macd_data['MACD'][-1]
            signal = macd_data['signal'][-1]
            
            # Buy Signal - MACD crosses above Signal line and short EMA is above long EMA
            if macd > signal and ema12[-1] > ema26[-1]:
                allocation_dict[ticker] = 1.0  # Assign full investment to this ticker
                log(f"Buy signal for {ticker}")
            
            # Sell Signal - MACD crosses below Signal line
            elif macd < signal:
                allocation_dict[ticker] = 0.0  # Move to cash for this ticker
                log(f"Sell signal for {ticker}")
            
            # No action, just log the status
            else:
                log(f"No action for {ticker}. MACD: {macd}, Signal: {signal}")

        # Create and return target allocation based on the signals
        return TargetAllocation(allocation_dict)