# Import packages
import numpy as np
from jupyter_dash import JupyterDash
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px

class InteractivePlotMixin:
    '''Mixin class used in CellLine class for displaying an interactive plot.
    '''
    def __init_options(self, df):
        '''Initialize options for the interactive plot.
        '''
        # Cell line list
        cell_line_list = self.get_cell_line_list()

        # Cell line options; [{'label': 'Sample CL1', 'value': ['CL1-1', 'CL1-2', 'CL1-3']}]
        cell_line_options = []
        for cell_line in cell_line_list:
            exp_list = list(self.get_cell_line(cell_line).keys())
            cell_line_options.append({'label': cell_line, 'value': ', '.join(exp_list)})

        # Experiment ID options; {'cell line': 'experiment ID'}
        exp_options = {}
        for cl in cell_line_list:
            exp_lst = list(self.get_cell_line(cl).keys())
            exp_options[cl] = [exp for exp in exp_lst]
        
        # Profile options
        profile_options = [{'label': 'Concentration', 'value': 'concentration'}, 
                           {'label': 'Cumulative Concentration', 'value': 'cumulative'}, 
                           {'label': 'Specific Rate', 'value': 'spRate'}]
        
        # Species options
        species_options = df['species'].unique()
        
        # Method options for cumulative concentration and specific rate
        method_list = df['method'].unique()
        method_options = [{'label': 'Two-Point Calculation', 'value': 'twoPoint'}]
        if 'polynomial' in method_list:
            method_options.append({'label': 'Polynomial', 'value': 'polynomial'})
        if 'rollingWindowPolynomial' in method_list:
            method_options.append({'label': 'Rolling Window', 'value': 'rollingWindowPolynomial'})
        
        # Plot style options for each profile
        cl_option = {'label': 'Cell Line ID', 'value': 'cellLine'}
        exp_option = {'label': 'Experiment ID', 'value': 'runID'}
        method_option = {'label': 'Method', 'value': 'method'}

        plot_style_options = [cl_option, exp_option]
        plot_style_options2 = [cl_option, exp_option, method_option]

        options = {'cellLine': cell_line_options,
                   'runID': exp_options,
                   'species': species_options,
                   'profile': profile_options,
                   'method': method_options,
                   'style1': plot_style_options,
                   'style2': plot_style_options2}
        return options
    
    def __init_layout(self, mode, options):
        '''Initialize the layout
        '''
        # Initialize the app
        if mode=='inline':
            app = JupyterDash(__name__)
        else:
            app = Dash(__name__)

        # Get options
        cell_line_options = options['cellLine']
        exp_options = options['runID']
        species_options = options['species']
        profile_options = options['profile']
        method_options = options['method']
        plot_style_options1 = options['style1']
        plot_style_options2 = options['style2']

        #
        global radio_buttons

        # App layout
        app.layout = html.Div([
            html.Div(
                children=[
                    html.Div(
                        children=[html.Div("Cell Line: ", style={"margin-right": "10px", "font-weight": "bold"}),
                                  dcc.Dropdown(id='cell-line-dropdown',
                                               options=cell_line_options,
                                               value=[],
                                               placeholder='Select Cell Lines', 
                                               multi=True,),],
                        style={'width': '40%', 'display': 'inline-block', 'margin-right': '20px'},
                    ),
                    html.Div(
                        children=[html.Div("Experiment ID: ", style={"margin-right": "10px", "font-weight": "bold"}),
                                  dcc.Dropdown(id='experiment-dropdown',
                                               value=[],
                                               placeholder='Select Experiment ID',
                                               multi=True,),],
                        style={'width': '40%', 'display': 'inline-block'},
                    ),],
                style={'display': 'flex', 'align-items': 'center'},
            ),
            html.Hr(),
            html.Div(
                children=[html.Div("Profile: ", style={"margin-right": "10px", "font-weight": "bold"}),
                          dcc.Dropdown(id='profile-dropdown', 
                                       options=profile_options, 
                                       value=[],
                                       placeholder='Select Profiles',
                                       multi=True,),],
                style={'width': '40%', 'display': 'inline-block', 'margin-right': '20px'},
            ),
            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[html.Div("Species: ", style={"margin-right": "10px", "font-weight": "bold"}),
                                  dcc.Dropdown(id='species-dropdown',
                                               options=species_options,
                                               value=[],
                                               placeholder='Select Species', 
                                               multi=True,
                                               ),],
                        style={'width': '50%', 'display': 'inline-block', 'margin-right': '20px'},
                    ),
                    html.Div(
                        children=[html.Div("SP. Rate Method: ", style={"margin-right": "10px", "font-weight": "bold"}),
                                  dcc.Dropdown(id='method-dropdown', 
                                               options=method_options, 
                                               value=[],
                                               placeholder='Select Method',
                                               multi=True,
                                               ),],
                        style={'width': '50%', 'display': 'inline-block'},
                    ),],
                style={'display': 'flex', 'align-items': 'center'},
            ),
            html.Hr(),
            html.Div(children=radio_buttons, id='radio-container', style={'display': 'flex', 'flex-direction': 'row'}),
            html.Hr(),
            # Display
            html.Div(id='figure-container'),
        ])
        return app

    def interactive_plot(self, mode='inline'):
        '''Interactive Plot.
        '''
        # Initialization
        df = self.get_plot_data() # Get data for plotting
        self._plot_data = df
        options = self.__init_options(df=df)
        app = self.__init_layout(mode=mode, options=options)

        # Update expriment ID dropdown
        app.callback(
            Output(component_id='experiment-dropdown', component_property='options'),
            Input(component_id='cell-line-dropdown', component_property='value'),
        )(self.__set_exp_options)

        # Update graph style options
        '''app.callback(
            Output('radio-container', 'children'),
            Input('profile-dropdown', 'value'),
        )(self.__update_radio_buttons)'''

        # Update profiles to dosplay
        app.callback(
            Output('figure-container', 'children'),
            Input('profile-dropdown', 'value'),
            Input('experiment-dropdown', 'value'),
            Input('species-dropdown', 'value'),
            Input('method-dropdown', 'value'),
            Input('color-option-1', 'value'),
            Input('color-option-2', 'value'),
            Input('color-option-3', 'value'),
            Input('line-option-1', 'value'),
            Input('line-option-2', 'value'),
            Input('line-option-3', 'value'),
            Input('symbol-option-1', 'value'),
            Input('symbol-option-2', 'value'),
            Input('symbol-option-3', 'value'),
            Input('legend-radio', 'value'),
            State('cell-line-dropdown', 'value')
        )(self.__display_profiles)

        # Start the app
        if mode=='inline':
            app.run_server(mode="inline")
        else:
            app.run_server()
        
    
    def __set_exp_options(self, cl_chosen):
        '''Update expriment ID dropdown
        '''
        options = []
        if cl_chosen==[]:
            return options
        
        for cl in cl_chosen:
            for exp in cl.split(', '):
                options.append({'label': exp, 'value': exp})
        return options
    
    def __update_radio_buttons(self, selected_options):
        '''Update graph style option buttons for each profile.
        '''
        radio_buttons = []
        if 'concentration' in selected_options:
            radio_buttons.append(html.Div([
                html.Label('Concentration Graph Style', style={"font-weight": "bold"}),
                html.Br(),
                html.Label('Color'),
                dcc.RadioItems(
                    id='color-option-1',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}], 
                    value='cellLine',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Line'),
                dcc.RadioItems(
                    id='line-option-1',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}],
                    value='runID',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Symbol'),
                dcc.RadioItems(
                    id='symbol-option-1',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}],
                    value='cellLine',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                )
            ], style={'margin-bottom': '20px', 'margin-right': '40px'}))

        if 'cumulative' in selected_options:
            radio_buttons.append(html.Div([
                html.Label('Cumulative Concentration Graph Style', style={"font-weight": "bold"}),
                html.Br(),
                html.Label('Color'),
                dcc.RadioItems(
                    id='color-option-2',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}], 
                    value='cellLine',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Line'),
                dcc.RadioItems(
                    id='line-option-2',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}],
                    value='runID',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Symbol'),
                dcc.RadioItems(
                    id='symbol-option-2',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'}],
                    value='runID',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                )
            ], style={'margin-bottom': '20px', 'margin-right': '40px'}))

        if 'spRate' in selected_options:
            radio_buttons.append(html.Div([
                html.Label('Specific Rate Graph Style', style={"font-weight": "bold"}),
                html.Br(),
                html.Label('Color'),
                dcc.RadioItems(
                    id='color-option-3',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'},
                             {'label': 'Method', 'value': 'method'}], 
                    value='cellLine',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Line'),
                dcc.RadioItems(
                    id='line-option-3',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'},
                             {'label': 'Method', 'value': 'method'}],
                    value='runID',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                ),
                html.Label('Symbol'),
                dcc.RadioItems(
                    id='symbol-option-3',
                    options=[{'label': 'Cell Line', 'value': 'cellLine'},
                             {'label': 'Run ID', 'value': 'runID'},
                             {'label': 'Method', 'value': 'method'}],
                    value='method',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                )
            ], style={'margin-bottom': '20px', 'margin-right': '40px'}))

        return radio_buttons
    
    def __display_profiles(self, profiles, run_ids, species, method, 
                           color_1, color_2, color_3, 
                           line_1, line_2, line_3,
                           symbol_1, symbol_2, symbol_3, 
                           legend, cell_line,):
        '''Display profiles. 
        '''
        if not (run_ids and species and profiles and cell_line):
            return None
        # Filtering data
        df = self._plot_data
        df = filter_data(df, 'species', species)
        df = filter_data(df, 'runID', run_ids)
        
        # Creating figures
        figures = {}
        if 'concentration' in profiles:
            data = filter_data(df, 'profile', ['concentration'])
            data = filter_data(data, 'kind', ['beforeFeed', 'afterFeed'])
            fig = create_figure(data, 'line', True, 'Concentration', color_1, line_1, symbol_1, legend)
            fig = rename_yaxis(data, fig, 'concentration')
            figures['figure1'] = fig

        if 'cumulative' in profiles:
            data = filter_data(df, 'profile', ['cumulative'])
            data1 = filter_data(data, 'method', ['twoPoint'])
            data2 = filter_data(data, 'method', ['polynomial'])

            fig1 = create_figure(data1, 'scatter', False, 'Cumulative Concentration', color_2, line_2, symbol_2, legend)
            fig2 = create_figure(data2, 'line', False, 'Cumulative Concentration', color_2, line_2, None, legend)
            for fig_data in fig2.data:
                fig1.add_trace(fig_data)
            fig = rename_yaxis(data2, fig1, 'cumulative')
            figures['figure2'] = fig

        if 'spRate' in profiles and method:
            data = filter_data(df, 'profile', ['spRate'])
            data = filter_data(data, 'method', method)
            fig = create_figure(data, 'line', True, 'Specific Rate', color_3, line_3, symbol_3, legend)
            fig = rename_yaxis(data, fig, 'spRate')
            figures['figure3'] = fig
        
        # Create children
        children = [dcc.Graph(figure=fig, id=id) for id, fig in figures.items()]
        return [html.Div(
                    style={'overflow-x': 'scroll', 'display': 'flex'},
                    children=children,
                ),]
    
def create_figure(df, kind, makers, title, color, line_dash, symbol, legend):
    '''Create a figure of plotly.express
    '''
    if kind=='line':
        fig = px.line(df, x='runTime', y='value', title=title, facet_row='species',
                      markers=makers,
                      color=color,
                      line_dash=line_dash,
                      symbol=symbol,
                      )
        
    elif kind=='scatter':
        fig = px.scatter(df, x='runTime', y='value', title=title, facet_row='species',
                         color=color,
                         symbol=symbol,
                         )
    
    fig.update_yaxes(matches=None)
    fig.for_each_annotation(lambda a: a.update(visible=False))

    spc_list = df['species'].unique()
    height_per_row = 500
    fig.update_layout(height=height_per_row * len(spc_list), width=800)

    if legend=="on":
        fig.update_layout(showlegend=True, legend_x=1, legend_y=1)
    else:
        fig.update_layout(showlegend=False)
    return fig

def filter_data(df, column, values):
    '''
    '''
    return df[df[column].isin(values)]

def rename_yaxis(df, fig, profile):
    '''Rename y-axis nanme.
    '''
    spc_list = df['species'].unique()
    yaxis_titles = {}
    for s in spc_list:
        if profile=='concentration':
            if s=='product':
                unit = '(mg/l)'
            else:
                unit = '(mM)'
            yaxis_titles[s] = f"{s.capitalize()} {unit}"
        elif profile=='cumulative':
            if s=='product':
                unit = '(mg)'
            else:
                unit = '(mmol)'
            yaxis_titles[s] = f"{s.capitalize()} {unit}"
        else: # spRate
            if s=='product':
                unit = '(mg/10^9 cell/hr)'
            else:
                unit = '(mmol/10^9 cell/hr)'
            yaxis_titles[s] = f"{s.capitalize()} {unit}"

    for i, annotation in enumerate(fig.layout.annotations):
        yaxis = 'yaxis' + str(i + 1)
        fig['layout'][yaxis]['title']['text'] = yaxis_titles[annotation.text.split('=')[-1]]
    return fig

radio_buttons = []
radio_buttons.append(html.Div([
    html.Label('Concentration Graph Style', style={"font-weight": "bold"}),
    html.Br(),
    html.Div([
        html.Label('Color:  '),
        dcc.RadioItems(
            id='color-option-1',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}], 
            value='cellLine',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Line:   '),
        dcc.RadioItems(
            id='line-option-1',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}],
            value='runID',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Symbol'),
        dcc.RadioItems(
            id='symbol-option-1',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}],
            value='cellLine',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'})
], style={'margin-bottom': '20px', 'margin-right': '40px'}))

radio_buttons.append(html.Div([
    html.Label('Cumulative Concentration Graph Style', style={"font-weight": "bold"}),
    html.Br(),
    html.Div([
        html.Label('Color:  '),
        dcc.RadioItems(
            id='color-option-2',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}], 
            value='cellLine',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Line:   '),
        dcc.RadioItems(
            id='line-option-2',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}],
            value='runID',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Symbol'),
        dcc.RadioItems(
            id='symbol-option-2',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'}],
            value='runID',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        )
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
], style={'margin-bottom': '20px', 'margin-right': '40px'}))

radio_buttons.append(html.Div([
    html.Label('Specific Rate Graph Style', style={"font-weight": "bold"}),
    html.Br(),
    html.Div([
        html.Label('Color:  ', ),
        dcc.RadioItems(
            id='color-option-3',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'},
                        {'label': 'Method', 'value': 'method'}], 
            value='cellLine',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Line:   '),
        dcc.RadioItems(
            id='line-option-3',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'},
                        {'label': 'Method', 'value': 'method'}],
            value='runID',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
    html.Div([
        html.Label('Symbol: '),
        dcc.RadioItems(
            id='symbol-option-3',
            options=[{'label': 'Cell Line', 'value': 'cellLine'},
                        {'label': 'Run ID', 'value': 'runID'},
                        {'label': 'Method', 'value': 'method'}],
            value='method',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        )
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'})
], style={'margin-bottom': '20px', 'margin-right': '40px'}))

radio_buttons.append(html.Div([
    html.Label('Legend', style={"font-weight": "bold"}),
    dcc.RadioItems(
        id='legend-radio', 
        options=['on', "off"], 
        value='on', 
        inline=True,
    ),
]))