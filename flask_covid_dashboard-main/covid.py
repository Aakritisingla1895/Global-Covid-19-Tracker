import pandas as pd
import numpy as np
import dateutil
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data
from plotly.subplots import make_subplots
import plotly.express as px
import json

#only in jupyter notebook need plotly offline mode
#I still got some error when using Jupyterlab
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode(connected=True)

#loading data
total_confirmed=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
#Replace US with United States
total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)
total_death=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',encoding='utf-8',na_values=None)
total_death.replace(to_replace='US', value='United States', regex=True, inplace=True)
total_recovered=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',encoding='utf-8',na_values=None)
total_recovered.replace(to_replace='US', value='United States', regex=True, inplace=True) 
print (total_confirmed)

#grouped total confirmed data
grouped_total_confirmed = total_confirmed[["Country/Region",total_confirmed.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_confirmed.columns[-1], ascending=False)
grouped_total_confirmed.reset_index(inplace=True)
grouped_total_confirmed.columns=["Country/Region", 'confirmed']
grouped_total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)

#Chart.js can't plot dataframe object, so we need to change some to list
barplot_confirmed_values=grouped_total_confirmed["confirmed"].values.tolist()
country_names=grouped_total_confirmed["Country/Region"].values.tolist()
print (grouped_total_confirmed)

#global time series confirmed data frame
global_confirmed_timeseries = pd.DataFrame(total_confirmed[total_confirmed.columns[4:]].sum())
global_confirmed_timeseries.reset_index(inplace=True)
global_confirmed_timeseries.columns= ['date', 'total confirmed']

#global daily new cases = global daily confirmed at date (t) -  global daily confirmed at date (t-1)
global_confirmed_timeseries["daily new cases"] = global_confirmed_timeseries['total confirmed'] - global_confirmed_timeseries['total confirmed'].shift()
global_confirmed_timeseries=global_confirmed_timeseries.fillna(0)
print (global_confirmed_timeseries)



#grouped total recovered data
grouped_total_recovered = total_recovered[["Country/Region",total_recovered.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_recovered.columns[-1], ascending=False)
grouped_total_recovered.reset_index(inplace=True)
grouped_total_recovered.columns=["Country/Region", 'recovered']
grouped_total_recovered.replace(to_replace='US', value='United States', regex=True, inplace=True)

#Chart.js can't plot dataframe object, so we need to change some to list
barplot_recovered_values=grouped_total_recovered["recovered"].values.tolist()
country_names=grouped_total_confirmed["Country/Region"].values.tolist()
print (grouped_total_recovered)

#global time series recovered data frame
global_recovered_timeseries = pd.DataFrame(total_recovered[total_recovered.columns[4:]].sum())
global_recovered_timeseries.reset_index(inplace=True)
global_recovered_timeseries.columns= ['date', 'total recovered']

#global daily recovered = global daily recovered at date (t) -  global daily recovered at date (t-1)
global_recovered_timeseries["daily new recovered"] = global_recovered_timeseries['total recovered'] - global_recovered_timeseries['total recovered'].shift()
global_recovered_timeseries=global_recovered_timeseries.fillna(0)
print (global_recovered_timeseries)

# grouping the data by each country to get total confirmed cases
grouped_total_death = total_death[["Country/Region",total_death.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_death.columns[-1], ascending=False)
grouped_total_death.reset_index(inplace=True)
grouped_total_death.columns=["Country/Region", 'deaths']
grouped_total_death.replace(to_replace='US', value='United States', regex=True, inplace=True)

#Chart.js can't plot dataframe object, so we need to change some to list
barplot_death_values=grouped_total_death["deaths"].values.tolist()
global_death_timeseries = total_death[total_death.columns[4:]].sum()


#global time series death data frame
global_death_timeseries = pd.DataFrame(total_death[total_death.columns[4:]].sum())
global_death_timeseries.reset_index(inplace=True)
global_death_timeseries.columns= ['date', 'total deaths']

#global daily deaths = global daily deaths at date (t) -  global daily deaths at date (t-1)
global_death_timeseries["daily new deaths"] = global_death_timeseries['total deaths'] - global_death_timeseries['total deaths'].shift()
global_death_timeseries=global_death_timeseries.fillna(0)
print (global_death_timeseries)


#merge all the data to get full time series dataframe
timeseries_final=pd.merge(global_confirmed_timeseries,global_recovered_timeseries,how='inner',on='date')
timeseries_final = pd.merge(timeseries_final,global_death_timeseries,how='inner',on='date')
print (timeseries_final)

# total confirmed cases globally
total_confirmed[total_confirmed.columns[-1]].sum()
# total recovered cases globally
total_recovered[total_recovered.columns[-1]].sum()


total_death[total_death.columns[-1]].sum()
# I need data that contain population for each country to calculate confirmed cases/population
# I download it from : https://github.com/samayo/country-json/blob/master/src/country-by-population.json
df_pop = pd.read_json('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')
print (df_pop)

#some country name has different  format, so I need to change it to match my first dataset
df_pop.columns=['Country/Region','population']
df_pop=df_pop.replace(to_replace='Russian Federation', value='Russia')

# I also need country code for geographical analysis, Altair need numerical code and Plotly need alfabetical code
#country code and id for later geographical analysis
url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
country_code = pd.read_csv(url)
country_code = country_code[["English short name","Alpha-3 code","Numeric"]]
country_code.columns=["Country/Region", "code3", "id"]

#Change the data for later merging
#If not match the value will be deleted, so we need to make sure each country name from each table has same value
country_code=country_code.replace(to_replace='Russian Federation (the)', value='Russia')
country_code=country_code.replace(to_replace='United Kingdom (the)', value='United Kingdom')
country_code=country_code.replace(to_replace='United States (the)', value='United States')
country_code=country_code.replace(to_replace='Viet Nam', value='Vietnam')
print (country_code)


# merge them all
final_df=pd.merge(grouped_total_confirmed,grouped_total_recovered,how='inner',on='Country/Region')
final_df=pd.merge(final_df,grouped_total_death,how='inner',on='Country/Region')
final_df=pd.merge(final_df,df_pop,how='inner',on='Country/Region')
final_df=pd.merge(country_code,final_df,how='inner',on='Country/Region')
final_df = final_df.sort_values(by="confirmed", ascending=False)
final_df.reset_index(inplace=True, drop=True)
final_df.to_json("new_map.json")
#print (final_df)

# calculate cases/million and total death rate
final_df['cases/million'] = ((final_df['confirmed']/final_df['population'])*1000000).round(2)
final_df['death rate(%)'] = ((final_df['deaths']/final_df['confirmed'])*100).round(2)
print (final_df)



country = "Indonesia"
total_all_confirmed = total_confirmed.groupby("Country/Region").sum()
total_all_confirmed.reset_index(inplace=True)
mask = (total_all_confirmed['Country/Region'] == country) 
total_all_confirmed=total_all_confirmed.loc[mask]
total_all_confirmed = total_all_confirmed[total_all_confirmed.columns[-1]].sum()
print (total_all_confirmed)


# function to filter timeseries analysis by country
# I use "case" variable just for column name: e.g, case = confirmed, case = deaths
def get_by_country(df, country, case):
    mask = (df['Country/Region'] == country) 
    df = df.loc[mask]
    df_country = df.groupby("Country/Region").sum()
    df_country = pd.DataFrame(df[df.columns[4:]].sum())
    df_country.reset_index(inplace=True)
    df_country.columns=['date', f"value_{case}"]
    df_country[f"daily_new_{case}"] = df_country[f"value_{case}"] - df_country[f"value_{case}"].shift()
    df_country=df_country.fillna(0)
    return df_country


#use function above to get merged dataframe
def get_by_country_merged(total_confirmed, total_death, total_recovered, country):
    #apply to each timeseries
    country_confirmed_tseries = get_by_country(total_confirmed, country, "confirmed" )
    country_death_tseries = get_by_country(total_death, country, "death" )
    country_recovered_tseries = get_by_country(total_recovered, country, "recovered" )
    
    #merge them all
    country_timeseries_final=pd.merge(country_confirmed_tseries,country_death_tseries,how='inner',on='date')
    country_timeseries_final = pd.merge(country_timeseries_final,country_recovered_tseries,how='inner',on='date')
    country_timeseries_final.reset_index(inplace=True)
    return country_timeseries_final

#example for China:
country_tseries = get_by_country(total_confirmed, "China", "confirmed")
# it will give me total confirmed cases per day in US, also I can use this for total_deaths and total_recovered too
print (country_tseries)

#example merged for US:
US_ts = get_by_country_merged(total_confirmed, total_death, total_recovered, "China")
print (US_ts)

# ref : https://www.highcharts.com/demo/maps/tooltip
chartjs_ccode = pd.read_json("https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json")
print (chartjs_ccode)


#dump it to external json_file
import json
chartjs_map = final_df[["code3", "Country/Region", "confirmed" ]]
chartjs_map.columns = ["code3", "name", "value"]
chart_json = chartjs_map.to_dict('records')

with open('chart_js.json', 'w') as fout:
    json.dump(chart_json, fout)

print (chart_json)

# Plot Altair 1: Per country total cases and cases/million populations

source = final_df

#base configuration
base = alt.Chart(source).encode(
        alt.X('Country/Region:N',sort=None), tooltip=['Country/Region', 'confirmed', 'cases/million']
).properties( height = 500,
        title='Total Confirmed Cases/Country'
)

#base title configuration

#bar chart
bar = base.mark_bar(color='#5276A7').encode(
    alt.Y('confirmed:Q', axis=alt.Axis(titleColor='#5276A7'))
)
#point for cases/million and its axis
point = base.mark_circle(size=60, color='red').encode(
    alt.Y('cases/million:Q', axis=alt.Axis(titleColor='red'))
)
#merge the plot
alt.layer(bar, point).resolve_scale(y='independent')

# Plot Altair 2: Global aggregates confirmed, recovered, and deaths (Im not using this at my webapp, only for example)
source = timeseries_final

base = alt.Chart(source).encode(x='date:T')

line1 =  base.mark_line(color='green').encode(
    y='total confirmed:Q'
)


line2=  base.mark_line(color='blue').encode(
    y='total recovered:Q'
)
line3=  base.mark_line(color='red').encode(
    y='total deaths:Q'
)
(line1 + line2 + line3).properties(width=600)

#Plot Altair 3: Global time series chart for daily new cases (Im not using this at my webapp, only for example)

source = timeseries_final

base = alt.Chart(source).encode(x='date:T')

line=  base.mark_line(color='blue').encode(
    y='daily new cases:Q', tooltip=['yearmonthdate(date)','daily new cases']
).properties(width=600)

#Plot Altair 3: per country time series chart for daily new cases (Im not using this at my webapp, only for example)
#this example using US_ts from previous function

source = US_ts

base = alt.Chart(source).encode(x='date:T')

line=  base.mark_line(color='blue').encode(
    y='daily_new_confirmed:Q', tooltip=['yearmonthdate(date)','daily_new_confirmed']
).properties(width=600)

print (line)


#Plot Altair 4: Global time series chart for daily new cases, recovered, and deaths - version 1 (Im not using this at my webapp)
import altair as alt
from vega_datasets import data

source = timeseries_final

base = alt.Chart(source).encode(x='date:T')
base = alt.Chart(source).encode(
        alt.X('date:T'), tooltip=['yearmonthdate(date)','daily new cases', 'daily new recovered', 'daily new deaths']
)

line1 =  base.mark_line(color='green').encode(
    y='daily new cases:Q'
)

line2=  base.mark_line(color='blue').encode(
    y='daily new recovered:Q'
)
line3=  base.mark_line(color='red').encode(
    y='daily new deaths:Q'
)
chart = (line1 + line2 + line3).properties(width=1000)
print (chart)


#Plot ALtair 5: Global time series chart for daily new cases, recovered, and deaths - version 2 (Im not using this at my webapp)
import altair as alt


data = timeseries_final
base = alt.Chart(data).transform_fold(
    ['daily new cases', 'daily new recovered', 'daily new deaths']
)
line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    color='key:N',
    tooltip=['yearmonthdate(date)','daily new cases', 'daily new recovered', 'daily new deaths']
).properties(width=700)



#Plot Altair 6; Global time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)

import altair as alt
import pandas as pd
import numpy as np


#declare data and initialization
data = timeseries_final

#specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
base = alt.Chart(data).transform_fold(
    ['daily new cases', 'daily new recovered', 'daily new deaths']
)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date'], empty='none')

# The basic line
line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    color='key:N',
    
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = base.mark_point().encode(
    x='date:T',
    opacity=alt.value(0),
    tooltip=[ alt.Tooltip('yearmonthdate(date)', title="Date")]
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'value:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(data).mark_rule(color='gray').encode(
    x='date:T',
    
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=900, height=300, title='Global Time Series'
)

#Plot Altair 6a; per_country time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)
# I use US data
import altair as alt
import pandas as pd
import numpy as np


#declare data and initialization
data = US_ts
#column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

#specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
base = alt.Chart(data).transform_fold(
    ['daily_new_confirmed', 'daily_new_recovered', 'daily_new_death']
)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date'], empty='none')

# The basic line
line = base.mark_line().encode(
    x='date:T',
    y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    color='key:N',
    
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = base.mark_point().encode(
    x='date:T',
    opacity=alt.value(0),
    tooltip=[ alt.Tooltip('yearmonthdate(date)', title="Date")]
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'value:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(data).mark_rule(color='gray').encode(
    x='date:T',
    
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=900, height=300
)

#Plot Altair 7 geographical analysis; ref : https://github.com/altair-viz/altair/issues/2044
import altair as alt
from vega_datasets import data
world_source = final_df

source = alt.topo_feature(data.world_110m.url, "countries")
background = alt.Chart(source).mark_geoshape(fill="white")

foreground = (
    alt.Chart(source)
    .mark_geoshape(stroke="black", strokeWidth=0.15)
    .encode(
        color=alt.Color(
            "confirmed:N", scale=alt.Scale(scheme="redpurple"), legend=None,
        ),
        tooltip=[
            alt.Tooltip("Country/Region:N", title="Country"),
            alt.Tooltip("confirmed:Q", title="confirmed cases"),
        ],
    
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(world_source, "id", ["confirmed", "Country/Region"]),
    )
)

final_map = (
    (background + foreground)
    .configure_view(strokeWidth=0)
    .properties(width=700, height=400)
    .project("naturalEarth1")
)
print (final_map)

#Plotly plot 1: Geographical analysis



df = final_df

fig = go.Figure(data=go.Choropleth(
    locations = df['code3'],
    z = df['cases/million'],
    text = df['Country/Region'],
    colorscale = 'Darkmint',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = '#cases <br>per million populations',
))

fig.update_layout(
    title_text='Covid 19 confirmed cases',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
            CSSE at Johns Hopkins University</a>',
        showarrow = False
    )]
)

fig.show()


# Plotly plot 2: Per country total cases and cases/million populations

df = final_df
#print(df.head())
df.index = df['Country/Region']
fig = go.Figure()
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
  go.Bar(
      x=df.index,
      y=df["confirmed"],
      name="# of confirmed cases",
      marker_color='#39ac39',
      opacity=1
  ),
  secondary_y=False
)

fig.add_trace(
  go.Scatter(
      x=df.index,
      y=df["cases/million"],
      mode="lines",
      name="cases/million",
      marker_color='#b23434',
      opacity=0.7
  ),
  secondary_y=True
)

# Add figure title
fig.update_layout(legend=dict(
  orientation="h",
  yanchor="bottom",
  y=1.02,
  xanchor="right",
  x=0.93),
  title={
  'text': '<span style="font-size: 20px;">Global aggregate cases</span><br><span style="font-size: 10px;">(click and drag)</span>',
  'y': 0.97,
  'x': 0.45,
  'xanchor': 'center',
  'yanchor': 'top'},
  paper_bgcolor="#ffffff",
  plot_bgcolor="#ffffff",
  width=1500, height=700
)


# Set x-axis title
fig.update_xaxes( tickangle=45)

# Set y-axes titles
fig.update_yaxes(title_text="# of confirmed cases",
               secondary_y=False, showgrid=False)
fig.update_yaxes(title_text="cases/millions", tickangle=45 , secondary_y=True, showgrid=False)

#Plotly plot 3: Global time series chart for daily new cases, recovered, and deaths
df = timeseries_final

fig = px.line(df, x='date', y=['daily new cases','daily new recovered', 'daily new deaths'], title='Global daily new cases')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


#Plotly plot 3a per country time series chart for daily new cases, recovered, and deaths
# I use Indonesia data
df = get_by_country_merged(total_confirmed, total_death, total_recovered, "Indonesia")
#column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

fig = px.line(df, x='date', y=['daily_new_confirmed','daily_new_death', 'daily_new_recovered'], title='Indonesia daily new cases')

fig.update_xaxes(rangeslider_visible=True)
fig.show()


#loading data
def load_data():
    
    #loading data
    total_confirmed=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    #Replace US with United States
    total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)
    total_death=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',encoding='utf-8',na_values=None)
    total_death.replace(to_replace='US', value='United States', regex=True, inplace=True)
    total_recovered=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',encoding='utf-8',na_values=None)
    total_recovered.replace(to_replace='US', value='United States', regex=True, inplace=True)
    
    # I need data that contain population for each country to calculate confirmed cases/population
    # I download it from : https://github.com/samayo/country-json/blob/master/src/country-by-population.json
    df_pop = pd.read_json('https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')
    #some country name has different  format, so I need to change it to match my first dataset
    df_pop.columns=['Country/Region','population']
    df_pop=df_pop.replace(to_replace='Russian Federation', value='Russia')
    
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered= total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()
    return total_confirmed, total_death, total_recovered, df_pop, total_all_confirmed, total_all_recovered, total_all_deaths

def preprocessed_data(total_confirmed, total_death, total_recovered):
    #grouped total confirmed data
    grouped_total_confirmed = total_confirmed[["Country/Region",total_confirmed.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_confirmed.columns[-1], ascending=False)
    grouped_total_confirmed.reset_index(inplace=True)
    grouped_total_confirmed.columns=["Country/Region", 'confirmed']
    grouped_total_confirmed.replace(to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_confirmed_values=grouped_total_confirmed["confirmed"].values.tolist()
    country_names=grouped_total_confirmed["Country/Region"].values.tolist()
    

    #global time series confirmed data frame
    global_confirmed_timeseries = pd.DataFrame(total_confirmed[total_confirmed.columns[4:]].sum())
    global_confirmed_timeseries.reset_index(inplace=True)
    global_confirmed_timeseries.columns= ['date', 'total confirmed']

    #global daily new cases = global daily confirmed at date (t) -  global daily confirmed at date (t-1)
    global_confirmed_timeseries["daily new cases"] = global_confirmed_timeseries['total confirmed'] - global_confirmed_timeseries['total confirmed'].shift()
    global_confirmed_timeseries=global_confirmed_timeseries.fillna(0)
    

    #grouped total recovered data
    grouped_total_recovered = total_recovered[["Country/Region",total_recovered.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_recovered.columns[-1], ascending=False)
    grouped_total_recovered.reset_index(inplace=True)
    grouped_total_recovered.columns=["Country/Region", 'recovered']
    grouped_total_recovered.replace(to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_recovered_values=grouped_total_recovered["recovered"].values.tolist()
    country_names=grouped_total_confirmed["Country/Region"].values.tolist()
    

    #global time series recovered data frame
    global_recovered_timeseries = pd.DataFrame(total_recovered[total_recovered.columns[4:]].sum())
    global_recovered_timeseries.reset_index(inplace=True)
    global_recovered_timeseries.columns= ['date', 'total recovered']

    #global daily recovered = global daily recovered at date (t) -  global daily recovered at date (t-1)
    global_recovered_timeseries["daily new recovered"] = global_recovered_timeseries['total recovered'] - global_recovered_timeseries['total recovered'].shift()
    global_recovered_timeseries=global_recovered_timeseries.fillna(0)
    

    # grouping the data by each country to get total confirmed cases
    grouped_total_death = total_death[["Country/Region",total_death.columns[-1]]].groupby("Country/Region").sum().sort_values(by=total_death.columns[-1], ascending=False)
    grouped_total_death.reset_index(inplace=True)
    grouped_total_death.columns=["Country/Region", 'deaths']
    grouped_total_death.replace(to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_death_values=grouped_total_death["deaths"].values.tolist()
    global_death_timeseries = total_death[total_death.columns[4:]].sum()
    
    #global time series death data frame
    global_death_timeseries = pd.DataFrame(total_death[total_death.columns[4:]].sum())
    global_death_timeseries.reset_index(inplace=True)
    global_death_timeseries.columns= ['date', 'total deaths']

    #global daily deaths = global daily deaths at date (t) -  global daily deaths at date (t-1)
    global_death_timeseries["daily new deaths"] = global_death_timeseries['total deaths'] - global_death_timeseries['total deaths'].shift()
    global_death_timeseries=global_death_timeseries.fillna(0)
    global_death_timeseries


    #merge all the data to get full time series dataframe
    timeseries_final=pd.merge(global_confirmed_timeseries,global_recovered_timeseries,how='inner',on='date')
    timeseries_final = pd.merge(timeseries_final,global_death_timeseries,how='inner',on='date')
    timeseries_final
    return grouped_total_confirmed,grouped_total_recovered,grouped_total_death, timeseries_final, country_names


def merge_data(grouped_total_confirmed, grouped_total_recovered, grouped_total_death):
# I also need country code for geographical analysis, Altair need numerical code and Plotly need alfabetical code
    #country code and id for later geographical analysis
    url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
    country_code = pd.read_csv(url)
    country_code = country_code[["English short name","Alpha-3 code","Numeric"]]
    country_code.columns=["Country/Region", "code3", "id"]

    #Change the data for later merging
    #If not match the value will be deleted, so we need to make sure each country name from each table has same value
    country_code=country_code.replace(to_replace='Russian Federation (the)', value='Russia')
    country_code=country_code.replace(to_replace='United Kingdom (the)', value='United Kingdom')
    country_code=country_code.replace(to_replace='United States (the)', value='United States')
    country_code=country_code.replace(to_replace='Viet Nam', value='Vietnam')

    # merge them all
    final_df=pd.merge(grouped_total_confirmed,grouped_total_recovered,how='inner',on='Country/Region')
    final_df=pd.merge(final_df,grouped_total_death,how='inner',on='Country/Region')
    final_df=pd.merge(final_df,df_pop,how='inner',on='Country/Region')
    final_df=pd.merge(country_code2,final_df,how='inner',on='Country/Region')
    final_df = final_df.sort_values(by="confirmed", ascending=False)
    final_df.reset_index(inplace=True, drop=True)

    # calculate cases/million and total death rate
    final_df['cases/million'] = ((final_df['confirmed']/final_df['population'])*1000000).round(2)
    final_df['death rate(%)'] = ((final_df['deaths']/final_df['confirmed'])*100).round(2)

    return final_df



def altair_global_cases_per_country(final_df):
# Plot Altair 1: Per country total cases and cases/million populations

    source = final_df

    #base configuration
    base = alt.Chart(source).encode(
            alt.X('Country/Region:N',sort=None), tooltip=['Country/Region', 'confirmed', 'cases/million']
    )

    #bar chart
    bar = base.mark_bar(color='#5276A7').encode(
        alt.Y('confirmed:Q', axis=alt.Axis(titleColor='#5276A7'))
    )
    #point for cases/million and its axis
    point = base.mark_circle(size=60, color='red').encode(
        alt.Y('cases/million:Q', axis=alt.Axis(titleColor='red'))
    )
    #merge the plot
    chart = alt.layer(bar, point).resolve_scale(y='independent')
    chart_json = chart.to_json()
    return chart_json


def altair_global_time_series(timeseries_final):
    #Plot Altair 6; Global time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)
    #declare data and initialization
    data = timeseries_final

    #specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
    base = alt.Chart(data).transform_fold(
        ['daily new cases', 'daily new recovered', 'daily new deaths']
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # The basic line
    line = base.mark_line().encode(
        x='date:T',
        y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
        color='key:N',

    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = base.mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
        tooltip=[ alt.Tooltip('yearmonthdate(date)', title="Date")]
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(data).mark_rule(color='gray').encode(
        x='date:T',

    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=900, height=300
    )
    chart_json = chart.to_json()
    return chart_json


def  altair_per_country_time_series(total_confirmed, total_death, total_recovered, country_name):
    #Plot Altair 6a; per_country time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)
    # I use US data

    #declare data and initialization
    data = get_by_country_merged(total_confirmed, total_death, total_recovered, country_name)
    #column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

    #specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
    base = alt.Chart(data).transform_fold(
        ['daily_new_confirmed', 'daily_new_recovered', 'daily_new_death']
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # The basic line
    line = base.mark_line().encode(
        x='date:T',
        y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
        color='key:N',

    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = base.mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
        tooltip=[ alt.Tooltip('yearmonthdate(date)', title="Date")]
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(data).mark_rule(color='gray').encode(
        x='date:T',

    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=900, height=300
    )
    chart
    chart_json = chart.to_json()
    return chart_json

#Plot Altair 7 geographical analysis; ref : https://github.com/altair-viz/altair/issues/2044
def altair_geo_analysis(final_df):
    world_source = final_df

    source = alt.topo_feature(data.world_110m.url, "countries")
    background = alt.Chart(source).mark_geoshape(fill="white")

    foreground = (
        alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "confirmed:N", scale=alt.Scale(scheme="redpurple"), legend=None,
            ),
            tooltip=[
                alt.Tooltip("Country/Region:N", title="Country"),
                alt.Tooltip("confirmed:Q", title="confirmed cases"),
            ],

        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(world_source, "id", ["confirmed", "Country/Region"]),
        )
    )

    final_map = (
        (background + foreground)
        .configure_view(strokeWidth=0)
        .properties(width=700, height=400)
        .project("naturalEarth1")
    )
    final_map_json = final_map.to_json()
    return final_map_json

#Plotly plot 1: Geographical analysis

def plotly_geo_analysis(final_df):
    df = final_df

    fig = go.Figure(data=go.Choropleth(
        locations = df['code3'],
        z = df['cases/million'],
        text = df['Country/Region'],
        colorscale = 'Darkmint',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = '#cases <br>per million populations',
    ))

    fig.update_layout(
        title_text='Covid 19 confirmed cases',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
                CSSE at Johns Hopkins University</a>',
            showarrow = False
        )]
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def global_cases_per_country(final_df):
# Plotly plot 2: Per country total cases and cases/million populations

    df = final_df
    #print(df.head())
    df.index = df['Country/Region']
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
      go.Bar(
          x=df.index,
          y=df["confirmed"],
          name="# of confirmed cases",
          marker_color='#39ac39',
          opacity=1
      ),
      secondary_y=False
    )

    fig.add_trace(
      go.Scatter(
          x=df.index,
          y=df["cases/million"],
          mode="lines",
          name="cases/million",
          marker_color='#b23434',
          opacity=0.7
      ),
      secondary_y=True
    )

    # Add figure title
    fig.update_layout(legend=dict(
      orientation="h",
      yanchor="bottom",
      y=1.02,
      xanchor="right",
      x=0.93),
      title={
      'text': '<span style="font-size: 20px;">Global aggregate cases</span><br><span style="font-size: 10px;">(click and drag)</span>',
      'y': 0.97,
      'x': 0.45,
      'xanchor': 'center',
      'yanchor': 'top'},
      paper_bgcolor="#ffffff",
      plot_bgcolor="#ffffff",
      width=1500, height=700
    )


    # Set x-axis title
    fig.update_xaxes( tickangle=45)

    # Set y-axes titles
    fig.update_yaxes(title_text="# of confirmed cases",
                   secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="cases/millions", tickangle=45 , secondary_y=True, showgrid=False)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def plotly_global_timeseries(timeseries_final):
    #Plotly plot 3: Global time series chart for daily new cases, recovered, and deaths
    df = timeseries_final
    #notice that I use plotly express (px) not graph_objects as before, just for more variances
    fig = px.line(df, x='date', y=['daily new cases','daily new recovered', 'daily new deaths'], title='Global daily new cases')

    fig = fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(width=1500, height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

def plotly_per_country_time_series(total_confirmed, total_death, total_recovered, country_name):
    #Plotly plot 3a per country time series chart for daily new cases, recovered, and deaths
    # I use Indonesia data
    df = get_by_country_merged(total_confirmed, total_death, total_recovered, country_name)
    #column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

    fig = px.line(df, x='date', y=['daily_new_confirmed','daily_new_death', 'daily_new_recovered'], title=f'{country_name} daily new cases')

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(width=1500, height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


# function to filter timeseries analysis by country
# I use "case" variable just for column name: e.g, case = confirmed, case = deaths
def get_by_country(df, country, case):
    mask = (df['Country/Region'] == country) 
    df = df.loc[mask]
    df_country = df.groupby("Country/Region").sum()
    df_country = pd.DataFrame(df[df.columns[4:]].sum())
    df_country.reset_index(inplace=True)
    df_country.columns=['date', f"value_{case}"]
    df_country[f"daily_new_{case}"] = df_country[f"value_{case}"] - df_country[f"value_{case}"].shift()
    df_country=df_country.fillna(0)
    return df_country


#use function above to get merged dataframe
def get_by_country_merged(total_confirmed, total_death, total_recovered, country):
    #apply to each timeseries
    country_confirmed_tseries = get_by_country(total_confirmed, country, "confirmed" )
    country_death_tseries = get_by_country(total_death, country, "death" )
    country_recovered_tseries = get_by_country(total_recovered, country, "recovered" )
    
    #merge them all
    country_timeseries_final=pd.merge(country_confirmed_tseries,country_death_tseries,how='inner',on='date')
    country_timeseries_final = pd.merge(country_timeseries_final,country_recovered_tseries,how='inner',on='date')
    country_timeseries_final
    return country_timeseries_final

#example
china_ts = get_by_country_merged(total_confirmed, total_death, total_recovered, "China")
print (china_ts)


def get_per_country_data(total_confirmed, total_death, total_recovered, country_name):
    #total confirmed per country
    total_confirmed_per_country = total_confirmed.groupby("Country/Region").sum()
    total_confirmed_per_country.reset_index(inplace=True)
    mask = (total_confirmed_per_country['Country/Region'] == country_name) 
    total_confirmed_per_country = total_confirmed_per_country.loc[mask]
    total_confirmed_per_country = total_confirmed_per_country[total_confirmed_per_country.columns[-1]].sum()
    
    #total deaths per country
    total_death_per_country = total_death.groupby("Country/Region").sum()
    total_death_per_country.reset_index(inplace=True)
    mask = (total_death_per_country['Country/Region'] == country_name) 
    total_death_per_country=total_death_per_country.loc[mask]
    total_death_per_country = total_death_per_country[total_death_per_country.columns[-1]].sum()
    
    #total recovered per country
    total_recovered_per_country = total_recovered.groupby("Country/Region").sum()
    total_recovered_per_country.reset_index(inplace=True)
    mask = (total_recovered_per_country['Country/Region'] == country_name) 
    total_recovered_per_country=total_recovered_per_country.loc[mask]
    total_recovered_per_country = total_recovered_per_country[total_recovered_per_country.columns[-1]].sum()
    return total_confirmed_per_country, total_death_per_country, total_death_per_country

""" HTML selector for user input in web page
ref : https://www.w3schools.com/tags/tag_select.asp

I need HTML selector for retrieving country input : https://stackoverflow.com/questions/53388003/select-country-dropdown-in-html-page
e.g:
<select>
<option value="Afghanistan">Afghanistan</option>
<option value="Albania">Albania</option>
<option value="Algeria">Algeria</option>
<option value="American Samoa">American Samoa</option>
...
</select>

If I use the selector from stack overflow solution, I need to filter manualy which country that doesnt exist in my table 
and also which country that has different format, so I will create my own selector based on countries in "final_df"
"""
#I also need to sort my final_df alphabetically by Country name so the selector also sorted
final_df.reset_index(inplace=True, drop=True)
with open('custom_html_selector.txt', 'w') as opened_file:
    for key,value in final_df.sort_values(by=["Country/Region"]).iterrows():
        opened_file.write(f"""<option value="{value['Country/Region']}">{value['Country/Region']}</option>\n""")
        print(f"""<option value="{value['Country/Region']}">{value['Country/Region']}</option>\n""")


def load_chartjs_map_data():
  # ref : https://www.highcharts.com/demo/maps/tooltip
  chartjs_ccode = pd.read_json(
      "https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json")
  chartjs_ccode
  chartjs_map = final_df[["code3", "Country/Region", "confirmed"]]
  chartjs_map.columns = ["code3", "name", "value"]
  chart_json = chartjs_map.to_dict('records')
  return chart_json