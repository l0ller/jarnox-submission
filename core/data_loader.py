import os
import pandas as pd


class StockDataLoader:

    @staticmethod
    def load_ohlcv(data_dir: str) -> pd.DataFrame:
        all_dfs = []

        for file in os.listdir(data_dir):
            if not file.endswith(".csv"):
                continue

            path = os.path.join(data_dir, file)
            df = pd.read_csv(path)

            # 🔹 Normalize column names
            df.columns = [c.strip().title() for c in df.columns]

            # 🔹 Required columns check
            required = {"Date", "Open", "High", "Low", "Close", "Volume", "Symbol"}
            if not required.issubset(df.columns):
                continue

            # 🔹 Fix dtypes (CRITICAL)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True).dt.tz_localize(None)

            for col in ["Open", "High", "Low", "Close", "Volume"]:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", "", regex=False)
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df.dropna(subset=["Date", "Open", "High", "Low", "Close"], inplace=True)

            all_dfs.append(df)

        if not all_dfs:
            raise ValueError("❌ No valid OHLCV data found")

        return pd.concat(all_dfs, ignore_index=True)

def main():
    data_dir = "data"
    df = StockDataLoader.load_ohlcv(data_dir)
    print(f"Loaded {len(df)} rows across {df['Symbol'].nunique()} symbols")
    print(df.head())
if __name__ == "__main__":
    main()