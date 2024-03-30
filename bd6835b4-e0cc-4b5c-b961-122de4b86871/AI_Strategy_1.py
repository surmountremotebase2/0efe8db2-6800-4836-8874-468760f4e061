from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Define thresholds
        rsi_overbought = 70
        rsi_oversold = 30

        # Get the latest MACD and RSI values
        macd_data = MACD(self.ticker, data["ohlcv"], fast=12, slow=26)
        rsi_data = RSI(self.ticker, data["ohlcv"], length=14)
        
        # Initialize the allocation dictionary with no allocation
        allocation_dict = {self.ticker: 0}

        if macd_data is not None and rsi_data is not None and len(macd_data['MACD']) > 1:
            # Get the latest and second latest MACD and signal line values
            latest_macd = macd_data['MACD'][-1]
            prev_macd = macd_data['MACD'][-2]
            latest_signal = macd_data['signal'][-1]
            prev_signal = macd_data['signal'][-2]

            # Get the latest RSI value
            latest_rsi = rsi_data[-1]

            # Check for MACD crossover and RSI conditions
            if latest_macd > latest_signal and prev_macd <= prev_signal and latest_rsi < rsi_overbought:
                # Buy signal: MACD crosses above the signal line, and RSI not overbought
                allocation_dict[self.ticker] = 1
            elif (latest_macd < latest_signal and prev_macd >= prev_signal) or latest_rsi > rsi_overbought:
                # Sell/avoid signal: MACD crosses below the signal line, or RSI overbought
                allocation_dict[self.ticker] = 0

        return TargetAllocation(allocation_dict)