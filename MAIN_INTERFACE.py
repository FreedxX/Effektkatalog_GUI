# python toolkits
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import copy
import threading
import networkx as nx
from py2neo import Graph, ServiceUnavailable, ConnectionUnavailable  # WireError
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# user defined functions
from FUNCTIONS_FOR_INTERFACE import NameProperties
from FUNCTIONS_FOR_INTERFACE import ExeQuery
from FUNCTIONS_FOR_INTERFACE import FilterQ
from FUNCTIONS_FOR_INTERFACE import Cosmetic
from FUNCTIONS_FOR_INTERFACE import Draw_every_path_in_one_Graph
from FUNCTIONS_FOR_INTERFACE import name_reader
from FUNCTIONS_FOR_INTERFACE import Draw_every_var_for_effect
from FUNCTIONS_FOR_INTERFACE import match_n_add, chrosscheck_cypher, add_parameter, chrosscheck_cypher_get_neighbours
from FUNCTIONS_FOR_INTERFACE import AutocompleteCombobox
from FUNCTIONS_FOR_INTERFACE import ScrollableImage
from FUNCTIONS_FOR_INTERFACE import Link
# from FUNCTIONS_FOR_INTERFACE import button_pressed



# Author: Stephan Matzke
# contact: stephan_matzke@gmx.net


class GUIApp:
    """ This class is the Main Interface for the Effect-catalog-tool

        Open Graphical User Interface to query Effect-chains

        This Program is used to help designers to evaluate physical effect catalogs (GER: Effekt/-Konstruktionskataloge)
        Users can Query a potenial effect combination between and impact variable and a cause variable
        Effects, and variables are represented as Nodes, Nodes have properties (like dictionaries)
        e.g.: (Node('Geometrische Eigenschaft', Einheit='m', Name='Abstand', **{'SI-Einheit': 'm'})
        associated paper: DOI- XXXX

        the query is programmed in CYPHER. Cypher is the programming language of neo4j the tool for the graph DBMS
        https://neo4j.com/docs/cypher-refcard/current/
            Cypher Read query structure:
                [USE]
                [MATCH WHERE]
                [OPTIONAL MATCH WHERE]
                [WITH [ORDER BY] [SKIP] [LIMIT]]
                RETURN [ORDER BY] [SKIP] [LIMIT]

        The DBMS needs to setup with the graph database by import



        Prerequisites are following toolkits/files:

            - networkx
            - py2neo
            - tkinter
            - matplotlib
            - FUNCTIONS_FOR_INTERFACE.py
            - QUERY_FOR_INTERFACE.py

        software used is:
            - Pycharm 2021.2.3 (community Edition)  build October 19, 2021
            - Neo4j 4.4.3 build 11 January 2022

        to change the used PW please change auth in line 101:  self.graph = Graph(auth=('neo4j', 'neo4j3'))

        If needed toolkits can be installed with Anaconda:

        conda install -c conda-forge matplotlib
        conda install -c conda-forge pandas
        conda install -c conda-forge py2neo
        conda install -c conda-forge networkx
        conda update --all

        if before installing monotonic matplotlib runs
        conda install -c conda-forge monotonic

        if packaging is not found
        conda install -c conda-forge packaging

        if matplotlib runs but py2neo not
        conda install -c conda-forge regex
        conda install -c anaconda pillow
        conda install -c conda-forge requests


    :param:  impacts and cause
    :param:  filter and selection options

    :return: Effect-chains for input

         """

    # constructor is a special function run when we first create an instance of the class method
    # constructor initializes a instance oif the class
    # constructor is __init__(self)

    def __init__(self):

        # self is a marker of an Instance. self.variable =/= variable the first one is only
        # the instance is referenced to the GUI app class GUIApp == self.

        # a variable can be referenced to the GUIApp class by the prefix self. by adding the prefix
        # prior to the variable: e.g.: self.variable
        #




        try:
            # copied from the python documentation:
            # The try statement specifies exception handlers and/or cleanup code for a group of statements:

            # setup the toolkit py2neo, respectively the Graph class object
            # variables are the authenification auth=(Username, Password)

             # for "Test dbms
            # graph = Graph(auth=('neo4j','neo4jj'))
            # graph = Graph(auth=('neo4j', 'neo4j3'))  # for dbms "test"  # for insert dbms PW: neo4j3 , 'neo4j2',
            # Graph username and passwort variable is set to  default
            self.graphus='neo4j'
            self.graphpw ='neo4j3'
            self.graph = Graph(auth=(self.graphus, self.graphpw))

        except (IndexError, ConnectionUnavailable, OSError):

            self.prompt = tk.Tk()
            # except (IndexError, ConnectionRefusedError, IOError, OSError, TypeError,
            #         ServiceUnavailable, ConnectionUnavailable):

            # all these Error type occur when no neo4j connection can be established,
            # the handler displays an according message and ask user to check the server or the password

            # Below ist the Function Label from Tintker used the tkinter toolkit is abbreviated
            # the label is dispalyed in the window named prompt
            self.label2 = ttk.Label(self.prompt, text="Bitte geben Sie das korrekte Passwort für die Datenbank ein: \nBeenden mit STRG+Q")
            self.label3 = tk.Label(self.prompt)
            self.label3["fg"] = "#333333"
            self.label3["justify"] = "center"
            self.label3["text"] = "Eingabe Benutzername"

            self.entry1 = ttk.Entry(self.prompt)

            self.label4 = tk.Label(self.prompt)
            self.label4["fg"] = "#333333"
            self.label4["justify"] = "center"
            self.label4["text"] = "Eingabe Passwort  "

            self.entry2 = ttk.Entry(self.prompt)

            self.button1 = ttk.Button(self.prompt)
            self.button1["text"] = "Ok"
            self.button1["command"] = self.resetuserandpw


            self.prompt.bind('<Control-q>', lambda event=None: self.root.destroy())
            # binds the input '<Control-q>'  of the tk.Tk() window named "root" to
            # an anoymous event handler (lambdafunction) which calls tk.Tk().destroy()
            # destroy ends the window,

            # the packer is a function of tk to arrange the widgets automatic in the window
            self.label2.pack(side="top", fill="x", pady=10, padx =10)
            self.label3.pack(side="top", fill="x", pady=10)
            self.entry1.pack(side="top", fill="x", pady=00, padx =30)
            self.label4.pack(side="top", fill="x", pady=10)
            self.entry2.pack(side="top", fill="x", pady=0, padx =30)
            self.button1.pack(side="top", fill="x", pady=10)

            self.prompt.mainloop()
            # tk.Tk().mainloop() starts the GUI -- important function

        # ============ FIRST STEPS ===========
        # Create instance of TK() TK stands for Tkinter a toolkit in Phyton for GUIs
        # the TK() class build the basestructure for the programm
        # to access TK() we imported in line 1 Tkinter as tk tk is a abbreviation
        # when we call tk.something something is referenced to the TKinter toolkit
        #
        # the instance created by running tk.TK() is reference or "namded" self.root
        # root is an instance of the GUIApp (-> self.)
        # root represents the class level variable od Tk()

        self.root = tk.Tk()

        # now we can accesw the class instance self.root
        # we are accessing the function self.root.title (tk.TK().title())

        # to create a GUI window with the title "Effektkatalog Abfrage GUI"
        # this is done by setting the argument string to "Effektkatalog Abfrage GUI"
        # in Phyton arguments can be acces directly (by position) or by keyword string="Effektkatalog Abfrage GUI"

        self.root.title("Effektkatalog Abfrage GUI")

        try:


            self.graph = Graph(auth=(self.graphus, self.graphpw))
            # reset the graph assignemtn with the new pw and username


            # getting resolution of screen to place window in the middle of the screen
            # screenwidth = self.root.winfo_screenwidth()
            # screenheight = self.root.winfo_screenheight()

            # creating a placeholder
            # string %D is a placeholder
            # set the geometry according to tk.Tk().geometry(widthx, height, xpostion,yposition) in px
            # WXGA (FHD) display 1280x800 px should by fine for most displays
            ft = tkFont.Font(family='Times', size=10)
            alignstr = '%dx%d+%d+%d' % (1280, 800, 50, 50)
            self.root.geometry(alignstr)

            self.myfont = tkFont.Font(family='TkDefaultFont', size=8)
            self.root.option_add('*font', self.myfont)
            self.mystyle = ttk.Style()
            self.mystyle.configure("my.TCheckbutton", font=('TkDefaultFont', 8))
            self.mystyle.configure("my.TButton", font=('TkDefaultFont', 8))

            # should window be resizeable with mouse cursor?
            self.root.resizable(width=True, height=True)
            # self.default_font = tk.tkFont.nametofont("TkDefaultFont")
            # self.default_font.configure(size=48)


            # variables needed in the following
            # the variables are declared here as empty types (list()..) some as None-type
            self.G = nx.Graph()
            self.G2 = nx.MultiDiGraph()
            self.G3 = nx.MultiDiGraph()
            self.G4 = nx.MultiDiGraph()
            self.Gmod = nx.Graph()
            self.Gorg = nx.Graph()
            self.Gclick = nx.Graph()
            self.lvar = None
            self.listpar = None
            self.listeff = None
            self.effectdict = {}
            self.originalNamesQueryPaths = list()
            self.modifiedNamesQuerypaths = list()
            self.cosmeticoriginal = Cosmetic(None)
            self.cosmeticmodified = Cosmetic(None)
            self.DataTable = ExeQuery()
            self.attrDict = dict()
            self.NamesQueryPaths = list()
            self.newmenu = list()
            self.adparameter = tuple()
            self.a = str()
            self.b = str()
            self.c = int()
            self.paths = list()
            self.username = str()
            self.PW = str()
            self.listexample = tuple()
            self.colourdict = list()
            self.labeldict = dict()
            self.query2 = str()
            self.data_table2 = None
            self.dist1 = 30
            self.dist2r1 = 30
            self.dist2r2 = 30
            self.dist2r3 = 30
            self.UW = bool()
            self.gs = list()
            self.query=list((str(),int()))


            # ====== Setup Tabs ======

            # this is a function from Tkinter ttk to create tabs
            # ttk is simialr to tk but uses more 'modern' style

            self.tabControl = ttk.Notebook(self.root)


            # setup  3 taps with ttk.Frame().add 12 tab is hidden immediately again

            self.tab0 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab0, text="Effektabfrage aus DBMS")
            # self.tabControl.hide(self.tab1) <-- this is a commented out line of code = not compiled by the interpreter
            # use STRG+ / to bulk un-/ re- comment lines

            self.tab4 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab4, text="Effektinformationen")
            # self.tabControl.hide(self.tab4)


            self.tab1 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab1, text="Effekteingabe in DBMS")

            self.tab2 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab2, text="Effekteingabe in DBMS")
            self.tabControl.hide(self.tab2)

            self.tab3 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab3, text="Parametereingabe in DBMS")
            self.tabControl.hide(self.tab3)

            self.tab5 = ttk.Frame(self.tabControl)
            self.tabControl.add(self.tab5, text="Informationen zur Vollständigkeit")
            # self.tabControl.hide(self.tab5)



            # place the tab control in the gui window with tk.Frame.pack
            self.tabControl.pack(expand=1, fill="both")

            print("\n\n=========================================================================")
            print("==============================SETUP RUNNING==============================")
            print("=========================================================================\n\n")

            # ====== Setup widgets for tab0  - LEFT COLUMN======

            # use tk.Label to crate a label = a plain line of text
            self.ent0t0 = tk.Label(self.tab0)

            # label for optm0t0 (Domäne)

            # setup of label (color, text position, displayed text, and absolute position in window)
            # attributes for Label objects can be set up directly like the tab Label(self.tab0)
            # or later by addressing the attribute directly self.Label["Attribute Name"]
            self.ent0t0["fg"] = "#333333"
            self.ent0t0["justify"] = "left"
            self.ent0t0["text"] = "Auswahl Domäne    \n(nur Zustandsgrößen)"
            self.ent0t0.place(x=50, y=20, width=130, height=40)

            # setup  of a tuple of listentries for the AutocompleteCombobox
            # the listentries are filled by using the function NameProperties.GetNode()
            # for more information STRG click on NameProperties
            self.listentr0t0 = [*sorted(NameProperties("Domäne", None, None, self.graph).GetNode()), "Bitte Wählen"]

            # AutocompleteCombobox is a 'ttk.Combobox` widget that features autocompletion.
            self.optm0t0 = AutocompleteCombobox(self.tab0, self.listentr0t0, 'readonly')
            self.optm0t0.place(x=50, y=60, width=200, height=30)

            # bind the event "<<ComboboxSelected>>" to the user defined function  self.optm0t0_command
            self.optm0t0.bind("<<ComboboxSelected>>", self.optm0t0_command)

            # set the Entry to display in the Combobox to "Bitte Wählen"
            self.optm0t0.set("Bitte Wählen")

            # repeat for other widgets
            self.ent1t0 = tk.Label(self.tab0)

            # label for optm1t0 (Teildomäne)
            self.ent1t0["fg"] = "#333333"
            self.ent1t0["justify"] = "left"
            self.ent1t0["text"] = "Auswahl Subdomäne \n(nur Zustandsgrößen)"
            self.ent1t0.place(x=50, y=110, width=132, height=40)

            self.listentr1t0 = [*sorted(NameProperties("Teildomäne", None, None, self.graph).GetNode()), "Bitte Wählen"]
            self.optm1t0 = AutocompleteCombobox(self.tab0, self.listentr1t0, 'readonly')
            self.optm1t0.place(x=50, y=150, width=200, height=30)
            self.optm1t0.bind("<<ComboboxSelected>>", self.optm1t0_command)
            self.optm1t0.set("Bitte Wählen")

            self.ent2t0 = tk.Label(self.tab0)
            # label for optm1t0 (Teildomäne)
            self.ent2t0["fg"] = "#333333"
            self.ent2t0["justify"] = "left"
            self.ent2t0["text"] = "Auswahl Zustandsgröße"
            self.ent2t0.place(x=50, y=210, width=145, height=40)

            self.listentr2t0 = ["Flussgröße", "Extensum", "Potentialgröße",
                                "Primärgröße", 'Abgeleitete Größe', "None"]
            self.optm2t0 = AutocompleteCombobox(self.tab0, self.listentr2t0, 'readonly')
            self.optm2t0.place(x=50, y=240, width=200, height=30)
            self.optm2t0.bind("<<ComboboxSelected>>", self.optm2t0_command)
            self.optm2t0.set("Bitte Wählen")

            self.ent3t0 = tk.Label(self.tab0)
            # label for optm1t0 (Teildomäne)
            self.ent3t0["fg"] = "#333333"
            self.ent3t0["justify"] = "left"

            self.ent3t0["text"] = "Auswahl Ursache"
            self.ent3t0.place(x=50, y=300, width=105, height=40)

            # Get Relationship is similar to getNode but returns the nodes connetected to "Teildomäne"
            self.listentr3t0 = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()]
            self.optm3t0 = AutocompleteCombobox(self.tab0, self.listentr3t0, 'readonly')
            self.optm3t0.place(x=50, y=330, width=200, height=30)
            self.optm3t0.bind("<<ComboboxSelected>>", self.optm3t0_command)
            self.optm3t0.set("Bitte Wählen")


            self.msg6t0 = ttk.Label(self.tab0)
            self.msg6t0.place(x=50, y=380, width=120, height=40)
            self.msg6t0["justify"] = "left"
            self.msg6t0["text"] = "Maximale Pfadlänge\nder Abfrage"

            self.entr1t0 = ttk.Entry(self.tab0, validate="key",
                                     validatecommand=(self.tab0.register(lambda char:  char.isdigit()), '%S'))
            self.entr1t0.place(x=50+160, y=380, width=40, height=30)
            self.entr1t0.insert(tk.END,10)

            self.msg7t0 = ttk.Label(self.tab0)
            self.msg7t0.place(x=50, y=420, width=150, height=40)
            self.msg7t0["justify"] = "left"
            self.msg7t0["text"] = "Maximale Summe des Gewichts \nder Abfrage"

            self.entr2t0 = ttk.Entry(self.tab0, validate="key",
                                     validatecommand=(self.tab0.register(lambda char: char.isdigit()), '%S'))
            self.entr2t0.place(x=50 + 160, y=420, width=40, height=30)
            self.entr2t0.insert(tk.END, 20)

            self.chb2t0 = ttk.Checkbutton(self.tab0, style="my.TCheckbutton")
            self.chb2t0Var = tk.BooleanVar()
            self.chb2t0["text"] = "Verwenden der Kantengewichte"
            self.chb2t0["offvalue"] = False
            self.chb2t0["onvalue"] = True
            self.chb2t0["variable"] = self.chb2t0Var
            self.chb2t0.place(x=50, y=460, width=190, height=20)


            self.msg5t0 = ttk.Label(self.tab0)
            self.msg5t0.place(x=50, y=490, width=200, height=30)
            self.msg5t0["justify"] = "left"

            # ====== Setup widgets for tab0  - MID COLUMN======

            self.ent5t0 = tk.Label(self.tab0)
            # label for optm0t0 (Domäne)
            self.ent5t0["fg"] = "#333333"
            self.ent5t0["justify"] = "left"
            self.ent5t0["text"] = "Auswahl Domäne    \n(nur Zustandsgrößen)"
            self.ent5t0.place(x=300, y=20, width=130, height=40)

            self.listentr5t0 = [*sorted(NameProperties("Domäne", None, None, self.graph).GetNode()), "Bitte Wählen"]
            self.optm5t0 = AutocompleteCombobox(self.tab0, self.listentr5t0, 'readonly')
            self.optm5t0.place(x=300, y=60, width=200, height=30)
            # self.entr0t0.bind("<<ComboboxSelected>>", lambda _: self.entr0t0_command )
            self.optm5t0.bind("<<ComboboxSelected>>", self.optm5t0_command)
            self.optm5t0.set("Bitte Wählen")

            self.ent6t0 = tk.Label(self.tab0)
            # label for optm1t0 (Teildomäne)
            self.ent6t0["fg"] = "#333333"
            self.ent6t0["justify"] = "left"
            self.ent6t0["text"] = "Auswahl Subdomäne \n(nur Zustandsgrößen)"
            self.ent6t0.place(x=300, y=110, width=130, height=40)

            self.listentr6t0 = [*sorted(NameProperties("Teildomäne", None, None, self.graph).GetNode()), "Bitte Wählen"]
            self.optm6t0 = AutocompleteCombobox(self.tab0, self.listentr6t0, 'readonly')
            self.optm6t0.place(x=300, y=150, width=200, height=30)
            self.optm6t0.bind("<<ComboboxSelected>>", self.optm6t0_command)
            self.optm6t0.set("Bitte Wählen")

            self.ent7t0 = tk.Label(self.tab0)
            # label for optm1t0 (Teildomäne)
            self.ent7t0["fg"] = "#333333"
            self.ent7t0["justify"] = "left"
            self.ent7t0["text"] = "Auswahl Variable oder Parameter"
            self.ent7t0.place(x=300, y=210, width=195, height=40)

            self.listentr7t0 = ["Flussgröße", "Extensum", "Potentialgröße",
                                "Primärgröße", 'Abgeleitete Größe', "Gestaltparameter",
                                "Stoffliche Eigenschaft", "Geometrische Eigenschaft", "None"]
            self.optm7t0 = AutocompleteCombobox(self.tab0, self.listentr7t0, 'readonly')
            self.optm7t0.place(x=300, y=240, width=200, height=30)
            self.optm7t0.bind("<<ComboboxSelected>>", self.optm7t0_command)
            self.optm7t0.set("Bitte Wählen")

            self.ent8t0 = tk.Label(self.tab0)
            # label for optm1t0 (Teildomäne)
            self.ent8t0["fg"] = "#333333"
            self.ent8t0["justify"] = "left"
            self.ent8t0["text"] = "Auswahl Wirkungsgröße"
            self.ent8t0.place(x=300, y=300, width=145, height=40)

            self.listentr8t0 = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()]+["beliebig"]
            self.optm8t0 = AutocompleteCombobox(self.tab0, self.listentr8t0, 'readonly')
            self.optm8t0.place(x=300, y=330, width=200, height=30)
            self.optm8t0.bind("<<ComboboxSelected>>", self.optm8t0_command)
            self.optm8t0.set("Bitte Wählen")

            self.chb1t0 = ttk.Checkbutton(self.tab0)
            self.chb1t0["text"] = "Alle direkten Schleifen \n(z.B.: A-B-A / A-B-C-A) filtern"
            self.chb1t0Var = tk.IntVar()
            self.chb1t0["offvalue"] = False
            self.chb1t0["style"] = "my.TCheckbutton"
            self.chb1t0["onvalue"] = True
            self.chb1t0["command"] = self.chb1t0_command
            self.chb1t0["variable"] = self.chb1t0Var
            self.chb1t0.place(x=300, y=380, width=170, height=36)

            self.chb0t0 = ttk.Checkbutton(self.tab0, style="my.TCheckbutton")
            self.chb0t0Var = tk.BooleanVar()
            self.chb0t0["text"] = "nur Pfade von Zustandsgrößen"
            self.chb0t0["offvalue"] = False
            self.chb0t0["onvalue"] = True
            self.chb0t0["command"] = self.chb0t0_command
            self.chb0t0["variable"] = self.chb0t0Var
            self.chb0t0.place(x=300, y=420, width=190, height=36)


            self.btn9t0 = ttk.Button(self.tab0)
            # button for optm3t1 (type Zustandgröße Eingang)
            self.btn9t0["text"] = "Start der Abfrage "
            self.btn9t0["style"] = "my.TButton"
            self.btn9t0.place(x=300, y=474, width=200, height=36)
            self.btn9t0["command"] = self.btn9t0_command
            self.msg5t0.config(text="")



            # currently not used
            # self.msg4t0 = tk.Label(self.tab0)
            # self.msg4t0["bg"] = "#ffffff"
            # self.msg4t0["justify"] = "left"
            # self.msg4t0.place(x=640, y=525, width=590, height=230)
            # the listbox ist the area whrer the results are displayed
            self.msg4t0 = tk.Listbox(self.tab0)
            self.msg4t0["bg"] = "#ffffff"
            self.msg4t0["justify"] = "left"
            # self.msg4t0["selectmode"] = "EXTENDED"

            self.msg4t0.activate(0)
            self.msg4t0.insert(0, " ")
            self.msg4t0.selection_anchor(0)
            self.msg4t0.place(x=50, y=525, width=1180, height=230)
            # self.msg4t0.bind("<Button-3>", self.btn4t0_command)
            self.msg4t0.bind("<ButtonRelease-1>", self.msg4t0_command1)
            self.msg4t0.bind("<Return>", self.msg4t0_command1)

            # =============== right side figure=============
            # make graph field adjustable to screen height? - NO

            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1, 1, 1)
            self.fig.tight_layout()
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color='orange')
            self.FCtk1t0 = FigureCanvasTkAgg(self.fig, master=self.tab0)
            # self.FCtk1t1.draw()
            # self.FCtk1t1["bg"] = "#ffffff"
            # self.FCtk1t1["justify"] = "left"
            self.FCtk1t0.get_tk_widget().place(x=580, y=30, width=650, height=480)

            self.btn4t0 = ttk.Button(self.tab0)
            self.btn4t0["text"] = "Effektinformationen"
            self.btn4t0["style"] = "my.TButton"
            self.btn4t0["command"] = self.btn4t0_command
            self.btn4t0.place(x=580, y=30, width=120, height=30)

            self.button = ttk.Button(master=self.tab0, text="Quit", command=self._quit, style="my.TButton")
            self.button.place(x=0, y=0, width=38, height=30)

            # ====== Setup for Effektinformation tab =============

            self.btn8t4 = ttk.Button(self.tab4)
            # button for optm3t1 (type Zustandgröße Eingang)
            self.btn8t4["text"] = "Angrenzende Effekte Anzeigen"
            self.btn8t4["style"] = "my.TButton"
            self.btn8t4.place(x=50, y=280, width=200, height=36)
            #grid(row=12, column=1, sticky="n s w e", )
            self.btn8t4["command"] = self.btn8t4_command

            self.ent7t4 = tk.Label(self.tab4)
            # label for optm1t0 (Teildomäne)
            self.ent7t4["fg"] = "#333333"
            self.ent7t4["justify"] = "left"
            self.ent7t4["text"] = "Auswahl Objekt-Eigenschaft"
            self.ent7t4.place(x=50, y=20, width=170, height=36)
            #grid(row=1, column=1, sticky="sw", padx=5, pady=5)

            self.listentr7t4 = ["Name", "Ausprägung"]
            self.optm7t4 = AutocompleteCombobox(self.tab4, self.listentr7t4, 'readonly')
            self.optm7t4.place(x=50, y=50, width=200, height=30)
            #grid(row=2, column=1, sticky="nw",padx=5,pady=5, ipady=5)  #
            self.optm7t4.bind("<<ComboboxSelected>>", self.optm7t4_command)
            self.optm7t4.set("Name")

            self.ent1t4 = tk.Label(self.tab4)
            # label for optm1t0 (Teildomäne)
            self.ent1t4["fg"] = "#333333"
            self.ent1t4["justify"] = "left"
            self.ent1t4["text"] = "Auswahl Typ"
            self.ent1t4.place(x=50, y=80, width=80, height=40)
            #grid(row=4, column=1, sticky="sw", padx=5, pady=5)

            self.listentr1t4 = ["Zustandsgröße", "Parameter",
                                "Effekt", "Parameter-Effekt", "alle"]
            self.optm1t4 = AutocompleteCombobox(self.tab4, self.listentr1t4, 'readonly')
            self.optm1t4.place(x=50, y=110, width=200, height=30)
            #grid(row=5, column=1, sticky="nw",padx=5,pady=5, ipady=5)
            self.optm1t4.bind("<<ComboboxSelected>>", self.optm1t4_command)
            self.optm1t4.set("Bitte Wählen")



            self.ent2t4 = tk.Label(self.tab4)
            # label for optm1t0 (Teildomäne)
            self.ent2t4["fg"] = "#333333"
            self.ent2t4["justify"] = "left"
            self.ent2t4["text"] = "Auswahl Objekt nach Eigenschaft"
            self.ent2t4.place(x=50, y=140, width=200, height=40)
            #grid(row=6, column=1, sticky="n s w e")

            self.listentr2t4 = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()] + \
                                [*NameProperties("Effekt", None, None, self.graph).GetNode()] + \
                                [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            self.optm2t4 = AutocompleteCombobox(self.tab4, self.listentr2t4, 'readonly')
            self.optm2t4.place(x=50, y=170, width=200, height=30)
            #grid(row=7, column=1, sticky="n s w e")  #
            self.optm2t4.bind("<<ComboboxSelected>>", self.optm2t4_command)
            self.optm2t4.set("Bitte Wählen")

            self.ent3t4 = tk.Label(self.tab4)
            # label for optm1t0 (Teildomäne)
            self.ent3t4["fg"] = "#333333"
            self.ent3t4["justify"] = "left"
            self.ent3t4["text"] = "Auswahl Objekt aus angewählter Effektkette"
            self.ent3t4["wraplength"]=150
            self.ent3t4.place(x=50, y=204, width=142, height=36)
            #grid(row=9, column=1, sticky="n s w e")            #

            self.listentr3t4 = ["Effektkette n/a"]
            self.optm3t4 = AutocompleteCombobox(self.tab4, self.listentr3t4, 'readonly')
            self.optm3t4.place(x=50, y=240, width=200, height=30)
            #grid(row=10, column=1, sticky="n s w e")   #
            self.optm3t4.bind("<<ComboboxSelected>>", self.optm3t4_command)
            self.optm3t4.set("Bitte Wählen")

            self.ent5t4 = tk.LabelFrame (self.tab4)
            self.ent5t4["text"] = "Effektinformationen"
            self.ent5t4.place(x=50, y=320, width=200, height=410)
            #grid(row=13, column=1, sticky="n s w e")

            self.ent6t4 = tk.Label(self.ent5t4)
            self.ent6t4["justify"] = "left"
            self.ent6t4["text"] = "Bitte wählen sie ein Objekt beim Namen aus um Informationen hier anzeigen zu lassen"
            self.ent6t4["wraplength"]= 180
            self.ent6t4.place(x=5, y=5)

            self.link8t4 = Link(self.ent5t4, link='www.google.com', font=self.myfont )
            self.link8t4["text"]=""
            self.link8t4.place(x=5, y=360)

             # clicking the link



            self.fig4 = plt.figure()
            self.axt4 = self.fig4.add_subplot(1, 1, 1)
            self.fig4.tight_layout()
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            nx.draw(self.G4, ax=self.axt4, with_labels=True, font_weight='bold', node_color='orange')
            self.FCtk1t4 = FigureCanvasTkAgg(self.fig4, master=self.tab4)
            # self.FCtk1t1.draw()
            # self.FCtk1t1["bg"] = "#ffffff"
            # self.FCtk1t1["justify"] = "left"
            self.FCtk1t4.get_tk_widget().place(x=300, y=30, width=900, height=700)
            #grid(row=1, column=3, padx=15,pady=15, rowspan=14, columnspan=14, sticky="n s w e")


            self.buttont4 = ttk.Button(master=self.tab4, text="Quit", command=self._quit, style="my.TButton")
            self.buttont4.place(x=0, y=0, width=38, height=30) #grid(row=0, column=0, sticky="n w", padx =4, ipady = 5  )

            # ========================Tab 5  overview of completness=============================

            self.labelt5 = tk.Label(self.tab5, text=
            "Hier dargestellt finden sich alle direkten (Reichweite 1) "
            "Effekte der Datenbank zum Zeitpunkt der Konfiguration")
            self.labelt5.place(x=50, y=20, width=550)
            self.img  = tk.PhotoImage(file="Matrix_füllstand_1675_1142.png")
            self.image_window = ScrollableImage(self.tab5, image=self.img, scrollbarwidth=20,
                                           width=1150, height=700)
            # self.linecanvast5 = tk.Canvas(self.tab5, width=1100, height=800)
            self.image_window.place(x=50, y=50)
            # self.meta = tk.PhotoImage(file='Matrix_füllstand.png')
            # self.linecanvast5.create_image(10, 10, image=self.meta, anchor="nw")

            self.buttont5 = ttk.Button(master=self.tab5, text="Quit", command=self._quit, style="my.TButton")
            self.buttont5.place(x=0, y=0, width=38, height=30)


            # ====== Setup widgets for tab0  Setup Password box for "Effekteingabe Fenster" =====
            self.dist1 = 30
            self.ent0t1 = tk.Label(self.tab1)
            self.ent0t1["fg"] = "#333333"
            self.ent0t1["justify"] = "center"
            self.ent0t1["text"] = "Eingabe Benutzername"
            self.ent0t1.place(x=50, y=self.dist1, width=135, height=25)

            self.dist1 = self.dist1 + 30
            self.entr0t1 = ttk.Entry(self.tab1)
            self.entr0t1.place(x=50, y=self.dist1, width=145, height=25)

            self.dist1 = self.dist1 + 40
            self.ent1t1 = tk.Label(self.tab1)
            self.ent1t1["fg"] = "#333333"
            self.ent1t1["justify"] = "center"
            self.ent1t1["text"] = "Eingabe Passwort  "
            self.ent1t1.place(x=50, y=self.dist1, width=120, height=25)

            self.dist1 = self.dist1 + 30
            self.entr1t1 = ttk.Entry(self.tab1)
            self.entr1t1.place(x=50, y=self.dist1, width=145, height=25)

            self.dist1 = self.dist1 + 40
            self.btn1t1 = ttk.Button(self.tab1)
            self.btn1t1.place(x=50, y=self.dist1, width=50, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn1t1["text"] = "Ok"
            self.btn1t1["command"] = self.btn1t1_command

            self.btn1t1 = ttk.Button(self.tab1)
            self.btn1t1.place(x=105, y=self.dist1, width=50, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn1t1["text"] = "Lock"
            self.btn1t1["command"] = self.btn2t1_command

            # ====== Setup widgets for tab2 ======

            self.ent0t2 = tk.Label(self.tab2)
            self.ent0t2["fg"] = "#333333"
            self.ent0t2["justify"] = "center"
            self.ent0t2["text"] = "Eingabe Effektbezeichnung"
            self.ent0t2.place(x=50, y=self.dist2r1, width=155, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr0t2 = (NameProperties('Effekt', None, None, self.graph).GetNode()+
                                NameProperties('Parameter-Effekt', None, None, self.graph).GetNode())
            self.entr0t2 = AutocompleteCombobox(self.tab2, self.listentr0t2, 'normal')
            self.entr0t2.bind("<<ComboboxSelected>>", self.removelabel)
            self.entr0t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40

            self.ent20t2 = tk.Label(self.tab2)
            self.ent20t2["fg"] = "#333333"
            self.ent20t2["justify"] = "left"
            self.ent20t2["text"] = "Beschreibung einfügen  "
            self.ent20t2.place(x=50, y=self.dist2r1, width=140, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.entr20t2 = ScrolledText(self.tab2)
            self.entr20t2.place(x=50, y=self.dist2r1, width=200, height=50)
            self.dist2r1 = self.dist2r1 + 60

            self.ent9t2 = tk.Label(self.tab2)
            self.ent9t2["fg"] = "#333333"
            self.ent9t2["justify"] = "left"
            self.ent9t2["text"] = "Eingabe Literaturquelle Effekt "
            self.ent9t2.place(x=50, y=self.dist2r1, width=175, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr9t2 = list(['None',] + NameProperties('Effekt', None, None, self.graph).GetOtherProperties("Literatur"))
            self.entr9t2 = AutocompleteCombobox(self.tab2, self.listentr9t2, 'normal')
            self.entr9t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40


            self.ent12t2 = tk.Label(self.tab2)
            self.ent12t2["fg"] = "#333333"
            self.ent12t2["justify"] = "left"
            self.ent12t2["text"] = "Eingabe Formel des Effekts"
            self.ent12t2.place(x=50, y=self.dist2r1, width=160, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr12t2 = list(['None',] + NameProperties('Effekt', None,
                                                                None, self.graph).GetOtherProperties("Formel"))
            self.entr12t2 = AutocompleteCombobox(self.tab2, self.listentr12t2, 'normal')
            self.entr12t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40

            self.ent13t2 = tk.Label(self.tab2)
            self.ent13t2["fg"] = "#333333"
            self.ent13t2["justify"] = "left"
            self.ent13t2["text"] = "Getroffene Vereinfachungen"
            self.ent13t2.place(x=50, y=self.dist2r1, width=160, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr13t2 = list(['None',] + NameProperties('Effekt', None, None, self.graph
                                                                ).GetOtherProperties("Getroffene_Vereinfachungen"))
            self.entr13t2 = AutocompleteCombobox(self.tab2, self.listentr13t2, 'normal')
            self.entr13t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40

            self.ent14t2 = tk.Label(self.tab2)
            self.ent14t2["fg"] = "#333333"
            self.ent14t2["justify"] = "left"
            self.ent14t2["text"] = "Ausprägung des Effektes  "
            self.ent14t2.place(x=50, y=self.dist2r1, width=155, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr14t2 = list(['None',] + NameProperties('Effekt', None, None, self.graph
                                                                ).GetOtherProperties("Ausprägung"))
            self.entr14t2 = AutocompleteCombobox(self.tab2, self.listentr14t2, 'normal')
            self.entr14t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40

            self.ent21t2 = tk.Label(self.tab2)
            self.ent21t2["fg"] = "#333333"
            self.ent21t2["justify"] = "left"
            self.ent21t2["text"] = "Link"
            self.ent21t2.place(x=50, y=self.dist2r1, width=35, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.entr21t2 = ttk.Entry(self.tab2)
            self.entr21t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 40 #+ 80

            self.ent22t2 = tk.Label(self.tab2)
            self.ent22t2["fg"] = "#333333"
            self.ent22t2["justify"] = "left"
            self.ent22t2["text"] = "Einschränkungen"
            self.ent22t2.place(x=50, y=self.dist2r1, width=90, height=25)
            self.dist2r1 = self.dist2r1 + 25

            self.listentr22t2 = list(['None', ]) # + NameProperties('Effekt', None, None, self.graph
                                                  #               ).GetOtherProperties("Einschränkungen"))
            self.entr22t2 = AutocompleteCombobox(self.tab2, self.listentr22t2, 'normal')
            self.entr22t2.place(x=50, y=self.dist2r1, width=200, height=30)
            self.dist2r1 = self.dist2r1 + 30

            self.ent0t2 = tk.Label(self.tab2)
            self.ent0t2["fg"] = "#333333"
            self.ent0t2["justify"] = "left"
            self.ent0t2["text"] = "Bitte 'Chross-Check' durchführen um Effektdopplungen durch unter-\n" \
                                  "schiedliche bezeichnungen zu vermeiden"
            self.ent0t2.place(x=50, y= self.dist2r1 , width=330, height=45)
            self.dist2r1 = self.dist2r1 + 30

            self.msg3t2 = tk.Listbox(self.tab2)
            self.msg3t2["bg"] = "#ffffff"
            self.msg3t2["justify"] = "left"
            self.msg3t2.place(x=50, y=600, width=700, height=160)

            # ==========================================
            # ============= middle column ==============
            # ==========================================

            self.ent1t2 = tk.Label(self.tab2)
            self.ent1t2["fg"] = "#333333"
            self.ent1t2["justify"] = "center"
            self.ent1t2["text"] = "Eingabe Parameter 1 - falls verf.  "
            self.ent1t2.place(x=300, y=self.dist2r2, width=195, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr1t2 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr1t2 = AutocompleteCombobox(self.tab2, self.listentr1t2, 'readonly')
            self.entr1t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr1t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent2t2 = tk.Label(self.tab2)
            self.ent2t2["fg"] = "#333333"
            self.ent2t2["justify"] = "center"
            self.ent2t2["text"] = "Eingabe Parameter 2 - falls verf.  "
            self.ent2t2.place(x=300, y=self.dist2r2, width=195, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr2t2 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr2t2 = AutocompleteCombobox(self.tab2, self.listentr2t2, 'readonly')
            self.entr2t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr2t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent3t2 = tk.Label(self.tab2)
            self.ent3t2["fg"] = "#333333"
            self.ent3t2["justify"] = "center"
            self.ent3t2["text"] = "Eingabe Parameter 3 - falls verf. "
            self.ent3t2.place(x=300, y=self.dist2r2 , width=190, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr3t2 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr3t2 = AutocompleteCombobox(self.tab2, self.listentr3t2, 'readonly')
            self.entr3t2.place(x=300, y=self.dist2r2 , width=200, height=30)
            self.entr3t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent23t2 = tk.Label(self.tab2)
            self.ent23t2["fg"] = "#333333"
            self.ent23t2["justify"] = "center"
            self.ent23t2["text"] = "Eingabe Parameter 4 - falls verf. "
            self.ent23t2.place(x=300, y=self.dist2r2, width=190, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr23t2 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr23t2 = AutocompleteCombobox(self.tab2, self.listentr3t2, 'readonly')
            self.entr23t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr23t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent4t2 = tk.Label(self.tab2)
            self.ent4t2["fg"] = "#333333"
            self.ent4t2["justify"] = "center"
            self.ent4t2["text"] = "Eingabe Parameter 5 - falls verf. "
            self.ent4t2.place(x=300, y=self.dist2r2, width=190, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr4t2 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr4t2 = AutocompleteCombobox(self.tab2, self.listentr4t2, 'readonly')
            self.entr4t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr4t2.set("None")
            self.dist2r2 = self.dist2r2 + 60

            self.ent15t2 = tk.Label(self.tab2)
            self.ent15t2["fg"] = "#333333"
            self.ent15t2["justify"] = "center"
            self.ent15t2["text"] = "Eingabe Beispiel 1 zu Effekt  "
            self.ent15t2.place(x=300, y=self.dist2r2, width=170, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr15t2 = ('None',) + (NameProperties("Beispiel", None, None, self.graph).GetRelationship())
            self.entr15t2 = AutocompleteCombobox(self.tab2, self.listentr15t2, 'write')
            self.entr15t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr15t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent16t2 = tk.Label(self.tab2)
            self.ent16t2["fg"] = "#333333"
            self.ent16t2["justify"] = "center"
            self.ent16t2["text"] = "Eingabe Beispiel 2 zu Effekt  "
            self.ent16t2.place(x=300, y=self.dist2r2, width=170, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr16t2 = ('None',) + (NameProperties("Beispiel", None, None, self.graph).GetRelationship())
            self.entr16t2 = AutocompleteCombobox(self.tab2, self.listentr16t2, 'write')
            self.entr16t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr16t2.set("None")
            self.dist2r2 = self.dist2r2 + 40

            self.ent17t2 = tk.Label(self.tab2)
            self.ent17t2["fg"] = "#333333"
            self.ent17t2["justify"] = "center"
            self.ent17t2["text"] = "Eingabe Beispiel 3 zu Effekt  "
            self.ent17t2.place(x=300, y=self.dist2r2, width=170, height=25)
            self.dist2r2 = self.dist2r2 + 25

            self.listentr17t2 = ('None',) + (NameProperties("Beispiel", None, None, self.graph).GetRelationship())
            self.entr17t2 = AutocompleteCombobox(self.tab2, self.listentr17t2, 'write')
            self.entr17t2.place(x=300, y=self.dist2r2, width=200, height=30)
            self.entr17t2.set("None")
            self.dist2r2 = self.dist2r2 + 60

            # ==========================================
            # ============== right column ==============
            # ==========================================


            self.ent5t2 = tk.Label(self.tab2)
            self.ent5t2["fg"] = "#333333"
            self.ent5t2["justify"] = "center"
            self.ent5t2["text"] = "Eingabe Variable 1 -  falls verf. "
            self.ent5t2.place(x=550, y=self.dist2r3, width=180, height=25)
            self.dist2r3 = self.dist2r3 + 25

            self.listentr5t2 = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())
            self.entr5t2 = AutocompleteCombobox(self.tab2, self.listentr5t2, 'readonly')
            self.entr5t2.place(x=550, y=self.dist2r3, width=200, height=30)
            self.entr5t2.set("None")
            self.dist2r3 = self.dist2r3 + 40

            self.ent6t2 = tk.Label(self.tab2)
            self.ent6t2["fg"] = "#333333"
            self.ent6t2["justify"] = "center"
            self.ent6t2["text"] = "Eingabe Variable 2 -  falls verf. "
            self.ent6t2.place(x=550, y=self.dist2r3, width=180, height=25)
            self.dist2r3 = self.dist2r3 + 25

            self.listentr6t2 = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())
            self.entr6t2 = AutocompleteCombobox(self.tab2, self.listentr6t2, 'readonly')
            self.entr6t2.place(x=550, y=self.dist2r3, width=200, height=30)
            self.entr6t2.set("None")
            self.dist2r3 = self.dist2r3 + 40

            self.ent7t2 = tk.Label(self.tab2)
            self.ent7t2["fg"] = "#333333"
            self.ent7t2["justify"] = "center"
            self.ent7t2["text"] = "Eingabe Variable 3 - falls verf. "
            self.ent7t2.place(x=550, y=self.dist2r3, width=180, height=25)
            self.dist2r3 = self.dist2r3 + 25

            self.listentr7t2 = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())
            self.entr7t2 = AutocompleteCombobox(self.tab2, self.listentr7t2, 'readonly')
            self.entr7t2.place(x=550, y=self.dist2r3, width=200, height=30)
            self.entr7t2.set("None")
            self.dist2r3 = self.dist2r3 + 40

            self.ent8t2 = tk.Label(self.tab2)
            self.ent8t2["fg"] = "#333333"
            self.ent8t2["justify"] = "center"
            self.ent8t2["text"] = "Eingabe Variable 4 - falls verf. "
            self.ent8t2.place(x=550, y=self.dist2r3, width=180, height=25)
            self.dist2r3 = self.dist2r3 + 25

            self.listentr8t2 = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())
            self.entr8t2 = AutocompleteCombobox(self.tab2, self.listentr8t2, 'readonly')
            self.entr8t2.place(x=550, y=self.dist2r3, width=200, height=30)
            self.entr8t2.set("None")
            self.dist2r3 = self.dist2r3 + 60

            self.chb0t2 = ttk.Checkbutton(self.tab2, style="my.TCheckbutton")
            self.chb0t2Var = tk.StringVar()
            self.chb0t2["text"] = "Parameter-Effekt"
            self.chb0t2["offvalue"] = "Effekt"
            self.chb0t2["onvalue"] = "Parameter-Effekt"
            # self.chb0t2["command"] = print("click") #self.chb0t2_command
            self.chb0t2["variable"] = self.chb0t2Var
            self.chb0t2.place(x=550, y=335, width=200, height=30)
            self.chb0t2.invoke()

            self.btn1t2 = ttk.Button(self.tab2)
            self.btn1t2.place(x=550, y=400, width=200, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn1t2["text"] = "Prüfe Eingaben"
            self.btn1t2["command"] = self.btn1t2_command

            self.btn2t2 = ttk.Button(self.tab2)
            self.btn2t2.place(x=550, y=465, width=200, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn2t2["text"] = "Cross check"
            self.btn2t2["command"] = self.btn2t2_command

            self.btn7t2 = ttk.Button(self.tab2)
            self.btn7t2.place(x=550, y=497, width=200, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn7t2["text"] = "Zeige Effekt"
            self.btn7t2["command"] = self.showeffect


            self.btn6t2 = ttk.Button(self.tab2)
            self.btn6t2.place(x=550, y=530, width=200, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn6t2["text"] = "Lösche Eingaben"
            self.btn6t2["command"] = self.clearT2

            self.msg1t2 = tk.Label(self.tab2, text= "")
            self.msg1t2.place(x=550, y=570, width=260, height=20)



            # ====================================
            # ======== right most row ============
            # ====================================

            self.ent8t2 = tk.Label(self.tab2)
            self.ent8t2["fg"] = "#333333"
            self.ent8t2["justify"] = "center"
            self.ent8t2["text"] = "Ergebnis Chross-Check"
            self.ent8t2.place(x=800, y=30, width=145, height=25)

            self.fig2t2 = plt.figure()
            self.ax2t2 = self.fig2t2.add_subplot(1, 1, 1)
            nx.draw(self.G3, ax=self.ax2t2, with_labels=True, font_weight='bold', node_color='orange')
            self.FCtk2t2 = FigureCanvasTkAgg(self.fig2t2, master=self.tab2)
            # self.FCtk1t1.draw()
            # self.FCtk1t1["bg"] = "#ffffff"
            # self.FCtk1t1["justify"] = "left"
            self.FCtk2t2.get_tk_widget().place(x=800, y=30+25, width=430, height=230)

            self.ent8t2 = tk.Label(self.tab2)
            self.ent8t2["fg"] = "#333333"
            self.ent8t2["justify"] = "center"
            self.ent8t2["text"] = " Zusammenfassung der Eingaben "
            self.ent8t2.place(x=800, y=300, width=195, height=25)

            self.fig1t2 = plt.figure()
            self.ax1t2 = self.fig1t2.add_subplot(1, 1, 1)
            nx.draw(self.G2, ax=self.ax1t2, with_labels=True, font_weight='bold', node_color='orange')
            self.FCtk1t2 = FigureCanvasTkAgg(self.fig1t2, master=self.tab2)
            # self.FCtk1t1.draw()
            # self.FCtk1t1["bg"] = "#ffffff"
            # self.FCtk1t1["justify"] = "left"
            self.FCtk1t2.get_tk_widget().place(x=800, y=330, width=430, height=390)




            self.btn3t2 = ttk.Button(self.tab2)
            self.btn3t2.place(x=800, y=730, width=430, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn3t2["text"] = "Bestätigung Eingaben und einfügen in die Datenbank"
            self.btn3t2["command"] = self.btn3t2_command

            self.buttont2 = ttk.Button(master=self.tab2, text="Quit", command=self._quit, style="my.TButton")
            self.buttont2.place(x=0, y=0, width=38, height=30)

            self.btn4t2 = ttk.Button(self.tab2, style="my.TButton")
            self.btn4t2.place(x=0, y=35, width=38, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn4t2["text"] = "Lock"
            self.btn4t2["command"] = self.btn2t1_command

            # ======================================
            # ================ TAB 3 ===============
            # ======================================

            self.ent1t3 = tk.Label(self.tab3)
            self.ent1t3["fg"] = "#333333"
            self.ent1t3["justify"] = "center"
            self.ent1t3["text"] = "Eingabe Parameter Einordnung"
            self.ent1t3.place(x=50, y=30, width=180, height=25)


            self.listentr1t3 = ['None', "Gestaltparameter", "Stoffliche Eigenschaft", "Geometrische Eigenschaft"]
            self.entr1t3 = AutocompleteCombobox(self.tab3, self.listentr1t3, 'readonly')
            self.entr1t3.place(x=50, y=30+25, width=200, height=30)
            self.entr1t3.set("None")



            self.ent2t3 = tk.Label(self.tab3)
            self.ent2t3["fg"] = "#333333"
            self.ent2t3["justify"] = "center"
            self.ent2t3["text"] = "Eingabe Parameter Name"
            self.ent2t3.place(x=50, y=55+40, width=160, height=25)


            self.listentr2t3 = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
            self.entr2t3 = AutocompleteCombobox(self.tab3, self.listentr2t3, 'write')
            self.entr2t3.place(x=50, y=95+25, width=200, height=30)
            self.entr2t3.set("None")

            self.ent3t3 = tk.Label(self.tab3)
            self.ent3t3["fg"] = "#333333"
            self.ent3t3["justify"] = "left"
            self.ent3t3["text"] = "Eingabe Einheit Effekt        "
            self.ent3t3.place(x=50, y=120+40, width=160, height=25)

            self.listentr3t3 = ['None', ]  # + (NameProperties('Effekt', None, None, graph).GetNode())
            self.entr3t3 = AutocompleteCombobox(self.tab3, self.listentr3t3, 'normal')
            self.entr3t3.place(x=50, y=160+25, width=200, height=30)

            self.ent4t3 = tk.Label(self.tab3)
            self.ent4t3["fg"] = "#333333"
            self.ent4t3["justify"] = "left"
            self.ent4t3["text"] = "Eingabe Einheit in Basis Einheit "
            self.ent4t3.place(x=50, y=185+40, width=190, height=25)

            self.listentr4t3 = ['None', ]  # + (NameProperties('Effekt', None, None, graph).GetNode())
            self.entr4t3 = AutocompleteCombobox(self.tab3, self.listentr4t3, 'normal')
            self.entr4t3.place(x=50, y=225+25, width=200, height=30)


            self.btn1t3 = ttk.Button(self.tab3)
            self.btn1t3.place(x=50, y=250+40, width=200, height=30)
            # self.btn1t2["justify"] = "center"
            self.btn1t3["text"] = "Create new parameter"
            self.btn1t3["command"] = self.btn1t3_command

            self.buttont3 = ttk.Button(master=self.tab3, text="Quit", command=self._quit, style="my.TButton")
            self.buttont3.place(x=0, y=0, width=38, height=30)

            self.button2t3 = ttk.Button(self.tab3, style="my.TButton")
            self.button2t3.place(x=0, y=35, width=38, height=30)
            # self.btn1t2["justify"] = "center"
            self.button2t3["text"] = "Lock"
            self.button2t3["command"] = self.btn2t1_command

            # self.entr5t3 = ttk.Entry(self.tab3)
            # self.entr5t3.place(x=300, y=60, width=400, height=200)
            # self.entr5t3.insert(tk.END, "Cypher  QUERY")

            self.linecanvast5 = tk.Canvas(self.tab3, width=1100, height=800)
            self.linecanvast5.place(x=270, y=50)
            self.meta = tk.PhotoImage(file='Graph_Meta_small.png')
            self.linecanvast5.create_image(30, 350, image=self.meta, anchor="nw")
            self.linecanvast5.create_line (0, 0, 0, 650, width=6)




            self.ent5t3 = tk.Label(self.tab3)
            self.ent5t3["fg"] = "#333333"
            self.ent5t3["justify"] = "left"
            self.ent5t3["text"] = "Eingabe Knoten 1"
            self.ent5t3.place(x=300, y=0 + 40, width=100, height=25)

            self.listentr5t3 = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()] + \
                                [*NameProperties("Effekt", None, None, self.graph).GetNode()] + \
                                [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            self.entr5t3 = AutocompleteCombobox(self.tab3, self.listentr5t3, 'normal')
            self.entr5t3.bind("<<ComboboxSelected>>", self.entr5t3_command)
            self.entr5t3.place(x=300, y=5+65, width=200, height=30)

            self.ent6t3 = tk.Label(self.tab3)
            self.ent6t3["text"] = " -----"
            self.ent6t3.place(x=500, y=12+ 60, width=25, height=25)

            self.ent7t3 = tk.Label(self.tab3)
            self.ent7t3["text"] = "Gewicht"
            self.ent7t3.place(x=525, y=00 + 40, width=45, height=25)

            self.entr6t3 = ttk.Entry(self.tab3, validate="key",
                                     validatecommand=(self.tab3.register(lambda char: char.isdigit()), '%S'))
            self.entr6t3.place(x=525, y=5+65, width=40, height=30)

            self.ent8t3 = tk.Label(self.tab3)
            self.ent8t3["text"] = "----->"
            self.ent8t3.place(x=565, y=12+60, width=26, height=25)


            self.ent9t3 = tk.Label(self.tab3)
            self.ent9t3["fg"] = "#333333"
            self.ent9t3["justify"] = "left"
            self.ent9t3["text"] = "Eingabe Knoten 2"
            self.ent9t3.place(x=595, y=0 + 40, width=100, height=25)

            self.button4t3 = ttk.Button(self.tab3, style="my.TButton")
            self.button4t3.place(x=850, y=70, width=100, height=30)
            self.button4t3["text"] = "Anwenden"
            self.button4t3["command"] = self.btn4t3_command

            self.listentr7t3 = ['None', ]  # + (NameProperties('Effekt', None, None, graph).GetNode())
            self.entr7t3 = AutocompleteCombobox(self.tab3, self.listentr7t3, 'normal')
            self.entr7t3.place(x=595, y=5 + 65, width=200, height=30)

            self.ent10t3 = tk.Label(self.tab3)
            self.ent10t3["text"] = "Es können die Kantengewichte zwischen benachbarten Knoten verändert werden"
            self.ent10t3.place(x=300, y=120, width=400, height=25)

            self.ent11t3 = tk.Label(self.tab3)
            self.ent11t3["fg"] = "#333333"
            self.ent11t3["justify"] = "left"
            self.ent11t3["text"] = "Ändern des individuellen Knotengewichts"
            self.ent11t3.place(x=300, y=40 + 120, width=200, height=25)

            self.listentr11t3 = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()] + \
                                [*NameProperties("Effekt", None, None, self.graph).GetNode()] + \
                                [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            self.entr11t3 = AutocompleteCombobox(self.tab3, self.listentr11t3, 'normal')
            self.entr11t3.place(x=300, y=30 + 160, width=200, height=30)

            self.button5t3 = ttk.Button(self.tab3, style="my.TButton")
            self.button5t3.place(x=850, y=190, width=100, height=30)
            self.button5t3["text"] = "Anwenden"
            self.button5t3["command"] = self.btn5t3_command

            self.ent12t3 = tk.Label(self.tab3)
            self.ent12t3["text"] = "Gewicht"
            self.ent12t3.place(x=525, y=40 + 120, width=45, height=25)

            self.entr12t3 = ttk.Entry(self.tab3, validate="key",
                                     validatecommand=(self.tab3.register(lambda char: char.isdigit()), '%S'))
            self.entr12t3.place(x=525, y=30 + 160, width=40, height=30)

            self.ent13t3 = tk.Label(self.tab3)
            self.ent13t3["fg"] = "#333333"
            self.ent13t3["justify"] = "left"
            self.ent13t3["text"] = "Ändern des  allg Knotengewichts"
            self.ent13t3.place(x=300, y=40 + 190, width=160, height=25)

            self.listentr13t3 = ["Flussgröße", "Extensum", "Potentialgröße", "Primärgröße",
                                 'Abgeleitete Größe', "Gestaltparameter", "Stoffliche Eigenschaft",
                                 "Geometrische Eigenschaft", "Effekt", "Parameter-Effekt"]
            self.entr13t3 = AutocompleteCombobox(self.tab3, self.listentr13t3, 'normal')
            self.entr13t3.place(x=300, y=30 + 230, width=200, height=30)

            self.ent14t3 = tk.Label(self.tab3)
            self.ent14t3["text"] = "Gewicht"
            self.ent14t3.place(x=525, y=40 + 190, width=45, height=25)

            self.button6t3 = ttk.Button(self.tab3, style="my.TButton")
            self.button6t3.place(x=850, y=260, width=100, height=30)
            self.button6t3["text"] = "Anwenden"
            self.button6t3["command"] = self.btn6t3_command

            self.entr14t3 = ttk.Entry(self.tab3, validate="key",
                                      validatecommand=(self.tab3.register(lambda char: char.isdigit()), '%S'))
            self.entr14t3.place(x=525, y=30 + 230, width=40, height=30)

            self.ent16t3 = tk.Label(self.tab3)
            self.ent16t3["fg"] = "#333333"
            self.ent16t3["justify"] = "left"
            self.ent16t3["text"] = "Ändern des  allg Kantengewichts"
            self.ent16t3.place(x=300, y=40 + 260, width=160, height=25)

            self.listentr16t3 = ["ABLEITUNG", "HAT_PARAMETER", "URSACHE_WIRKUNG" ]
            self.entr16t3 = AutocompleteCombobox(self.tab3, self.listentr16t3, 'normal')
            self.entr16t3.place(x=300, y=30 + 300, width=200, height=30)

            self.ent15t3 = tk.Label(self.tab3)
            self.ent15t3["text"] = "Gewicht"
            self.ent15t3.place(x=525, y=40 + 260, width=45, height=25)

            self.entr15t3 = ttk.Entry(self.tab3, validate="key",
                                      validatecommand=(self.tab3.register(lambda char: char.isdigit()), '%S'))
            self.entr15t3.place(x=525, y=30 + 300, width=40, height=30)

            self.button7t3 = ttk.Button(self.tab3, style="my.TButton")
            self.button7t3.place(x=850,  y=330, width=100, height=30)
            self.button7t3["text"] = "Anwenden"
            self.button7t3["command"] = self.btn7t3_command

            self.ent17t3 = tk.LabelFrame(self.tab3)

            self.ent17t3["text"] = "Info zu Gewichten"
            self.ent17t3.place(x=980, y=70, width=250, height=280)

            self.ent18t3 = tk.Label(self.ent17t3)
            self.ent18t3["justify"] = "left"
            self.ent18t3["text"] = "Neue Effekte und Parameter erhalten automatisch Standartgewichte " \
                                   "für Kanten und Knoten \n\n Zustandsgrößen: \t\t 2\n Parameter: \t\t 5\n Effekte: \t\t\t 3" \
                                   "\n Parameter-Effekte: \t 3\n URSACHE_WIRKUNG: \t 2 \n HAT_PARAMETER: \t 4"
            self.ent18t3["wraplength"] = 235
            self.ent18t3.place(x=5, y=5)

            print("\n\n=========================================================================")
            print("===========================MAINLOOP STARTED==============================")
            print("=========================================================================\n\n")

            self.root.bind('<Control-q>', lambda event=None: self.root.destroy())
            # binds the input '<Control-q>'  of the tk.Tk() window named "root" to
            # an anoymous event handler (lambdafunction) which calls tk.Tk().destroy()
            # destroy ends the window,


        except ConnectionUnavailable: #(OSError, ConnectionUnavailable, IndexError)
        # except (IndexError, ConnectionRefusedError, IOError, OSError, TypeError,
        #         ServiceUnavailable, ConnectionUnavailable):

            # all these Error type occur when no neo4j connection can be established,
            # the handler display an according message

            self.label2 = ttk.Label(text="Bitte starte zuerst einen NEO4J Server \n"
                                         "Alternativ war ihr Passwort nicht korrekt"
                                         "\nBeenden mit STRG+Q")

            self.root.bind('<Control-q>', lambda event=None: self.root.destroy())
            # binds the input '<Control-q>'  of the tk.Tk() window named "root" to
            # an anoymous event handler (lambdafunction) which calls tk.Tk().destroy()
            # destroy ends the window,
            self.label2.pack(side="top", fill="x", pady=10, padx=5)

            self.button1 = ttk.Button(self.root)
            self.button1["text"] = "Ok"
            self.button1["command"] = self._quit
            self.button1.pack(side="top", fill="x", pady=10, padx=20)

        self.root.mainloop()
        # tk.Tk().mainloop() starts the GUI -- important function

    def _quit(self):

        """This function gets called to end the programm"""

        self.root.quit()  # stops mainloop
        self.root.destroy()

        # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL state

        print("\n\n=========================================================================")
        print("================================LE FIN===================================")
        print("=========================================================================")
        print("=======most roles:      Stephan Matzke===================================")
        print("=========================================================================")
        print("=========================================================================")

    def  resetuserandpw(self):
        """ This function overwrites the fedault username and passwort from the prompt window in case the default
            passwort was wrong

            :return: ssetup for new Password and Username, destroys prompt
            """
        #t he Variable Graph username and graph password is overwritten with the Entrys of the Entrylabels
        self.graphus = str(self.entry1.get())
        self.graphpw = str(self.entry2.get())

        # quit of Tk.Window and kill of application
        self.prompt.quit()
        self.prompt.destroy() # stops mainloop


    def optm0t0_command(self, event):
        """ This function is a eventhandler for the optm5t0 Combobox command - aka Auswahl Domäne Ursachenseite
            it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm1t0 and optm3t0)
            the function updates the optm1t0 the domain instance of the effect variable and resets optm30
            to "Bitte Wählen"

            aswell it makes an case distinction whether parameters must be queried

        """

        self.newmenu = NameProperties("Domäne", str(self.optm0t0.get()), None, self.graph).GetRelationship()
        # FUNCTIONS_FOR_INTERCAE.NameProperties.GetRelationship(nodelabelS, NameStrt, nodelabelE, graph):
        # --> see FUNCTIONS_FOR_INTERFACE.py
        # tk.Listbox.get() returns the current value selected
        # str() converts a variable into a string variable

        self.optm1t0["values"] = self.newmenu
        # resets tk.Listbox attribute "values" with the new menu (string tuple of the name properties of Nodes)

        self.optm3t0.set("Bitte Wählen")
        # sets the displayed string in the tk.Listbox to "Bitte Wählen"

        self.optm1t0.set("Bitte Wählen")

    def optm1t0_command(self, event):
        """ This function is a eventhandler for the optm1t0 Combobox command - aka Auswahl Subdomäne Ursachenseite
            it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm2t0 and optm3t0)
            the function updates the optm3t0 the final instance of the effect variable and resets optm20
            to "Bitte Wählen"

            aswell it makes an case distinction whether parameters must be queried
        """
        print(str(self.optm0t0.get()))
        self.newmenu = NameProperties("Teildomäne", str(self.optm1t0.get()),
                                      str(self.optm2t0.get()), self.graph).GetRelationship()
        self.optm3t0["values"] = self.newmenu
        self.optm3t0.set("Bitte Wählen")
        self.optm2t0.set("Bitte Wählen")

    def optm2t0_command(self, event):

        """ This function is a eventhandler for the optm2t0 Combobox command - aka Auswahl Variable oder
            Parameter Wirkungseite. it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm3t0)
            the function updates the optm3t0 the final instance of the effect variable and resets it to "Bitte Wählen"
            aswell it makes an case distinction whether parameters must be queried
                """
        self.newmenu = NameProperties("Teildomäne", str(self.optm1t0.get()),
                                      str(self.optm2t0.get()), self.graph).GetRelationship()
        self.optm3t0["values"] = self.newmenu
        self.optm3t0.set("Bitte Wählen")

    def optm3t0_command(self, event):
        """ This function is a eventhandler for the optm3t0 Combobox command - aka Auswahl Ursache
            it handles the update of the message label msg5t0 - it resets it after a new input (tk.Label.config)
            """
        self.msg5t0.config(text="")

    def optm5t0_command(self, event):
        """ This function is a eventhandler for the optm5t0 Combobox command - aka Auswahl Domäne Wirkungseite
            it calls GetRelationshipto get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm6t0 and optm8t0)
            the function updates the optm6t0 the domain instance of the effect variable and resets optm80
            to "Bitte Wählen"

            aswell it makes an case distinction whether parameters must be queried
        """
        print(str(self.optm5t0.get()))
        self.newmenu = NameProperties("Domäne", str(self.optm5t0.get()), None, self.graph).GetRelationship()
        self.optm6t0["values"] = self.newmenu
        self.optm8t0.set("Bitte Wählen")
        self.optm6t0.set("Bitte Wählen")

    def optm6t0_command(self, event):
        """ This function is a eventhandler for the optm6t0 Combobox command - aka Auswahl Subdomäne Wirkungseite
            it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm7t0 and optm8t0)
            the function updates the optm8t0 the final instance of the effect variable and resets optm70
            to "Bitte Wählen"

            aswell it makes an case distinction whether parameters must be queried
        """

        #  case differentiation
        if str(self.optm6t0.get()) == "Bitte Wählen":
            self.adparameter = tuple(NameProperties("Parameter", None, None, self.graph).GetRelationship())
        else:
            self.adparameter = tuple()

        # basic query to get the "narrowed" options
        self.newmenu = NameProperties("Teildomäne", str(self.optm6t0.get()),
                                      str(self.optm7t0.get()), self.graph).GetRelationship()

        # update of the downstream comboboxes and reset
        self.optm8t0["values"] = (sorted(self.newmenu + self.adparameter + "beliebig"))
        self.optm8t0.set("Bitte Wählen")
        self.optm7t0.set("Bitte Wählen")

    def optm7t0_command(self, event):

        """ This function is a eventhandler for the optm7t0 Combobox command - aka Auswahl Variable
            oder Parameter Wirkungseite. it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm8t0)
            the function updates the optm8t0 the final instance of the effect variable and resets it to "Bitte Wählen"
            aswell it makes an case distinction whether parameters must be queried
                """


        self.newmenu = NameProperties("Teildomäne", str(self.optm6t0.get()),
                                      str(self.optm7t0.get()), self.graph).GetRelationship() + \
                       NameProperties("Parameter", None, str(self.optm7t0.get()), self.graph).GetRelationship()

        self.optm8t0["values"] = (sorted(self.newmenu + ("beliebig",)))
        self.optm8t0.set("Bitte Wählen")


    def optm8t0_command(self, event):
        """ This function is a eventhandler for the optm8t0 Combobox command - aka Auswahl Wirkungsgöße
            it handles the update of the message label msg5t0 - it resets it after a new input (tk.Label.config)
            """
        self.msg5t0.config(text="")


    def btn9t0_command(self):
        """ This function is a eventhandler for the btn9t0 button command, aka Start der Abfrage
            it collects the elected variables, checks for invalid inputs (and prints an corresponding message)

            :return: updated and Drawn Graph in GUI + updated Listbox
            """
        # reassign for a smaller sentence

        self.a = str(self.optm3t0.get())
        self.b = str(self.optm8t0.get())
        self.c = self.chb1t0Var.get()
        self.d = self.entr1t0.get()
        self.e = self.chb0t0Var.get()
        self.f = self.entr2t0.get() # max length of node weight sum
        self.h = str(self.optm7t0.get())
        

        print("\n\n=========================================================================")
        print("=============================QUERY STARTED===============================")
        print("=========================================================================\n\n")
        # check for invalid selections

        if self.a == "Bitte Wählen" or self.b == "Bitte Wählen" or self.a == "None" or self.b == "None" or int(self.d) >=15 :
            # print error message in listbox
            self.msg5t0.config(text="Ungültige Abfrage - Bitte anpassen!")
            # reset of hte result Listbox entry (the first ("0") entry to the last ("END") entry is deleted
            self.msg4t0.delete("0", "end")
            #the Data whicht will be displayed in the Query is resetted to an empty löist ("short:  []")
            self.originalNamesQueryPaths = []
            self.modifiedNamesQuerypaths = []

            print("\n\n=========================================================================")
            print("=============================QUERY INVALID===============================")
            print("=========================================================================\n\n")

        else:
            if self.b == "beliebig" and int(self.d) >=6:
                self.msg5t0.config(text="Bitte kürzere Pfadlänge bei beliebigen Ziel")

                return
            elif self.b == "beliebig":
                self.b = ""
            try:
                # print query notification
                self.msg5t0.config(text="Abfrage läuft - bitte warten")

                #start thread to seperate run the query
                threading.Thread(target=self.querythread).start()

            except TypeError: # TypeError
                self.msg5t0.config(text="Keine Ergebnisse mit <= %s Knoten" %self.entr1t0.get())
                # the matplitlib axis windiow gets reseted
                self.ax.clear()
                # the axis border gets set to invisible
                self.ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
                # the blank window is displayed (nothing displayed)
                self.FCtk1t0.draw()
                #his functions updates the LISTBOX msg4t0 by deleting old content and insertion of new content
                self.changemsg4t0([" keine Ergebnisse", ])


    def querythread(self):

        # what is happening in the following -well let me explain
        # (but also check the functions itself by STRG+click on it)
        # self.chb2t0Var
        # cause and impact gets transferred to ExeQuery and the Query is executed
        self.DataTable = ExeQuery.execute(self, cause=self.a, impact=self.b, graph=self.graph, length=self.d,
                                          quw=self.e, mweight=self.f, addinf=self.h)

        # all properties of the Effekts are collected and written to the dictonary attrDict to be used later
        self.attrDict = ExeQuery.ExtractfromTable(self, datatable=self.DataTable)

        # the node name properties of the Query results are extracted to be used
        self.NamesQueryPaths = ExeQuery.QueryPathNames(self, datatable=self.DataTable)

        # (a filtered group and an unfilterd group is recieved)
        self.originalNamesQueryPaths = list(self.NamesQueryPaths[0])
        # looks like [('Kraft', 'Hebelgesetz4', 'Abstand', 'Hebelgesetz2', 'Abstand'), ('Kraft'
        if self.NamesQueryPaths[0] == []:
            self.msg5t0.config(text="Kein Ergebnis")
            self.msg4t0.delete(0, "end")


        else:
            self.modifiedNamesQuerypaths = list(FilterQ.FilterLoops(self, paths=self.NamesQueryPaths[1]))
            self.modifiedNamesQuerypaths2 = list(FilterQ.FilterLoops(self, paths=self.modifiedNamesQuerypaths))
            # self.modifiedNamesQuerypaths = list(FilterQ.FilterSimilarPaths(self, paths=self.NamesQueryPaths[1]))
            # self.modifiedNamesQuerypaths = list(FilterQ.FilterLoops(self, paths=self.NamesQueryPaths[1]))
            # looks like[('Kraft', 'Hebelgesetz4', 'Abstand'), ('Kraft'

            # the paths are cleaned to be printed as a string
            self.cosmeticoriginal = Cosmetic(self.originalNamesQueryPaths).Paths()
            self.cosmeticmodified = Cosmetic(self.modifiedNamesQuerypaths).Paths()
            self.cosmeticmodified2 = Cosmetic(self.modifiedNamesQuerypaths2).Paths()



            # selection which esult is to be shown is made by the CHECKBOX filtered and unfilterd
            if bool(self.c) is True:
                # Filter is on

                # the cahngemasg4t0 function takes the seleced list of nodes and disaplyed it
                self.changemsg4t0(self.cosmeticmodified)

                #old graph will be reseted
                self.ax.clear()

                # the variable mod lsit is set to the modified graphs
                self.Gmodnlist = Draw_every_path_in_one_Graph(self.modifiedNamesQuerypaths, self.graph)

                # Gmod is a variable is a list of two lists and the first list si set to the colormap
                self.colorlistmod=copy.deepcopy(self.Gmodnlist[1])

                self.G = self.Gmodnlist[0]
                nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color=self.colorlistmod, font_size=7)
                self.FCtk1t0.draw()
                self.msg5t0.config(text="Es werden " + str(self.msg4t0.size() - 1) + " Ergebnisse angezeigt")

            else:
                # Filter is off
                # samesies but with opposite dataset
                self.changemsg4t0(self.cosmeticoriginal)
                self.ax.clear()
                print(self.DataTable)
                print("Org")
                print(self.originalNamesQueryPaths)
                self.Gorg = Draw_every_path_in_one_Graph(self.originalNamesQueryPaths, self.graph)
                self.colorlist = copy.deepcopy(self.Gorg[1])
                self.G = self.Gorg[0]
                nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color=self.colorlist, font_size=7)
                self.FCtk1t0.draw()
                self.msg5t0.config(text="Es werden " + str(self.msg4t0.size() - 1) + " Ergebnisse angezeigt")

        print("\n\n=========================================================================")
        print("=============================QUERY FINISHED==============================")
        print("=========================================================================\n\n")


    def msg4t0_command1(self, event):
        """ click event in listbox aka Results
            Takes state of chb1t0Var (Filter checkbox)
            and the selected line in the msg4t0
            updates the graph

            :param:

            :returns: single path graph or full graph
        """

        print("\n\n=========================================================================")
        print("====================start of msg4t0_command (LISTBOX)====================")
        print("=========================================================================\n")

        if bool(self.chb1t0Var.get()) is True:
            # bool() True means filter please
            # use of modified paths (self.modifiedNamesQuerypaths)
            # to be drawn paths (self.paths is assignede to modifed paths
            self.paths = self.modifiedNamesQuerypaths

        else: # #nofilter
            self.paths = self.originalNamesQueryPaths

        if int(self.msg4t0.curselection()[0]) == 0:
            # curseselection returns the line which is selecetd in gui listbox (blue line)
            print("print all paths")
            # first item in Listbox is "Zeige alle an" (show all) so use of all list items 0 self.paths

            self.Gclick = Draw_every_path_in_one_Graph(self.paths, self.graph)
            self.ax.clear()
            self.colorlist = copy.deepcopy(self.Gclick[1])
            # https://stackoverflow.com/questions/184710/what-is-the-difference-between-a-deep-copy-and-a-shallow-copy
            self.G = self.Gclick[0]
            nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color=self.colorlist, font_size=7)

            self.optm3t4.set("Effekt n/a") # all effects cannot be shown in tab4 "alle"
            self.optm3t4.delete(0, "end") # remove of inputs in optm3t4

        else:
            print("print path for selection of line item No." + str(self.msg4t0.curselection()[0]))
            self.row = int(self.msg4t0.curselection()[0]) - 1
            # rownumber of cursorselection adujstment to to  all line in msg4t0
            self.Gclick = \
                Draw_every_path_in_one_Graph([self.paths[self.row], ],self.graph)
            self.ax.clear()
            self.colorlist = copy.deepcopy(self.Gclick[1])
            self.G = self.Gclick[0]
            nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color=self.colorlist, font_size=7)

            print(self.paths[int(self.msg4t0.curselection()[0]) - 1])

            # delete old and set new
            self.optm3t4.delete(0,"end")
            self.optm3t4.set("bitte wählen")
            self.optm3t4["values"]=[*self.paths[int(self.msg4t0.curselection()[0]) - 1], "alle"]

        self.FCtk1t0.draw()


    def chb1t0_command(self):
        """Checkbox Command for the click event "Filter loops"
            Either presets the Query Filter setting default is no Filter
            or changes the results to filtered/unfilterd


            :return: filtered oder unfilterd Listbox and displayed Graph
                    """

        print("\n\n=========================================================================")
        print("=================start of chb1t0_command (CHECKOX left)==================")
        print("=========================================================================\n")

        if self.modifiedNamesQuerypaths == [] or self.originalNamesQueryPaths == []:
            # modifiednamesQuery path is a list of node paths without duplicate nodes (A-B-A)
            # prior to first query no paths are available to prevent error: existence of paths is confirmed
            print("QueryPaths void")
            print("mod: " + str(len(self.modifiedNamesQuerypaths)))
            print("org: " + str(len(self.originalNamesQueryPaths)))
        else:
            print("QueryPaths exists")
            print("#mod: " + str(len(self.modifiedNamesQuerypaths)))
            print("#org: " + str(len(self.originalNamesQueryPaths)))
            if bool(self.chb1t0Var.get()):
                # filter on
                print("filtered items are shown")


                # same functions as in btn9t0_command but no new query
                self.changemsg4t0(self.cosmeticmodified)

                self.Gmod = Draw_every_path_in_one_Graph(self.modifiedNamesQuerypaths, self.graph)[0]
                self.ax.clear()
                self.G = copy.deepcopy(self.Gmod)
                nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color='orange', font_size=7)
                self.FCtk1t0.draw()
                self.msg5t0.config(text="Es werden " + str(self.msg4t0.size() - 1) + " Ergebnisse angezeigt")

            else:
                # filter off
                print("all items are shown")
                # same functions as in btn9t0_command but no new query
                self.changemsg4t0(self.cosmeticoriginal)

                self.Gorg = Draw_every_path_in_one_Graph(self.originalNamesQueryPaths, self.graph)[0]
                self.ax.clear()
                self.G = copy.deepcopy(self.Gorg)
                nx.draw(self.G, ax=self.ax, with_labels=True, font_weight='bold', node_color='orange', font_size=7)
                self.FCtk1t0.draw()
                self.msg5t0.config(text="Es werden " + str(self.msg4t0.size() - 1) + " Ergebnisse angezeigt")

    def btn4t0_command(self):

        print("\n\n=========================================================================")
        print("==========================Get Effect Details=============================")
        print("=========================================================================\n\n")

        def popupmsg(pmsg):
            """This functions opens another tk window used as popup menu to display the effect informations

            :returns: None but displays the node properties """
            # https://pythonprogramming.net/tkinter-popup-message-window/

            popup = tk.Tk()  # opens another instance of tk.window named popup
            popup.wm_title("Effektinformationen!")
            label = ttk.Label(popup, text=pmsg)  # label to display the effect informations
            label.pack(side="top", fill="x", pady=10)  # pack can be used to position the widget 'label' into the window
            b1 = ttk.Button(popup, text="Okay", command=popup.destroy)  # this buttons ends the tk window
            b1.pack()
            popup.mainloop()

        msg = ""
        try:
            # copied from the python documentation:
            # The try statement specifies exception handlers and/or cleanup code for a group of statements:
            # In this case it is used as an exception handler for an IndexError
            # The IndexError may occur when the "Effektinformation" button is pressed before a Query is started
            # IndexError occurs when a list index is out of range or not available (thus not yet existing)

            if int(self.msg4t0.curselection()[0]) == 0:
                # the tuple index 0 is used to display all effects
                if len(self.attrDict.items()) <= 5:
                    # only max 5 Effects will be displayed in order to keep the popup menu
                    # within displayable size
                    for el, val in self.attrDict.items():
                        # two counters means two simultaneous for-loops for every el index is a separate val loop
                        # probably not necessary

                        # first line for the Name property
                        msg = msg + str(el) + "\n\t\tName: \t\t\t\t" + str(val['Name']) + "\t\n"
                        # now all other property
                        msg = msg + "\t\tFormel:\t\t\t\t " + str(val['Formel']) + "\t\n"
                        msg = msg + "\t\tLiteratur:\t\t\t\t " + str(val['Literatur']) + "\t\n"
                        msg = msg + "\t\tGetroffene Vereinfachungen:\t" + str(
                            val['Getroffene_Vereinfachungen']) + "\t\n"
                        msg = msg + "\t\tAusprägung:\t\t\t" + str(val['Ausprägung']) + "\t\n"
                        msg = msg + "\t\tLink:\t\t\t\t" + str(val['Link']) + "\t\n"
                        msg = msg + "\t\tEinschränkung:\t\t\t\t" + str(val['Einschränkung']) + "\t\n"
                        msg = msg + "\t\tBeschreibung:\t\t\t" + str(val['Beschreibung']) + "\t\n"


                        msg = msg + "\n"

                else:

                    msg = "Effektliste zu lang bitte wähle einzelne Ketten aus"
                    popupmsg(msg)

            else:
                # if an element  other than the first index is selected only the effect information of the
                # element will be displayed
                # get cursor selection and then compare each element of the path  with each dictonary item
                for element in self.paths[int(self.msg4t0.curselection()[0]) - 1]:
                    for k in self.attrDict.keys():
                        # if match  extract all sub dicts
                        # if the element name is matching one k of the effect dictionary it will be displayes
                        if k == element:
                            # if matching the massage string is build by adding of the attributes
                            msg = msg + str(k) + "\n\t\tName: \t\t\t\t" + str(
                                self.attrDict[str(element)]['Name']) + "\t\n"

                            msg = msg + "\t\tFormel:\t\t\t\t" + str(self.attrDict[str(element)]['Formel']) + "\t\n"
                            msg = msg + "\t\tLiteratur:\t\t\t\t" + str(
                                self.attrDict[str(element)]['Literatur']) + "\t\n"
                            msg = msg + "\t\tGetroffene Vereinfachungen:\t" + str(
                                self.attrDict[str(element)]['Getroffene_Vereinfachungen']) + "\t\n"
                            msg = msg + "\t\tAusprägung:\t\t\t" + str(
                                self.attrDict[str(element)]['Ausprägung']) + "\t\n"
                            msg = msg + "\t\tLink: \t\t\t\t" + str(self.attrDict[str(element)]['Link']) + "\t\n"
                            msg = msg + "\t\tEinschränkung: \t\t\t" + str(
                                self.attrDict[str(element)]['Einschränkung']) + "\t\n"
                            msg = msg + "\t\tBeschreibung: \t\t\t" + str(
                                self.attrDict[str(element)]['Beschreibung']) + "\t\n"
                            msg = msg + "\n"
                popupmsg(msg)
        except IndexError:
            # the error means no query was executed before, there for the warnin message will be displayed

            msg = "  Bitte wähle erst eine Abfrage  "
            popupmsg(msg)

    def changemsg4t0(self, newnames):
        """ This functions updates the LISTBOX msg4t0
            by deleting old content and insertion of new content


            :param: list of nodelabel names in pretty depiction (node1 - node2 - node3)

            :returns: Nothing but updates msg4t0

            """

        self.msg4t0.insert(0, "Zeige alle an")
        self.msg4t0.delete(1, "end")
        for line in range(len(newnames)):
            self.msg4t0.insert(line + 1, str(newnames[line]))
        print(newnames)

    def chb0t0_command(self):
        """ Narrows the 'Wirkungsgröße' variable down to only state variables when true"""

        if self.chb0t0Var.get():  # =If self.checkbox.variable is True
            self.optm8t0["values"] = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()]
            self.optm8t0.set("Bitte Wählen")

        else:
            self.optm8t0["values"] = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                           [*NameProperties("Parameter", None, None, self.graph).GetRelationship()]
            self.optm8t0.set("Bitte Wählen")



    def optm2t4_command(self, event):

        """ This function is a eventhandler for the optm7t0 Combobox command - aka Auswahl Variable
            oder Parameter Wirkungseite. it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm8t0)
            the function updates the optm8t0 the final instance of the effect variable and resets it to "Bitte Wählen"
            aswell it makes an case distinction whether parameters must be queried
                """

        self.optm3t4.set("None")

    def optm3t4_command(self, event):

        """ This function is a eventhandler for the optm7t0 Combobox command - aka Auswahl Variable
            oder Parameter Wirkungseite. it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm8t0)
            the function updates the optm8t0 the final instance of the effect variable and resets it to "Bitte Wählen"
            aswell it makes an case distinction whether parameters must be queried
                """

        self.optm2t4.set("None")

    def optm7t4_command(self, event):

        """ This function is a eventhandler for the optm7t4 Combobox command - aka Objekt-Eigenschaft
                    it calls GetRelationship to get a fresh query of the option menu
                    parameters for the query are the set values of the downstream autocompleteComboboxes (optm1t4, optm2t4)
                    the function updates the optm8t4 the final instance of the effect variable and resets optm2t4 and optm3t4
                    to "Bitte Wählen"

                    aswell it makes an case distinction whether parameters must be queried
                """


        if str(self.optm7t4.get())==  "Name":  # optm7t4 is name or ausprägung optm2t4 auswahl objekt nach eigenschsft
            self.adoptm1 = ["Zustandsgröße", "Parameter",
                                "Effekt", "Parameter-Effekt", "alle"]
            #list for menu is set to all variable which have a name property

            self.adoptm2= [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()] + \
                                [*NameProperties("Effekt", None, None, self.graph).GetNode()] + \
                                [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            # all effects, parameter-effetks, parameter, and variables are gathered

        else: # str(self.optm7t4.get())==  "Ausprägung":

            #Same to name case but for Ausprägung
            self.adoptm1= ["Effekt", "Parameter-Effekt", "alle"]
            self.adoptm2 = list(set( [*NameProperties("Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]+ \
            [*NameProperties("Parameter-Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]))

        #overall reset of values with list and set to default
        self.optm1t4["values"] = self.adoptm1
        self.optm1t4.set("Bitte Wählen")
        self.optm2t4["values"] = self.adoptm2
        self.optm2t4.set("Bitte Wählen")

    def optm1t4_command(self, event):
        """ This function is a eventhandler for the optm1t4 Combobox command - aka Auswahl typ
            it calls GetRelationship to get a fresh query of the option menu
            parameters for the query are the set values of the downstream autocompleteComboboxes (optm2t4)
            the function updates the optm8t0 the final instance of the effect variable and resets optm2t4 and optm3t4
            to "Bitte Wählen"

            aswell it makes an case distinction whether parameters must be queried
        """

        #  case differentiation
        # basic query to get the "narrowed" options

        if str(self.optm1t4.get()) == "alle" or str(self.optm1t4.get()) == "Bitte Wählen":
            if str(self.optm7t4.get()) == "Bitte Wählen" or str(self.optm7t4.get()) == "Name": # auswahl getroffen
                self.adparameter = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()] + \
                               [*NameProperties("Parameter", None, None, self.graph).GetRelationship()] + \
                                [*NameProperties("Effekt", None, None, self.graph).GetNode()] + \
                                [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            else:
                self.adparameter = list(set([*NameProperties("Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]+ \
                     [*NameProperties("Parameter-Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]))

        elif str(self.optm1t4.get()) == "Zustandsgröße":
            self.adparameter = [*NameProperties("Teildomäne", None, None, self.graph).GetRelationship()]

        elif str(self.optm1t4.get()) == "Parameter":
            self.adparameter = [*NameProperties("Parameter", None, None, self.graph).GetRelationship()]

        elif  str(self.optm1t4.get()) == "Parameter-Effekt": # Effekt or Parameter-Effekt
            if str(self.optm7t4.get()) == "Bitte Wählen" or str(self.optm7t4.get()) == "Name":
                self.adparameter = [*NameProperties("Parameter-Effekt", None, None, self.graph).GetNode()]
            else:
                self.adparameter = [*NameProperties("Parameter-Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]

        else:
            if str(self.optm7t4.get()) == "Bitte Wählen" or str(self.optm7t4.get()) == "Name":
                self.adparameter =[*NameProperties("Effekt", None, None, self.graph).GetNode()]

            else:
                self.adparameter = [*NameProperties("Effekt", None, None, self.graph).GetOtherProperties("Ausprägung")]


                    # update of the downstream comboboxes and reset
        self.optm2t4["values"] = (sorted(self.adparameter))
        # optm2t4 object by property (as choosen in optm7t4 = Name or Property)
        self.optm2t4.set("Bitte Wählen")
        self.optm3t4.set("Bitte Wählen")

    def btn8t4_command(self):
        # as reminder optm3t4 is  element from effectchain optm2t4 is an objekt (effekt by name, or characteristic)


        if str(self.optm3t4.get()) == "alle":
            # all effects from effectchain should be displayed

            # all paths are displayed in graph
            # self.paths is an assignemt of the queried paths into a list
            # self row is the rownumber of the selected row in the QUERY tab (tab0)
            self.gs = tuple(self.paths[self.row])

        elif (str(self.optm3t4.get()) == "None" or str(self.optm3t4.get()) == "Bitte Wählen"
              or str(self.optm3t4.get()) == "Effektkette n/a" ) and \
                (str(self.optm2t4.get()) == "None" or str(self.optm2t4.get()) == "Bitte Wählen"):
            # both optionmenus are not selected: invalid command
            return

        elif str(self.optm3t4.get()) == "None" or str(self.optm3t4.get()) == "Bitte Wählen":
            # no effect chain is selected  --> use of Object property (optm2t4)
            self.gs = [str(self.optm2t4.get()),]
            # graph paths is set accordingly  aka Name is taken from optm2t4 via .get()


        elif str(self.optm2t4.get()) == "None" or str(self.optm2t4.get()) == "Bitte Wählen":
            # no effect property is selected  --> use of effectchain (optm3t4)
            self.gs = [str(self.optm3t4.get()),]
            # graph paths is set accordingly  aka Name is taken from optm3t4 via .get()

        else:
            return

        # Overall distinction between Name property

        if str(self.optm7t4.get()) == "Name":
            # effect is only pictured by

            self.checkcypher = chrosscheck_cypher_get_neighbours(self.gs, ["None"], self.graph)
            # get neighbour nodes is similar to chrosscheck results a cypher string

            self.DataTable = self.graph.run(self.checkcypher).to_table()
            #cyüher string is exectudet in neo4j, result is returned in a table as datatable

            self.query = [str(), 1] # add variable self.query as tuple needed in querypathnames with # of CYPHER QUERIES
            # due to Exequery .querypathnames normally gets a tuple of a Table and a integer
            self.CheckNames = list(ExeQuery.QueryPathNames(self, datatale=self.DataTable)[0])
            # checknames is an list of Node.Name attributes of teh connected nodes

            # self.attrDict = ExeQuery.ExtractfromTable(self, datatable=self.DataTable[0])

            self.inftext = str()  # empty string data type to be filled in the following
            self.inftext = str(self.DataTable[0][0].nodes[0]['Name']) + ": "

            if str(self.DataTable[0][0].nodes[0]['Link']) == "None": # if the node has no link its not an effect :D

                # nodes of variables or parameters only have
                self.inftext = self.inftext + "\n\n Einheit:\n " + str(self.DataTable[0][0].nodes[0]['Einheit'])
                self.linktext = "https://de.wikipedia.org/w/index.php?search=" \
                                +str(self.DataTable[0][0].nodes[0]['Name'])+ \
                                     "&title=Spezial:Suche&profile=advanced&fulltext=1&ns0=1"

                # this is a test link it will either be repalced with a node property "link" or deprecated

            else:
                self.linktext =  str(self.DataTable[0][0].nodes[0]['Link'])
                self.inftext = self.inftext + "\n\n Literatur:\n " + str(self.DataTable[0][0].nodes[0]['Literatur'])
                self.inftext = self.inftext + "\n\n Ausprägung:\n " + str(self.DataTable[0][0].nodes[0]['Ausprägung'])
                self.inftext = self.inftext + "\n\n Beschreibung:\n " + str(self.DataTable[0][0].nodes[0]['Beschreibung'])
                self.inftext = self.inftext + "\n\n Formel:\n " + str(self.DataTable[0][0].nodes[0]['Formel'])
                self.inftext = self.inftext + "\n\n Getr. Vereinfachungen:\n " + str(
                    self.DataTable[0][0].nodes[0]['Getroffene_Vereinfachungen'])
                self.inftext = self.inftext + "\n\n Einschränkung:\n " + str(self.DataTable[0][0].nodes[0]['Einschränkung'])


            print(self.inftext)
            self.ent6t4["text"] = self.inftext
            # the text in the effectinfomation tab is updated
            self.link8t4["text"] = "Link zu Effekt in Wikipedia"
            self.link8t4.newlink(self.linktext)

        elif  str(self.optm7t4.get()) == "Ausprägung" and str(self.optm3t4.get()) == "alle":
            # function for all effects

            # print order of notes in self.ent6t4["text"]
            # display characteristic in graph window
            pass

        else:
            # characteristic of nodes is searched
            self.checkcypher = "match p=(n) \n" \
                        "WHERE n.`Ausprägung`='"+ str(self.optm2t4.get())+"'\n"\
                        "return distinct p"
            print(self.checkcypher)
            # cypher string is created and sipalyed in the console

            self.DataTable = self.graph.run(self.checkcypher).to_table()
            # cypher is exceuted and resuslt is transferd into a table

            self.ent6t4["text"] = "Bitte wählen sie ein Objekt beim Namen aus um Informationen hier anzeigen zu lassen"
            # change of text in the "eigenschaftsboc"

            self.query = [str(), 1] # agian the definition of a an needed inputparameter

            self.CheckNames = list(ExeQuery.QueryPathNames(self, datatale=self.DataTable)[0])
            #get the names of the nodes matched with the "Ausprägung"

        # self.checkattr = ExeQuery.ExtractfromTable(self, datatable=self.checktable)
        # self.CheckNames = ExeQuery.QueryPathNames(self, datatale=self.checktable)
        # self.checkcosmetic = Cosmetic().Paths()


        # overall reset of axt4
        self.axt4.clear()

        # create graph from nodes list (checknames)
        self.drawn = Draw_every_path_in_one_Graph(self.CheckNames, self.graph)
        #returns graph and colorlist as tuple

        self.G4 = self.drawn[0] # only use graph not colorlist
        nx.draw(self.G4, ax=self.axt4, with_labels=True, font_weight='bold',
                node_color=self.drawn[1], font_size=7)

        self.FCtk1t4.draw()
        # draw and draw all



    def btn1t1_command(self):

        """ Yes I Know the plain Passwort is here in the code, but please do only add Effects
            if you know what you are doing"""

        self.username = ""  # "Effektschreiber"
        self.PW = ""  # "neo4j3"

        if self.username == self.entr0t1.get() and self.PW == self.entr1t1.get():
            # if password is correct show and hide tabs or retrun
            self.tabControl.add(self.tab2)
            self.tabControl.add(self.tab3)
            self.tabControl.hide(self.tab1)

        else:
            return

    def btn2t1_command(self):
        """ Hide function for hide buttons deletes also username an password """
        self.entr0t1.delete(0, "end")
        self.entr1t1.delete(0, "end")
        self.tabControl.hide(self.tab2)
        self.tabControl.hide(self.tab3)
        self.tabControl.add(self.tab1)

    def btn1t2_command(self):
        """ This function get the effects inputs (Effekteingabe) and display it as to check the given inputs



            :parameter:  self.lvar
            :parameter:  self.listpa
            :parameter:  self.listeff

            :returns: self.FCtk1t2.draw() -  drawn graph


        """

        print("\n\n=========================================================================")
        print("==============================CHECK INPUTS===============================")
        print("=========================================================================\n\n")

        # "Check inputs"
        # wtih the get function the current state of the imputs is received and written into a tuple
        self.listpar = [self.entr4t2.get(), self.entr3t2.get(), self.entr2t2.get(), self.entr1t2.get(),
                        self.entr23t2.get()]
        self.lvar = [self.entr8t2.get(), self.entr7t2.get(), self.entr6t2.get(), self.entr5t2.get()]
        self.listeff = [self.entr0t2.get(),self.entr20t2.get('1.0', tk.END), self.entr9t2.get(),
                        self.entr12t2.get(), self.entr13t2.get(), self.entr14t2.get(), self.entr21t2.get(),
                        self.chb0t2Var.get(), self.entr22t2.get()]
        # 0efffetkbezeichung, 1beschreibung, 2literatur, 3formel,  4vereinfachungen, 5ausprägung, 6link. 7effektlabel
        self.listexample = [self.entr15t2.get(), self.entr16t2.get(), self.entr17t2.get()]
        # => listeff=[Effektname, Literatur, Einheit, Formel]
        print(self.lvar)
        print(self.listeff[7])

        # if no statevariable is set / its considered any invalaid sentence
        if (self.lvar[0] == "None" and self.lvar[1] == "None" and self.lvar[2] == "None" \
                and self.lvar[3] == "None" and self.chb0t2Var.get() != "Parameter-Effekt") \
                or self.listeff[0] == "None" or self.listeff[0] == "" :
            print("case 1")
            print(self.lvar[0], self.lvar[1], self.lvar[2] ,self.lvar[3], self.chb0t2Var.get() ,self.listeff[0],self.listeff[0])
            self.ax1t2.clear()
            # therefore a text is diplayed in the graph window
            self.ax1t2.text(0.2, 0.6, r'-Bitte Eingabe überprüfen-', fontsize=10)

            # removal of the boarder for the text (just for cosmetic)
            self.ax1t2.spines[['top', 'right', 'bottom', 'left']].set_visible(False)

            # draw displays the text
            self.FCtk1t2.draw()

        elif (self.listpar[0] == "None" and self.listpar[1] == "None" and self.listpar[2] == "None" \
                and self.listpar[3] == "None" and self.chb0t2Var.get() != "Effekt" ) \
                or self.listeff[0] == "None" or self.listeff[0] == "":
            print("case 2")
            self.ax1t2.clear()
            self.ax1t2.text(0.2, 0.6, r'-Bitte Eingabe überprüfen-', fontsize=10)
            self.ax1t2.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
            self.FCtk1t2.draw()

        # otherwise the statement is valid and the graph is drawn
        else:
            print("case 3")

            # Node("Effekt", Name=listofeff[0], Literatur=listofeff[1],
            #      Einheit=listofeff[2], SI_Einheit=listofeff[3], Formel=listofeff[4],
            #      Getroffene_Vereinfachungen=listofeff[5], Ausprägung=listofeff[6], Beschreibung=listofeff[7])
            msg = [str(self.listeff[7]), "",]
            msg.append("Name:\t" + str(self.listeff[0]))
            msg.append("Formel:                               " + str(self.listeff[3]))
            msg.append("Literatur:                             " + str(self.listeff[2]))
            msg.append("Getroffene Vereinfachungen: " + str(self.listeff[4]))
            msg.append("Ausprägung:                       "+ str(self.listeff[5]))
            msg.append("Link:                                  " + str(self.listeff[6]))
            msg.append("Beschreibung:                    " + str(self.listeff[1]))
            print(msg)
            self.msg3t2.delete(0, "end")
            for line in range(len(msg)):
                self.msg3t2.insert(line + 1, str(msg[line]))


            # clear potential exisitng graphs and other images displayed
            self.G2.clear()
            self.ax1t2.clear()

            # call def Draw_every_var_for_effect with the inputs and refernce the instance to 'temp' variable
            temp = Draw_every_var_for_effect(self.lvar, self.listpar, self.listeff, self.listexample)
            self.G2 = temp[0]

            # reference the other returns properly
            self.colourdict = temp[2]
            self.labeldict = temp[1]

            # call nx.draw to create the graph
            # draw_shell align the node in a shell pattern
            nx.draw_shell(self.G2, ax=self.ax1t2, labels=self.labeldict, with_labels=True, font_weight='bold',
                          node_color=self.colourdict,
                          font_size=7)

            #  call the FCtk1t2 instance og FigureCanvasTkAgg().draw() to display the graph in the GUI
            self.FCtk1t2.draw()

    def btn2t2_command(self):
        """ This function get the effects inputs (Effekteingabe) perform a chross check of similar variable
            chrosscheck the given inputs



                   :parameter:  self.lvar
                   :parameter:  self.listpa
                   :parameter:  self.listeff

                   :returns: self.FCtk1t2.draw() -  drawn graph


               """
        self.listpar = [self.entr4t2.get(), self.entr3t2.get(), self.entr2t2.get(), self.entr1t2.get(),
                        self.entr23t2.get()]
        # get all inputs and combine the  to a list
        self.lvar = [self.entr8t2.get(), self.entr7t2.get(), self.entr6t2.get(), self.entr5t2.get()]
        # get all inputs and combine the  to a list
        self.listeff = [self.entr0t2.get(), self.entr20t2.get('1.0', tk.END), self.entr9t2.get(),
                        self.entr12t2.get(), self.entr13t2.get(), self.entr14t2.get(), self.entr21t2.get(),
                        self.chb0t2Var.get(), self.entr22t2.get()]
        # get all inputs information and combine the  to a list with a fiyed postion

        # => listeff=[Effektname, Literatur, Einheit, Formel]

        if self.lvar[0] == "None" and self.lvar[1] == "None" and self.lvar[2] == "None" \
                and self.lvar[3] == "None" and self.chb0t2Var.get() == "Effekt":
            # check if a effect without any parameters, variables or input is present

            #reset of graph display
            self.ax2t2.clear()
            # display error message insted
            self.ax2t2.text(0.2, 0.6, r'-Bitte Eingabe überprüfen-', fontsize=10)
            self.ax2t2.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
            self.FCtk2t2.draw()
        elif self.listpar[0] == "None" and self.listpar[1] == "None" and self.listpar[2] == "None" \
                and self.listpar[3] == "None" and self.chb0t2Var.get() == "Parameter-Effekt":
            # check if a parametereffect without any parameters, variables or input is present
            self.ax2t2.clear()
            self.ax2t2.text(0.2, 0.6, r'-Bitte Eingabe überprüfen-', fontsize=10)
            self.ax2t2.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
            self.FCtk2t2.draw()
        else:
            self.query2 = chrosscheck_cypher(self.lvar, self.listpar, self.graph)
            # perform chrosscheck of neighboured nodes
            self.data_table2 = self.graph.run(self.query2).to_table()
            #chrosscheck is written into a table

            self.chrosschecknames = name_reader(self.data_table2)
            # node names are extracted

            # graph 3 (chrosscheck) ist reset
            self.G3.clear()
            self.ax2t2.clear()


            if not self.chrosschecknames:
                # chrosshecknames is empty = no match
                self.ax2t2.text(0.35, 0.6, r'-Keine Ergebnisse-', fontsize=10)
                self.ax2t2.spines[['top', 'bottom', 'right', 'left']].set_visible(False)
                self.FCtk2t2.draw()

            else:
                # chross cehck found effect bewteen to nodes
                self.G3 = Draw_every_path_in_one_Graph(self.chrosschecknames, self.graph)[0]
                nx.draw(self.G3, ax=self.ax2t2, with_labels=True, font_weight='bold', node_color='orange',
                        font_size=7)
                self.FCtk2t2.draw()

    def clearALLrels(self):
        # this is dead code, former planned for function to delete all relationships connecting a node
        pass

    def showeffect(self):
        """
        this function is used to get graph inputs associated to a node, to enable more relationships or changes of
         the properties
        :return: node-properties
        """
        try: # try if any error occours there is propably no node with the Name in entr0t2
            self.effdict= NameProperties(None, self.entr0t2.get(), None, self.graph).GetInfo()
            # extract of dict {"ID": self.ID, "Lb": self.Lb, "Name": self.Name, "L": self.L, "F": self.F, "B": self.B ,
            #"A": self.A, "Lit":self.Lit, "V": self.V}

            print(self.effdict)
            # set the optmmenu to  the values of the effectdict
            # self.entr20t2.delete(int(0), tk.END)
            self.entr9t2.set(self.effdict["Lit"])
            self.entr12t2.set(self.effdict["F"])
            self.entr13t2.set(self.effdict["V"])
            self.entr14t2.set(self.effdict["A"])
            self.entr21t2.delete(int(0), tk.END)
            self.entr20t2.delete(int(0), tk.END)
            self.entr20t2.insert(tk.END,self.effdict["B"])
            self.entr21t2.insert(tk.END,self.effdict["L"])
            self.entr22t2.set(self.effdict["E"])

        except (IndexError, TypeError): # effekt not found, or nothing to show
            return

        print("\n\n=========================================================================")
        print("==============================Inputs Reset=============================")
        print("=========================================================================\n\n")

        self.effdict = () #reset of effektdict as list



    def btn3t2_command(self):
        """ This function adds a new effect to neo4j dbms after check inputs is completed"""
        # print(self.lvar)
        # print(self.listpar)
        # print(self.listeff)

        if self.listeff is None or self.listeff[0] == "":
            print("error with inputs")

        elif self.lvar is None or self.listpar is None or self.listeff is None:
            print("error with inputs")

        elif self.listpar is None and self.chb0t2Var.get() == "Parameter-Effekt":
            print("error with inputs")

        elif self.lvar is None and  self.chb0t2Var.get() == "Effekt":
            print("error with inputs")


        else:

            threading.Thread(target=match_n_add(self.lvar, self.listpar, self.listeff,
                                                self.graph, self.listexample)).start()
            #the match_n_add is done in an thread to avoid influence of the normal behavior of the gui (e.g. wait issue)
            print("\n\n=========================================================================")
            print("==============================EFFECT ADD TO DBMS===============================")
            print("=========================================================================\n\n")
        self.msg1t2['text'] = "Effekt ergänzt!"

    def removelabel(self, event):

        self.msg1t2['text'] = ""

    def btn1t3_command(self):
        """ This command adds a parameter to the graph database  """

        threading.Thread(target=add_parameter(self.entr1t3.get(), self.entr2t3.get(), self.entr3t3.get(),
                      self.entr4t3.get(),  self.graph)).start()


        # reset the parameter input
        self.entr1t3.set("None")
        self.entr2t3.set("None")
        self.entr3t3.set("None")
        self.entr4t3.set("None")

        # update the paramter comboxvalues
        self.entr1t2["values"] = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
        self.entr2t2["values"] = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
        self.entr3t2["values"] = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
        self.entr4t2["values"] = ('None',) + (NameProperties("Parameter", None, None, self.graph).GetRelationship())
        self.entr8t2["values"] = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())

    def clearT2(self):

        self.entr4t2.set("None")
        self.entr3t2.set("None")
        self.entr2t2.set("None")
        self.entr1t2.set("None")
        self.entr8t2.set("None")
        self.entr7t2.set("None")
        self.entr6t2.set("None")
        self.entr5t2.set("None")
        self.entr22t2.set("")
        self.entr23t2.set("None")
        self.entr0t2.set("")
        self.entr20t2.delete(0.0, tk.END)
        self.entr9t2.set("")
        self.entr12t2.set("")
        self.entr13t2.set("")
        self.entr14t2.set("")
        self.entr21t2.delete(0, tk.END)
        self.msg3t2.delete(0, "end")

        # self.ax2t2= plt.figure().add_subplot(1, 1, 1)
        # self.ax1t2= self.fig1t2.add_subplot(1, 1, 1)

        self.entr0t2['values'] = tuple(list(NameProperties('Effekt', None, None, self.graph).GetNode()) +
                                   list(NameProperties('Parameter-Effekt', None, None, self.graph).GetNode()))

        self.entr9t2['values'] = list(['None', ] + NameProperties('Effekt', None,
                                                            None, self.graph).GetOtherProperties("Literatur"))
        self.entr12t2['values'] = list(['None', ] + NameProperties('Effekt', None,
                                                             None, self.graph).GetOtherProperties("Formel"))
        self.entr13t2['values'] = list(['None', ] + NameProperties('Effekt', None, None, self.graph
                                                             ).GetOtherProperties("Getroffene_Vereinfachungen"))
        self.entr14t2['values'] = list(['None', ] + NameProperties('Effekt', None, None, self.graph
                                                             ).GetOtherProperties("Ausprägung"))
        self.entr8t2['values'] = ('None',) + (NameProperties("Teildomäne", None, None, self.graph).GetRelationship())

        print("\n\n=========================================================================")
        print("==============================Inputs Reset=============================")
        print("=========================================================================\n\n")


    def entr5t3_command(self, event):



        self.changequery = "match p=(n {Name:'" +str(self.entr5t3.get())+ "'})\
                            -[r:URSACHE_WIRKUNG|HAT_PARAMETER|ABLEITUNG]-(e) return distinct e"
        print(self.changequery)
        self.data_table = self.graph.run(self.changequery).to_table()

        self.attr = tuple(sorted(set([nodes[0].end_node['Name'] for nodes in self.data_table])))
        # removes duplicates (set) sort alphabetically and capitalize the first letter --> then return as tuple
        if self.attr == []:
            self.attr = ["NaN - please change search!"]

        else:
            pass

        self.entr7t3["values"] =self.attr

    def btn4t3_command(self):

        """button command for the set weight for a distinct relationship"""

        self.entr5t3.get() # node name
        self.entr6t3.get() # node name
        self.entr7t3.get() # relationship weight

        self.changequery = "match p=(n {Name:'"+str(self.entr5t3.get())+"'})-[r]-(e" \
                                                                         "{Name:"+str(self.entr7t3.get())+"})" \
                            "set r.weight = "+str(self.entr6t3.get())
        print(self.changequery)
        self.graph.run(self.changequery)
        # cypherstatement as string is exceuted

    def btn5t3_command(self):
        """button command for the set weight for a distinct node"""
        self.entr12t3.get()
        self.entr11t3.get()

        self.changequery = "match p=(n {Name:'" + str(self.entr11t3.get()) + "'})" \
                                                                          "set n.weight = " + str(self.entr12t3.get())
        print(self.changequery)
        self.graph.run(self.changequery)
        # cypherstatement as string is exceuted

    def btn6t3_command(self):
        """button command for the set weight for a  node by label"""
        self.entr13t3.get()
        self.entr14t3.get()

        self.changequery = "match p=(n: `"+str(self.entr13t3.get())+"`)" \
                            "\nset n.weight = " + str(self.entr14t3.get())
        print(self.changequery)
        self.graph.run(self.changequery)

    def btn7t3_command(self):
        """button command for the set weight for a  relationship by label"""
        self.entr15t3.get()
        self.entr16t3.get()


        self.changequery = "match ()-[r:`"+str(self.entr16t3.get())+"`]-()" \
                            "\nset r.weight = " + str(self.entr15t3.get())
        print(self.changequery)
        self.graph.run(self.changequery)



if __name__ == "__main__":
    # __name__ is the name of the python file
    # __main__ is the main program which is running the file
    #  so __name__ == "__main__" checks weather the program is a main program and if so
    #  it starts execute itself with teh following commands

    app = GUIApp()
