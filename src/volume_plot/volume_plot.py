import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd


def generate_bar_of_dots(c1=100, c2=16, width=15):
    return pd.DataFrame([
        {
            'type': 0 if i < c1 else 1,
            'x': i % width,
            'y': i // width,
        } for i in range(0, c1 + c2 - 1)
    ])

def get_population_dots():

	dots = generate_bar_of_dots()

	return html.Div([
	    dcc.Graph(
	        id='volume1',
	        config={
	        'displayModeBar': False
	        },
	        figure={
	            'data': [
	                go.Scatter(
	                    x=dots[dots['type'] == i]['x'],
	                    y=dots[dots['type'] == i]['y'],
	                    text='foo',
	                    mode='markers',
	                    opacity=0.7,
	                    marker={
	                        'size': 10,
	                        'line': {'width': 0.5, 'color': 'white'}
	                    },
	                    name=i
	                ) for i in dots['type'].unique()
	            ],
	            'layout': go.Layout(
	                width=315,
	                height=300,
	                showlegend=False,
	                xaxis=dict(
	                    autorange=True,
	                    showgrid=False,
	                    zeroline=False,
	                    showline=False,
	                    autotick=True,
	                    ticks='',
	                    showticklabels=False
	                ),
	                yaxis=dict(
	                    autorange='reversed',
	                    showgrid=False,
	                    zeroline=False,
	                    showline=False,
	                    autotick=True,
	                    ticks='',
	                    showticklabels=False
	                )
	            )
	        }
	    )],
	    style={'width': '20%', 'display': 'inline-block'})