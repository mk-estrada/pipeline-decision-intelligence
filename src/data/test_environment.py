#For clean setup, repo heartbeat

import pandas as pd
import numpy as np

def main():
    print("Environment check passed.")
    print(f"Pandas version: {pd.__version__}")
    print(f"NumPy version: {np.__version__}")

if __name__ == "__main__":
    main()