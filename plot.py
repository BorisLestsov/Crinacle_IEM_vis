import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
sns.set()

log_plot = False

d = {}
m = {'A+':13, 'A-':11, 'A=':12, 'B+':10, 'B-':8, 'B=':9, 'C+':7, 'C-':5, 'C=':6, 'D+':4, 'D-':2, 'D=':3, 'E=':1, 'F=':0, 'S-':14, 'S=':15}
colors = [
        'ff0000',
        'cc4125',
        'ff9900',
        'd78100',
        '9c5d00',
        '00d900',
        '00ae00',
        '008800',
        '0000ff',
        '0000b9',
        '00006d',
        '9900ff',
        '7300c1',
        '3d0067',
        'ff00ff',
        '000000',
        ]

def hex2rgb(h):
    return list(float(int(h[i:i+2], 16))/255 for i in (0, 2, 4))

colors = list(map(hex2rgb, colors))[::-1]
print(colors)

with open("raw.txt", 'r') as f:
    for i, line in enumerate(f):
        line = line.split('\t')
        line[2] = int(line[2]) if line[2] != '' else np.nan
        line = [m[line[0]]] + line
        d[i] = line
    d[i] = line + ['\n']

df = pd.DataFrame.from_dict(d, orient='index')
df.columns = ['IntRank', 'Rank', 'Model', 'Price', 'Signature', 'Comments', 'Setup', 'Based on', 'SHR']
print(df.dtypes)
sns.set(style='darkgrid')

# df.to_csv('crinacle.csv')

m_inv = {v:k for k,v in m.items()}
f, axs = plt.subplots(figsize=(8, 6))
f = sns.boxplot(x='Rank', y='Price', data=df, order=[m_inv[i] for i in range(len(m))], whis=0.8, palette=colors)

if log_plot:
    f.set_yscale('log')
    f.set_ylim(5, 10000)
    yticks=np.array([10**i for i in range(1, 5)])
    f.set_yticks(yticks)
    f.set_yticklabels(yticks)
else:
    f.set_ylim(5, 5000)
    f.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    f.yaxis.set_tick_params(which='minor')

sns.set(rc={"xtick.bottom" : True, "ytick.left" : True})
f.yaxis.set_tick_params(which='minor', labelsize=5)
f.xaxis.set_tick_params(which='major', labelsize=15, color=colors)
[ii.set_color(colors[i]) for i, ii in enumerate(plt.gca().get_xticklabels())]
f.yaxis.set_minor_formatter(ticker.ScalarFormatter())
f.grid(b=True, which='major', color='w', linewidth=1.0)
f.grid(b=True, which='minor', color='w', linewidth=0.3)
f.set_title("Crinacle's IEM ranking")


# colorize box outlines
for i,box_col in enumerate(colors):
    box_col = [c/3 for c in box_col]
    # box_col = (0.25, 0.25, 0.25)
    mybox = f.artists[i]
    mybox.set_edgecolor(box_col)

    # Loop over them here, and use the same colour as above
    for j in range(i*6,i*6+6):
        line = f.lines[j]
        line.set_color(box_col)
        line.set_mfc(box_col)
        line.set_mec(box_col)


# plt.show()
plt.draw()
plt.savefig("out.png", dpi=300)

df.dropna(inplace=True)
print("Corr:", np.corrcoef(df['IntRank'], df['Price']))
