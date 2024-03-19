import warnings
warnings.filterwarnings('ignore')
import yfinance as yf
import pandas as pd

class Finance:
    @staticmethod
    def gen_fibo(limit: int = 200):
        a = b = 1
        while True:
            a, b = b, a + b
            if b >= limit:
                return
            yield b

    def __init__(self):
        self.fibo = list(self.gen_fibo(60))

    @staticmethod
    def fetch_history(symbol: str) -> pd.DataFrame:
        data = yf.Ticker(symbol).history(period='1y')
        return data

    def update_momentum(self, symbol: str):
        price = self.fetch_history(symbol).Close
        momentum = []
        cal_momentum = lambda f:\
            lambda x: (x.iloc[-1] / x.iloc[0] - 1)
        for f in self.fibo:
            m = price.rolling(f)\
                .apply(cal_momentum(f))\
                .iloc[-1]
            if not pd.isna(m):
                momentum.append(m)
        score = sum(momentum) / len(momentum) * 252
        return score

if __name__ == "__main__":
    finance = Finance()
    print(finance.fetch_history('TQQQ').tail())
    print(finance.update_momentum('TQQQ'))