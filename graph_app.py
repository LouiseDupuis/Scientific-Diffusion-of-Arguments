"""import sys
#sys.path.insert(0,'..')
sys.path.insert(0,'../..')"""


from logging import raiseExceptions
from typing import Protocol
import dash
from matplotlib.pyplot import step
import visdcc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
# from graphs import DebateDAG,DebateGraph,DebateTree
from run_ import run_debate
import pandas as pd
import random
#### Utilities for Visualisation





def convert_to_visdcc_format(graph):
    """ Converts a networkx graph into a compatible format for visualisation with visdcc
    Returns : nodes a list of nodes
              edges a list of edges 
    """

    nodes = []
    for node in graph.nodes:
        color = '#8FC6F5'
        if node == 0:
            color = '#F5866A'
        title = graph.nodes[node]["wv"]
        value = graph.euler_semantic(node)
        size = 20 * value + 5
        nodes.append({'id': node, 'label': str(node), 'shape': 'dot', 'size' : size, 'color' :color, 'title': title})
    
    edges = []
    for  source, target, data in graph.edges(data=True):
        if data["type"] == "support":
            color = "#6BB8FA"
        else:
            color = "#F55F40"

        edges.append({
            'id': str(source) + "__" + str(target),
            'from': source,
            'to': target,
            'width': 2,
            'arrows':{'to':True},
            'color': {
                    'color':color,
                    'highlight':'#848484',
                    'hover': '#848484',
                    'inherit': 'from',
                    'opacity':1.0
                    }
        })
    
    return nodes, edges

def generate_table(table, max_rows=10):

    if table is not None:
        dataframe = pd.DataFrame.from_records([table])
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ])



class GraphApp():

    """ Attributes : 
    - debate model 
    - game_stats 
    - app
    """

    def __init__(self) -> None:
        self.debate_model = None
        self.game_stats = None

        self.agent_graph = None





    def create_app(self):

        # create app
        self.app = dash.Dash(__name__)

        #define layout
        self.app.layout = html.Div([
            html.H1(children='Debate Visualisation'),

            html.Div( [
            
            html.Div([

            html.Div(["Number of Agents: ",
                dcc.Input(id='input-nb-agents', value='5', type='text')]),
            html.Div(["Number of Steps: ",
                dcc.Input(id='input-nb-steps', value='7', type='text')]),
            html.Div(["World Value: ",
                dcc.Input(id='input-world', value='0.9', type='text')]),
             html.Div(["Interval size: ",
                dcc.Input(id='input-I', value='0.1', type='text')]),
             html.Div(["sigma: ",
                dcc.Input(id='input-sigma', value='0.5', type='text')]),
            html.Div(["p favor: ",
                dcc.Input(id='input-p-favor', value='0.5', type='text')]),
            html.Div(["p against: ",
                dcc.Input(id='input-p-against', value='0.5', type='text')]),
            html.Div(["seed: ",
                dcc.Input(id='input-seed', value='random', type='text', disabled= True)]),
            
            html.Button('Run Simulation', id='run-button'),
            ], id = 'paramters'),

            html.Div([html.H2(children='Metrics'), 
            html.Div(id = 'results'),
            html.Div(id = 'output-table')], className='table-component')
            ], className='row'),


            

            #graph components : 
            html.Div([

            # ====================== Public Graph ====================================
            html.Div([
                html.Div([html.H2(children='Public Graph'), 
            html.Div(id='public-graph'),], className='block'), 
            html.Div(id = 'p-selected-nodes'),
             html.Div( id = 'public-slider', children = dcc.Slider(
                                    id='slider',
                                    min = 0,
                                    value = 0,
                                    max = 0
                                )),
             html.H2(id='step-title'),
             html.Div(id='step-graph'),
             html.Div(id = 's-selected-nodes', children = '')
             ], className='column' ),

            # ===================== Agent Graphs ===========================================

            html.Div([html.H2(id = 'agent-title', children='Agent Graphs'),
                html.Div(id = 'agent-slider-container', children = dcc.Slider(
                                    id='agent-slider',
                                    min = 0,
                                    value  = 0,
                                    max = 0
                                )),
                dcc.Dropdown( id = 'agent-dropdown',
                        value=None
                    ),  
            html.Div(id='agent-graph')
            , html.Div(id = 'a-selected-nodes'), html.Div(id = 'agent-info')], className='column' )
        
            
            ],  className='row')
            
        ])
        
        # define callbacks 


        ##============= MAIN CALLBACK========================================
        @self.app.callback(
            [ Output('public-graph', 'children'), Output('output-table', 'children'), Output('agent-dropdown', 'options'), Output('slider', 'max'), Output('agent-slider', 'max'), Output('results', 'children')],
            [Input('input-nb-agents', 'value'),Input('input-nb-steps', 'value'), Input('input-world', 'value'), Input('input-I', 'value'), Input('input-sigma', 'value'), Input('input-seed', 'value'),  Input('run-button', 'n_clicks'), Input('input-p-favor', 'value'),Input('input-p-against', 'value')] )
        def run_simulation(nb_agents, nb_steps, world_value, interval_size, sigma, seed, nb_clicks, p_favor, p_against):

            if nb_clicks is not None:
                changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
                if 'run-button' in changed_id:

                    try:
                            nb_agents = int(nb_agents)
                            nb_steps = int(nb_steps)
                            world_value = float(world_value)
                            interval_size = float(interval_size)
                            sigma = float(sigma)
                            #seed = float(seed)
                            p_favor = float(p_favor)
                            p_against = float(p_against)

                            random.seed(seed)
                    except:
                            raise("Invalid Arguments")
                    
                    # not using the seed
                    self.debate_model, self.game_stats = run_debate(num_s_agents = nb_agents, step_count = nb_steps, world_value = world_value, seed = None, p_favor = p_favor, p_against = p_against, interval_size = interval_size, sigma = sigma, lightmode=False)

                    public_nodes, public_edges = convert_to_visdcc_format(self.debate_model.public_scientific_graph)

                    # building the options for the agent dropdown 

                    dropdown_options=[
                            {'label': 'Merged Graph', 'value': 'Merged'}
                        ]
                    for agent in self.debate_model.schedule.agents:
                        dropdown_options += [{'label': 'Agent ' + str(agent.name), 'value': agent.name}]

                    return [ 
                            visdcc.Network(id = 'p-graph', selection = {'nodes':[], 'edges':[]},data ={'nodes': public_nodes, 'edges': public_edges}, options = dict(height= '350px', width= '100%', interaction = dict(hover= True))), 
                            generate_table(self.game_stats), 
                            dropdown_options,
                            self.game_stats['Steps'] - 1,
                            self.game_stats['Steps'] - 1, "Collective Error :" + str(round(abs(self.game_stats['World Value'] - self.game_stats['Result']), 5)) + "\n" + "STD of Opinions :" + str(round(self.game_stats['STD of Agent\'s Opinion'], 5))]
                               
            
            return ( None, None, [], 0, 0, None)

        @self.app.callback(
            [Output('agent-graph', 'children'),Output('agent-title', 'children')],
            [Input('agent-dropdown', 'value'), Input('agent-slider', 'value')])
        def update_output(value, step):
            if self.debate_model is not None and value is not None :
                # if value =='Merged':
                #     merged_value, merged_graph = self.debate_model.get_merged_value(step)
                #     print("MERGED VALUE : ", merged_value)
                #     nodes, edges = convert_to_visdcc_format(merged_graph, self.debate_model.semantic)
                #     title = "Merged Graph Step " + str(step)
                #     self.agent_graph = merged_graph
                #     return [visdcc.Network(id = 'agent-net',selection = {'nodes':[], 'edges':[]}, data ={'nodes': nodes, 'edges': edges},
                #                 options = dict(height= '400px', width= '100%', interaction = dict(hover= True))), title, None]
                
                for agent in self.debate_model.complete_state[step].schedule.agents:
                    if agent.name == value:
                        g = agent.opinion_graph
                        self.agent_graph = g
                        nodes, edges = convert_to_visdcc_format(self.agent_graph)
                        title = "Agent Graphs Step " + str(step)
                        #strategy = "Strategy : " + str(self.debate_model.strategies[step][agent.name][0])

                        return [visdcc.Network(id = 'agent-net',selection = {'nodes':[], 'edges':[]}, data ={'nodes': nodes, 'edges': edges},
                                    options = dict(height= '400px', width= '100%', interaction = dict(hover= True))), 
                                title]
                

            return None, 'Agent Graphs'
        

        @self.app.callback(
        [dash.dependencies.Output('step-graph', 'children'),dash.dependencies.Output('step-title', 'children')],
        [dash.dependencies.Input('slider', 'value'), Input('public-graph', 'children') ])
        def update_step_graph(value, public_graph):
            if value is not None and self.debate_model is not None:
                graph = self.debate_model.state[value]
                nodes, edges = convert_to_visdcc_format(graph)
                return [visdcc.Network(id = 'step-net',selection = {'nodes':[], 'edges':[]}, data ={'nodes': nodes, 'edges': edges},
                            options = dict(height= '400px', width= '100%', interaction = dict(hover= True))),
                            "Public Graph Step " + str(value)]
            return None, None
        

        # Callback for selection in original graph :
        @self.app.callback(
        Output('selected-nodes', 'children'),
        [Input('net', 'selection')])
        def myfun(x): 
            s = ''
            if len(x['nodes']) > 0 :
                argument = x['nodes'][0]
                s += "Argument "+str(argument)
                weight = self.debate_model.argument_graph.euler_semantic(argument)
                value = self.debate_model.semantic.get_argument_value(argument, self.debate_model.argument_graph)
                s += "\n Weight : " + str(weight) + " \n Value : " + str(value)
            return dcc.Markdown(s, style={"white-space": "pre"})
        
        # Callback for selection in final graph
        @self.app.callback(
        Output('p-selected-nodes', 'children'),
        [Input('p-graph', 'selection')])
        def myfun(x): 
            s = ''
            if len(x['nodes']) > 0 :
                argument = x['nodes'][0]
                s += "Argument " + str(argument)
                weight = self.debate_model.public_scientific_graph.get_argument_weight(argument)
                value = self.debate_model.semantic.get_argument_value(argument, self.debate_model.public_scientific_graph)
                s += "\n Value : " + str(value)
            return dcc.Markdown(s, style={"white-space": "pre"})

        # Callback for selection in step graph
        @self.app.callback(
        Output('s-selected-nodes', 'children'),
        [Input('step-net', 'selection'), dash.dependencies.Input('slider', 'value')])
        def myfun(x, value): 
            s = ''
            if x is not None and len(x['nodes']) > 0 :

                graph = self.debate_model.state[value]
                argument = x['nodes'][0]
                s += "Argument " + str(argument)
                upvotes, downvotes = graph.get_argument_votes(argument)
                weight = graph.get_argument_weight(argument)
                up_list = graph.nodes[argument]["up_list"]
                down_list = graph.nodes[argument]["down_list"]
                value = self.debate_model.semantic.get_argument_value(argument, graph)
                s += "\n " + str(upvotes) + " +  [" + str(up_list) + "] | " + str(downvotes) + " - [" + str(down_list)  + " ] \n Weight : " + str(weight) + " \n Value : " + str(value)
                return dcc.Markdown(s, style={"white-space": "pre"})
            return None
        

        # Callback for selection in agent graph
        @self.app.callback(
        Output('a-selected-nodes', 'children'),
        [Input('agent-net', 'selection'), Input('agent-slider', 'value'), Input('agent-dropdown', 'value')])
        def myfun(x, step, agent): 
            s = ''
            if x is not None and len(x['nodes']) > 0 :

                graph = self.agent_graph
                argument = x['nodes'][0]
                s += "Argument " + str(argument)
                weight = graph.get_argument_weight(argument)
                value = self.debate_model.semantic.get_argument_value(argument, graph)

                if agent == "Merged":
                    upvotes, downvotes = graph.get_argument_votes(argument)
                    up_list = graph.nodes[argument]["up_list"]
                    down_list = graph.nodes[argument]["down_list"]
                    s += "\n " + str(upvotes) + " +  [" + str(up_list) + "] | " + str(downvotes) + " - [ " + str(down_list)  +" ] \n Weight : " + str(weight) + " \n Value : " + str(value)
                    return dcc.Markdown(s, style={"white-space": "pre"})

                s += "\n Weight : " + str(weight) + " \n Value : " + str(value)
                return dcc.Markdown(s, style={"white-space": "pre"})
            return None

  
        
        return self.app

# define main calling
if __name__ == '__main__':

    random.seed(42)

    graph_app = GraphApp()
    graph_app.create_app()

    graph_app.app.run_server(debug=True)


