
  # 1 = TRUE
  # 0 = FALSE

  # P = 0 or 1.
  # P*P = P

  #    || = OR.      P || Q = ~(~P||~Q) = 1-(1-P)*(1-Q)
  #    && = AND.     P && Q = P*Q
  #    -> = IMPLIES. P -> Q = 1-P*(1-Q)
  #    ~ = NOT.      ~P = 1-P


  # P || P 	= 1-(1-P)*(1-P)
  #		= 1-(1-2P+P*P)
  #		= 1-(1-2P+P)
  #		= 1-(1-P)
  #		= P

  # P ||~P 	= 1-(1-P)*P
  #		= 1-(P-P*P)
  #		= 1-(P-P)
  #		= 1

  # P&&(P->Q) -> Q  	= 1 - [P*(1-P+P*Q)]*(1-Q)
  #			= 1 - (P*(1-P)*(1-Q) + P*P*Q*(1-Q))
  #			= 1 - (0*(1-Q) + P*P*0)
  #			= 1

def logicToMath(Formula="(~(P->~P)&&~(Q->~Q))->~(P->~Q)", verbose=True, debugMode=False):

  if "&&&&" in Formula:
    return "0"
  if "||||" in Formula:
    return "0"
  if "PP" in Formula:
    return "0"
  if "PQ" in Formula:
    return "0"
  if "QP" in Formula:
    return "0"
  if "QQ" in Formula:
    return "0"
  if "()" in Formula:
    return "0"
  if "->->" in Formula:
    return "0"
  if "~)" in Formula:
    return "0"
  if "~->" in Formula:
    return "0"
  if ")~" in Formula:
    return "0"

  if verbose or debugMode:
    print("\nInput Formula = " + Formula)
    print("\nFinding parentheses...")
  #search through formula to find locations and nest levels of parentheses.
  leftLocations = []
  rightLocations = []
  leftLevels = []
  rightLevels = []
  nestLevel = 0
  numleft = 0
  numright = 0
  for i in range(len(Formula)):
    if Formula[i:i+1] == "(":
      if debugMode:
        print("Found ( at i = {} with nestLevel = {}".format(i, nestLevel))
      leftLocations.append(i)
      leftLevels.append(nestLevel)
      nestLevel -= 1
      numleft += 1
    elif Formula[i:i+1] == ")":
      nestLevel += 1
      if debugMode:
        print("Found ) at i = {} with nestLevel = {}".format(i, nestLevel))
      rightLocations.append(i)
      rightLevels.append(nestLevel)
      numright += 1
    else:
      continue

  if debugMode:
    print("nestLevel =", nestLevel)
    print("numleft =", numleft)
    print("numright =", numright)

  #Check that there is a ")" for every "("
  if numleft-numright > 0:
    if verbose or debugMode:
      print("ERROR: Missing \")\" in formula!")
    return "0"
  elif numleft-numright < 0:
    if verbose or debugMode:
      print("ERROR: Missing \"(\" in formula!")
    return "0"

  #match left and right parentheses.
  if verbose or debugMode:
    print("Matching sets of parentheses...")
  numSubs = numleft + 1 #+1 for the original formula.
  pairs = [] #[numSubs][2]
  nummatched = 1
  for i in range(len(Formula)):
    if (i >= len(leftLocations)):
      break
    j = 0
    if debugMode:
      print("( at", leftLocations[i],"with nestLevel =", leftLevels[i])
    #pairs[nummatched][0] = leftLocations[i]
    while j < numright:
      #print("  j =", j)
      if (rightLocations[j] > leftLocations[i]) and (rightLevels[j] == leftLevels[i]):
        if debugMode:
          print("	matched to ) at", rightLocations[j], "with nestLevel =", rightLevels[j])
        pairs.append([leftLocations[i], rightLocations[j]])
        nummatched += 1
        break
      else:
        #print("	not matched to ) at", rightLocations[j], "with nestLevel =", rightLevels[j])
        j += 1
  #Check that every parenthesis has a match
  if not ( (len(pairs) == numleft) and (len(pairs) == numright)):
    if verbose or debugMode:
      print("ERROR: Parentheses don't match!")
    return "0"

  #extract the contents enclosed by the parentheses.
  if verbose or debugMode:
    print("Extracting subFormulas...")
  subFormulas = []
  subFormulaNames = []
  for i in range(numSubs):
    subFormulaNames.append("@" + str(i))
    if i == 0:
      subFormulas.append(Formula)
    else:
      #print("pairs[", i, "] = (", pairs[i][0], "," pairs[i][1], ")")
      subFormulas.append(Formula[pairs[i-1][0]:pairs[i-1][1]+1])
    if debugMode:
      print(subFormulaNames[i] + " = " + subFormulas[i])

  #Replace statements in inner parentheses with statement names
  for i in range(numSubs):
    replaceIndex = numSubs-1-i;
    replaceFormula = subFormulas[replaceIndex] #Start with the last subFormula and replace it in every other formula where it appears.
    if debugMode:
      print()
    for j in range(replaceIndex):
      if debugMode:
        print(subFormulas[j], " ---> ")
      subFormulas[j] = subFormulas[j].replace(replaceFormula, subFormulaNames[replaceIndex])
      if debugMode:
        print(subFormulas[j])

  #Print simplified formulas
  if verbose or debugMode:
    print("Behold the simplified formulas: ")
    for i in range(numSubs):
      print(subFormulaNames[i], "=", subFormulas[i])

  #Generate Math statements
  if verbose or debugMode:
    print("Translating to algebraic formulas...")
  subMathFormulas = []
  subMathFormulaNames = []
  for i in range(numSubs):
    subMathFormulaNames.append("@" + str(i))
    subMathFormulas.append(subFormulas[i])
  
  #Change the '&&' to '*'
  for i in range(numSubs):
    if debugMode:
      print(subMathFormulas[i], " --->  ")
    #Replace the substring '&&' in the formula with '*'
    subMathFormulas[i] = subMathFormulas[i].replace("&&", "*")
    if debugMode:
      print(subMathFormulas[i])

  #Change the 'P->Q' to '(1-P*(1-Q))'
  for i in range(numSubs):
    pos = 1
    while pos > 0:
      #Search in the subMathFormula for a '->'
      pos = subMathFormulas[i].find("->")#returns -1 if it doesn't find anything.
      if (pos > 0):
        if debugMode:
          print("Found \'->\' in @{} at position {}".format(i, pos))
          print(subMathFormulas[i], " --->  ")
      else:
        if debugMode:
          print("Found no \'->\' in @{}".format(i))
        break
      #Get the statement 'P' that precedes it
      strP = subMathFormulas[i][pos-1:pos]
      strAt = subMathFormulas[i][pos-2:pos-1]
      if (strAt == "@") or (strAt == "~"):
        strP = subMathFormulas[i][pos-2:pos]
      if (subMathFormulas[i][pos-2:pos-1] == "~"):
        strP = subMathFormulas[i][pos-3:pos]
      #Get the statement 'Q' that follows
      strQ = subMathFormulas[i][pos+2:pos+3]
      if (strQ == "~"):
        strQ = subMathFormulas[i][pos+2:pos+4]
      elif (strQ == "@"):
        strQ = subMathFormulas[i][pos+2:pos+4]
      if (strQ == "~@"):
        strQ = subMathFormulas[i][pos+2:pos+5]
      #Replace the substring 'P->Q' in the formula with '(1-P*(1-Q))'
      mathString = "(1-"+strP+"*(1-"+strQ+"))"
      posP = subMathFormulas[i].find(strP)
      subMathFormulas[i] = subMathFormulas[i].replace(strP+"->"+strQ, mathString)
      if debugMode:
        print(subMathFormulas[i])

  #Change the '~P' to '(1-P)'
  for i in range(numSubs):
    pos = 1
    while pos > 0:
      #Search in the subMathFormula for a '~'
      pos = subMathFormulas[i].find("~");#returns -1 if it doesn't find anything.
      if pos > 0:
        if debugMode:
          print("Found \'~\' in @{} at position {}".format(i, pos))
          print(subMathFormulas[i], " --->  ")
      else:
        if debugMode:
          print("Found no \'~\' in @{}".format(i))
        continue
      #Get the statement 'P' that follows
      strP = subMathFormulas[i][pos+1:pos+2]
      if (strP == "@"):
        strP = subMathFormulas[i][pos+1:pos+3]
      #print("strP = " + strP)
      #Replace the substring '~P' in the formula with '(1-P)'
      mathString = "(1-"+strP+")";
      subMathFormulas[i] = subMathFormulas[i].replace("~"+strP, mathString)
      if debugMode:
        print(subMathFormulas[i])

  #Print out mathematical statements
  if verbose or debugMode:
    for i in range(numSubs):
      print(subMathFormulaNames[i] + " = " + subMathFormulas[i])

  #Flatten the main formula
  if verbose or debugMode:
    print("Flattening the main mathematical expression...")
  mathFormula = subMathFormulas[0]
  while (mathFormula.find("@") >= 0):
    if debugMode:
      print("mathFormula = " + mathFormula)
    posat = mathFormula.find("@")
    if (posat < 0):
      break
    numSub = int(mathFormula[posat+1])
    atSub = mathFormula[posat:posat+2]
    if debugMode:
      print("numSub =", numSub)
    mathFormula = mathFormula.replace(atSub, subMathFormulas[numSub])

  if verbose or debugMode:
    print(mathFormula)
  return mathFormula
