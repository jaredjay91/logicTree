#import json
import csv
# Build an interface where the user can input new statements and save them to the tree.

# This is basically a dictionary where the key is the statement id and the value is the statement.
class LogicTree():
  
  def __init__(self, definitions, premises):
    self.statements = {}
    for definition in definitions:
      self.statements["D:" + definition.term] = definition.characteristics
      print(definition.term + ":", definition.characteristics)
    index = 0
    for premise in premises:
      premise.id_number = index
      self.statements["P:"+ str(index)] = premise.info
      print(premise.info)
      index += 1

  def append(self, statement):
    new_id_number = max(self.get_id_numbers)+1
    self.statements[new_id_number] = statement
    for parent_id in statement.parents:
      statements[parent_id].children.append(statement.id_number)

  def get_id_numbers(self):
    id_numbers = self.statements.keys

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

  def print_argument(self, statement_id):
    pass

  def get_definitions(self):
    pass

  def grow(self):
    pass


class Statement():
  
  def __init__(self, statement_string, id_number=0, parents=[], children=[]):
    self.info = {"statement_string":statement_string, "id_number":id_number, "parents":parents, "children":children}


class Definition():

  def __init__(self, term, list_of_defining_characteristics):
    self.term = term
    self.characteristics = list_of_defining_characteristics

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

