import requests
import pandas as pd
import plotly.express as px
import numpy as np
import dash_table
import re
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash
app=dash.Dash(__name__)
with open('India_states.geojson', "r") as read_it:
    geo = json.load(read_it)

r=requests.get("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69",params={'api-key':'579b464db66ec23bdd0000015adf32c2af2647097dac9fa70ff21027',
                                                                                                 "format":'json','offset':0,'limit':6733})
j=r.json()
df=pd.DataFrame(j['records'])
df.dropna(axis=0,inplace=True,how='any')
def regex(x):
    x=re.sub("_",' ',x)
    return x
df['state']=df['state'].apply(lambda x:regex(x))
df=df[df['pollutant_avg']!='NA']
df['pollutant_avg']=list(map(int,df['pollutant_avg']))
df['pollutant_min']=list(map(int,df['pollutant_min']))
df['pollutant_max']=list(map(int,df['pollutant_max']))
for feature in geo['features']:
    i=feature['properties']['ST_NM']
    feature['id']=i
df['state']=df['state'].replace({'Delhi':'NCT of Delhi','TamilNadu':'Tamil Nadu'})
pollutants=['SO2', 'PM10', 'OZONE', 'PM2.5', 'NO2', 'NH3', 'CO']
l=['pollutant_min', 'pollutant_max', 'pollutant_avg']
fig = px.choropleth_mapbox(df, geojson=geo, color="state",
                          locations='state',
                           center={"lat":20.593684 ,"lon":78.96}
                           ,mapbox_style='carto-positron',zoom=2)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
bar=px.bar()
table_df=df[df['city']=='Gandhinagar']
table_df=table_df[table_df['pollutant_id']=='PM2.5'][['city','station','pollutant_avg']]


app.layout=html.Div(
    children=[html.Div(
        children=[dcc.Dropdown(id='pollutant',value="PM2.5",options=[{'label':x,'value':x} for x in pollutants]),
                  dcc.Dropdown(id='min_max',value='pollutant_avg',options=[{'label':x,'value':x}for x in l]),
                  ]),
        dcc.Graph(id='map',figure=fig,style={'float':'left','width':'50%'},hoverData={'points':[{'location':'Gujarat'}]}),
        dcc.Graph(id='bar',figure=bar,style={'float':'right','width':'49%'})
          ])

@app.callback(
    Output('map','figure'),
    [Input('pollutant','value'),Input('min_max','value')]
)
def fun(p,col):
    data=df[df['pollutant_id']==p]
    data=data.groupby('state')[col].agg(np.mean).reset_index()
    data.columns=['state',p+col]
    fig=px.choropleth_mapbox(data,geojson=geo,locations='state',color=p+col,
                             center={"lat": 20.593, "lon": 78.96}
                             ,mapbox_style='carto-positron',zoom=3
                             )
    return fig
@app.callback(Output('bar','figure'),[
    Input('map','hoverData'),Input('pollutant','value'),Input('min_max','value')
])
def fun2(f,p,col):
    data=df[df['state']==f['points'][0]['location']]
    data=data[data['pollutant_id']==p]
    table=data
    table = table[['city', 'station', 'pollutant_avg']]
    table=table.to_dict('records')
    data=data.groupby('city')[col].agg(np.mean).reset_index()
    fig=px.bar(data,x='city',y=col)
    return fig


if __name__=="__main__":
    app.run_server(debug=True)
