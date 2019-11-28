import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import altair as alt  

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Supermarket team scheduling dashboard'

# Import cleaned data
# To run from `src` directory keep code below
# To run from home directory, change path to '/data/supermarket_sales.csv'

df = pd.read_csv('data/supermarket_sales_clean.csv')

def make_heat_map(branch_index, func, plot_title):
    
    '''Make a heat map by day of week and time of day
    
    Parameters
    ---
    branch_index: Str
    func: Str
    plot_title: Str
    '''
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    times = ['Morning', 'Afternoon', 'Evening']
    
    heat_map = (alt
                .Chart(df)
                .mark_rect()
                .encode(alt.X('Day_of_week:N', title=None, sort=days),
                        alt.Y('Time_of_day:N', title=None, sort=times),
                        alt.Color(func, type = 'quantitative' ,title=None, scale=alt.Scale(scheme='greens')),
                        tooltip=[alt.Tooltip('Day_of_week', title='Day of the week'), 
                                 alt.Tooltip('Time_of_day', title='Time of the day'),
                                 alt.Tooltip(func, type='quantitative', title=plot_title, format=',.0f')])
                .configure_axisX(labelAngle=45)
                .transform_filter(alt.FieldEqualPredicate(field='Branch', equal= branch_index))
                .configure_axis(labelFontSize=13, titleFontSize=13)
                .configure_title(fontSize=14)
                .properties(width=180, height=130, title=plot_title)
    )   
    return heat_map
    
def make_total_sales(branch_index='A'):
    total_sales = make_heat_map(branch_index, 'sum(Total)', 'Total Sales')

    return total_sales

def make_customer_traffic(branch_index='A'):
    customer_traffic = make_heat_map(branch_index, 'count(Invoice ID)', 'Customer Traffic')

    return customer_traffic

def make_transaction_size(branch_index='A'):
    transaction_size = make_heat_map(branch_index, 'mean(Total)', 'Average Transaction Size')

    return transaction_size

def make_customer_satisfaction(branch_index='A'):
    customer_satisfaction = make_heat_map(branch_index, 'mean(Rating)', 'Average Satisfaction')

    return customer_satisfaction

def make_bar_plot(day_of_week, time_of_day, branch_index, func, plot_title, y_title):
    '''Make a bar plot filtered by branch, day of week, and time of day 
    
    Parameters
    ---
    day_of_week: Str
    time_of_day: Str
    func: Str
    plot_title: Str
    branch_index: Str
    '''
    bar_plot = (alt
                .Chart(df)
                .mark_bar(color = 'cornflowerblue')
                .encode(alt.X('Product line:N', title=None),
                        alt.Y(func, type='quantitative', title=y_title),
                        tooltip=[alt.Tooltip('Product line', title='Product line'),
                                alt.Tooltip('Day_of_week', title='Day of Week'),
                                alt.Tooltip('Time_of_day', title='Time of Day'),
                                alt.Tooltip(func, title=plot_title)])
                .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=branch_index))
                .transform_filter(alt.FieldEqualPredicate(field='Day_of_week', equal=day_of_week))
                .transform_filter(alt.FieldEqualPredicate(field='Time_of_day', equal=time_of_day))
                .properties(width=250, height=175, title= plot_title)
    )
    return bar_plot

def con_plt(day_of_week='Monday', time_of_day='Morning', branch_index='A'):
    bar_plot_sales = make_bar_plot(day_of_week, time_of_day, branch_index, 'sum(Total)', 'Total Sales', 'Sales in MMK')
    bar_plot_traffic = make_bar_plot(day_of_week,time_of_day, branch_index, 'count(Invoice ID)', 'Customer Traffic', 'Transactions')
    bar_plot_trans = make_bar_plot(day_of_week, time_of_day, branch_index, 'mean(Total)', 'Average Transaction Size', 'Sales in MMK')
    bar_plot_rating = make_bar_plot(day_of_week, time_of_day, branch_index, 'mean(Rating)', 'Average Satisfaction', 'Rating')
    
    return (alt.concat(bar_plot_sales, bar_plot_traffic, bar_plot_trans, bar_plot_rating, columns=4)
                .configure_axis(labelFontSize=13, titleFontSize=13)
                .configure_title(fontSize=14)
                .configure_axisX(labelAngle=45)
            )

con_plt('Monday', 'Morning', 'A')
make_total_sales('A')
make_customer_traffic('A')
make_transaction_size('A')
make_customer_traffic('A')

app.layout = html.Div([
    html.H1('Supermarket Staffing'),
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
    
    html.H2('Store Performance Summary'),

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
    
    html.Label('Select day of week:'),
    
    # Arrange dropdown menu to select day of week
    dcc.Dropdown(
        id='day_of_week',
        options=[{'label': i, 'value': i} for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']],
        value='Monday'),
    
    html.Label('Select time of day:'),
    
    # Arrange dropdown menu to select time of day
    dcc.Dropdown(
        id='time_of_day',
        options=[{'label': i, 'value': i} for i in df['Time_of_day'].unique()],
        value='Morning'),
    
     html.H2('Store Performance By Department'),

    # Arrange bar plots
    html.Iframe(
        sandbox='allow-scripts',
        id='bar_plots',
        height='400',
        width='1500',
        style={'border-width': '0px'},
        srcDoc=con_plt().to_html()
        ),
])

# Update heat maps
@app.callback(
    [Output('total_sales', 'srcDoc'),
     Output('customer_traffic', 'srcDoc'),
     Output('transaction_size', 'srcDoc'),
     Output('customer_satisfaction','srcDoc')],

     [dash.dependencies.Input('Store', 'value')])

def update_plot(branch_index):
    updated_total_sales = make_total_sales(branch_index).to_html()
    updated_customer_traffic = make_customer_traffic(branch_index).to_html()
    updated_transaction_size= make_transaction_size(branch_index).to_html()
    updated_customer_satisfaction = make_customer_satisfaction(branch_index).to_html()

    return updated_total_sales, updated_customer_traffic, updated_transaction_size, updated_customer_satisfaction

# Update bar plots
@app.callback(
    dash.dependencies.Output('bar_plots', 'srcDoc'),
    [dash.dependencies.Input('day_of_week', 'value'),
     dash.dependencies.Input('time_of_day', 'value'),
     dash.dependencies.Input('Store', 'value')])

def update_plot(day_of_week, time_of_day, branch_index):
    bar_plots = con_plt(day_of_week, time_of_day, branch_index).to_html()
    return bar_plots


if __name__ == '__main__':
    app.run_server(debug=True)