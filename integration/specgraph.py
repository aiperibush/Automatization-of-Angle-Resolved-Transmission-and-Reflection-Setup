import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

fig,ax=plt.subplots(figsize=(6,6))
df=pd.read_csv("test.csv")
df = df.rename(columns={'Unnamed: 0': 'Angles'})
df=df.set_index("Angles")
print(df)
ax=sns.heatmap(df, cmap="mako", linewidths=0) #, xticklabels=True, yticklabels=True)
# ax.set_ylim(0,100)

ax.xaxis.set_major_locator(ax.MaxNLocator(4))
# for index, label in enumerate(ax.get_xticklabels()):
#     if index%4==0:
#         label.set_visible(True)
#     else:
#         label.set_visible(False)
# ax.set_xticklabels(df.columns)
plt.show()