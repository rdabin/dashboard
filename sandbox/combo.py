import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.metrics_calculator import metrics_calculator as mc
from src.data_builder import data_builder

TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'

raw_data = data_builder.create_sample_df()
roc_data = mc.build_roc_data_fast(raw_data)

# Initialise App
app = dash.Dash()

# TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Controls
# TODO: slider marks don't display (apart from 0.5) - not sure why.
threshold_slider = dcc.Slider(id='threshold',
                              value=0.5,
                              min=0.0,
                              max=1.0,
                              step=0.01,
                              marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
                              )

# Layout.  Base stylesheet has twelve columns.
app.layout = html.Div([
    # TODO: would be nice to pin this title/slider div to the top of the window when scrolling. CSS?
    html.Div([
        html.H4(children='HODAC Threshold Explorer'),
        html.Div([threshold_slider]),
    ], className='row'),

    html.Div([
        html.Div([dcc.Graph(id='dist_figure')], className='six columns'),
        html.Div([dcc.Graph(id='pie_chart')], className='six columns')
    ], className='row'),

    html.Div([
        html.Div([dcc.Graph(id='roc_figure')], className='four columns'),
        html.Div([dcc.Graph(id='cost_figure')], className='four columns'),
        html.Div([dcc.Graph(id='histogram')], className='four columns')
    ], className='row')
])

# Callbacks
@app.callback(Output('pie_chart', 'figure'),
              [Input('threshold', 'value')])
def make_pie_figure(threshold):
    tp, fp, tn, fn = mc.confusion_matrix(raw_data, threshold)

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
            domain={"x": [0, 0.4], 'y': [0.6, 1]},
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
            domain={"x": [0.6, 1], 'y': [0.6, 1]},
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
            domain={"x": [0, 0.4], 'y': [0, 0.4]},
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
            domain={"x": [0.6, 1], 'y': [0, 0.4]},
            marker=dict(colors=[FP_COLOUR, TN_COLOUR])
        )
    ]

    figure = dict(data=data, layout=dict(autosize=True, title='Confusion Matrix Explanation'))

    return figure


@app.callback(Output('histogram', 'figure'),
              [Input('threshold', 'value')])
def make_bar_figure(threshold):
    TP, FP, TN, FN = mc.confusion_matrix(raw_data, threshold)

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


@app.callback(Output('dist_figure', 'figure'),
              [Input('threshold', 'value')])
def make_dist_figure(threshold):
    class0 = go.Histogram(
        x=raw_data[raw_data['class'] == 0].score,
        opacity=0.75
    )
    class1 = go.Histogram(
        x=raw_data[raw_data['class'] == 1].score,
        opacity=0.75
    )

    data = [class0, class1]
    layout = go.Layout(barmode='overlay')

    return go.Figure(data=data, layout=layout)


@app.callback(Output('roc_figure', 'figure'),
              [Input('threshold', 'value')])
def make_roc_figure(threshold):
    line = go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        line=dict(
            color='rgb(180, 180, 180)',
            width=1,
            dash='dash'
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

    layout = go.Layout(
        showlegend=False,
        xaxis={'type': 'linear', 'title': 'FPR'},
        yaxis={'title': 'TPR'},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

    return go.Figure(data=[line, curve], layout=layout)


@app.callback(Output('cost_figure', 'figure'),
              [Input('threshold', 'value')])
def make_cost_figure(threshold):
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

    layout = go.Layout(
        showlegend=False,
        xaxis={'type': 'linear', 'title': 'threshold'},
        yaxis={'title': 'cost'},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

    return go.Figure(data=[curve], layout=layout)


if __name__ == '__main__':
    app.run_server()
