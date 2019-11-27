import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc                 
import dash_html_components as html 
import altair as alt                
from dash.dependencies import Input, Output        

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

# load data
df = pd.read_csv('./data/supermarket_sales.csv',
                 parse_dates = {'Date_time': ['Date', 'Time']})

# Add day of the week
df['Day_of_week'] = df['Date_time'].dt.weekday_name

# Assign transactions between 09:00-12:59 as 'Morning'
morning = df.set_index('Date_time').between_time('09:00', '12:59')
morning['Time_of_day'] = 'Morning'

# Assign transactions between 13:00-16:59 as 'Afternoon'
afternoon = df.set_index('Date_time').between_time('13:00', '16:59')
afternoon['Time_of_day'] = 'Afternoon'

# Assign transactions between 17:00-20:59 as 'Evening'
evening = df.set_index('Date_time').between_time('17:00', '20:59')
evening['Time_of_day'] = 'Evening'

new_df = pd.concat([morning, afternoon, evening])

def update_graph(DayofWeek, TimeofDay, func, pltTitle, branch_index):
    '''
    plot barplots of different functions for specific DayofWeek and TimeofDay 
    
    Parameters
    ---
    DayofWeek: Str
    TimeofDay: Str
    func: Str
    pltTitle: Str
    branch_index: Str
    '''
    chart = alt.Chart(new_df).mark_bar(color = "cornflowerblue").encode(
            alt.X('Product line:N'),
            alt.Y(func, type ='quantitative'),
            tooltip=[alt.Tooltip('Product line', title = 'Day of the week'),
                     alt.Tooltip(func, title = pltTitle)]
        ).transform_filter(
            alt.FieldEqualPredicate(field='Branch', equal= branch_index)
        ).transform_filter(
            alt.FieldEqualPredicate(field='Day_of_week', equal= DayofWeek)
        ).transform_filter(
            alt.FieldEqualPredicate(field='Time_of_day', equal= TimeofDay)
        ).properties(width=280, height=200, title= pltTitle)
    return chart

def con_plt(DayofWeek = "Monday", TimeofDay = "Morning"):
    plt1 = update_graph(DayofWeek, TimeofDay, 'sum(Total)', "Total Sales", "A")
    plt2 = update_graph(DayofWeek, TimeofDay, 'count(Invoice ID)', "Customer Traffic", "A")
    plt3 = update_graph(DayofWeek, TimeofDay, "mean(Total)", "Average Transaction Size", "A")
    plt4 = update_graph(DayofWeek, TimeofDay, "mean(Rating)", "Average Satisfaction", "A")
    
    return alt.concat(plt1, plt2, plt3, plt4, columns=4)

con_plt("Monday", "Morning")

app.layout = html.Div([
    html.Label('Please choose Day of Week'),
    dcc.Dropdown(
        id = 'DayofWeek',
        options = [{'label': i, 'value': i} for i in new_df['Day_of_week'].unique()],
        value = 'Day of Week'),
    html.Label('Please choose Time of Day'),
    dcc.Dropdown(
        id = 'TimeofDay',
        options = [{'label': i, 'value': i} for i in new_df['Time_of_day'].unique()],
        value = 'Time of Day'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='400',
        width='1400',
        style={'border-width': '5px'},

        ################ The magic happens here
        #srcDoc=open('complex_chart.html').read()
        srcDoc = con_plt().to_html()
        ################ The magic happens here
        ),
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('DayofWeek', 'value'),
     dash.dependencies.Input('TimeofDay', 'value')])

def update_plot(DayofWeek, TimeofDay):
    updated_plot = con_plt(DayofWeek, TimeofDay).to_html()
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True)