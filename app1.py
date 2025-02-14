import pandas as pd
import dash 
from dash import html, dcc, Dash, Input, Output
import plotly.express as px
import plotly.graph_objects as go

##### Load Data###
iris = px.data.iris()
df = pd.DataFrame(iris, columns=iris.columns)

##### Charts ####
def create_histogram(df, x, color):
    fig = px.histogram(df, x=x, color=color)
    fig.update_layout(
        title="Histogram",
        xaxis_title=x,
        yaxis_title="Frequency",
        legend_title=color,
        plot_bgcolor='#e5ecf6',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    return fig

def create_scatter(data, x, y, color):
    

    if x == y:
        return go.Figure()  # Return an empty figure if x and y are the same
        
    fig = px.scatter(data, x=x, y=y, color=color)
    fig.update_layout(
        title="Scatter Plot",
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color,
        plot_bgcolor='#e5ecf6',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )  
    return fig

def create_pie_chart(data, names, values):
    fig = go.Figure(data=[go.Pie(labels=names, values=values)])
    fig.update_layout(
        title="Pie Chart",
        plot_bgcolor='#e5ecf6',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )  
    return fig

def create_bar_chart(data, x, y, color):
    fig = px.bar(data, x=x, y=y, color=color)
    fig.update_layout(
        title="Bar Chart",
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color,
        plot_bgcolor='#e5ecf6',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )  
    return fig

#### widgets ####
hist_dropdown = dcc.Dropdown(
    id='hist_dropdown',
    options=[{'label': i, 'value': i} for i in df.columns if i != 'species'],
    value='sepal_length', clearable=False,
    className='dropdown text-dark p-2'
)

x_axis = dcc.Dropdown(
    id='x_axis',
    options=[{'label': i, 'value': i} for i in df.columns if i != 'species'],
    value='sepal_length', clearable=False,
    className='dropdown text-dark p-2'
)

y_axis = dcc.Dropdown(
    id='y_axis',
    options=[{'label': i, 'value': i} for i in df.columns if i != 'species'],
    value='sepal_width', clearable=False,
    className='dropdown text-dark p-2'
)   

avg_dropdown = dcc.Dropdown(
    id='avg_dropdown',
    options=[{'label': i, 'value': i} for i in df.columns if i != 'species'],
    value='sepal_length', clearable=False,
    className='dropdown text-dark p-2'
)

###### layout ####
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sidebar = html.Div(
    [
        html.H1("Iris Dataset", className="display-4 text-center"),
        html.Hr(),
        html.P("Select the feature to plot", className="lead text-center"),
        html.Br(),
        html.H5("Histogram", className="text-center"),
        hist_dropdown,
        
        #html.Br(),
        html.H5("Scatter Plot", className="text-center"),
        html.P("X-axis"),   
        x_axis,
        html.P("Y-axis"),
        y_axis,
        #html.Br(),
        html.H5("Bar Chart", className="text-center"), 
        avg_dropdown
    ],
    className="col-2 bg-dark border-right text-white",
    style={"height": "100vh", "width": "20%", "position": "fixed", "top": 0, "left": 0, "overflow-x": "hidden", "padding-top": "20px"}
)

main = html.Div(children=[
    html.Br(),
    html.H1("Iris Dataset", className="display-4 text-center"),
    html.Hr(),
    html.Div([
        dcc.Graph(id='histogram', className='col-6'),
        dcc.Graph(id='scatter', className='col-6'),
    ], className="row"),
    html.Div(children=[
        
        dcc.Graph(id='bar_chart', className='col-6'),
        dcc.Graph(id='pie_chart', className='col-6')
    ], className="row")
], className="col-10", style={"margin-left": "20%"})

app.layout = html.Div(children=[
    html.Div(children=[sidebar, main], className="row")
], className="container-fluid", style={"height": "100vh"})

###### callbacks ####
@app.callback(
    Output('histogram', 'figure'),
    Input('hist_dropdown', 'value')
)
def update_histogram(selected_feature):
    return create_histogram(df, selected_feature, 'species') 

@app.callback(
    Output('scatter', 'figure'),
    [Input('x_axis', 'value'), Input('y_axis', 'value')]
)
def update_scatter(x, y):
    return create_scatter(df, x, y, 'species')  

@app.callback(
    Output('pie_chart', 'figure'),
    Input('avg_dropdown', 'value')
)
def update_pie_chart(selected_feature):
    return create_pie_chart(df, df['species'], df[selected_feature])    

@app.callback(
    Output('bar_chart', 'figure'),
    Input('avg_dropdown', 'value')
)
def update_bar_chart(selected_feature):
    return create_bar_chart(df, 'species', selected_feature, 'species') 

##### run server ####
if __name__ == '__main__':
    app.run_server(debug=True, port=8086)
