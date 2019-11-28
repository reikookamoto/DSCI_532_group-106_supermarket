import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc                 
import dash_html_components as html 
import altair as alt                
from dash.dependencies import Input, Output        

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Supermarket Dashboard'

# load data, .py should be run in `src` directory in this case 
# if you are going to run from home directory, change path to '/data/supermarket_sales.csv'
df = pd.read_csv('../data/supermarket_sales.csv',
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

def update_graph(DayofWeek, TimeofDay, branch_index, func, pltTitle):
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
            tooltip=[alt.Tooltip('Product line', title = 'Product line'),
                     alt.Tooltip('Day_of_week', title = "Day of Week"),
                     alt.Tooltip('Time_of_day', title = "Time of Day"),
                     alt.Tooltip(func, title = pltTitle)]
        ).transform_filter(
            alt.FieldEqualPredicate(field='Branch', equal= branch_index)
        ).transform_filter(
            alt.FieldEqualPredicate(field='Day_of_week', equal= DayofWeek)
        ).transform_filter(
            alt.FieldEqualPredicate(field='Time_of_day', equal= TimeofDay)
        ).properties(width=280, height=200, title= pltTitle)
    return chart

def con_plt(DayofWeek = "Monday", TimeofDay = "Morning", branch_index = "A"):
    plt1 = update_graph(DayofWeek, TimeofDay, branch_index, 'sum(Total)', "Total Sales")
    plt2 = update_graph(DayofWeek, TimeofDay, branch_index, 'count(Invoice ID)', "Customer Traffic")
    plt3 = update_graph(DayofWeek, TimeofDay, branch_index, "mean(Total)", "Average Transaction Size")
    plt4 = update_graph(DayofWeek, TimeofDay, branch_index, "mean(Rating)", "Average Satisfaction")
    
    return alt.concat(plt1, plt2, plt3, plt4, columns=4)

con_plt("Monday", "Morning", "A")

app.layout = html.Div([
    html.Label('Please choose Store'),
    dcc.RadioItems(
        id = 'Store',
        options = [{'label': i, 'value': i} for i in ["A", "B", "C"]],
        value = 'Branch'),
    html.Label('Please choose Day of Week'),
    dcc.Dropdown(
        id = 'DayofWeek',
        options = [{'label': i, 'value': i} for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]],
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

        srcDoc = con_plt().to_html()
        ),
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('DayofWeek', 'value'),
     dash.dependencies.Input('TimeofDay', 'value'),
     dash.dependencies.Input('Store', 'value')])

def update_plot(DayofWeek, TimeofDay, branch_index):
    updated_plot = con_plt(DayofWeek, TimeofDay, branch_index).to_html()
    return updated_plot
