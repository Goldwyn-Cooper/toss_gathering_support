import warnings
warnings.filterwarnings('ignore')
import yfinance as yf
import pandas as pd

class Finance:
    def __init__(self) -> None:
        self.fibo = self.get_fibo(13)

    @staticmethod    
    def get_fibo(n: int) -> list:
        fibo = [0] * max(n+1, 3)
        fibo[1] = 1
        fibo[2] = 1
        for i in range(3, n+1):
            fibo[i] = fibo[i-1] + fibo[i-2]
        return fibo[3:]

    @staticmethod
    def fetch_history(symbol: str) -> pd.DataFrame:
        data = yf.Ticker(symbol).history(period='1y')
        return data

    def update_momentum(self, symbol: str):
        price = self.fetch_history(symbol).Close
        momentum = []
        cal_momentum = lambda f:\
            lambda x: (x.iloc[-1] / x.iloc[0] - 1) / f
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