import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
import plotly.figure_factory as ff
import plotly.plotly as py
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
import csv,os
app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

######### LOADING DATA
path_to_data = 'data/'
BACKGROUND = 'rgb(230, 230, 230)'




def plot_net(g,gs_name,pval):
    pos=nx.fruchterman_reingold_layout(g)
    N = nx.number_of_nodes(g)
    labels = [str(u[0]) for u in g.nodes(data=True)]
    d = g.degree().values()
#     hover_text = ["%s <br> Pvalue: 10e-%f"%i for i in zip(labels,colors)]
    hover_text = ["%s <br> "%i for i in labels]
    
    Xv=[pos[k][0] for k in g.nodes()]
    Yv=[pos[k][1] for k in g.nodes()]
    Xed=[]
    Yed=[]
    for edge in nx.edges(g):
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None] 

    ### plotting setting

    trace3=Scatter(x=Xed,
                   y=Yed,
                   mode='lines',
                   line=Line(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   )

    trace4=Scatter(x=Xv,
                   y=Yv,
                   mode='markers',
                   name='net',
                   marker=Marker(symbol='dot',
                                 size=20, 
                                 color=d,
                                  colorscale='Viridis',
                                  showscale=True,
                                  colorbar = dict(
                                             title = 'Gene association, -log(pvalue)',
                                             titleside = 'top',
                                             tickmode = 'array',
#                                              ticktext = color_map.keys(),
#                                              tickvals = list(set(colors)),
                                             ticks = 'outside'
                                         ),
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=hover_text,
                   hoverinfo='text'
                   )

    annot="Size of nodes is proportional to gene degree in the network."

    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title='' 
              )

    layout=Layout(title= "Disease module for <b>"+ gs_name +"</b>,",
        titlefont=dict(
            family='Courier New, monospace',
            size=12
#             color='#7f7f7f'
        ),
        font= Font(size=12),
        showlegend=False,
        autosize=False,
        width=350,
        xaxis=XAxis(axis),
        yaxis=YAxis(axis),          
        margin=dict(b=40,l=5,r=10,t=40),
        hovermode='closest',
        annotations=Annotations([
               Annotation(
               showarrow=False, 
                text='This igraph.Graph has the Kamada-Kawai layout',  
                xref='paper',     
                yref='paper',     
                x=0,  
                y=-0.1,  
                xanchor='left',   
                yanchor='bottom',  
                font=Font(
                size=14 
                )     
                )
            ]),           
        )

    data1=Data([trace3, trace4])
    fig1=Figure(data=data1, layout=layout)
    fig1['layout']['annotations'][0]['text']=annot
    return fig1


def trait_sim_graph():
    g = nx.read_graphml(path_to_data+'trait_similarity_network.graphml')
    pos=nx.fruchterman_reingold_layout(g)
    N = nx.number_of_nodes(g)
    labels = [str(u[1]['name']) for u in g.nodes(data=True)]
    d = g.degree().values()

    Xv=[pos['n'+str(k)][0] for k in range(N)]
    Yv=[pos['n'+str(k)][1] for k in range(N)]
    Xed=[]
    Yed=[]
    for edge in nx.edges(g):
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None] 
    
    ### plotting setting

    trace3=Scatter(x=Xed,
                   y=Yed,
                   mode='lines',
                   line=Line(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   )

    trace4=Scatter(x=Xv,
                   y=Yv,
                   mode='markers',
                   name='net',
                   marker=Marker(symbol='dot',
                                 size=[20+i for i in d], 
                                 color=d,
                                colorscale='Viridis',
                                 showscale=False,
                                 colorbar = dict(
                                            title = 'Number of modules',
                                            titleside = 'top',
                                            tickmode = 'array',
                                            ticks = 'outside'
                                        ),
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=labels,
                   hoverinfo='text'
                   )

    annot="This networkx.Graph has the Fruchterman-Reingold layout<br>Code:"+    "<a href='http://nbviewer.ipython.org/gist/empet/07ea33b2e4e0b84193bd'> [2]</a>"

    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title='' 
              ),

    layout=Layout(
                title='<br>Network of Phenotypes',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=40,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Source: <a href='https://www.biorxiv.org/content/early/2018/02/15/265553'> Open Community Challenge Reveals Molecular Network Modules with Key Roles in Diseases</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False),
                width= 450)
    data1=Data([trace3, trace4])
    fig1=Figure(data=data1, layout=layout)
    return fig1

###### LOADING DATA

df =pd.read_csv(path_to_data+'SC1_sig_disease_modules_with_consensus_new_gwas_cat_04042018.txt')
annotations = pd.read_csv(path_to_data+'annotationEnrichment_terms_sig_modules_05042018.txt',low_memory=False)

# graph_list= {}
# for f in os.listdir(path_to_data+'/networks/'):
#     if f.endswith('.txt'):
#         net= '_'.join(f.split('_')[:2])
#         g= nx.read_edgelist(path_to_data+'/networks/'+f,delimiter='\t',data=(('weight',float),))
#         graph_list[net] = g

G3= nx.read_edgelist(path_to_data+'networks/3_signal_omnipath_directed.txt',delimiter='\t',data=(('weight',float),))

L = csv.reader(open(path_to_data+'SC1_sig_modules_with_consensus_23102017.txt','rU'),delimiter='\t')
sig_modules= {}
all_genes =[]
for r in L:
    teamName=r[1]
    if teamName not in sig_modules:
        sig_modules[teamName]={}
    if r[2] not in sig_modules[teamName]:
        sig_modules[teamName][r[2]]={}
    sig_modules[teamName][r[2]][int(r[3])]=r[4:]
    all_genes+=r[4:]


######### functions



def get_logo():
    import base64
    image_filename = 'data/banner_vis.jpg' # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    logo = html.Div([

        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), height='150', width='1000')
        ], className="ten columns padded"),

        

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Disease Pathways')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/overview', className="tab first"),

        dcc.Link('Disease Pathways   ', href='/disease-pathways', className="tab"),

        dcc.Link('Enrichment Analysis   ', href='/enrichment-analysis', className="tab"),
        
        dcc.Link('Contact us   ', href='/contact-us', className="tab")

        

    ], className="row ")
    return menu

def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def filter_data(selection):
    df_subset = df.loc[df['trait.simplified'].isin(selection)].sort_values(['pval','module_size']).reset_index()
    return df_subset.rename(columns={'module_size':'Module Size','pval':'Pvalue','index':'Module ID','net':'Network'})
def filter_annotation(x):
    res = annotations[(annotations['teamName']==x[0])  & (annotations['net']==x[1]) & (annotations['mid']==x[2])].iloc[:,[2,5]]
    return res.rename({'pathwayDb':'Annotation DB','term':'Term'}).head()
