import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import style_recommendations as sr

#sites_df = pd.read_csv('stablishments_catalog.csv')
sites_df = pd.read_csv('Catálogos - Establecimientos.csv')
sites_df['Latitud'] = sites_df['Latitud'].str.replace(',','.').astype(np.float64)
sites_df['Longitud'] = sites_df['Longitud'].str.replace(',','.').astype(np.float64)

px.set_mapbox_access_token(open("mapbox_token.txt").read())
token = open("mapbox_token.txt").read()

colors_imagotipo = {'yellow': '#e5b622',
                    'brown': '#623812',
                    'grey_l': '#e4e4e4',
                    'grey_m': '#B4AA99'}

beers_dict = {'Bohemia Oscura': 'Boh_Osc',
              'Corona': 'Cor',
              'Dos Equis Ambar': 'Dos_Equ_Amb',
              'Dos Equis Laguer': 'Dos_Equ_Lag',
              'Indio': 'Ind',
              'Modelo Especial': 'Mod_Esp',
              'Negra Modelo': 'Neg_Mod',
              'Sol': 'Sol',
              'Tecate Light': 'Tec_Lig',
              'Victoria': 'Vic'}

lager_dict = {'Pilsner': 'Pil',
              #'Pale Lager': 'Pal_Lag',
              'Amber Lager': 'Amb_Lag',
              'Bock': 'Boc',
              'Dark Lager': 'Dar_Lag'}

lager_colors = {'Pilsner': '#F7F1AE',
                'Amber Lager': '#BB5B18',
                'Bock': '#8C2D11',
                'Dark Lager': '#480F08'}

ale_dict = {'Wheat Beer':'Whe_Bee',
            'Pale Ale': 'Pal_Ale',
            'Indian Pale Ale': 'Ind_Pal_Ale',
            'Strong Ale': 'Str_Ale',
            'Brown Ale': 'Bro_Ale',
            'Stout': 'Sto'}

ale_colors = {'Wheat Beer':'#EDC15A',
              'Pale Ale': '#DB8D19',
              'Indian Pale Ale': '#BB5C18',
              'Strong Ale': '#A03B15',
              'Brown Ale': '#791E0E',
              'Stout': '#050101'}
#---------------------------------------------------------------------------------------------------
tpu_card = dbc.Card(dbc.CardBody([html.P("¿No sabes qué beber?"),
                                  html.P("Usemos tu opinión sobre cervezas comerciales para recomendarte estilos de artesanales."),
                                  html.P('Califica las cervezas, del 1 (no me gusta) al 5 (me encanta). Las que no conozcas márcalas como sin respuesta (SR).')]),
                    style={'height': '100%'})

upt_card = dbc.Card(dbc.CardBody([html.P("¿Ya sabes qué estilos te gustan más?"),
                                  html.P("Compártenos tus gustos de cervezas y estilos para  ayudar a recomendar estilos a usuarios nuevos.")]),
                    style={'height': '100%'})

hp_card = dbc.Card(dbc.CardBody([html.P("¿No sabes dónde ir a beber?"),
                                 html.P("Checa el mapa de sitios junto con sus respectivas redes y horarios.")]),
                    style={'height': '100%'})

beer_marks = {0: 'SR',
              1: '1',
              2: '2',
              3: '3',
              4: '4',
              5: '5'}

beer_inputs = []
for bc in beers_dict.keys():
    bc_input = html.Div([dbc.Row([dbc.Label(bc,
                                            width=3,
                                            style={'text-align': 'right'}),
                                  dbc.Col([dcc.Slider(min=0,max=5,step=None,
                                                      value=0,
                                                      id=beers_dict[bc]+'_input',
                                                      marks=beer_marks)],
                                          width=7)]),
                         html.Hr()])
    beer_inputs.append(bc_input)

beer_form = dbc.Form(beer_inputs)

comercial = dbc.Row(dbc.Col([beer_form],
                            width={"size": 10, "offset": 1},
                            style={"margin-bottom": "15px"}))

tpu_button = html.Div([dbc.Button("Obtener Recomendaciones",
                                  id='compute',
                                  color="primary",
                                  n_clicks=0)],
                      style={"margin-bottom": "20px"},
                      className="d-grid gap-2 col-6 mx-auto")

graph_card = dbc.Card(dbc.CardBody([html.H4("¿Qué tan afín eres a cada estilo?"),
                                    html.P("Mientras más alto el valor, más probable es que te guste una cerveza de ese estilo. La línea punteada indica el promedio")]),
                      color="light",
                      outline=True,
                      style={'height': '100%'})

craft_graph = dcc.Graph(id='craft-graph',
                        config={'staticPlot':True,
                                'displayModeBar': False})

tab_tpu = html.Div([dbc.Row([dbc.Col(tpu_card,
                                     width={"size": 10, "offset": 1},
                                     style={'margin-top': '10px','margin-bottom': '10px'})]),
                    comercial,
                    tpu_button,
                    html.Hr(),
                    graph_card,
                    craft_graph])

tab_upt = html.Div([dbc.Row([dbc.Col(upt_card,
                                     width={"size": 10, "offset": 1},
                                     style={'margin-top': '10px','margin-bottom': '10px'})]),
                    html.Iframe(src="https://docs.google.com/forms/d/e/1FAIpQLSe_Lv46PUgeETxOaF1Pr3T0svWMR91KAaImJXKzthY6xp-OGw/viewform?embedded=true",
                                style={'width':"100%",
                                       'height':"900px"})])

tap_dropdown = dcc.Dropdown(id='tap-dropdown',
                            options=[{'label':place, 'value':place} for place in sites_df['Nombre']],
                            value='Hermana República')

tap_networks = html.Div([html.A("Facebook",
                                id= 'tap-fb',
                                target="_blank"),
                         html.Br(),
                         html.A("Instagram",
                                id='tap-ig',
                                target="_blank")],
                        style={'textAlign': 'center'})

tab_hp = html.Div([dbc.Row(dbc.Col(hp_card,
                                   width={"size": 10, "offset": 1},
                                   style={'margin-top': '10px','margin-bottom': '10px'})),
                   dbc.Row(dbc.Col(tap_dropdown,
                                   width={"size": 10, "offset": 1},
                                   style={'margin-top': '10px','margin-bottom': '10px'})),
                   dcc.Graph(id='beer-map'),
                   tap_networks])

report = dbc.Col([dcc.Store(id='report-data'),
                  dbc.Tabs([dbc.Tab(tab_tpu,
                                    label='Todos para uno',
                                    active_label_style={'color': colors_imagotipo['brown']},
                                    activeTabClassName='active'),
                            dbc.Tab(tab_upt,
                                    label='Uno para todos',
                                    active_label_style={'color': colors_imagotipo['brown']},
                                    activeTabClassName='active'),
                            dbc.Tab(tab_hp,
                                    label='Hoppy places',
                                    active_label_style={'color': colors_imagotipo['brown']},
                                    activeTabClassName='active')],
                           className="nav-tabs-gestor"),
                  html.Div(id='data-analysis')],
                 width=12)
#---------------------------------------------------------------------------------------------------
app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
server = app.server
app.layout = html.Div([html.H1('Chelasabe',
                               style={'textAlign': 'center',
                                      'color': colors_imagotipo['yellow']}),
                       html.H1('"Pienso, luego pisto"',
                               style={'textAlign': 'center',
                                      'color': colors_imagotipo['yellow']}),
                       report,
                       dcc.Location(id="url")])
#---------------------------------------------------------------------------------------------------
def render_recommendations(style_scores):
    style_avg = sum(style_scores) / len(style_scores)
    fig = go.Figure()

    fig.add_trace(go.Bar(y=[['Lagers'] * 4, list(lager_dict.keys())],
                         x=style_scores[:4],
                         orientation='h',
                         marker=dict(color=list(lager_colors.values()))))

    fig.add_trace(go.Bar(y=[['Ales'] * 6, list(ale_dict.keys())],
                         x=style_scores[4:],
                         orientation='h',
                         marker=dict(color=list(ale_colors.values()))))

    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=style_avg / 5,
                  y0=0,
                  x1=style_avg / 5,
                  y1=1,
                  line=dict(color=colors_imagotipo['yellow'],
                            width=2,
                            dash='dot'))

    fig.update_layout(showlegend=False,
                      height=500,
                      xaxis=dict(title='Afinidad',
                                 titlefont_size=16,
                                 tickfont_size=14,
                                 dtick=1.0),
                      margin=dict(l=20,
                                  r=20,
                                  b=20,
                                  t=0),
        template='seaborn')

    fig.update_xaxes(range=[0, 5],
                     constrain='domain')

    return fig
#---------------------------------------------------------------------------------------------------
@app.callback(Output('craft-graph', 'figure'),
              Input('compute', 'n_clicks'),
              [State(beers_dict[bc]+'_input', 'value') for bc in beers_dict.keys()])
def com_rec(n_clicks, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10):
    if n_clicks == 0:
        return render_recommendations([0] * 10)
    else:
        form = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
        rec = sr.drink_team_rec(form)
        return render_recommendations(rec)

@app.callback(Output('beer-map', 'figure'),
              Output('tap-fb', 'href'),
              Output('tap-ig', 'href'),
              Input('tap-dropdown', 'value'))
def update_map(tap):
    tap_df = sites_df[sites_df.Nombre == tap]

    fig = go.Figure(go.Scattermapbox(mode="markers",
                                     lon=tap_df['Longitud'].values,
                                     lat=tap_df['Latitud'].values,
                                     text=tap_df['Horario'].values,
                                     textposition='bottom center',
                                     hovertemplate='Horario: %{text}<extra></extra>',
                                     marker={'size': 15,
                                             'symbol': "beer",
                                             'color': colors_imagotipo['yellow']}))

    fig.update_layout(mapbox={'accesstoken': token,
                              'style': "streets",
                              'center': {'lat': tap_df['Latitud'].values[0],
                                         'lon': tap_df['Longitud'].values[0]},
                              'zoom': 14},
                      showlegend=False,
                      margin=dict(t=20, b=20, l=0, r=0))

    return fig, tap_df['Facebook'].values[0], tap_df['Instagram'].values[0]
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()