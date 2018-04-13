'''
Created on Apr 10, 2018

@author: schoobdar
'''
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from dash.dependencies import Input, Output
from app import *

def jaccard_overlap(m1,m2):
    return 1.* len(set(m1).intersection(m2))/len(set(m1).union(m2))

# total number of genes 
def find_enriched_module(selected_m):
    M =len(set(all_genes))
    from scipy.stats import hypergeom
    N = len(selected_m) # sample size
    overlap_profile=[]
    for m,i  in sig_modules.iteritems():
        for n,j in i.iteritems():
            for l,k in j.items():
                d= jaccard_overlap(k,selected_m)
                l_intersect = len(set(selected_m).intersection(k))
                l_n= len(k)
                if d>0:
                    pval = hypergeom.sf(l_intersect-1, M, l_n, N)
                    overlap_profile.append([m,n,l,l_intersect,d,pval])
                
    mp = pd.DataFrame(overlap_profile)
    mp.columns=['teamName','network','mid','intersection','Jaccard','pvalue']
    res = mp[mp.pvalue*mp.shape[0]<0.05]
    res['-log(p)'] = res.pvalue.apply(lambda x:round(-1*np.log10(x),1))
    return res.iloc[:,[1,3,4,6]].sort_values('-log(p)',ascending=False)
 


layout = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1
            html.Div([
                html.H6('Disease Module Enrichment Analysis',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("Enter a list of gene symboles, comma seperated and press submit."),
                dcc.Input(id='input-box', type='text'),
                html.Button('Submit', id='button'),
            ], className="row"),
            # Row 2
            html.Div([
                html.H6('List of disease modules that the input gene list is enriched in.',
                        className="gs-header gs-text-header padded"),
                html.Br([]),
                html.P("Select a module from list to visualize it."),
                dt.DataTable(
                      rows=[{}],
                      # optional - sets the order of columns    
                      row_selectable=True,
                      filterable=True,
                      sortable=True,
                      selected_row_indices=[],
                      id='datatable-enrichedModules'
                        )
            ], className="row "),
            # Row 3
            html.Div([

                html.Div([
                    html.H6(["Selected module graph"], className="gs-header gs-text-header padded"),
                    dcc.Graph(
                            id='graph-traitModule-en',
                            )
                    ], className=" six columns"),
                html.Div([
                    html.H6(["Annotated terms"],
                            className="gs-header gs-text-header padded"),
                    html.Table(id='datatable-annotationTerms-en')
                    ], className="six columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")



@app.callback(
    dash.dependencies.Output('datatable-enrichedModules', 'rows'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_enriched_modules(n_clicks, value):
    import re
    print  value
    query_set = filter (lambda x:x!='' and x is not None,map(lambda x:re.sub('[^A-Za-z0-9]+', '',str(x)).upper(),value.split(',')))
    print query_set
    return find_enriched_module(query_set).to_dict('records')


@app.callback(
    Output('graph-traitModule-en', 'figure'),
    [Input('datatable-enrichedModules', 'rows'),
     Input('datatable-enrichedModules', 'selected_row_indices')])
def update_figure_enrichment(rows, selected_row_indices):
    res = rows[0]
    pval = res['pvalue']
    selected_m = sig_modules[res['teamName']][res['network']][res['mid']]
#     sg= graph_list[ind[1]].subgraph(selected_m)
    sg = G3.subgraph(selected_m)
    return plot_net(sg,res['network'],pval)

@app.callback(
    Output('datatable-annotationTerms-en', 'children'),
    [Input('datatable-enrichedModules', 'rows'),
     Input('datatable-enrichedModules', 'selected_row_indices')])
def update_anno_table_en(rows, selected_row_indices):
    import re
    res = rows[0]
    ind =[str(res['teamName']),str(res['network']),int(res['mid'])]
    print res
    print selected_row_indices
    print ind
    print filter_annotation(ind)
    return make_dash_table(filter_annotation(ind))
