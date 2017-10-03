import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.graph_objs as go
import pandas as pd
import numpy as np

from src.metrics_calculator import metrics_calculator as mc
from src.data_builder import data_builder as bd
from src.methods import methods as mt

app = dash.Dash()

# raw_data = pd.read_csv('data/cover-output-1506343018603.csv')
raw_data = bd.create_sample_df()
roc_data = mc.build_roc_data(raw_data)

# define some parameters
resolution = 4 # number of points per 10 - this is not working properly 
bins1 = 40 # number of bins on histogram data
step = 1/bins1 # this is for the slider, to make step same size as histogram bins
point_size  = 10 # data point size for the histogram plot

# setup color scheme for TPs and TNs
TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='hist_with_slider', animate=True),
    dcc.Slider(
        id='th_slider',
        value=0.5,
        min=0.0,
        max=1.0,
        step=step,
        marks={i/10: '{}'.format(i/10) for i in range(0, 10)}),
    html.Div(id='threshold')
    
])

@app.callback(
    dash.dependencies.Output('hist_with_slider', 'figure'),
    [dash.dependencies.Input('th_slider', 'value')])

def update_histogram(threshold):
    """
    Update histogram coloring according to slider threshold

    """
    hist_exp, bins_exp, colors_exp = mt.histogram_data(raw_data, threshold, resolution, bins1,
        TP_COLOUR = TP_COLOUR, FP_COLOUR = FP_COLOUR, TN_COLOUR = TN_COLOUR, FN_COLOUR = FN_COLOUR)
    figure={
        'data': [
            go.Scatter(
                x=bins_exp,
                y=hist_exp,
                text='Histogram',
                mode='markers',
                opacity=0.7,
                
                marker={
                    'size': point_size,
                    'color' : colors_exp,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            )
        ],
        'layout': go.Layout(
            width = 600,
            height = 300,
            xaxis={'type': 'linear', 'title': 'Threshold'},
            yaxis={'title': 'Counts'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure


@app.callback(
    Output(component_id='threshold', component_property='children'),
    #[Input(component_id='th_slider', component_property='value')]
    [Input(component_id='hist_with_slider', component_property='hoverData')]
)
def update_text_graph(input_value):
    hover_data = input_value['points'][0]
    print(hover_data)
    print(type(hover_data))
    for key in hover_data.keys():
        print(key)
    threshold = hover_data['x']
    print(threshold)
    return 'Threshold: "{}"'.format(threshold)




if __name__ == '__main__':
    app.run_server()