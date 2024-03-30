from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = []
        
    @property
    def interval(self):
        # Defines the data interval for analysis; "1day" for daily data.
        return "1day"

    @property
    def assets(self):
        # Asset(s) this strategy will analyze; here, it's "AAPL".
        return self.tickers

    @property
    def data(self):
        # Defines additional data required by the strategy, if any.
        return self.data_list

    def run(self, data):
        # The core logic of the trading strategy.
        
        # Initialize allocation with zero for conservative approach
        allocation_dict = {"AAPL": 0}
        
        # Generate MACD signals for "AAPL" using the MACD technical indicator.
        macd_data = MACD("AAPL", data["ohlcv"], fast=12, slow=26)
        
        if macd_data is not None:
            macd_line = macd_data['MACD']
            signal_line = macd_data['signal']
            
            if len(macd_line) > 0 and len(signal_line) > 0:
                # Check the latest MACD and Signal line values to decide the position.
                if macd_line[-1] > signal_line[-1]:
                    # MACD line crosses above the signal line - bullish signal.
                    log("MACD bullish crossover detected, buying AAPL.")
                    allocation_dict["AAPL"] = 0.5  # Allocate 50% to "AAPL"
                elif macd_line[-1] < signal_line[-1]:
                    # MACD line crosses below the signal line - bearish signal.
                    log("MACD bearish crossover detected, selling AAPL.")
                    allocation_dict["AAPL"] = 0  # Reduce allocation to "AAPL" to 0%
        
        return TargetAllocation(allocation_dict)