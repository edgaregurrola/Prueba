import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

df = pd.read_csv('../data/data-science-proyecto2-master/synergy_logistics_database.csv')

df_op1 = df.groupby(['destination']).count().sort_values(
    'register_id', ascending=False)[['direction']]
df_op1 = df_op1.reset_index().rename(columns={
    'destination':'Paises destino','direction':'Total de impotaciones y exportaciones'})
df_op1.iloc[0:10].to_csv('../outputs/Opcion_1.csv')

plt.figure(figsize=(10,5))
ax = sns.barplot(x= df_op1['Paises destino'],
           y=df_op1['Total de impotaciones y exportaciones'])

ax.set_xticklabels(ax.get_xticklabels(), rotation=50, ha="right")

ax.set_ylabel('Exportaciones e Importaciones')
ax.set_xlabel('Paises')

plt.tight_layout()

plt.savefig('../outputs/Opcion_1.png')


df_op2 = df.groupby(['transport_mode']).sum().sort_values(
    'total_value', ascending=False).reset_index()
df_op2 = df_op2[['transport_mode','total_value']].rename(columns={
    'transport_mode':'Tipo de transporte','total_value':'Valor total ($)'})
df_op2.to_csv('../outputs/Opcion_2.csv')

plt.figure(figsize=(5,5))
ax = sns.barplot(x=df_op2['Tipo de transporte'],
           y=df_op2['Valor total ($)'])

ax.set_xticklabels(ax.get_xticklabels(), rotation=50, ha="right")

plt.tight_layout()

plt.savefig('../outputs/Opcion_2.png')


df_op3 = df.groupby(['origin']).sum().sort_values(
    'total_value', ascending=False).reset_index().copy()
df_op3['pct'] = 100*df_op3['total_value'].cumsum() / sum(df_op3['total_value'])
df_op3 = df_op3[['origin','total_value','pct']].rename(columns={'origin':'Paises',
                                                                         'total_value':'Valor total ($)',
                                                                         'pct':'Porcentaje acumulado'})
df_op3.loc[df_op3['Porcentaje acumulado']<=80].to_csv('../outputs/Opcion_3.csv')

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=df_op3['Paises'],y=df_op3["Valor total ($)"], ax=ax)

ax.set_xticklabels(ax.get_xticklabels(), rotation=50, ha="right")

ax2 = ax.twinx()
ax2.plot(df_op3['Paises'], df_op3["Porcentaje acumulado"], color='grey', marker=".", ms=7)
ax2.yaxis.set_major_formatter(PercentFormatter())

plt.savefig('../outputs/Opcion3.png')
