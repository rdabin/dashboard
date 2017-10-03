import dash
from src.graph import graph
from src.table import table
from src.metrics_calculator import metrics_calculator
from src.data_builder import data_builder
from src.callback_manager import callback_manager
from src.volume_plot import volume_plot

# TODO: imports to remove once refactored callbacks etc into modules
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


# TODO: extract to config file. - json?
############# GLOBAL CONFIG 
TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'


########### Load data
# datafile = 'data/data.csv'
# if not os.path.isfile(datafile):
#     raw_data = build_data.create_sample_datafile(num_records=1000, datafile)
# else:
#     raw_data = pd.read_csv(datafile)
raw_data = data_builder.create_sample_df()


# calculate roc data
roc_data = metrics_calculator.build_roc_data(raw_data)
###########


########### create graph divs

# TODO: create modules?
slider = html.Div([
    dcc.Slider(
        id='slider',
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.01,
        marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
    )],
    style={'width': '48%', 'display': 'inline-block'}
)
pie_chart = dcc.Graph(id='pie_chart')
histogram = dcc.Graph(id='histogram')



roc_graph = graph.get_graph(roc_data)
volume_plot = volume_plot.get_population_dots()
cost_graph = graph.get_cost_graph(roc_data)
###############



######## initialise app

#TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout = html.Div([
    html.H4(children='HODAC Threshold Explorer'),
    slider,
    roc_graph,
    volume_plot,
    pie_chart,
    histogram,
    cost_graph
])
#########


# TODO: move to modules
######## callbacks
@app.callback(Output('pie_chart', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):
    
    tp, fp, tn, fn = metrics_calculator.confusion_matrix(raw_data, slider)
    
    data = [
        dict(
            type='pie',
            ids=['TP', 'FN'],
            labels=['True positive', 'False negative'],
            values=[tp, fn],
            text=[TP_TEXT, FN_TEXT],
            hoverinfo='value',
            name='Recall',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FN_COLOUR]),
            # Haven't been able to get this annotation to work yet
            # annotations=[dict(text='Recall', x=0.2, y=0.9, xref='paper', yref='paper')]
        ),
        dict(
            type='pie',
            ids=['TP', 'FP'],
            labels=['True positive', 'False positive'],
            values=[tp, fp],
            hoverinfo='value',
            text=[TP_TEXT, FP_TEXT],            
            name='Precision',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FP_COLOUR])                        
        ),
        dict(
            type='pie',
            ids=['TP', 'TN', 'FP', 'FN'],
            labels=['True positive', 'True negative', 'False positive', 'False negative'],
            values=[tp, tn, fp, fn],
            text=[TP_TEXT, TN_TEXT, FP_TEXT, FN_TEXT],                        
            hoverinfo='value',
            name='Accuracy',
            pull=[0, 0, 0.1, 0.1],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0, 0.4]},
            marker=dict(colors=[TP_COLOUR, TN_COLOUR, FP_COLOUR, FN_COLOUR])                                    
        ),
        dict(
            type='pie',
            ids=['FP', 'TN'],
            labels=['False positive', 'True negative'],
            values=[fp, tn],
            text=[FP_TEXT, TN_TEXT],                        
            hoverinfo='value',
            name='False positive rate',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0, 0.4]},
            marker=dict(colors=[FP_COLOUR, TN_COLOUR])                        
        )
    ]

    figure = dict(data=data, layout=dict(autosize=True, title='Confusion Matrix Explanation'))
    
    return figure

@app.callback(Output('histogram', 'figure'),
              [Input('slider', 'value')])
def make_histogram_figure(slider):

    TP, FP, TN, FN = metrics_calculator.confusion_matrix(df, slider)

    figure = go.Figure(
        data=[
            go.Bar(
                x=['TP', 'FP', 'TN', 'FN'],
                y=[TP, FP, TN, FN],
                name='My Bar Chart'
            )
        ]
    )

    return figure



### REGISTER CONTROLLER CALLBACKS
#callback_manager.register_callbacks(app)


if __name__ == '__main__':
    app.run_server()
