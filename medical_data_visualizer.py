import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['overweight'] = (df['Weight'] / ((df['Height'] / 100) ** 2))
df['overweight'] = df['overweight'].apply(lambda x: 1 if x > 25 else 0)

# 3
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
                     var_name='variable', value_name='value')
    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().to_frame('total').reset_index()
    
    # 7
    g = sns.catplot(data=df_cat, x='variable', y='total', hue='value', col='cardio', kind='bar')
    
    # 8
    fig = g.fig
    
    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975)) &
                 (df['ap_lo'] <= df['ap_hi'])]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(corr)

    # 14
    fig, ax = plt.subplots(figsize=(10, 8))

    # 15
    sns.heatmap(corr, annot=True, fmt='.1f', cmap='coolwarm', mask=mask, linewidths=0.5, square=True, ax=ax)

    # 16
    fig.savefig('heatmap.png')
    return fig

# 17
draw_cat_plot()

# 18
draw_heat_map()
