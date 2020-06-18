import dash
import plotly
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SUPERHERO])
df = pd.read_csv('test.csv')

colors = sorted(['rgb(255,127,80)', 'rgb(255,160,122)','rgb(255,140,0)', 'rgb(119,136,153)',
          'rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(255,228,225)'
          'rgb(99, 79, 37)','rgb(129, 180, 179)', 'rgb(124, 103, 107)',
          'rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
          'rgb(175, 49, 35)', 'rgb(36, 73, 147)', 'rgb(146, 123, 21)', 
          'rgb(177, 180, 34)', 'rgb(206, 206, 40)', 'rgb(158, 202, 225)'],
          key = lambda x: int((x.split(',')[1]).strip().replace(",",'')))

def make_bar(df, machine):
    fig = go.Figure()
    if machine:
	    dff = df[df['region'] == machine[0]]
	    fig.add_bar(x = dff['city'],
	                y = dff['jobs_committed'],
	                marker = {"color": "rgb(175, 51, 21)"},
	                orientation = "v",  
	                name = 'jobs_committed')

	    fig.update_layout(xaxis={'title': 'Region', 'title.standoff': 2, 'visible': True, 'color': 'black'},
	                      yaxis={'title': 'Number of Jobs', 'title.standoff': 2,'visible': True, 'showline': True, 'showgrid': True},
	                      autosize=True,
	                      plot_bgcolor='rgb(255,255,255)',
	                      hovermode='closest',
	                      margin = {'t': 1, 'b': 1, 'pad': 2})   
    return fig


def make_pie(df, machine):
    fig = go.Figure()
    if machine:
	    dff = df[df['region'] == machine[0]]
	    fig.add_pie(labels = dff['city'],
	                values = dff['jobs_committed'],
	                marker_colors = colors,
	                title = 'Number of Jobs by Region')    
    return fig

 
def make_hist(df, machine):
    fig = go.Figure()
    if machine:
	    dff = df[df['region'] == machine[0]]    
	    fig.add_histogram(x = dff['jobs_committed'], 
	    	              marker = {"color": 'rgb(175, 51, 21)'})
	    	              
    return fig

app.layout = html.Div([
	                  html.H3('CUSA LOG FILES',
	                  	      style = {'textAlign':'left', 'margin-top': 10, 'margin-left': 10}),
	                  dbc.Row([dbc.Col(width = 0.5),
	                  	       dbc.Col(
	                  	               html.Div([
	                  		                     html.H5('Machine', style = {'textAlign':'left', 'margin-left': 20}),
	                  	                         dcc.Dropdown(id = 'machine', value = '', multi=True,
	                  	                         	          options = [{'label': i, 'value': i} for i in df['region'].unique()], 
	                  	                       	              placeholder = "Select a machine",
	                  	                       	              style = {'margin-left': 8, 'color': 'gray'})]),
	                                   width = 2),
                               dbc.Col(width = 1),
                               dbc.Col(html.Div([html.H5('Graph 1', style = {'textAlign':'left'}),
                               	                 dcc.Graph(id = 'graph1')]), #figure={'data':'', 'layout':{'title':'Graph 1'}}
                                       width = 8),
	                          ]),
	                  dbc.Row([dbc.Col(width = 3),
	                  	       dbc.Col(html.Div([html.H5('Graph 2', style = {'textAlign':'left', 'margin-top': 15}), 
	                  	       	                 dcc.Graph(id = 'graph2')]), width = 4), # figure = make_pie(df)
	                  	       dbc.Col(html.Div([html.H5('Graph 3', style = {'textAlign':'left', 'margin-top': 15}), 
	                  	       	                 dcc.Graph(id = 'graph3')]), width = 4) # figure = make_hist(df)	                  	       	          
	                  	      ]),
                      dbc.Row([dbc.Col(width = 3),
                      	       dbc.Col(html.Div([html.H5('All Data', style = {'textAlign':'left', 'margin-top': 15}),
                      	       	                 dash_table.DataTable(id = 'table1',
                      	       	                 	                  columns = [{'name': i, 'id': i, 'deletable': True} for i in df.columns],
                      	       	                 	                  # data = df.to_dict(orient = 'records'),
                      	       	                 	                  filter_action = 'native', #custom
                                                                      filter_query = '',
                                                                      # editable=True,

                                                                      sort_action = 'native', #custom 
                                                                      sort_mode = 'multi',
                                                                      sort_by = [],
                                                                      style_table = {'maxHeight': '800px',
                                                                                     'maxWidth': '1000px',
                                                                                     'overflowX': 'scroll',
                                                                                     'overflowY': 'scroll'},
                                                                      style_cell = {'maxWidth': '150px',
                                                                                    'height': '90',
                                                                                    'textAlign': 'left',
                                                                                    'textOverflow': 'ellipsis',
                                                                                    'color': 'black'},
                                                                      style_header={'fontWeight': 'bold',
                                                                                    'color':'black'}                                                                                                                    
                      	       	                 	                 )
                      	       	                ]), width = 8)

                      	      ])
	                  ])


@app.callback(
    [Output(component_id='graph1', component_property='figure'),
     Output(component_id='graph2', component_property='figure'),
     Output(component_id='graph3', component_property='figure')],
    [Input(component_id='machine', component_property='value')]
)
def update_graph(machine):
	graph1 = make_bar(df, machine)
	graph2 = make_pie(df, machine)
	graph3 = make_hist(df, machine)
	return graph1, graph2, graph3

@app.callback(
    Output(component_id='table1', component_property='data'),
   [Input(component_id='machine', component_property='value')]
)
def update_table(machine):
	if machine:
		sub_df = df[df['region'] == machine[0]].reset_index(drop=True)
		return sub_df.to_dict(orient = 'records')
	else:
		return df.to_dict(orient = 'records')
                 

if __name__ == '__main__':
	app.run_server(debug = True)

