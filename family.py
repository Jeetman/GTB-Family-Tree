import csv
from graphviz import Digraph

# Create a Digraph object and add nodes and edges
dot = Digraph(name='root', engine='dot')

# Create Dictionary to store relationship data for each member
relationships = {}

# Create Subgraphs for each class (ex. Newbie class of 2022)
year_subgraphs = {}

# Read the CSV file and populate relationships
with open('family.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        #extract column values of each row

        #collect member name
        name = row['Name'].strip()

        #collect list of littles 
        littles = row['Little(s)'].split(',')

        #determine year joined
        year_joined = row['Year you joined']

        #we will create a unqiue subgraph for each class (year joined)
        #and store these in the year_subgraphs dictionary
        if year_joined not in year_subgraphs:
                #create the subgraph (will be added as subgraph later)
                class_subgraph = Digraph(name=str(year_joined))
                
                #the main purpose is so all members of the same class have the same rank!
                class_subgraph.attr(rank='same')
                
                #add a node to act as a label for each class subgraph
                class_subgraph.node(year_joined, shape='ellipse',style="filled", fillcolor="gold")

                #save the subclass
                year_subgraphs[year_joined] = class_subgraph

        #grab the subgraph for this member
        class_subgraph = year_subgraphs[year_joined]
        
        #check if member is captain
        if row['Captain'].strip() == "Yes":
            #add a node for captain to subgraph
            class_subgraph.node(name, shape='doubleoctagon',style="filled", fillcolor="gold")
        else:
            #add a node for general member to subgraph
            class_subgraph.node(name,shape='hexagon')

        #populate dictionary
        relationships[name] = {'littles': littles, 'year_joined': year_joined}


#get a list of all classes sorted
unique_years = sorted(set(relationship['year_joined'] for relationship in relationships.values()))


# Add edges from lowest to highest year
for i in range(len(unique_years) - 1):
    dot.edge(unique_years[i], unique_years[i+1], color='blue')

# Modify attributes of root graph 
# Refer to https://www.graphviz.org/doc/info/attrs.html
dot.attr(labelloc='t')
dot.attr(label='GTB Lineage',fontsize='25')
dot.attr(bgcolor="white")
dot.attr(center="true")


# Add edges between bigs and littles
for name, relationship in relationships.items():
    littles = relationship['littles']
    for little in littles:
        if not little.isspace() and little != "":
            dot.edge(name, little.strip(), color='blue')


# Add the year subgraphs to the main graph
for year, year_subgraph in year_subgraphs.items():
    #this subgraph contains a node used to display the class 
    dot.subgraph(year_subgraph)

# Render the graph and save it as an image
dot.render('bigs_littles_tree', view=True, format='png')
