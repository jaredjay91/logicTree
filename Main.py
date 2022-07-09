from LogicTree import *

#The goal is this:
#I write a few definitions and premises, and then the LogicTree 
#automatically generates the arguments that follow from the 
#definitions and premises, and then it prints it out.
#Definition(term, defining_attributes)

definition1 = Definition("Dog", ["is an animal", "has 4 legs"])# So any entity with attribute ("animal with 4 legs") satisfies the definition of a dog. This is equivalent to the statement P->Q where P = X has attribute (animal with 4 legs), and Q = X is a dog.
#Statement(statement_string). The program should take the statement "A cat is an animal with 4 legs" and interpret it correctly as cat has attributes (animal with 4 legs)

premise1 = Statement("A cat is an animal and has 4 legs")

definitions = [definition1]
premises = [premise1]

myTree = LogicTree(definitions, premises)

myTree.grow()# Apply tautologies to premises and definitions to obtain new statements in the tree. For example, the syllogism ((P->Q)&P)->Q where P = X has attribute (animal with 4 legs), and Q = X is a dog. It should see that the substatement (P->Q) is true by the definition, and P is the premise for a cat, so it can conclude Q for the cat. In other words, it should conclude that "A cat is a dog".
  
#The real test:
#definition1 = Definition("living thing", ["is highly organized", "has the ability to acquire materials and energy", "responds to its environment", "reproduces", "adapts"])
#definition2 = Definition("Abortion", "Willfully terminating a human fetus or embryo")
#definition3 = Definition("To kill", "To willfully cause a living thing to stop living")
#definition4 = Definition("A living human", ["is living thing", "has a complete human genome in each of its cells"])
#definition5 = Definition("Innocent", ["has not committed any crimes"])
#premise1 = 
myTree.save("treefile.csv")

#argument_dict = {"S1": {"statement_type":"definition", "parents":[], "children":["S4"]},
#                "S2": {"statement_type":"definition", "parents":[], "children":["S4"]},
#                "S3": {"statement_type":"definition", "parents":[], "children":["S5"]},
#                "S4": {"statement_type":"definition", "parents":["S1","S2"], "children":["S5","S6"]},
#                "S5": {"statement_type":"definition", "parents":["S4","S3"], "children":["S6"]},
#                "S6": {"statement_type":"definition", "parents":["S5","S4"], "children":[]},}