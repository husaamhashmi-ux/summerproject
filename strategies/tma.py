import backtrader as bt

class TripleMovingAverageStrategy(bt.Strategy):
    params = (
        ('short_period', 10),
        ('medium_period', 50),
        ('long_period', 100),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.short_period
        )

        self.medium_ma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.medium_period
        )

        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.long_period
        )
        self.order = None    

    def next(self):
        # Check if an entry order is pending
        if self.order:
            return

        # Entry Logic
        if not self.position:
            # Long entry
            if self.short_ma[0] > self.medium_ma[0] and self.medium_ma[0] > self.long_ma[0]:
                self.order = self.buy()

            # Short entry
            elif self.short_ma[0] < self.medium_ma[0] and self.medium_ma[0] < self.long_ma[0]:
                self.order = self.sell()

        # Exit Logic (Trailing Stop)
        else:
            if self.position.size > 0:
                self.sell(exectype=bt.Order.StopTrail, trailpercent=0.02)
            elif self.position.size < 0:
                self.buy(exectype=bt.Order.StopTrail, trailpercent=0.02)

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
