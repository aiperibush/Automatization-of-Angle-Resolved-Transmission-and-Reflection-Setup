import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv("test1.csv")

sns.set_theme(context="paper", style="ticks", palette="viridis")

ax=sns.scatterplot(data=df, x="Wavelength (nm)", y="Power (mW)", palette="turbo", hue="Wavelength (nm)")

plt.title("Visible Light Power Per Wavelength")

plt.legend([],[], frameon=False)

plt.show()