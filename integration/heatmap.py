import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme()

# filename="file.csv"
# df=pd.DataFrame(filename)

flights_long = sns.load_dataset("flights")
flights = flights_long.pivot("month", "year", "passengers")

f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(flights, cmap="mako", linewidths=0, ax=ax)
plt.show()