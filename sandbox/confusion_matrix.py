import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.data_builder import data_builder
from src.metrics_calculator import metric_calculations as mc

df = data_builder.create_sample_df()

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
                    marks={0: '0', 0.5: '0.5', 1: '1'})

app.layout = html.Div([dcc.Graph(id='example_graph'),
                       slider])


# Selectors, main graph -> pie graph
@app.callback(Output('example_graph', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):

    TP, FP, TN, FN = mc.confusion_matrix(df, slider)

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


if __name__ == '__main__':
    app.run_server()
