# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:24:39 2017


"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from src.metrics_calculator import metrics_calculator as mc
from src.data_builder import data_builder as bd

TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'

df = bd.create_sample_df()

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

pie_chart = dcc.Graph(id='pie_chart')

app.layout = html.Div([pie_chart,
                       slider])

pie_layout = dict(
    autosize=True,
    title='Confusion Matrix Explanation',
)

# Selectors, main graph -> pie graph
@app.callback(Output('pie_chart', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):
    
    tp, fp, tn, fn = mc.confusion_matrix(df, slider)
    
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

    
    
    figure = dict(data=data, layout=pie_layout)
    return figure

if __name__ == '__main__':
    app.run_server()