import dash_bootstrap_components as dbc
import dash_tabulator
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import style_recommendations as sr

sites_df = pd.read_csv('stablishments_catalog.csv')
sites_df['Latitud'] = sites_df['Latitud'].str.replace(',','.').astype(np.float64)
sites_df['Longitud'] = sites_df['Longitud'].str.replace(',','.').astype(np.float64)

px.set_mapbox_access_token(open("mapbox_token.txt").read())
token = open("mapbox_token.txt").read()

colors_imagotipo = {'yellow': '#e5b622',
                    'brown': '#623812',
                    'grey_l': '#e4e4e4',
                    'grey_m': '#B4AA99'}

beer_columns = [{"title": "Cerveza",
                 "field": "beer",
                 'hozAlign': "center",
                 'headerHozAlign': "center",
                 'headerSort': False},
                {'title': "Calificación",
                 'field': "rating",
                 'formatter': "star",
                 'hozAlign': "center",
                 'headerHozAlign': "center",
                 'headerSort': False,
                 'editor': True}]

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

beer_data = [{'id': beers_dict[key], 'beer': key, 'rating': '0'} for key in beers_dict.keys()]

lager_dict = {'Pilsner': 'Pil',
              #'Pale Lager': 'Pal_Lag',
              'Amber Lager': 'Amb_Lag',
              'Bock': 'Boc',
              'Dark Lager': 'Dar_Lag'}

lager_colors = {'Pilsner': '#f9e16c',
                #'Pale Lager': '#f9e16c',
                'Amber Lager': '#ad4418',
                'Bock': '#983013',
                'Dark Lager': '#a73e16'}

ale_dict = {'Wheat Beer':'Whe_Bee',
            'Pale Ale': 'Pal_Ale',
            'Indian Pale Ale': 'Ind_Pal_Ale',
            'Strong Ale': 'Str_Ale',
            'Brown Ale': 'Bro_Ale',
            'Stout': 'Sto'}

ale_colors = {'Wheat Beer':'#f9e16c',
              'Pale Ale': '#e49c1a',
              'Indian Pale Ale': '#e49c1a',
              'Strong Ale': '#c05925',
              'Brown Ale': '#983013',
              'Stout': '#240b0b'}
#---------------------------------------------------------------------------------------------------
tpu_card = dbc.Card(dbc.CardBody([html.P("¿No sabes qué beber?"),
                                  html.P("Responde el cuestionario de cervezas para recomendarte estilos."),
                                  html.P('Usa una estrella para las que no te gustan, y cinco para las que más te gustan. Las cervezas que no conozcas déjalas sin estrellas.')]),
                    style={'height': '100%'})

upt_card = dbc.Card(dbc.CardBody([html.P("¿Ya sabes qué estilos te gustan más?"),
                                  html.P("Responde los cuestionarios de cervezas y estilos para  ayudar a recomendar estilos a usuarios nuevos.")]),
                    style={'height': '100%'})

hp_card = dbc.Card(dbc.CardBody([html.P("¿No sabes dónde ir a beber?"),
                                 html.P("Checa el mapa de sitios junto con sus respectivas redes y horarios.")]),
                    style={'height': '100%'})

beer_form = dash_tabulator.DashTabulator(id='beer-form',
                                         columns=beer_columns,
                                         data=beer_data)

comercial = dbc.Row(dbc.Col([beer_form],
                            width={"size": 10, "offset": 1},
                            style={"margin-bottom": "15px"}))

tpu_button = dbc.Row(dbc.Col([dbc.Button("Obtener Recomendaciones",
                                         id='compute',
                                         color="primary",
                                         n_clicks=0)],
                             width={'size':4,'offset':4},
                             style={"margin-bottom": "20px"}))

craft_graph = dcc.Graph(id='craft-graph')

tab_tpu = html.Div([dbc.Row([dbc.Col(tpu_card,
                                     width={"size": 10, "offset": 1},
                                     style={'margin-top': '10px','margin-bottom': '10px'})]),
                    comercial,
                    tpu_button,
                    craft_graph])

tab_upt = html.Div([dbc.Row([dbc.Col(upt_card,
                                     width=12)])])

tap_dropdown = dcc.Dropdown(id='tap-dropdown',
                            options=[{'label':place, 'value':place} for place in sites_df['Nombre']],
                            value='Apóstol Tap Room')

tap_networks = html.Div([html.A("Facebook",
                                id= 'tap-fb',
                                target="_blank"),
                         html.Br(),
                         html.A("Instagram",
                                id='tap-ig',
                                target="_blank")],
                        style={'textAlign': 'center'})
tab_hp = html.Div([dbc.Row([hp_card,
                            tap_dropdown,
                            dcc.Graph(id='beer-map'),
                            tap_networks])])

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
app.layout = html.Div([html.H1('Chelasabe: "Pienso, luego pisto"',
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

    fig.update_layout(title='Recomendaciones de Estilos',
                      title_x=0.5,
                      showlegend=False,
                      xaxis=dict(title='Afinidad',
                                 titlefont_size=16,
                                 tickfont_size=14,
                                 dtick=1.0),
                      margin=dict(l=20,
                                  r=20,
                                  b=20,
                                  t=30))

    fig.update_xaxes(range=[0, 5],
                     constrain='domain')

    return fig
#---------------------------------------------------------------------------------------------------
@app.callback(Output('craft-graph', 'figure'),
              Input('compute', 'n_clicks'),
              [State('beer-form', 'data')])
def com_rec(n_clicks, beer_ratings):
    if n_clicks == 0:
        return render_recommendations([0] * 10)
    else:
        form = [float(beer['rating']) for beer in beer_ratings]
        rec = sr.drink_team_rec(form)
        return render_recommendations(rec)

@app.callback(Output('beer-map', 'figure'),
              Input('tap-dropdown', 'value'))
def update_map(tap):
    tap_df = sites_df[sites_df.Nombre == tap]

    fig = go.Figure(go.Scattermapbox(mode="markers+text",
                                     lon=tap_df['Longitud'].values,
                                     lat=tap_df['Latitud'].values,
                                     text=tap_df['Nombre'].values[0],
                                     textposition='bottom center',
                                     marker={'size': 15,
                                             'symbol': "beer",
                                             'color': 'rgb(229, 182, 34)'}))

    fig.update_layout(mapbox={'accesstoken': token,
                              'style': "streets",
                              'center': {'lat': tap_df['Latitud'].values[0],
                                         'lon': tap_df['Longitud'].values[0]},
                              'zoom': 13},
                      showlegend=False,
                      margin=dict(t=20, b=20, l=0, r=0))

    return fig
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()