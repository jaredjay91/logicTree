#import json
import csv
import schemdraw
from schemdraw import flow
import textwrap
# Build an interface where the user can input new statements and save them to the tree.

# This is basically a dictionary where the key is the statement id and the value is the statement.
class LogicTree():
  
  def __init__(self, definitions, premises, statements = []):
    self.statements = {}
    def_index = 1
    for definition in definitions:
      definition.id_number = "D" + str(def_index)
      self.statements[definition.id_number] = definition
      def_index += 1
    prem_index = 1
    for premise in premises:
      premise.id_number = "P"+ str(prem_index)
      self.statements[premise.id_number] = premise
      prem_index += 1
    if len(statements) > 0:
      stat_index = 1
      for statement in statements:
        statement.id_number = "S"+ str(stat_index)
        self.statements[statement.id_number] = statement
        stat_index += 1

  def append(self, statement, kind="S"):
    id_numbers = [int(a) for a in self.get_id_numbers(kind=kind)]
    new_id_number = kind + "1"
    if len(id_numbers) > 0:
        new_id_number = kind + str(max(id_numbers)+1)
    statement.id_number = new_id_number
    statement.truth_value = 1
    if len(statement.parents) < 1:
      statement.truth_value = 0.5
    else:
      for parent_id in statement.parents:
        statement.truth_value = statement.truth_value * self.statements[parent_id].truth_value
        parent_statement = self.statements[parent_id]
        parent_statement.children = parent_statement.children + [new_id_number]
    for child_id in statement.children:
      child_statement = self.statements[child_id]
      child_statement.parents = child_statement.parents + [new_id_number]
    self.statements[new_id_number] = statement


  def get_id_numbers(self, kind="S"):
    statement_keys = self.statements.keys()
    id_numbers = [name[1:] if (name[0] == kind) else 0 for name in statement_keys]
    filtered = list(filter(lambda id_number: int(id_number) > 0, id_numbers))
    return(filtered)

  def syllogism(self, statementP, statementQ):
    pass

  def save(self, filename):
    #data = json.dumps(self.statements)
    #f = open(filename,"w")
    #f.write(data)
    #f.close()
    with open(filename, 'w') as f:
      for key in self.statements.keys():
        f.write("%s,%s\n"%(key,self.statements[key]))

  def print(self, verbose=False):
    list_of_keys = sorted(self.statements.keys())
    for key in list_of_keys:
      self.statements[key].print(verbose=verbose)
    
  def print_argument(self, statement_id):
    pass

  def get_definitions(self):
    pass

  def grow(self):
    pass
    
  def getNumberOfGenerationsDown(self, statement):
    list_of_children = self.statements[statement].children
    if (len(list_of_children) < 1):
        return(1)
    else:
        max_generations = 0
        for child in list_of_children:
            generations = self.getNumberOfGenerationsDown(child) + 1
            if generations > max_generations:
                max_generations = generations
    return(max_generations)

  def getNumberOfGenerationsUp(self, statement):
    list_of_parents = self.statements[statement].parents
    if (len(list_of_parents) < 1):
        return(1)
    else:
        max_generations = 0
        for parent in list_of_parents:
            generations = self.getNumberOfGenerationsUp(parent) + 1
            if generations > max_generations:
                max_generations = generations
    return(max_generations)
  
  def get_generation(self, gen_val):
    statements_in_gen = []
    for s, val in self.statements.items():
        if val.generation == gen_val:
            statements_in_gen.append(s)
    return(statements_in_gen)
    
  def getMaxNumberOfGenerations(self):
    max_generations = 0
    for s, val in self.statements.items():
        # start on a statement with no parents and get the generations in the longest line.
        list_of_parents = val.parents
        if len(list_of_parents) < 1:
            generations = self.getNumberOfGenerationsDown(s)
            if (generations > max_generations):
                max_generations = generations
    return(max_generations)
    
  def draw_tree(self, detailed = False):
    #calculate # of generations in tree
    generations = self.getMaxNumberOfGenerations()
    unitSize = 4
    
    # label the generation and coordinates of each statement
    gen_counts = {}
    for i in range(generations):
        gen_counts[i] = 0
    for s, val in self.statements.items():
        gen_val = generations - self.getNumberOfGenerationsDown(s)
        val.generation = gen_val
        val.coords = (gen_counts[gen_val]*unitSize, -gen_val*unitSize)
        gen_counts[gen_val] += 1
        
    # order each generation by the amount of ancestry each statement has
    for i in range(generations):
        gen_statements = self.get_generation(i)
        ancestry_scores = []
        gen_coords = []
        for s in gen_statements:
            ancestry_scores.append([s, self.getNumberOfGenerationsUp(s)])
            gen_coords.append(self.statements[s].coords)
        ancestry_scores = sorted(ancestry_scores, key = lambda x: x[1], reverse = True)
        for i in range(len(ancestry_scores)):
            s = ancestry_scores[i][0]
            self.statements[s].coords = gen_coords[i]
        
    # center generations
    max_gen_count = max(gen_counts)
    for s, val in self.statements.items():
        gen_val = val.generation
        val.coords = (val.coords[0] + 0.5*unitSize*(max_gen_count - gen_counts[gen_val]), val.coords[1])
    
    # draw the tree
    elements = []
    with schemdraw.Drawing() as dwg:
        dwg_index = 0
        for s, val in self.statements.items():
            color = 'lightblue'
            if (len(val.parents) < 1):
                color = 'lightgreen'
            if not detailed:
                elements.append(flow.Process().at(val.coords).label(s + "(" + str(round(val.truth_value,2)) + ")", fontsize=16).fill(color))
            else:
                label = "\n".join(textwrap.wrap(s + ": " + val.statement_string + " (" + str(round(val.truth_value,2)) + ")", width=20))
                #9 lines with fontsize 10 fit a 3x3 square
                fontsize = 10
                num_lines = label.count("\n") + 1
                if num_lines > 5:
                    fontsize = 70/num_lines
                elements.append(flow.Process(w=3, h=2.5).at(val.coords).label(label, fontsize=fontsize).fill(color))
            dwg += elements[dwg_index]
            val.dwg_index = dwg_index
            dwg_index += 1
        for s, val in self.statements.items():
            s_elt = elements[val.dwg_index]
            for child in val.children:
                child_elt = elements[self.statements[child].dwg_index]
                #dwg += flow.Arc2(k=.1, arrow='->').at(s_elt.S).to(child_elt.N).label('', fontsize=10)
                dwg += flow.Arrow(k=.1, arrow='->').at(s_elt.S).to(child_elt.N).label('', fontsize=10)



class Statement():
  
  def __init__(self, statement_string, id_number=0, parents=[], children=[], generation=0, coords=(0,0)):
    self.statement_string = statement_string
    self.id_number = id_number
    self.parents = parents
    self.children = children
    self.truth_value = 0.5
    
  def print(self, verbose=False):
    if verbose:
      print(self.id_number, ": { truth_value =", self.truth_value, ", parents =", self.parents, ", children =", self.children, ", statement_string =", self.statement_string, "}")
    else:
      print(self.id_number, ": ", self.statement_string)
    


class Definition(Statement):

  def __init__(self, term, list_of_defining_characteristics, id_number=0, parents=[], children=[]):
    if isinstance(list_of_defining_characteristics, str):
        list_of_defining_characteristics = [list_of_defining_characteristics]
    statement_string = term + " = "
    if len(list_of_defining_characteristics) == 1:
        statement_string = statement_string + list_of_defining_characteristics[0]
    elif len(list_of_defining_characteristics) == 2:
        statement_string = statement_string + " and ".join(list_of_defining_characteristics)
    else:
        statement_string = statement_string + ", ".join(list_of_defining_characteristics[:-1]) + ", and " + list_of_defining_characteristics[-1]
    super().__init__(statement_string, id_number, parents, children)
    self.term = term
    self.characteristics = list_of_defining_characteristics
    self.truth_value = 1

  def check_against_def(self, list_of_object_characteristics):
    match = True
    for characteristic in self.characteristics:
      if not (characteristic in list_of_object_characteristics):
        match = False
        print("The condition " + characteristic + " is not satisfied.")
    return match
        

class Tautology():

  def __init__(self, formula):
    if not test_tautology(formula): #error!
      raise ValueError("The given formula is not a tautology!")
    self.formula = formula

