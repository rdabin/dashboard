from dash.dependencies import Input, Output

def register_callbacks(app):

    @app.callback(
        Output(component_id='threshold', component_property='children'),
        [Input(component_id='slider', component_property='value')]
    )
    def update_text(input_value):
        return 'Threshold: "{}"'.format(input_value)
