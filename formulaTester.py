from logicToMath import logicToMath
#import evaluate


def check_tautology(formula="(~(P->~P)&&~(Q->~Q))->~(P->~Q)", verbose=True, debugMode=False):

  if (formula.find("P") < 0) and (formula.find("Q") < 0):
    return False

  mathFormula = logicToMath(formula, verbose, debugMode)

  #Replace P's and Q's with 0's and 1's and evaluate the truth values.
  if verbose:
    #print(mathFormula)
    print("\nEvaluating the truth values...")
  average = 0
  for pval in [0, 1]:
    for qval in [0, 1]:
      mathFormula_eval = mathFormula.replace("P", str(pval))
      mathFormula_eval = mathFormula_eval.replace("Q", str(qval))
      #print(mathFormula_eval)
      try:
        truth_value = eval(mathFormula_eval)
      except:
        return False
      average += truth_value
      if verbose:
        print("P={}, Q={}: {}".format(pval, qval, truth_value))
  average = average/4.0
  if average == 1.0:
    return True
  else:
    return False


if __name__ == '__main__':
  is_tautology = check_tautology("(~(P->~P)&&~(Q->~Q))->~(P->~Q)", True, False)
  print(is_tautology)

  max_length = 9
  print("\nHere is a list of tautologies up to a length of",max_length)
  valid_chars = ["(", ")", "~", "P", "Q", "&&", "||", "->"]
  for length in range(1, max_length+1):
    hashcode = 10**length
    while hashcode < 2 * (10**length):
      hashstr = str(hashcode)[1:]
      if ("9" in hashstr) or ("8" in hashstr):
        hashcode += 1
        continue
      #print("hashstr =",hashstr)
      indices = [int(x) for x in hashstr]
      #print("indices =",indices)
      statement = ""
      for index in indices:
        #print("hashcode =",hashcode)
        #print("length =",length)
        #print("index =",index)
        statement = statement + valid_chars[index]
        valid = False
      try:
        valid = check_tautology(statement, False, False)
      except:
        valid = False
      if valid:
        print(statement)
      hashcode += 1

