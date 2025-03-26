#%%
import pandas as pd
import plotly.express as px
# %%
df = pd.read_excel('exportação.xlsx', dtype={'CNPJ':str})
df['LATITUDE'] = df['LATITUDE'].astype(str).apply(lambda x: float(str(x).split(':')[0]) - float(str(x).split(':')[1])/60 - float(str(x).split(':')[2].replace(',','.'))/3600  if len(str(x))>5 else 0)
df['LONGITUDE'] = df['LONGITUDE'].astype(str).apply(lambda x: float(str(x).split(':')[0]) - float(str(x).split(':')[1])/60 - float(str(x).split(':')[2].replace(',','.'))/3600  if len(str(x))>5 else 0)
# %%
def filtra(cnpj='00071508000180'):
    return "<br>"+"<br>".join([" ".join(list(str(y) for y in x)) for x in list(df[df['CNPJ'] == cnpj][['Produto','Tancagem (m³)','Qtde de Bico']].values)])
filtra()

#%%
def waz(cnpj='00071508000180'):
    lat = df[df['CNPJ'] == cnpj]['LATITUDE'].min()
    lon = df[df['CNPJ'] == cnpj]['LONGITUDE'].min()
    return f"<a href='https://www.waze.com/ul?ll={lat},{lon}&navigate=yes&zoom=17'>waze</a>"
waz()

# %%
cnpj_prime = pd.read_excel('exportação_com_prime.xlsx', dtype={'CNPJ':str})['CNPJ'].to_list()
# %%
df2 = df[['Razão Social','CNPJ','Vinculação a Distribuidor','LATITUDE','LONGITUDE','MUNICÍPIO','BAIRRO','Endereço']].drop_duplicates()
df2 = df2[df2['LATITUDE']<0]
df2['prime'] = df2['CNPJ'].apply(lambda x: "sim" if x in cnpj_prime else "não")
df2['combs'] = df2['CNPJ'].apply(filtra)
df2['waze'] = df2['CNPJ'].apply(waz)
df2
#%%

px.scatter_mapbox(data_frame=df2, lat='LATITUDE', lon='LONGITUDE', title="Localização dos Postos", color='prime', width=800, height=600, hover_data=['CNPJ','Razão Social','prime','combs','waze'], mapbox_style='open-street-map').show()

# %%
fig = px.scatter_mapbox(data_frame=df2,  animation_frame='prime', title="Localização dos Postos", lat='LATITUDE', lon='LONGITUDE', color='Vinculação a Distribuidor', width=800, height=600, hover_data=['CNPJ','Razão Social','MUNICÍPIO','BAIRRO','Endereço','waze','prime','combs'], mapbox_style='open-street-map')
fig.update_layout(
    title_x=0.5,
    title_y=0.95,
    legend=dict(x = 0,y = 0, orientation = 'v'),
    margin={"l": 10, "r": 10, "b": 10, "t": 50}
)
fig.show()

# %%

fig.write_html('postos_prime.html')

# %%
