from py2neo import Graph
import networkx as nx

class QueryCYPHER():
    """ This class/function gets a tuple of node labels and properties and returns a CYPHER query
        Cypher is the programming language of neo4j the tool for the graph DBMS

        https://neo4j.com/docs/cypher-refcard/current/



        """

    def __init__(self, NodeTpl, LengthQuery, ExceptionPath, quw, maxweight):

        self.NodeTpl = NodeTpl
        self.QueryLength = LengthQuery
        self.ExceptionPath = ExceptionPath
        self.query2 = str()
        self.QueryVariablelength = str()
        self.NumberInputs = int()
        self.UW = quw
        self.Maxweight = maxweight

    def VariableLength(self):
        """ This class/function gets a tuple of node labels and properties
                    lorme ispsum

                    :param:  NodeTpl - Tuple of (Startnodelabel, Startnodenameproperty, Endnodelabel , Endnodenameproperty)
                    :param:  LengthQuery - int() of chain length for query
                    :param:  ExecptionPath - Cypher string of path which will be excluded from query (not implemented yet)

                    :returns: cypher string for Query

                """
        # this functions builds the query with variable lenght paths
        # Variables as Command Parameters
        # set manually for Test

        # input_startcategory = nodetuple[0] "Flussgröße"
        # input_startnode =  nodetuple[1] "Kraft"
        # input_endcategory = nodetuple[2]  "Flussgröße"
        # input_endnode = nodetuple[3]  "Kraft"
        # Lenght_query = "1..3"
        self.NumberInputs = 1 # potential future functions
         # potential future functions

        if self.UW is True:
            self.query3 = ""
            self.query2 = " \n \t\t\twith p,r \n \t\t\twhere NONE( rel in r WHERE type(rel)='HAT_PARAMETER') \
                           \n \t\t\twith p,r \n  \t\t\twhere NONE( rel in r WHERE type(rel)='ABLEITUNG') "
        else:
            self.query3 =  "|HAT_PARAMETER|ABLEITUNG"
            self.query2 = ""

            # here is the Query in CYPHER with is used to talk to the neo4j DBMS
        # cypher is the programming language  for neo4j


        self.QueryVariablelength = "\
            Match  p = (n:" + self.NodeTpl[0]+ " {Name:'" + self.NodeTpl[1] + \
                                   "'})-[r:URSACHE_WIRKUNG" +self.query3+"*" + str(
            self.QueryLength) + "]-(m:" + self.NodeTpl[2] + " {Name:'" + self.NodeTpl[3] + "'}) \n\
            where NONE( rel in r WHERE type(rel)='"+str("IST_TEIL")+"') \n \t\t\twith p,r \n\
            where NONE( rel in r WHERE type(rel)='"+str("WIRD_ANGEWENDET")+"') "+ self.query2 + " \
             \n \t\t\treturn distinct p, [node in Nodes(p) | node.Name ] as Names limit 500 \n  " \

            # removal of `` after p = (n:                                                                           \
            # with distinct p, m, n \n \
            # " + query2 +  "\n \
        print("Cypher Statement is: \n")
        print(str(self.QueryVariablelength).ljust(1))
        return self.QueryVariablelength, self.NumberInputs

    def VariableLengthwithnodeweights(self):
        """ This class/function gets a tuple of node labels and properties
                    lorme ispsum

                    :param:  NodeTpl - Tuple of (Startnodelabel, Startnodenameproperty, Endnodelabel , Endnodenameproperty)
                    :param:  LengthQuery - int() of chain length for query
                    :param:  ExecptionPath - Cypher string of path which will be excluded from query (not implemented yet)

                    :returns: cypher string for Query

                """
        # this functions builds the query with variable lenght paths
        # Variables as Command Parameters
        # set manually for Test

        # input_startcategory = nodetuple[0] "Flussgröße"
        # input_startnode =  nodetuple[1] "Kraft"
        # input_endcategory = nodetuple[2]  "Flussgröße"
        # input_endnode = nodetuple[3]  "Kraft"
        # Lenght_query = "1..3"
        self.NumberInputs = 1 # potential future functions
         # potential future functions

        if self.UW is True: # only :URSACHE_WIKRUNGSPFAD
            self.query3 = ""
            self.query2 = " \n \t\t\twith p,r \n \t\t\twhere NONE( rel in r WHERE type(rel)='HAT_PARAMETER') \
                           \n \t\t\twith p,r \n  \t\t\twhere NONE( rel in r WHERE type(rel)='ABLEITUNG') "
        else:
            self.query3 =  "|HAT_PARAMETER|ABLEITUNG"
            self.query2 = ""
        if self.NodeTpl[2] =="":
            self.query4 = " "

        elif self.NodeTpl[3] =="":
            self.query4 = ":`" + str(self.NodeTpl[2]) +"`"
        else:
            self.query4 = ":"+ str(self.NodeTpl[2])+ " {Name:'" + str(self.NodeTpl[3]) + "'}"

            # here is the Query in CYPHER with is used to talk to the neo4j DBMS
        # cypher is the programming language  for neo4j


        self.QueryVariablelength = "\
            Match  p = (n:" + self.NodeTpl[0]+ " {Name:'" + self.NodeTpl[1] + \
                                   "'})-[:URSACHE_WIRKUNG" +self.query3+"*" + str(
            self.QueryLength) + "]-(m"+ str(self.query4) + ") \n\
            with *,relationships(p) as r \n\
            where NONE( rel in r WHERE type(rel)='"+str("IST_TEIL")+"') \n \t\t\twith * \n\
            where NONE( rel in r WHERE type(rel)='"+str("WIRD_ANGEWENDET")+"') "+ self.query2 + " \n\
            with *, [nd in nodes(p) | (toInteger(nd.weight)) ] as weights\n\
            where apoc.coll.sum(weights) <=" +str(self.Maxweight) +" \n\
            \n \t\t\treturn distinct p, [nd in Nodes(p) | nd.Name ] as Names, apoc.coll.sum(weights) as rank, count(p), weights\n\
            order by apoc.coll.sum(weights)  limit 800 \n  " \

            # removal of `` after p = (n:                                                                           \
            # with distinct p, m, n \n \
            # " + query2 +  "\n \
        print("Cypher Statement is: \n")
        print(str(self.QueryVariablelength).ljust(1))
        return self.QueryVariablelength, self.NumberInputs

    def VariableLengthwithedgeweights(self):
        """ This class/function gets a tuple of node labels and properties
                    lorme ispsum

                    :param:  NodeTpl - Tuple of (Startnodelabel, Startnodenameproperty, Endnodelabel , Endnodenameproperty)
                    :param:  LengthQuery - int() of chain length for query
                    :param:  ExecptionPath - Cypher string of path which will be excluded from query (not implemented yet)

                    :returns: cypher string for Query

                """
        # this functions builds the query with variable lenght paths
        # Variables as Command Parameters
        # set manually for Test

        # input_startcategory = nodetuple[0] "Flussgröße"
        # input_startnode =  nodetuple[1] "Kraft"
        # input_endcategory = nodetuple[2]  "Flussgröße"
        # input_endnode = nodetuple[3]  "Kraft"
        # Lenght_query = "1..3"
        self.NumberInputs = 1 # potential future functions
         # potential future functions

        if self.UW is True:
            self.query3 = ""
            self.query2 = " \n \t\t\twith p,r \n \t\t\twhere NONE( rel in r WHERE type(rel)='HAT_PARAMETER') \
                           \n \t\t\twith p,r \n  \t\t\twhere NONE( rel in r WHERE type(rel)='ABLEITUNG') "
        else:
            self.query3 =  "|HAT_PARAMETER|ABLEITUNG"
            self.query2 = ""

            # here is the Query in CYPHER with is used to talk to the neo4j DBMS
        # cypher is the programming language  for neo4j


        self.QueryVariablelength = "\
            Match  p = (n:" + self.NodeTpl[0]+ " {Name:'" + self.NodeTpl[1] + \
                                   "'})-[:URSACHE_WIRKUNG" +self.query3+"*" + str(
            self.QueryLength) + "]-(m:" + self.NodeTpl[2] + " {Name:'" + self.NodeTpl[3] + "'}) \n\
            with *,relationships(p) as r \n\
            where NONE( rel in r WHERE type(rel)='"+str("IST_TEIL")+"') \n \t\t\twith * \n\
            where NONE( rel in r WHERE type(rel)='"+str("WIRD_ANGEWENDET")+"') "+ self.query2 + " \n\
            with *, [rel in r | (toInteger(rel.weight)) ] as weights\n\
            where apoc.coll.sum(weights) <=" +str(self.Maxweight) +" \n\
            \n \t\t\treturn distinct p, [nd in Nodes(p) | nd.Name ] as Names, apoc.coll.sum(weights) as rank, count(p), weights\n\
            order by apoc.coll.sum(weights)  limit 750 \n  " \

            # removal of `` after p = (n:                                                                           \
            # with distinct p, m, n \n \
            # " + query2 +  "\n \
        print("Cypher Statement is: \n")
        print(str(self.QueryVariablelength).ljust(1))
        return self.QueryVariablelength, self.NumberInputs