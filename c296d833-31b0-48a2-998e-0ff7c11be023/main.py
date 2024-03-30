from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        # Specify the assets the strategy will operate on
        return ["AAPL"]

    @property
    def interval(self):
        # Define the time interval for data points, e.g., daily
        return "1day"

    def run(self, data):
        # Initialize the allocation with no position
        allocation = {"AAPL": 0}
        # Check if we have enough data points to compute RSI
        if len(data["ohlcv"]) > 14:
            # Calculate the 14-period RSI for AAPL
            rsi_values = RSI("AAPL", data["ohlcv"], 14)
            # Get the most recent RSI value
            recent_rsi = rsi_values[-1]
            log(f"Recent RSI: {recent_rsi}")
            # RSI below 30 indicates oversold, thus a buy signal
            if recent_rsi < 30:
                log("Buy signal")
                allocation["AAPL"] = 1  # Full allocation to buy
            # RSI above 70 indicates overbought, thus a sell signal
            elif recent_rsi > 70:
                log("Sell signal")
                allocation["AAPL"] = 0  # No allocation, equivalent to selling
            else:
                log("No clear buy or sell signal")
        else:
            log("Not enough data to compute RSI")

        return TargetAllocation(allocation)