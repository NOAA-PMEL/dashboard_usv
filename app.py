from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    # refresh=True allows the browser to reload at the new URL
    dcc.Location(id='url', refresh=True)
])

@app.callback(
    Output('url', 'href'),
    Input('url', 'pathname')
)
def update_location(pathname):
    return "https://viz.pmel.noaa.gov/usv"

if __name__ == '__main__':
    app.run(debug=True,)