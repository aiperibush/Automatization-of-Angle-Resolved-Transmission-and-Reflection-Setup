import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


fig,ax=plt.subplots(figsize=(6,6))
df=pd.read_csv("samplex1y1.csv")
df.insert(0, "Angles", range(-60,60,1))
df = df.rename(columns={'Unnamed: 0': 'Angles'})
df=df.set_index("Angles")
ax=sns.heatmap(df, cmap="mako", linewidths=0) #, xticklabels=True, yticklabels=True)
ax.set(xlim=(300,850))
ax.set(ylim=(95,0))

ax.xaxis.set_tick_params(which='both', direction='out', length=1)
ax.yaxis.set_tick_params(which='both', direction='out', length=1)
ax.locator_params(axis='x', nbins=10)
ax.locator_params(axis='y', nbins=10)

plt.savefig("samplex1y1.png")
plt.show()
