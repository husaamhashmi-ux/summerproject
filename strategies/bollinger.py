import backtrader as bt

class BollingerBandsStrategy(bt.Strategy):
    params = (
        ('period', 20),  # Bollinger Bands lookback period
        ('devfactor', 3),  # Standard deviation multiplier
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(
            self.data.close,
            period=self.params.period,
            devfactor=self.params.devfactor
        )
        self.order = None

    def next(self):
        # Block overlapping orders
        if self.order:
            return

        current_price = self.data.close[0]

        # No position
        if not self.position:
            # Oversold -> Buy
            if current_price < self.bb.lines.bot[0]:
                self.order = self.buy()

            # Overbought -> Sell
            elif current_price > self.bb.lines.top[0]:
                self.order = self.sell()

        # Existing long position
        elif self.position.size > 0:
            # Exit long
            if current_price > self.bb.lines.top[0]:
                self.order = self.close()

        # Existing short position
        elif self.position.size < 0:
            # Exit short
            if current_price < self.bb.lines.bot[0]:
                self.order = self.close()

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
