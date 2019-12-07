import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import pandas as pd
import altair as alt
import datetime as dt

# Import cleaned data
df = pd.read_csv('data/supermarket_sales_clean.csv')

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
times = ['Morning', 'Afternoon', 'Evening']

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'


def make_total_sales(store_id='A'):

    # Create total sales heat map (unfiltered by store)

    total_sales = (alt
                    .Chart(df) # make this react to the radio
                    .mark_rect()
                    .encode(alt.X('Day_of_week:N', title=None, sort=days),
                    alt.Y('Time_of_day:N', title=None, sort=times),
                    alt.Color('sum(Total):Q', title=None, scale=alt.Scale(scheme='greens')),
                    tooltip=[alt.Tooltip('Day_of_week', title='Day of the week'), 
                            alt.Tooltip('Time_of_day', title="Time of the day"), 
                            alt.Tooltip('sum(Total):Q', title='Sales', format='$,.0f')])
                    .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=store_id))
                    .configure_axis(labelFontSize=13, titleFontSize=13)
                    .configure_title(fontSize=14)
                    .properties(width=180, height=130, title='Total sales')
    )

    return total_sales

def make_customer_traffic(store_id='A'):
    
    # Create customer traffic heat map (unfiltered by store)
    
    customer_traffic = (alt
                        .Chart(df)
                        .mark_rect()
                        .encode(
                            alt.X('Day_of_week:N', title=None, sort=days),
                            alt.Y('Time_of_day:N', title=None, sort=times),
                            alt.Color('count(Invoice ID):Q', title=None, scale=alt.Scale(scheme='greens')),
                            tooltip=[alt.Tooltip('Day_of_week', title = 'Day of the week'), 
                                    alt.Tooltip('Time_of_day', title = "Time of the day"), 
                                    alt.Tooltip('count(Invoice ID):Q', title = 'No. of transactions')])
                        .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=store_id))
                        .configure_axis(labelFontSize=13, titleFontSize=13)
                        .configure_title(fontSize=14)
                        .properties(width=180, height=130, title='Customer traffic')
    )

    return customer_traffic

def make_transaction_size(store_id='A'):
    
    # Create average transaction size heat map (unfiltered by store)
    
    transaction_size =  (alt
                        .Chart(df)
                        .mark_rect()
                        .transform_aggregate(groupby = ['Branch', 'Day_of_week', 'Time_of_day'],
                                            total_sales = 'sum(Total):Q',
                                            total_trxns = 'count(Invoice ID):Q')
                        .transform_calculate(Avg_trans_size = 'datum.total_sales / datum.total_trxns')
                        .encode(
                            alt.X('Day_of_week:N', title=None, sort=days),
                            alt.Y('Time_of_day:N', title=None, sort=times),
                            alt.Color('Avg_trans_size:Q', title=None, scale=alt.Scale(scheme='greens')),
                            tooltip=[alt.Tooltip('Day_of_week', title = 'Day of the week'), 
                                    alt.Tooltip('Time_of_day', title = "Time of the day"), 
                                    alt.Tooltip('Avg_trans_size:Q', title = 'Average transaction size', format='$,.0f')])
                        .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=store_id))
                        .configure_axis(labelFontSize=13, titleFontSize=13)
                        .configure_title(fontSize=14)
                        .properties(width=180, height=130, title='Average transaction size')
    )
    
    return transaction_size

def make_customer_satisfaction(store_id='A'):

    # Create customer satisfaction heat map (unfiltered by store)

    customer_satisfaction = (alt
                            .Chart(df)
                            .mark_rect()
                            .encode(
                                alt.X('Day_of_week:N', title=None, sort=days),
                                alt.Y('Time_of_day:N', title=None, sort=times),
                                alt.Color('mean(Rating):Q', title=None, scale=alt.Scale(scheme='greens')),
                                tooltip=[alt.Tooltip('Day_of_week', title = 'Day of the week'), 
                                        alt.Tooltip('Time_of_day', title = "Time of the day"), 
                                        alt.Tooltip('mean(Rating):Q', title = 'Average satisfaction', format='.2f')])
                            .transform_filter(alt.FieldEqualPredicate(field='Branch', equal=store_id))
                            .configure_axis(labelFontSize=13, titleFontSize=13)
                            .configure_title(fontSize=14)
                            .properties(width=180, height=130, title='Customer satisfaction')
    )

    return customer_satisfaction

        
app.layout = html.Div([
    html.H1('Supermarket team scheduling app'),

    # add dropdown
    dcc.Dropdown(
        id='store-filter',
        options=[
            {'label': 'Yangon Store', 'value': 'A'},
            {'label': 'Mandalay Store', 'value': 'B'},
            {'label': 'Naypyitaw Store', 'value': 'C'}
        ],
        value='A',
        style=dict(width='45%',
                   verticalAlign='middle')
    ),
    
    # adding some space
    html.Iframe(height='20', width='10', style={'border-width':'0'}),

    html.Div([
        # Arrange total sales heat map
        html.Iframe(
            sandbox='allow-scripts',
            id='total_sales',
            height=300,
            width=370,
            style={'border-width': '0'},
            srcDoc=make_total_sales().to_html()
            ),

        # Arrange customer traffic heat map
        html.Iframe(
            sandbox='allow-scripts',
            id='customer_traffic',
            height=300,
            width=350,
            style={'border-width': '0'},
            srcDoc=make_customer_traffic().to_html()
            ),
        
        # Arrange average transaction size heat map
        html.Iframe(
            sandbox='allow-scripts',
            id='transaction_size',
            height=300,
            width=355,
            style={'border-width': '0'},
            srcDoc=make_transaction_size().to_html()
            ),
        
        # Arrange customer satisfaction heat map
        html.Iframe(
            sandbox='allow-scripts',
            id='customer_satisfaction',
            height=300,
            width=350,
            style={'border-width': '0'},
            srcDoc=make_customer_satisfaction().to_html()
            )
    ]),

    html.Div([
        # ADD BARPLOTS HERE, IF POSSIBLE
    ])
])

# This callback tells Dash the output is the `plot` IFrame; srcDoc is a 
# special property that takes in RAW html as an input and renders it
# As input we take in the values from second dropdown we created (dd-chart) 
# then we run update_plot
@app.callback(
    [Output('total_sales', 'srcDoc'),
     Output('customer_traffic', 'srcDoc'),
     Output('transaction_size', 'srcDoc'),
     Output('customer_satisfaction', 'srcDoc')],

   [dash.dependencies.Input('store-filter', 'value')])
def update_plot(store_id):
   '''
   Takes in an xaxis_column_name and calls make_plot to update our Altair figure
   '''
   updated_total_sales = make_total_sales(store_id).to_html()
   updated_customer_traffic = make_customer_traffic(store_id).to_html()
   updated_transaction_size= make_transaction_size(store_id).to_html()
   updated_customer_satisfaction = make_customer_satisfaction(store_id).to_html()


   return updated_total_sales, updated_customer_traffic, updated_transaction_size, updated_customer_satisfaction
