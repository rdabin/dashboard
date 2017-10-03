import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from ..metrics_calculator import metrics_calculator

def get_graph(roc_data):

    line = go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        #opacity=0.7,
        line=dict(
            color = ('rgb(180, 180, 180)'),
            width = 1,
            dash = 'dash',   # dash options include 'dash', 'dot', and 'dashdot'
        )
    )

    curve = go.Scatter(
        x=roc_data['FPR'],
        y=roc_data['TPR'],
        text='hello world',
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 5,
            'line': {'width': 0.5, 'color': 'white'}
        },
    )

    #fig = go.Figure(data=[line, curve], layout=layout)


    return html.Div([
            dcc.Graph(
                id='roc-curve',
                figure={
                    'data': [
                        curve,
                        line
                    ],
                    'layout': go.Layout(
                        showlegend=False,
                        xaxis={'type': 'linear', 'title': 'FPR'},
                        yaxis={'title': 'TPR'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
    )

    
def get_cost_graph(roc_data):

    curve = go.Scatter(
        x=roc_data['threshold'],
        y=roc_data['cost'],
        text='hello world',
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 5,
            'line': {'width': 0.5, 'color': 'white'}
        },
    )

    #fig = go.Figure(data=[line, curve], layout=layout)


    return html.Div([
            dcc.Graph(
                id='cost-curve',
                figure={
                    'data': [
                        curve
                    ],
                    'layout': go.Layout(
                        showlegend=False,
                        xaxis={'type': 'linear', 'title': 'threshold'},
                        yaxis={'title': 'cost'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
    )   
    
def get_cost_graph_2():
    
    return html.Div([
            dcc.Graph(id='cost-curve')
        ],
        style={'width': '48%', 'display': 'inline-block'}
    )
    
def set_cost_callback(app, df):
    @app.callback(Output('cost-curve', 'figure'),
              [Input('goto_cost_minimum', 'n_clicks')],
              [State('fp_cost', 'value'),
               State('fn_cost', 'value')]
              )
    def update_cost_graph(n_clicks, fp_cost, fn_cost):
        print('df shape:', df.shape)
        roc_df = metric_calculator.build_roc_data_fast(df, float(fp_cost), float(fn_cost))
        print('roc_df shape:', roc_df.shape)
        curve = go.Scatter(
            x=roc_df['threshold'],
            y=roc_df['cost'],
            text='hello world',
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 5,
                'line': {'width': 0.5, 'color': 'white'}
            },
        )   
        print('curve built')
        figure={
            'data': [
                curve
            ],
            'layout': go.Layout(
                showlegend=False,
                xaxis={'type': 'linear', 'title': 'threshold'},
                yaxis={'title': 'cost'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
        
        return figure



# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.graph_objs as go
# import pandas as pd


# def get_graph(roc_data):

#   return html.Div([
#          dcc.Graph(
#              id='roc-curve',
#              figure={
#                  'data': [
#                      go.Scatter(
#                          x=roc_data['FPR'],
#                          y=roc_data['TPR'],
#                          text='hello world',
#                          mode='lines+markers',
#                          opacity=0.7,
#                          marker={
#                              'size': 5,
#                              'line': {'width': 0.5, 'color': 'white'}
#                          },
#                      )
#                  ],
#                  'layout': go.Layout(
#                      xaxis={'type': 'linear', 'title': 'FPR'},
#                      yaxis={'title': 'TPR'},
#                     margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                      legend={'x': 0, 'y': 1},
#                      hovermode='closest'
#                  )
#              }
#          )
#      ],
#      style={'width': '48%', 'display': 'inline-block'}
#  )