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

def mds_special():
    font = "Arial"
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    return {
        "config": {
            "title": {
                "fontSize": 24,
                "font": font,
                "anchor": "start", # equivalent of left-aligned.
                "fontColor": "#000000"
            },
            'view': {
                "height": 300, 
                "width": 400
            },
            "axisX": {
                "domain": True,
                #"domainColor": axisColor,
                "gridColor": gridColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": font,
                "labelFontSize": 12,
                "labelAngle": 90, 
                "tickColor": axisColor,
                "tickSize": 5, # default, including it just to show you can change it
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "X Axis Title (units)", 
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": font,
                "labelFontSize": 14,
                "labelAngle": 0, 
                #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "Y Axis Title (units)", 
                # titles are by default vertical left of axis so we need to hack this 
                #"titleAngle": 0, # horizontal
                #"titleY": -10, # move it up
                #"titleX": 18, # move it to the right so it aligns with the labels 
            },
        }
            }

# register the custom theme under a chosen name
alt.themes.register('mds_special', mds_special)

# enable the newly registered theme
alt.themes.enable('mds_special')

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

def update_heatmap(branch_index, func, pltTitle):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    times = ['Morning', 'Afternoon', 'Evening']
    
    chart = alt.Chart(new_df).mark_rect().encode(
     alt.X('Day_of_week:N', title=None, sort=days),
     alt.Y('Time_of_day:N', title=None, sort=times),
     alt.Color(func, type = 'quantitative' ,title=None, scale=alt.Scale(scheme='inferno'), sort="descending"),
     tooltip=[alt.Tooltip('Day_of_week', title='Day of the week'), 
              alt.Tooltip('Time_of_day', title="Time of the day"), 
              alt.Tooltip('sum(Total):Q', title='Sales', format='$,.0f')]
    ).transform_filter(
            alt.FieldEqualPredicate(field='Branch', equal= branch_index)
    ).properties(width=250, height=150, title=pltTitle
    ).configure_axis(labelFontSize=14, titleFontSize=14
    ).configure_title(fontSize=16)
    return chart

def con_heatmap1(branch_index = "A"):
    plt1 = update_heatmap(branch_index, 'sum(Total)', "Total Sales")

    return plt1

def con_heatmap2(branch_index = "A"):
    plt2 = update_heatmap(branch_index, 'count(Invoice ID)', "Customer Traffic")

    return plt2

def con_heatmap3(branch_index = "A"):
    plt3 = update_heatmap(branch_index, "mean(Total)", "Average Transaction Size")

    return plt3

def con_heatmap4(branch_index = "A"):
    plt4 = update_heatmap(branch_index, "mean(Rating)", "Average Satisfaction")

    return plt4

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
con_heatmap1("A")
con_heatmap2("A")
con_heatmap3("A")
con_heatmap4("A")

app.layout = html.Div([
    html.H1("Supermarket Dashboard"),
    html.Label('Please choose Store'),
    dcc.RadioItems(
        id = 'Store',
        options = [{'label': i, 'value': i} for i in ["A", "B", "C"]],
        value = 'Branch'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot2',
        height='250',
        width='342',
        style={'border-width': '5px'},

        srcDoc = con_heatmap1().to_html()
        ),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot3',
        height='250',
        width='342',
        style={'border-width': '5px'},

        srcDoc = con_heatmap2().to_html()
        ),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot4',
        height='250',
        width='342',
        style={'border-width': '5px'},

        srcDoc = con_heatmap2().to_html()
        ),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot5',
        height='250',
        width='342',
        style={'border-width': '5px'},

        srcDoc = con_heatmap2().to_html()
        ),
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

@app.callback(
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    updated_plot2 = con_heatmap1(branch_index).to_html()
    return updated_plot2

@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    updated_plot3 = con_heatmap2(branch_index).to_html()
    return updated_plot3

@app.callback(
    dash.dependencies.Output('plot4', 'srcDoc'),
    [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    updated_plot4 = con_heatmap3(branch_index).to_html()
    return updated_plot4

@app.callback(
    dash.dependencies.Output('plot5', 'srcDoc'),
    [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    updated_plot5 = con_heatmap4(branch_index).to_html()
    return updated_plot5


if __name__ == '__main__':
    app.run_server(debug=True)