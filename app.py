import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Supermarket team scheduling dashboard'

# Import cleaned data
# To run from `src` directory keep code below
# To run from home directory, change path to '/data/supermarket_sales.csv'

df = pd.read_csv('data/supermarket_sales_clean.csv')

def make_heat_map(branch_index, func, plot_title):
    
    """
    Make a heat map by day of week and time of day
    
    Parameters
    ----------
    branch_index: str
        the alphabet used to represent supermarket branch 
    func: str
        the variable to be associated with the color of the mark 
    plot_title: str
        the name to be used as title 

    Returns
    -------
    Altair chart object 
        a heatmap 
    """
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    times = ['Morning', 'Afternoon', 'Evening']
    
    heat_map = (alt
                .Chart(df)
                .mark_rect()
                .encode(alt.X('Day_of_week:N', title=None, sort=days),
                        alt.Y('Time_of_day:N', title=None, sort=times),
                        alt.Color(func, type = 'quantitative' ,title=None, scale=alt.Scale(scheme='greens')),
                        tooltip=[
alt.Tooltip(func, type='quantitative', title=plot_title, format=',.0f')])
                .configure_axisX(labelAngle=45)
                .transform_filter(alt.FieldEqualPredicate(field='Branch', equal= branch_index))
                .configure_axis(labelFontSize=13, titleFontSize=13)
                .configure_title(fontSize=14)
                .properties(width=180, height=130, title=plot_title)
    )   
    return heat_map
    
def make_total_sales(branch_index='A'):
    """
    Create total sales heatmap

    Parameters
    ----------
    branch_index: str
        the alphabet used to represent supermarket branch 

    Returns
    -------
    Altair chart object 
        a total sales heatmap

    """
    total_sales = make_heat_map(branch_index, 'sum(Total)', 'Total Sales (MMK)')

    return total_sales

def make_customer_traffic(branch_index='A'):
    """
    Create customer traffic heat map

    Parameters
    ----------
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    Altair chart object
        a customer traffic heatmap 

    """
    customer_traffic = make_heat_map(branch_index, 'count(Invoice ID)', 'Customer Traffic')

    return customer_traffic

def make_transaction_size(branch_index='A'):
    """
    Create average transaction size heat map

    Parameters
    ----------
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    Altair chart object
        a transaction size heatmap
    """
    transaction_size = make_heat_map(branch_index, 'mean(Total)', 'Average Transaction Size (MMK)')

    return transaction_size

def make_customer_satisfaction(branch_index='A'):
    """
    Create average customer satisfaction heat map
    
    Parameters
    ----------
    branch_index: str
        the alphabet used to represent supermarket branch
    
    Returns
    -------
    Altair chart object
        a customer satisfaction heatmap
    
    """
    customer_satisfaction = make_heat_map(branch_index, 'mean(Rating)', 'Average Satisfaction')

    return customer_satisfaction

def make_bar_plot(day_of_week, time_of_day, branch_index, func, plot_title, y_title):
    '''
    Make a bar plot filtered by branch, day of week, and time of day 
    
    Parameters
    ----------
    day_of_week: str
        the day of week ranging from Monday to Sunday 
    time_of_day: str
        the time of day ranging from morning to evening 
    func: str
        the variable to be used as y axis  
    plot_title: str
        the name to be used as title 
    branch_index: str
        the alphabet used to represent supermarket branch 

    Returns
    -------
    Altair chart object
        a bar plot 

    '''
    bar_plot = (alt
                .Chart(df)
                .mark_bar(color = 'cornflowerblue')
                .encode(alt.X('Product line:N', title=None),
                        alt.Y(func, type='quantitative', title=y_title),
                        tooltip=[alt.Tooltip('Product line', title='Product line'),
                                alt.Tooltip(func, title=plot_title)])
                .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=branch_index))
                .transform_filter(alt.FieldEqualPredicate(field='Day_of_week', equal=day_of_week))
                .transform_filter(alt.FieldEqualPredicate(field='Time_of_day', equal=time_of_day))
                .properties(width=250, height=175, title= plot_title)
    )
    return bar_plot

def con_plt(day_of_week='Monday', time_of_day='Morning', branch_index='A'):
    """
    Concatenate all bar plots
    
    Parameters
    ----------
    day_of_week: str
        the day of week ranging from Monday to Sunday 
    time_of_day: str
        the time of day ranging from morning to evening 
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    Altair chart object
        a concatenated bar plots
    """
    bar_plot_sales = make_bar_plot(day_of_week, time_of_day, branch_index, 'sum(Total)', 'Total Sales', 'Sales in MMK')
    bar_plot_traffic = make_bar_plot(day_of_week,time_of_day, branch_index, 'count(Invoice ID)', 'Customer Traffic', 'Transactions')
    bar_plot_trans = make_bar_plot(day_of_week, time_of_day, branch_index, 'mean(Total)', 'Average Transaction Size', 'Sales in MMK')
    bar_plot_rating = make_bar_plot(day_of_week, time_of_day, branch_index, 'mean(Rating)', 'Average Satisfaction', 'Rating')
    
    return (alt.concat(bar_plot_sales, bar_plot_traffic, bar_plot_trans, bar_plot_rating, columns=4)
                .configure_axis(labelFontSize=13, titleFontSize=13)
                .configure_title(fontSize=14)
                .configure_axisX(labelAngle=45)
            )

app.layout = html.Div([
    html.Div([ 
        html.H1(
            children = 'Supermarket Staffing',
            style = dict(textAlign = 'center')),

        html.P(
            children = 'Review past performance by store to improve staffing of the sales floor at your store',
            style = dict(textAlign = 'center')),

        html.Label('Select store:'),

        # Arrange radio buttoms to select branch
        dcc.RadioItems(
            id='Store',
            options=[
                {'label': 'Yangon', 'value': 'A'},
                {'label': 'Mandalay', 'value': 'B'},
                {'label': 'Naypyitaw', 'value': 'C'}
            ],
            value='A'),
    ], style = {"backgroundColor": "gainsboro"}),
  
    dcc.Tabs(id="tabs", children=[
        # The first tab 
        dcc.Tab(label='Store Performance Summary', children=[
            html.Div(children = [
                html.Div([
                    html.H2('Store Performance Summary'),

                    dcc.Markdown('''
                    **Purpose:**  Identify days and time periods of interest whether overstaffing or understaffing is happening

                    **Some guiding questions:**
                    - Are there periods of time with **high total sales**, **high customer traffic**, **high transaction sizes** but **low customer satisfaction**? 
                        - Have we previously understaffed when the store is busy?
                    - Are there periods of time with **low total sales**, **low customer traffic**, **low transaction sizes** and **high customer satisfaction**?
                        - Have we previously overstaffed when the store is quiet?
                    - Are there periods of **high customer traffic** but **small transaction sizes**?
                        - Would additional staff helping customers persuade customers to spend more? 
                    ''')
                    ], style = {"backgroundColor": "Beige", 'border-width': '0px'}
                ),

                dbc.Row([
                    # Arrange total sales heat map
                    html.Iframe(sandbox='allow-scripts',
                                id='total_sales',
                                height='300',
                                width='370',
                                style={'border-width': '0px'},
                                srcDoc=make_total_sales().to_html()
                    ),
                                
                    # Arrange customer traffic heat map
                    html.Iframe(sandbox='allow-scripts',
                                id='customer_traffic',
                                height='300',
                                width='370',
                                style={'border-width': '0px'},
                                srcDoc=make_customer_traffic().to_html()
                    ),
                                
                    # Arrange average transaction size heat map
                    html.Iframe(sandbox='allow-scripts',
                                id='transaction_size',
                                height='300',
                                width='370',
                                style={'border-width': '0px'},
                                srcDoc=make_transaction_size().to_html()
                    ),
                                
                    # Arrange customer satisfaction heat map
                    html.Iframe(sandbox='allow-scripts',
                                id='customer_satisfaction',
                                height='300',
                                width='370',
                                style={'border-width': '0px'},
                                srcDoc=make_customer_satisfaction().to_html()
                    )
                ]),
            ], className="container"), 
        ]),

        # the second tab
        dcc.Tab(label='Compare Store Performance By Department', children=[
            html.Div(children = [
                html.Div([
                    html.H2('Compare Store Performance By Department'),

                    dcc.Markdown('''
                    **Purpose:** Compare department-specific performance for a particular day and time to identify departments to add or reduce staff

                    **Guiding example:** I'm considering adding staff to Sunday evening. I could consider staffing more in Sports & Travel where there is highest traffic and lowest satisfaction. 
                    Before deciding, I can compare performance to Saturday afternoon. Sports and travel seems to also have high customer traffic but much lower transaction sizes on Saturday afternoon compared to Sunday evenings. 
                    I should staff more in Sports & Travel on Saturday afternoons instead.  

                    ''')
                ], style = {"backgroundColor": "aliceblue", 'border-width': '0px'}),

            
                html.H3('''Select first shift to compare:'''),
            
                html.Div([
                    # Arrange dropdown menu to select day of week
                    html.Label('Day of week:'),

                    dcc.Dropdown(
                        id='day_of_week',
                        options=[{'label': i, 'value': i} for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']],
                        value='Monday',
                        style={"width": '60%'}),
            
                    html.Label('Time of day:'),
            
                    # Arrange dropdown menu to select time of day
                    dcc.Dropdown(
                        id='time_of_day',
                        options=[{'label': i, 'value': i} for i in df['Time_of_day'].unique()],
                        value='Morning',
                        style={"width": '60%'})
                ], style={'columnCount': 2}),

                # Arrange bar plots
                html.Iframe(
                    sandbox='allow-scripts',
                    id='bar_plots',
                    height='400',
                    width='1500',
                    style={'border-width': '0px'},
                    srcDoc=con_plt().to_html()
                ),

                html.H3('''Select second shift to compare:'''),

                html.Div([
                    # Arrange dropdown menu to select day of week
                    html.Label('Day of week:'),

                    dcc.Dropdown(
                        id='day_of_week2',
                        options=[{'label': i, 'value': i} for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']],
                        value='Monday',
                        style={"width": '60%'}),
            
                    html.Label('Time of day:'),
            
                    # Arrange dropdown menu to select time of day
                    dcc.Dropdown(
                        id='time_of_day2',
                        options=[{'label': i, 'value': i} for i in df['Time_of_day'].unique()],
                        value='Morning',
                        style={"width": '60%'})
                ], style={'columnCount': 2}),

                # Arrange bar plots
                html.Iframe(
                    sandbox='allow-scripts',
                    id='bar_plots2',
                    height='400',
                    width='1500',
                    style={'border-width': '0px'},
                    srcDoc=con_plt().to_html()
                ),    
            ], className="container"),
        ]),
    ]),       
])

@app.callback(
    [Output('total_sales', 'srcDoc'),
     Output('customer_traffic', 'srcDoc'),
     Output('transaction_size', 'srcDoc'),
     Output('customer_satisfaction','srcDoc')],

     [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    """
    Update heatmaps

    Parameters:
    -----------
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    html object 
        all updated heatmaps in the format of html
    """
    updated_total_sales = make_total_sales(branch_index).to_html()
    updated_customer_traffic = make_customer_traffic(branch_index).to_html()
    updated_transaction_size= make_transaction_size(branch_index).to_html()
    updated_customer_satisfaction = make_customer_satisfaction(branch_index).to_html()

    return updated_total_sales, updated_customer_traffic, updated_transaction_size, updated_customer_satisfaction

@app.callback(
    dash.dependencies.Output('bar_plots', 'srcDoc'),
    [dash.dependencies.Input('day_of_week', 'value'),
     dash.dependencies.Input('time_of_day', 'value'),
     dash.dependencies.Input('Store', 'value')])

def update_plot(day_of_week, time_of_day, branch_index):
    """
    Update bar plots

    Parameters
    ----------
    day_of_week: str
        the day of week ranging from Monday to Sunday 
    time_of_day: str
        the time of day ranging from morning to evening 
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    html object 
        all updated bar plots in the format of html
    """
    bar_plots = con_plt(day_of_week, time_of_day, branch_index).to_html()
    return bar_plots

@app.callback(
    dash.dependencies.Output('bar_plots2', 'srcDoc'),
    [dash.dependencies.Input('day_of_week2', 'value'),
     dash.dependencies.Input('time_of_day2', 'value'),
     dash.dependencies.Input('Store', 'value')])

def update_plot(day_of_week, time_of_day, branch_index):
    """
    Update bar plots

    Parameters
    ----------
    day_of_week: str
        the day of week ranging from Monday to Sunday 
    time_of_day: str
        the time of day ranging from morning to evening 
    branch_index: str
        the alphabet used to represent supermarket branch

    Returns
    -------
    html object 
        all updated bar plots in the format of html

    """
    bar_plots = con_plt(day_of_week, time_of_day, branch_index).to_html()
    return bar_plots

if __name__ == '__main__':
    app.run_server(debug=True)
