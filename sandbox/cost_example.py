# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:57:22 2017
Handle different costs for false positives and false negatives
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from src.metrics_calculator import metrics_calculator as mc
from src.data_builder import data_builder as bd
from src.graph import graph

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

slider = dcc.Slider(id='slider', min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

fp_cost = dcc.Input(
        id='fp_cost',
        placeholder='Enter a value...',
        type='number',
        value=1
        )

fn_cost = dcc.Input(
        id='fn_cost',
        placeholder='Enter a value...',
        type='number',
        value=1
        )

goto_cost_minimum = html.Button('Submit', id='goto_cost_minimum')

cost_instructions = html.Div(id='cost_instructions',
             children='Enter a cost for each ' + FP_TEXT + ' and each ' + FN_TEXT
             + ' and press submit')

cost_graph = graph.get_cost_graph_2()
			 
app.layout = html.Div([fp_cost,
                       fn_cost,
                       goto_cost_minimum,
                       cost_instructions,
                       slider,
					   cost_graph])

@app.callback(Output('slider', 'value'),
              [Input('goto_cost_minimum', 'n_clicks')],
              [State('fp_cost', 'value'),
               State('fn_cost', 'value')]
              )
def find_cost_minimum(n_clicks, fp_cost, fn_cost):
    
    roc_df = mc.build_roc_data_fast(df, float(fp_cost), float(fn_cost))
    min_cost = roc_df['cost'].min()
    # If the minimum cost occurs at several different thresholds, take the first one
    min_cost_threshold = roc_df[roc_df['cost']==min_cost]['threshold'].iloc[0]
    
    return min_cost_threshold

graph.set_cost_callback(app, df)
	
if __name__ == '__main__':
    app.run_server()