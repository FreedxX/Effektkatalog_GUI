from py2neo import NodeMatcher
from py2neo import Node
from py2neo import Graph
import time
from QUERY_FOR_INTERFACE import QueryCYPHER
import copy
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import webbrowser

import threading


class NameProperties():

    """ Name properties is a class of functions  to get a group of nodes or a distinct node 
        and get thier name property"""

    def __init__(self, nodelabelS, nameStrt, nodelabelE, graph):

        self.nodelabelS = nodelabelS #start node label
        self.nameStart = nameStrt #start node name property
        self.nodelabelE = nodelabelE #end node label
        self.graph = graph

        self.endn = str() # string addion for endnode
        self.endn2 =str() # string addion for endnode
        self.teildomaene =  list()
        self.node = list()

        self.ID = int()   # ID property of node
        self.Lb =  str()    # Label property of node
        self.Name = str()   # Name property of node
        self.SI = str()     # unit property of node
        self.Einsch = str() # restriciton property of node

        self.nodelist = list()


    def GetRelationship(self):
        # print(self.nodelabelS, self.nameStart, self.nodelabelE)

        """
            entry: node label (var=label) and node name (var=Name)  to be queried in neo4j graph (var=graph)
            the function has different cases for different search types (e.g. if the label or the name is void)
    
            returns: tuple of Name Attributes which are connected to the node with the [:IST_TEIL] realtionship (=attr[])
            this function is used in the Query interface of the GUI
    
    
    
            toolkits needed for this function: py2neo (w/ Nodematcher and Graph)
            """



        if self.nodelabelE == "Bitte Wählen" or self.nodelabelE == None \
                or self.nodelabelE == "None" or self.nodelabelE == "N/A":
            # no end node = open search
            self.endn = ""
            self.endn2 = ""

        elif self.nodelabelE == "Parameter":  # before: "Gestaltparameter"
            self.endn = "n2:`" + self.nodelabelE + "`"
            self.endn2 = "<-[IST_TEIL]-()"

        else:
            self.endn  = "n2:`" + self.nodelabelE + "`"
            self.endn2 = ""

        if self.nodelabelS == "Bitte Wählen" or self.nodelabelS is None \
                or self.nodelabelS == "None" or self.nodelabelS == "N/A":
            self.nodelabelS = "n"

        else:
            self.nodelabelS = "n:" + self.nodelabelS


        if self.nameStart == "Bitte Wählen" or self.nameStart is None \
                or self.nameStart == "None" or self.nameStart == "N/A":
            query = "match p=(" + self.nodelabelS + ")<-[r:IST_TEIL]-(" + self.endn + ")" + self.endn2 + " return distinct p"
        # if endn == "":
        #     query = "match p=("+ nodelabel1 + ") return p"
        # else:
        #     query = "match p=(" + nodelabel1 + ")<-[r:IST_TEIL]-("+endn+") return p"

        else:
            if self.nodelabelS == "n":
                query = "match p=(" + self.nodelabelS + ") Where n.Name='" + self.nameStart + "'" + self.endn2 + " return distinct p"

            else:
                query = "match p=(" + self.nodelabelS + " {Name:'" + self.nameStart + "'})<-[r:IST_TEIL]-" \
                                                                           "(" + self.endn + ")" + self.endn2 + " return distinct p"

        # print(query)
        self.data_table = self.graph.run(query).to_table()

        self.attr = tuple(sorted(set([nodes[0].end_node['Name'] for nodes in self.data_table])))
        # removes duplicates (set) sort alphabetically and capitalize the first letter --> then return as tuple

        # case if nothing returned
        if self.attr == []:
            self.attr = ["NaN - please change search!"]

        else:
            pass
        #reset of labels
        self.nodelabelS = None
        self.NameStart = None
        self.nodelabelE = None

        return self.attr

    def GetNode(self):

        """
        entry: node label (var=label) and node name (var=Name)  to be queried in neo4j graph (var=graph)
        the function has different cases for different search types (e.g. if the label or the name is void)
        returns tuple of Name Attributes (=attr[])
        """

        matcher = NodeMatcher(self.graph)
        # matcher  is
        if self.nodelabelS is None:
            self.teildomaene = list(matcher.match(name=self.nameStart))

        elif self.nameStart == "Bitte Wählen" or self.nameStart is None:
            self.teildomaene = list(matcher.match(self.nodelabelS))

        else:
            self.teildomaene = list(matcher.match(self.nodelabelS, name=self.nameStart))

        #print(self.teildomaene)

        self.attr = tuple(sorted(set([nodes["Name"] for nodes in self.teildomaene])))
        if self.attr == []:
            self.attr = ["please select type from above"]

        else:
            pass

        return self.attr

    def GetInfo(self):

        # in GUI nodes currently are only handeld by their Name-propterties
        # This function gets the node ID
        self.matcher = NodeMatcher(self.graph)
        self.node = list(self.matcher.match(Name=self.nameStart))
        # use of py2neo mathcer to get a node with the name self.namestart

        self.ID = int(self.node[0].identity)
        self.Lb = str(self.node[0].labels)[1:]
        # get ID and label of node

        self.Name = self.node[0]["Name"]
        self.L = self.node[0]["Link"]
        self.F = self.node[0]["Formel"]
        self.B = self.node[0]["Beschreibung"]
        self.A = self.node[0]["Ausprägung"]
        self.Lit =  self.node[0]["Literatur"]
        self.V =  self.node[0]["Getroffene_Vereinfachungen"]
        self.Einsch = self.node[0]["Einschränkung"]
        #get other properties of node and return them as dict

        return {"ID": self.ID, "Lb": self.Lb, "Name": self.Name, "L": self.L, "F": self.F, "B": self.B ,
        "A": self.A, "Lit":self.Lit, "V": self.V, "E":self.Einsch}

    def GetOtherProperties(self, what):
        # in GUI nodes currently are only handeld by their Name-propterties
        # This function gets the node ID and label but returns only the as what decalared property
        self.matcher = NodeMatcher(self.graph)
        self.nodelist = list(self.matcher.match(self.nodelabelS))
        # get node by label

        self.sumlist = list()
        self.sumdict = dict()

        for line in range(len(self.nodelist)):

            self.ID = int(self.nodelist[line].identity)
            print(self.ID)
            self.Lb = str(self.nodelist[line].labels)[1:]
            print(self.Lb)
            # get ID and label of match and print them just for debugging


            print(self.nodelist[line][str(what)])
            self.sumdict[self.nodelist[line][str(what)]]= 0
            print(self.sumdict)
            # create dictionary entry of the property to avoid duplicates --> value = 0 for  simplicity
            # print(self.sumdict)

        self.sumlist = list(self.sumdict.keys())
        # change to list
        print(self.sumlist)

        return self.sumlist

class FilterQ():

    """ This class function filters duplicate nodes in paths"""

    def __init__(self, paths = None):
        self.copy_of_paths = paths
        self.filtered_list = list()
        self.newlist = list()
        self.line = int()
        self.element = int()
        self.flag = bool()

    def FilterLoops(self,  paths = None):
        # check if list is empty
        if self.copy_of_paths != []:
            # make a deepcopy
            self.filtered_list = copy.deepcopy(self.copy_of_paths)
            # https://stackoverflow.com/questions/184710/what-is-the-difference-between-a-deep-copy-and-a-shallow-copy

            # reset result list = newlist
            self.newlist = list()

            #check each line indiviually
            for self.line in range(len(self.filtered_list)):

                # reset flag
                # use self.flag as marker if element has loops
                # in loops found marker is set to true
                # look for A-B-A duplicates
                self.flag = False # if flag is changed its not copyed to  the filtered list
                for self.element in range(len(self.filtered_list[self.line]) - 3):
                    # print(range(len(filtered_list[line])-2))
                    # compare element 2 places in front with the current element
                    if self.filtered_list[self.line][self.element + 2] == self.filtered_list[self.line][self.element]:
                        self.flag = True
                # also for A-B-C-A duplicates
                for self.element in range(len(self.filtered_list[self.line]) - 4):
                    # print(range(len(filtered_list[line])-2))
                    if self.filtered_list[self.line][self.element + 3] == self.filtered_list[self.line][self.element]:
                        self.flag = True

                #         print(str(filtered_list[line][element + 2] )+ "=="+str( filtered_list[line][element]))
                # print(flag)
                if self.flag != True:
                    self.newlist.insert(self.line, self.filtered_list[self.line])

            return self.newlist
        else:
            pass

    def FilterSimilarPaths(self, paths=None):
        """ not used"""
        self.copy_of_paths = paths
        if self.copy_of_paths != []:
            # make a deepcopy


            self.filtered_list = copy.deepcopy(self.copy_of_paths)
            # https://stackoverflow.com/questions/184710/what-is-the-difference-between-a-deep-copy-and-a-shallow-copy

            # reset result list = newlist
            self.copylist = list()
            self.sorteddict = dict()
            self.sorteddict2 = dict()

            for self.line in range(len(self.filtered_list[0])):
                self.sorteddict[self.line] = set(self.filtered_list[0][self.line])
                self.sorteddict2[self.line] = set(self.filtered_list[0][self.line])  # other idea is set
                self.copylist.append(self.filtered_list[0][self.line])


            for self.line in range(len(self.sorteddict)):
                for self.element in range(self.line + 1, len(self.sorteddict2), 1):

                    if self.sorteddict[self.line] == self.sorteddict2[self.element]:
                        print(str(self.sorteddict[self.line]) + "=" + str(self.sorteddict2[self.element]))
                        self.sorteddict2[self.element] = 0
                        self.copylist.pop(self.element)
                        print("deleted")

            return list(self.copylist)
        else:
            pass







class ExeQuery():
    """ Exceutes Cypher Query and returns a list of paths (var_self.path_p)"""
    def __init__(self, cause = None, impact = None, graph = None, length=None, datatable= None, NxGraph = nx.Graph(),
                 quw=bool(), ax=plt.figure().add_subplot(1, 1, 1), names_of_qPaths=None, mweight= None, widget= None,
                 addinf=str()):
        self.a = cause
        self.b = impact
        self.graph = graph
        self.effectdict = dict()
        self.datael = dict()
        self.path_p = list()
        self.DataTable = datatable
        self.G = NxGraph
        self.ax = ax
        self.names_of_query_paths = names_of_qPaths
        self.d = length
        self.lenstr = str()
        self.drawnGraph = None
        self.UW = quw
        self.maxweight = mweight
        self.h = addinf

    def execute(self, cause, impact, graph, length, mweight, quw, addinf):
            """" Exceute Cypher statement end returns path as datatable
                    use of QUERY_FOR_INTERFACE.QueryCYPHER.VariableLength()  to get the Cypherstatement
                    as String which is passed to py2neo to exceute with use of py2neo.graph.run()to_table()
                    next steps extractfromtable -> querypathnames -> Cosmetic -> Draweverypathinone

                    :param string: cause  Input
                    :param string: impact Input
                    :param string: graph  ass. Graph

                    :returns: dataTable
            """

            self.UW = quw
            self.maxweight = mweight
            # self.node_tuple =["Flussgröße", "Kraft","Flussgröße", "Kraft"]
            # forms tuple to easier pass all needed inputs to Querycypher method

            if self.b == "" and (self.h == "None" or self.h == "Bitte Wählen"):
                self.node_tuple = [
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Lb"],
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Name"],"",""
                        ]
            elif  self.b == "" and  (self.h != "None" and self.h != "Bitte Wählen"):
                self.node_tuple = [
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Lb"],
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Name"],
                    self.h, ""
                        ]
            else:
                self.node_tuple = [
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Lb"],
                    NameProperties(None, self.a, None, self.graph).GetInfo()["Name"],\
                    NameProperties(None, self.b, None, self.graph).GetInfo()["Lb"],
                    NameProperties(None, self.b, None, self.graph).GetInfo()["Name"]
                            ]
            self.lenstr = "0.."+str(self.d)
            # calls QUERY_FOR_INTERFACE.QueryCYPHER.VariableLength()
            # self.query = QueryCYPHER(self.node_tuple, self.lenstr, False, self.UW, 15).VariableLength()

            if self.chb2t0Var.get():
                self.query = QueryCYPHER(self.node_tuple, self.lenstr, False, self.UW, self.maxweight). \
                    VariableLengthwithedgeweights()
                print("edge")
            else:
                self.query = QueryCYPHER(self.node_tuple, self.lenstr, False, self.UW, self.maxweight).\
                    VariableLengthwithnodeweights()
                print("node")


            # execute cypher string
            self.DataTable = self.graph.run(self.query[0]).to_table()
            # .run().to_table() executes CYPHER script and transfers it to a table

            return self.DataTable

    def ExtractfromTable(self, **kwargs):
            """ Extract dictonary from DataTable"""

            for el in range(len(self.DataTable)):
                for it in range(len(self.DataTable[el][0].nodes)):
                    if str(self.DataTable[el][0].nodes[it].labels) == ":Effekt" or\
                              str(self.DataTable[el][0].nodes[it].labels) == ":`Parameter-Effekt`" :
                        self.datael = dict() #  empty dictonary data type to be filled in the following
                        self.datael['Name']=(self.DataTable[el][0].nodes[it]['Name']) # dict entry ["Name"] will be linked to the specific adressed element of the table
                        self.datael['Link']=self.DataTable[el][0].nodes[it]['Link']
                        self.datael['Literatur']=(self.DataTable[el][0].nodes[it]['Literatur'])
                        self.datael['Ausprägung']=(self.DataTable[el][0].nodes[it]['Ausprägung'])
                        self.datael['Beschreibung']=(self.DataTable[el][0].nodes[it]['Beschreibung'])
                        self.datael['Formel']=(self.DataTable[el][0].nodes[it]['Formel'])
                        self.datael['Getroffene_Vereinfachungen']=(self.DataTable[el][0].nodes[it]['Getroffene_Vereinfachungen'])
                        self.datael['Einschränkung'] = (self.DataTable[el][0].nodes[it]['Einschränkung'])
                        # print(self.datael)
                        self.effectdict[self.datael['Name']]=self.datael


            return self.effectdict


    def QueryPathNames(self,*args, **kwargs):


            self.path_p = [] #okay
            for line in self.DataTable:
                for Inputs in range(self.query[1]):
                    if line[Inputs] != None:

                        if self.path_p == []:
                            self.path_p = [line[Inputs]]
                        else:
                            self.path_p.extend([line[Inputs]])
                    else:
                        pass
            self.names_of_query_paths = list(NameReader._ReadPath(self, listpath_p =self.path_p))  # okay

            self.copy_of_paths = copy.deepcopy(self.names_of_query_paths)

            return  self.copy_of_paths, self.names_of_query_paths


class ScrollableImage(tk.Frame):
    '''https://stackoverflow.com/questions/56043767/show-large-image-using-scrollbar-in-python'''
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set,
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows




# class GUI_DRAW2():
#     """  TBD"""
#
#     def __init__(self, names_of_qPaths=None, widget=None): #NxGraph=nx.Graph()):
#         self.G = nx.Graph()
#         self.names_of_query_paths = names_of_qPaths
#
#
#
#     def UpdateandDrawNxGraph(self, *args, **kwargs):
#
#         self.G.clear()  # okay
#
#
#         for line in range(len(self.names_of_query_paths)):
#
#             old_element = None
#             for element in self.names_of_query_paths[line]:
#                 # print(element)
#                 if element != "None":
#                     self.G.add_node(element, labels=element)
#                     if old_element == None:
#                         pass
#                     else:
#                         self.G.add_edge(old_element, element)
#                     old_element = element
#                 else:
#                     pass
#
#         return self.G
#
#
#             # self.FCtk1t0.draw()
#             #
#             # self.msg5t0.config(text = "Es werden "+ str(self.msg4t0.size()-1) + " Ergebnisse angezeigt")

class Cosmetic():

    def __init__(self, inputpath):
        self.newres = []
        self.names_of_query_paths = inputpath
        self.namespart2 = list()

    def Paths(self, *args, widget= None, **kwargs):
        # print("CosmeticPaths")
        # print(self.names_of_query_paths)
        for el in range(len(self.names_of_query_paths)):
            self.namespart2.insert(el,self.names_of_query_paths[el])

        for el in range(len(self.namespart2)):
                self.res1 = ""
                for i in self.namespart2[el]:

                    self.res1 = self.res1 + str(i) + " - "
                self.res1 = self.res1[:-2]
                self.namespart2[el]= self.res1

        # self.msg4t0.insert(0, "Zeige alle an")
        # self.msg4t0.delete(1, "end")
        # for line in range(len(self.namespart2)):
        #     self.msg4t0.insert(line + 1, str(self.namespart2[line]))
        # self.msg5t0.config(text="Es werden " + str(self.msg4t0.size() - 1) + " Ergebnisse angezeigt")
        return self.namespart2



class NameReader():
    def __init__(self, listpath_p = None):

        self.listpath_p = listpath_p
        self.nodes_p2 = list()
        self.nodes_p = list()

    def _ReadPath(self, listpath_p = None):
        # ==================================
        # the following tool picks the path_p list and extract every node of it and transfers it to a new list
        self.listpath_p = list(listpath_p)
        # name_reader(path_p)
        # create empty list
        self.nodes_p2= list()

        for line in listpath_p:
            newline = []
            for node_count in line.nodes:
                newline.append(node_count["Name"])
                #sorted(newline) # Sorted is paused due to the outputs are ordered by weight sum
            # print(*newline)
            self.nodes_p2.append(newline)

        self.nodes_p = list(dict.fromkeys((tuple(i) for i in self.nodes_p2)))
        # use transfer to dict to remove dupliucates by preserving the order
        return self.nodes_p


# def get_Node_info_by_Name(NodeName, graph):
#
#
#     # in GUI nodes currently are only handeld by their Name-propterties
#     # This function gets the node ID
#     matcher = NodeMatcher(graph)
#     node = list(matcher.match(Name=NodeName))
#
#     ID      = int(node[0].identity)
#     Lb      = str(node[0].labels)[1:]
#     Name    = node[0]["Name"]
#     SI      = node[0]["SI-Einheit"]
#     E       = node[0]["Einheit"]
#
#
#     return {"ID" : ID, "Lb":Lb, "Name": Name, "SI": SI, "E":E}
#
# def get_ID_by_Name(NodeName,graph):
#     matcher = NodeMatcher(graph)
#     nodeID = list(matcher.match(Name=NodeName))[0].identity
#     return nodeID



#     print (startLb)
#     print(str(startnode[0].identity), str(startnode[0].labels),
#           str(endnode[0]["Name"]), str(endnode[0].identity))
#     return
#
# Main_QUERY_NEO4j_prep("Kraft", "Verschiebung", graph)


# matcher = NodeMatcher(graph)
# match = list(matcher.match("Flussgröße"))
# attr = [nodes["Name"] for nodes in match]
#
#
#
# start_and_endnodes(input_startcategory, input_startnode, input_endcategory, input_endnode)
#
# query_variablelength(nodetpl, Lenght_query, return1_bool )
#
# name_reader(listpath_p)

def name_reader(listpath_p):
    # ==================================
    # the following tool picks the path_p list and extract every node of it and transfers it to a new list NO IT DOES NOT
    # it only reference it to itself

    listpath_p = list(listpath_p)
    # name_reader(path_p)
    # create empty list
    nodes_p2 = []

    for line in listpath_p:
        newline = []
        for node_count in line[0].nodes:
            newline.append(node_count["Name"])
            sorted(newline)
        # print(*newline)
        nodes_p2.append(newline)

    nodes_p = list(set(list(set(tuple(i) for i in nodes_p2))))
    return nodes_p

def Draw_every_path_in_one_Graph(names_of_query_paths_func, graph):
    #
    # Graph visualiziation with networkx
    #
    # Networkx is also a graph database toolkit but i will stick to neo4j
    # networkx is only used to
    # G = nx.MultiDiGraph()
    G = nx.MultiDiGraph()
    G.clear()
    colordict = dict()
    colorlist = list()
     # Graph(auth=('neo4j', 'neo4j3'))
    for line in range(len(names_of_query_paths_func)):

        old_element = None
        for element in names_of_query_paths_func[line]:
            nodes = NodeMatcher(graph)
            node = list((nodes.match(Name=str(element))))
            if any(ty in str(node[0].labels) for ty in [":Primärgröße", ":Flussgröße", ":Extensum",
                                                        ":Primärgröße", ":`Abgeleitete Groöße`"]):
                    color = "red"
            elif any(ty in str(node[0].labels) for ty in [":Effekt", "Parameter-Effekt", ":`Parameter-Effekt`" ]):
                  color = "orange"

            elif str(node[0].labels) ==":Beispiel":
                  color = "green"
            else:
                color = "grey"

            if element != "None":
                G.add_node(element, labels=element)
                colordict[element] = color
                if old_element == None:
                    pass
                else:
                    G.add_edge(old_element, element)
                old_element = element
            else:
                pass
        # H = nx.draw_shell(G, with_labels=True, font_weight='bold', node_color='orange', font_size=8)
    # plt.show()
    colorlist2= list(colordict.items())
    for element in range(len(colorlist2)):
        colorlist.append(colorlist2[element][1])

    return [G, colorlist]

def Draw_every_var_for_effect(listvar,listpar, listeff, listexample):
    """"
      Graph visualiziation with networkx:
      Chross check, collect all  associated parameters and variables of the "to-be-added-effect"
      parameters and variables will hand over as list (input: listvar and input: listpar)
      listeff is the new effekt only the new name will be needed (listeff[0])

      Void varibles "None" or None will be ignored

      Networkx is also a graph database toolkit but i will stick to neo4j
      networkx is only used to visualize in GUI (via Tkinter embedding of Matplotlib.toolkit called FigureCanvas)

      a networkx directedgraph  (nx.DiGraph) will be created (nodes and  edges)

      a dictonary will be created containing the networkx node identifier and the label

      returned will be the Graph and the dict

    :returns: [G: nx.Graph(), labeldict: dict(), colorlist: list()]
     """
    G = nx.DiGraph()
    G.clear()
    effect_element = listeff[0]
    counter = 0
    labeldict= {}

    colorlist = list()
    labeldict[effect_element]=listeff[0]
    colorlist.append("yellow")

    for element in sorted(listvar):


        if element == "None" or element == "N/A":
            pass


        elif element!= "None" and element != "N/A":

            G.add_node(counter, labels=element)
            G.add_edge(counter,effect_element, length = 1)
            labeldict[counter]=element
            colorlist.append("orange")

        else:
             pass
        counter = counter +1


    for element in sorted(listpar):

        if element == "None" or element == "N/A":
            pass

        elif element!= "None" and element != "N/A":
            G.add_node(counter, labels=element)
            G.add_edge(effect_element, counter, length = 1)
            labeldict[counter] = element
            colorlist.append("red")

        else:
             pass
        counter = counter + 1

    for element in sorted(listexample):

        if element == "None" or element == "N/A":
            pass

        elif element!= "None" and element != "N/A":
            G.add_node(counter, labels=element)
            G.add_edge(effect_element, counter, length = 1)
            labeldict[counter] = element
            colorlist.append("grey")

        else:
             pass
        counter = counter + 1

    # flip the first to elements in order to paint the effect yellow

    a = colorlist[0]
    b = colorlist[1]
    c = colorlist[2:]
    colorlist.clear()
    colorlist.insert(0,b)
    colorlist.insert(1,a)
    colorlist.extend(c)


        #H = nx.draw_shell(G, with_labels=True, font_weight='bold', node_color='orange', font_size=8)
        # plt.show()
    return [G, labeldict , colorlist]

def add_parameter(labelname, nameproperty, unit, Siunit, graph):
    """ this function adds a new parameter to the DBMS and connect it to the "Funktionsparameter"

        it checks whether the parameter is already given, if so -> pass
        if nameproperty  == None -> pass

    :param: str() - labelname
    :param: str() - nameproperty

    :returns: nothing- but an effect and relationship is added """

    try:
        nodes = NodeMatcher(graph)
        node = list((nodes.match(Name=nameproperty)))
        print("ID:" + str(node[0].identity))
        print(node[0].labels)
        print(node[0].nodes)


    except (IndexError):
        if nameproperty != "None" and nameproperty != "N/A":
            print(IndexError)
            newparameter = Node(str(labelname), Name=nameproperty, Einheit=unit, SI_Einheit=Siunit, weight=5)
            newparameter.__primarylabel__ = labelname
            newparameter.__primarykey__ = "Name"
            print(newparameter)
            graph.merge(newparameter)
            parident = str(newparameter.identity)
            ident = str(26) # ID of 'Funktionsrelevante Parameter'


            Cypherstate =   "match(n) where ID(n) = " + ident + " \n" \
                            "with n \n" \
                            "match (e) where ID(e)=" + parident + "\n" \
                            "with n, e\n" \
                            "create p= (e)-[:IST_TEIL]->(n)"
            # print(Cypherstate)
            graph.run(Cypherstate)
            print("new parameter added")



def match_n_add(listpar, listvar, listofeff,  graph, listexample):

    """
    entry: node label (var=label) and node name (var=Name)  to be queried in neo4j graph (var=graph)
    the function has different cases for different search types (e.g. if the label or the name is void)
    returns tuple of Name Attributes (=attr[])
    """
    # 0efffetkbezeichung, 1beschreibung, 2literatur, 3formel,  4vereinfachungen, 5ausprägung, 6link
    try:
        nodes = NodeMatcher(graph)
        eff = list((nodes.match(listofeff[7], Name=listofeff[0])))
        print(eff)
        print("ID:" + str(eff[0].identity))
        # print("Label:" + str(node[0].labels)[1:])
        effident = (str(eff[0].identity))
        counter = 0

    except (IndexError, KeyError) as e:
        neweffect = Node(listofeff[7], Name=listofeff[0], Literatur=listofeff[2],
                         Link=listofeff[6], Formel=listofeff[3], Einschränkung=listofeff[8],
                         Getroffene_Vereinfachungen=listofeff[4], Ausprägung=listofeff[5], Beschreibung=listofeff[1],
                         weight = 3)
        neweffect.__primarylabel__ = listofeff[7]
        neweffect.__primarykey__ = "Name"
        graph.merge(neweffect)
        effident = str(neweffect.identity)
        counter = 0



    for par in listpar:
        if par != "None" and par != "N/A":
            try:
                print(par)

                nodes = NodeMatcher(graph)
                node= list((nodes.match(Name=str(par))))
                print(node)
                print("ID:" + str(node[0].identity))
                #print("Label:" + str(node[0].labels)[1:])
                ident=(str(node[0].identity))


                Cypherstate= "match(n) where ID(n) = " +ident+ " \n" \
                             "with n \n" \
                             "match (e) where ID(e)="+effident+"\n" \
                             "with n, e\n" \
                             "create p= (n)-[:URSACHE_WIRKUNG {weight: '2'}]->(e)"
                #print(Cypherstate)
                graph.run(Cypherstate)
                counter = counter + 1

            except (IndexError, KeyError) as e:
                print(e)



        else:
            pass

    for var in listvar:
        if var != "None" and  var != "N/A":

            nodes = NodeMatcher(graph)
            node = list((nodes.match(Name=str(var))))
            print("ID:" + str(node[0].identity))
            #print("Label:" + str(node[0].labels)[1:])
            ident = (str(node[0].identity))

            Cypherstate = "match(n) where ID(n) = " + ident + " \n" \
                          "with n \n" \
                          "match (e) where ID(e)=" + effident + "\n" \
                          "with n, e\n" \
                          "create p= (n)<-[:HAT_PARAMETER {weight: '4'}]-(e)"
            #print(Cypherstate)
            graph.run(Cypherstate)
            counter = counter + 1
        else:
            pass
    for ex in listexample:
        if ex != "None" and ex != "N/A":
            try:
                nodes = NodeMatcher(graph)
                node = list((nodes.match(Name=str(var))))
                print("ID:" + str(node[0].identity))
                # print("Label:" + str(node[0].labels)[1:])
                exident = (str(node[0].identity))

            except (KeyError, IndexError):
                print("ID not found no node existing with %s as Name" % ex)

                newexample = Node("Beispiel", Name=ex)
                newexample.__primarylabel__ = "Beispiel"
                newexample.__primarykey__ = "Name"
                graph.merge(newexample)
                exident = str(newexample.identity)

                Cypherstate = "match(n) where ID(n) = " + effident + " \n" \
                              "with n \n" \
                              "match (e) where ID(e)=" + exident + "\n" \
                              "with n, e\n" \
                              "create p= (n)-[:HAT_BEISPIEL]->(e)"
                # print(Cypherstate)
                graph.run(Cypherstate)
                counter = counter + 1


        else:
            pass




    return str( str(counter)+" relationships added")

    # print(match_n_add(["Kraft","None", "Kraft"], ["Reibungskoeffizient"], ["None"], Graph(auth=('neo4j','neo4j3'))))

def chrosscheck_cypher(listvar,listpar, graph):
    # this function create the Cypher chrosscheck
    ident=[]

    for par in listpar:
        if par != "None":
            print(par)

            nodes = NodeMatcher(graph)
            node= list((nodes.match(Name=str(par))))
            print(node)
            print("ID:" + str(node[0].identity))
            #print("Label:" + str(node[0].labels)[1:])
            ident.append(int(node[0].identity))

        else:
            pass

    for var in listvar:
        if var != "None":
            nodes = NodeMatcher(graph)
            node = list((nodes.match(Name=str(var))))
            print("ID:" + str(node[0].identity))
            # print("Label:" + str(node[0].labels)[1:])
            ident.append(int(node[0].identity))

        else:
            pass

    cypherstatement2 = "match p=(n)-[r:URSACHE_WIRKUNG|HAT_PARAMETER]-(e)-[f:URSACHE_WIRKUNG|HAT_PARAMETER]-(m) \n" \
                  "WHERE ID(n) in " +str((ident))+" and ID(m)in " +str((ident))+"\n"\
                  "return p"

    print(cypherstatement2)

    return cypherstatement2

def   chrosscheck_cypher_get_neighbours(listvar, listpar, graph):
    # this function create the Cypher chrosscheck
    ident = []
    print(listvar)

    for par in listpar:
        if par != "None":
            print(par)

            nodes = NodeMatcher(graph)
            node = list((nodes.match(Name=str(par))))
            print(node)
            print("ID:" + str(node[0].identity))
            # print("Label:" + str(node[0].labels)[1:])
            ident.append(int(node[0].identity))

        else:
            pass

    for var in listvar:
        if var != "None":
            nodes = NodeMatcher(graph)
            node = list((nodes.match(Name=str(var))))
            print("ID:" + str(node[0].identity))
            # print("Label:" + str(node[0].labels)[1:])
            ident.append(int(node[0].identity))

        else:
            pass

    cypherstatement_new = "match p=(n)-[r:URSACHE_WIRKUNG|HAT_PARAMETER|ABLEITUNG*0..1]-(e) \n" \
                        "WHERE ID(n) in " + str((ident)) +"\n"\
                        "WITH * \n"\
                        "WHERE not e:Beispiel \n"\
                        "return distinct p"

    print(cypherstatement_new)

    return cypherstatement_new


def getNodesnbyproperty(nproperty, name):

    cypherstatement_new = "match p=(n {"+str(nproperty)+"='" +str(name)+"\n" \
                          "return distinct p"


    print(cypherstatement_new)

    return cypherstatement_new



# p = (n) - [r:URSACHE_WIRKUNG | HAT_PARAMETER]-(e) - [f: URSACHE_WIRKUNG | HAT_PARAMETER]-(m)
# where
# ID(n) in [32, 31, 29, 86, 15, 82] and ID(m) in [32, 31, 29, 86, 15, 82]
# return p

"""
Authors: Mitja Martini and Russell Adams
License: "Licensed same as original by Mitja Martini or public domain, whichever is less restrictive"
Source: https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html

Edited by RedFantom for ttk and Python 2 and 3 cross-compatibility and <Enter> binding
Edited by Juliette Monsel to include Tcl code to navigate the dropdown by Pawel Salawa
(https://wiki.tcl-lang.org/page/ttk%3A%3Acombobox, copyright 2011)
"""
import tkinter as tk
from tkinter import ttk

tk_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']


class AutocompleteCombobox(ttk.Combobox):
    """:class:`ttk.Combobox` widget that features autocompletion."""
    def __init__(self, master=None, completevalues=None, boxstate=None, **kwargs):
        """
        Create an AutocompleteCombobox.

        :param master: master widget
        :type master: widget
        :param completevalues: autocompletion values
        :type completevalues: list
        :param kwargs: keyword arguments passed to the :class:`ttk.Combobox` initializer
        """
        completevalues=sorted(completevalues, key=str.casefold)
        ttk.Combobox.__init__(self, master, values=completevalues, state='readonly', **kwargs)
        #self._completion_list = completevalues
        self._completion_list = completevalues
        self.configure(state=boxstate)
        if isinstance(completevalues, list):
            self.set_completion_list(completevalues)
            self.set_completion_list(sorted(completevalues, key=str.casefold))
        self._hits = []
        self._hit_index = 0
        self.position = 0
        # navigate on keypress in the dropdown:
        # code taken from https://wiki.tcl-lang.org/page/ttk%3A%3Acombobox by Pawel Salawa, copyright 2011
        # the folloing string is written in tcl tcl is an other langauge
        self.tk.eval("""
        proc ComboListKeyPressed {w key} {
        if {[string length $key] > 1 && [string tolower $key] != $key} {
                return
        }

        set cb [winfo parent [winfo toplevel $w]]
        set text [string map [list {[} {\[} {]} {\]}] $key]
        if {[string equal $text ""]} {
                return
        }

        set values [$cb cget -values]
        set x [lsearch -glob -nocase $values $text*]
        if {$x < 0} {
                return
        }

        set current [$w curselection]
        if {$current == $x && [string match -nocase $text* [lindex $values [expr {$x+1}]]]} {
                incr x
        }

        $w selection clear 0 end
        $w selection set $x
        $w activate $x
        $w see $x
        }

        set popdown [ttk::combobox::PopdownWindow %s]
        bind $popdown.f.l <KeyPress> [list ComboListKeyPressed %%W %%K]
        """ % (self))

    def set_completion_list(self, completion_list):
        """
        Use the completion list as drop down selection menu, arrows move through menu.

        :param completion_list: completion values
        :type completion_list: list
        """

        self._completion_list = sorted(completion_list, key=str.casefold) # casefold Work with a sorted list Update SM str.lower
        print(self._completion_list)
        self.configure(values=completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        #self.bind('<Return>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """
        Autocomplete the Combobox.

        :param delta: 0, 1 or -1: how to cycle through possible hits
        :type delta: int
        """
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower() in self.get().lower():
                _hits.append(element)
            # if element.lower().startswith(self.get().lower()):  # Match case insensitively
            #     _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """
        Event handler for the keyrelease event on this widget.

        :param event: Tkinter event
        """
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END)+2:  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position -= 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if event.keysym == "Return":
            self.handle_return(None)
            return
        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

    def handle_return(self, event):
        """
        Function to bind to the Enter/Return key so if Enter is pressed the selection is cleared

        :param event: Tkinter event
        """
        self.icursor(tk.END)
        self.selection_clear()

    def config(self, **kwargs):
        """Alias for configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure widget specific keyword arguments in addition to :class:`ttk.Combobox` keyword arguments."""
        if "completevalues" in kwargs:
            self.set_completion_list(kwargs.pop("completevalues"))
        return ttk.Combobox.configure(self, **kwargs)

    def cget(self, key):
        """Return value for widget specific keyword arguments"""
        if key == "completevalues":
            return self._completion_list
        return ttk.Combobox.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = ttk.Combobox.keys(self)
        keys.append("completevalues")
        return keys

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, item):
        return self.cget(item)


def button_pressed(self):
    # put text
    self.msg1t2['text'] = "Hello World!"
    # run clear_label after 2000ms (2s)
    self.msg1t2.after(10000, clear_label(self))

def clear_label(self):
    # remove text
    self.msg1t2['text'] = ""



class Link(tk.Label):

    # https://stackoverflow.com/questions/23482748/how-to-create-a-hyperlink-with-a-label-in-tkinter
    # changes are callback is not privaqte anymore so link can be changend

    def __init__(self, master=None, link=None, font=('Arial', 8), fg='black', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.default_color = fg  # keeping track of the default color
        self.color = 'blue'  # the color of the link after hovering over it
        self.default_font = font  # keeping track of the default font
        self.link = link

        """ setting the fonts as assigned by the user or by the init function  """
        self['fg'] = fg
        self['font'] = font

        """ Assigning the events to private functions of the class """

        self.bind('<Enter>', self._mouse_on)  # hovering over
        self.bind('<Leave>', self._mouse_out)  # away from the link
        self.bind('<Button-1>', self._callback)  # clicking the link

    def _mouse_on(self, *args):
        """
            if mouse on the link then we must give it the blue color and an
            underline font to look like a normal link
        """
        self['fg'] = self.color
        self['font'] = self.default_font

    def _mouse_out(self, *args):
        """
            if mouse goes away from our link we must reassign
            the default color and font we kept track of
        """
        self['fg'] = self.default_color
        self['font'] = self.default_font
    def newlink(self, link):
        self.link = link
    def _callback(self, *args):
        webbrowser.open_new(self.link)


if __name__ == '__main__':


    root = tk.Tk()

    lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket',
             'brackets',
             'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field',
             'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind',
             'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out',
             'part',
             'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless',
             'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']
    entry = AutocompleteCombobox(root, lista)
    entry.grid(row=0, column=0)

    URL = 'www.python.org'

    link = Link(root, URL, font=('sans-serif', 20), text='Python', bg='LightBlue')
    link.grid(row=1, column=0)

    root.mainloop()

