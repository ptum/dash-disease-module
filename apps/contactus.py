'''
Created on Apr 10, 2018

@author: schoobdar
'''

import dash_core_components as dcc
import dash_html_components as html
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
                html.H6('Contact information',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("")
            ], className="row"),
            

        ], className="subpage")

    ], className="page")
