import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import *

layout = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1
            html.Div([
                html.H6('Description',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
               
                html.P(['''
                        This is platform to browse and visualize the results of ''',
                        html.A(
                            children='DREAM challenge for disease modules identification',
                            target= '_blank',
                            href='https://www.synapse.org/#!Synapse:syn6156761/wiki/',
                            
                        ),
                        ' an open competition to comprehensively assess module identification methods across diverse gene, \
                        protein and signaling networks. Predicted network modules,association with complex traits and diseases are visualized through this platform.'
                    ])
                       
                       
            ], className="row"),
            # Row 2
            html.Div([
                html.Div([
                html.H6('Disease Pathways Network',
                          className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P('HOVER over nodes in the graph below to see the information about pathways related to the selected phenotype.'),
                dcc.Graph(
                id='graph-phenotype_network',
                style=dict(width='700px'),
                figure= trait_sim_graph()
                ), 
                ], className='eight columns',style=dict(textAlign='center')),
                html.Div([
                html.H6('Pathway informations',
                          className="gs-header gs-text-header padded"),
                html.Br([]),
                dcc.Graph(
                id='graph-phenotype_hist'
                ), 
                ], className='four columns',style=dict(textAlign='center'))  
            ], className="row "),

        ], className="subpage")

    ], className="page")
