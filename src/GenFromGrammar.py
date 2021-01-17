import sys
import csv
import random

class Env:
    # curLeft
    # curRhs
    # rules of type {left,[Rhs]}    
    def __init__(self):
        self.rules = {}
    pass
    
class Rhs:
    # rts of type [RightToken]
    # tips of type [Tip]
    def __init__(self):
        self.rts = []
        self.tips = []
    pass
    
class RightToken:
    # type, one of "Optional", "Literal", "Nonterm"
    # val, if Optional then [RightToken] else string
    def __str__(self):
        return self.type, self.val        

    def __repr__(self):
        return self.type + ":" + str(self.val)
       
    pass
    
class Tip:
    # stmtRhsId - the stmt rhs under which this tip lies. Type string
    # id - the tip id. Type string
    # val - the tip string

    def __str__(self):
        return str(self.id) + " " + self.val
        
    def __repr__(self):
        return str(self)
        
    # Returns whether tip is displayable, and returns string            
    def GetDisplayableAndString(self):    
        # t must start with "! <int> <tip sentence>"
        displayStr = self.val.split(None, 2)[2]
        bDisplayable = True
        if displayStr.strip() == "NO HINTS":
            bDisplayable = False
        return bDisplayable, displayStr          
    pass
    
Optional = "O"
Literal = "L"
NonTerm = "N" 
Id = "I"

# Reads a line that is an right-hand-side of a non-terminal, and returns a list of tokens
# The argument row is a list of words in that line
def ParseRhs(env, row):
    rightTokens = []   
    ri = 0
    while ri < len(row):
        r = row[ri]        
        if r == '[':
            closePareni = row.index(']',ri+1)
            if closePareni == -1:
                raise "Error. Unmatched parenthesis ["
            else:
                childRow = row[ri+1:closePareni]
                rts = ParseRhs(env, childRow)                
                t = RightToken()
                t.type = Optional
                t.val = Rhs()
                t.val.rts = rts
                ri = closePareni + 1                
        elif r[0] == '_':
            t = RightToken()
            t.type = NonTerm
            t.val = r
            ri += 1
        else:
            t = RightToken()
            t.type = Literal
            t.val = r
            ri += 1
        rightTokens.append(t)
    return rightTokens
    
# Returns an Rhs object    
def ParseRhsTopLevel(env, row):
    rhs = Rhs()
    rt = RightToken()
    rt.type = Id    
    rt.val = int(row[0])
    rhs.rts = [rt]
    rhs.rts += ParseRhs(env, row[1:])
    return rhs
        
def ParseRow(env, row):    
    
    if row[-1] == "=":
        if row[0][0] != '_':
            raise "Error. Left non-term does not start with _"
        else:
            env.curLeft = row[0]
            env.curRhs = None
            if row[0] in env.rules:
                print "Error. Rule for {0} repeated more than once".format(env.curLeft)
            else:
                env.rules[env.curLeft] = []
    elif row[0] == "!":
        if env.curRhs == None:
            raise "curRhs is None. Tip before rule?"
        tip = ParseTip(env, row)
        tip.stmtRhsId = GetIdFromRtTokens(env.curRhs.rts)
        env.curRhs.tips.append(tip)                
    else:
        rhs = ParseRhsTopLevel(env, row)
        env.curRhs = rhs
        env.rules[env.curLeft].append(rhs)
        
    return env
    
# Parses row with a tip and returns a Tip object    
def ParseTip(env, row):
    if row[0] != "!" or len(row) < 2:
        raise "ParseTip called on non-tip or bad-tip: " + ' '.join(row)
    
    tip = Tip()
    tip.id = row[1]
    tip.val = FixPunctuation(' '.join(row))
    return tip
    
def FixPunctuation(stmt):
    return stmt.replace(" ,", ",").replace(" .", ".")

# Returns both a statement, and the Id for the statement. IdParts is an accumulator of Ids as the string is built
def GenStmtForRhs(env, rhs, idParts):
    strs = []    
    for rt in rhs.rts:
        if rt.type == Literal:
            strs.append(rt.val)
        elif rt.type == NonTerm:
            rhss = env.rules[rt.val]
            rnd = random.randint(0, len(rhss)-1)
            idParts.append(GetIdFromRtTokens(rhss[rnd].rts))
            stmt, idParts = GenStmtForRhs(env, rhss[rnd], idParts)
            strs.append(stmt)
        elif rt.type == Optional:
            rnd = random.randint(0,1)
            idParts.append(rnd)
            if rnd:
                oRhs = rt.val                
                stmt, idParts = GenStmtForRhs(env, oRhs, idParts)
                strs.append(stmt)
        elif rt.type == Id:
            pass
        else:
            raise "GenStmtForRhs. Invalid right token type ", rt.type
    return FixPunctuation(' '.join(strs)), idParts
    
# Returns the sentence, and an id-based representation of it    
def GenerateSentence(env):
    rootRules = env.rules["_root"]    
    ri = random.randint(0, len(rootRules)-1)      
    stmt, ids = GenStmtForRhs(env, rootRules[ri], [GetIdFromRtTokens(rootRules[ri].rts)])
    return stmt, "s" + ".".join(map(str,ids))
    
def GetRhsByIdComponent(nonTerm, list_rhs, idComponent):
    for rhs in list_rhs:
        if rhs.rts[0].type == Id and rhs.rts[0].val == idComponent:
            return rhs
    raise Exception("No right token for this nonTerm {0}, idComponent {1}, in list {2}".format(nonTerm, idComponent, list_rts))
    
def GetRightTokensByIdComponent(nonTerm, list_rhs, idComponent):
    return GetRhsByIdComponent(nonTerm, list_rhs, idComponent).rts
    
def GetIdFromRtTokens(rtTokens):
    return rtTokens[0].val
    
# Function to generate a specific statement given idParts
def GenStmtFromRhsForId(env, rightTokens, idParts):
    strs = []
    idIndex = 0
    for rt in rightTokens:
        if rt.type == Literal:
            strs.append(rt.val)
        elif rt.type == NonTerm:
            nRts = env.rules[rt.val]
            i = idParts[idIndex]
            idIndex += 1
            rts = GetRightTokensByIdComponent(rt.val, nRts, i)
            stmt, idParts = GenStmtFromRhsForId(env, rts, idParts[idIndex:])
            idIndex = 0
            strs.append(stmt)
        elif rt.type == Optional:
            i = idParts[idIndex]
            idIndex += 1
            if i:
                oRts = rt.val                
                stmt, idParts = GenStmtFromRhsForId(env, oRts.rts, idParts[idIndex:])
                idIndex = 0
                strs.append(stmt)
        elif rt.type == Id:
            pass
        else:
            raise Exception("GenStmtFromRhsForId. Invalid right token type " +  rt.type)    
    return FixPunctuation(' '.join(strs)), idParts
            
# Returns the sentence, and an id-based representation of it    
def GenerateSentenceForId(env, id):
    rootRules = env.rules["_root"]
    idParts = map(int, id[1:].split('.'))    
    rootRules = env.rules["_root"]
    i = idParts[0]
    rts = GetRightTokensByIdComponent("_root", rootRules, i)    
    stmt, idParts = GenStmtFromRhsForId(env, rts, idParts[1:])
    return stmt
   
   
# Returns a list with duplicates removed
def RemoveDuplicates(l_in):
    l = []
    for e in l_in:
        if e not in l:
            l.append(e)
    return l
   
# Function to generate a specific statement given idParts
def GetTipsFromRhsForId(env, rhs, idParts):
    tipss = []
    idIndex = 0
    rightTokens = rhs.rts
    for rt in rightTokens:
        if rt.type == Literal:
            pass
        elif rt.type == NonTerm:
            nRts = env.rules[rt.val]
            i = idParts[idIndex]
            idIndex += 1
            childRhs = GetRhsByIdComponent(rt.val, nRts, i)
            tipss.append(childRhs.tips)
            moreTipss, idParts = GetTipsFromRhsForId(env, childRhs, idParts[idIndex:])            
            idIndex = 0
            tipss.extend(moreTipss)
        elif rt.type == Optional:
            i = idParts[idIndex]
            idIndex += 1
            if i:
                oRhs = rt.val                
                # tipss.append(oRhs.tips)   # Srineet: Bug fix on 13 mar '16. Commented this out. It only led to empty lists.
                moreTipss, idParts = GetTipsFromRhsForId(env, oRhs, idParts[idIndex:])                
                idIndex = 0
                tipss.extend(moreTipss)
        elif rt.type == Id:
            pass
        else:
            raise Exception("GetTipsFromRhsForId. Invalid right token type " +  rt.type)        
    return tipss, idParts
   
# Returns the Id for the set of tips
def GetTipsIdFromTips(env, tipss):
    idParts = []
    for tips in tipss:
        if not tips:
            idParts.append('0')
        else:
            idsForThisSet = []
            for t in tips:
                idsForThisSet.append(t.id)
            idParts.append('!'.join(idsForThisSet))
                            
    return "h" + ".".join(idParts)
    
# Combines the statement and tips Id using a _ in between
def CombineStmtAndTipsId(stmtId, tipsId):
    return "{0}_{1}".format(stmtId, tipsId)
    
# Separates a possibly joint statement+hints Id into the two separate Ids
def SeparateIds(combinedId):
    pos = combinedId.find('_')
    if pos != -1:
        return combinedId[0:pos], combinedId[pos+1:]
    else:
        return combinedId, ""
        
  
# Returns all applicable tips given a statement id   
# Returns [[Tip]]
def GetAllTipsForStmtId(env, stmtId):
    tipss = []
    rootRules = env.rules["_root"]
    idParts = map(int, stmtId[1:].split('.'))
    rhs = GetRhsByIdComponent("_root", rootRules, idParts[0])        
    tipss.append(rhs.tips)        
    moreTips, idParts = GetTipsFromRhsForId(env, rhs, idParts[1:])        
    tipss.extend(moreTips)
    # remove empty lists and return
    #return filter(lambda t: t, tipss)
    # Just return all, whether empty or not
    return tipss
    
# Gets a random set of tips for a statement Id
# Will only return non-empty if every sub-part of the statement has 
# Returns a list of list of tips - a sublist for randomly chosen tips from a stmtpart
def GetRandomTipsForStmtId_WithSublists(env, stmtId):
    tipss = GetAllTipsForStmtId(env, stmtId)
    # if any of the sublists is empty, that means we haven't yet
    # written up tips for that part of the statement. So don't 
    # emit any tips for the statement at all
    if any(not l for l in tipss):        
        return []      
        
    bAtleastOneTipAdded = False    
    
    while not bAtleastOneTipAdded:
        tipsRet = []
        for l in tipss:
            # First decide whether to include any tip from this set. 
            # say no with probability 1/8 (arbitrary)
            if random.random() < 0.125:
                tipsRet.append([])
            else:        
                howMany = random.randint(1, min(len(l), 2))                
                whichOnes = random.sample(range(0, len(l)), howMany)
                tipsToAppend = [l[w] for w in whichOnes if l[w].GetDisplayableAndString()[0]]
                if tipsToAppend: bAtleastOneTipAdded = True
                tipsRet.append(tipsToAppend)
    return tipsRet 

# Flat list of randomly chosen tips    
def GetRandomTipsForStmtId(env, stmtId):
    tipss = GetRandomTipsForStmtId_WithSublists(env, stmtId)
    return [t for tips in tipss for t in tips]

    
# returns the tip with the given id. Throws if not found
def GetTipWithId(tips, id):
    for t in tips:
        if t.id == id:
            return t
    raise Exception("GetTipWithId. Tip for id {0} not found in {1}".format(id, tips))
        
# Returns list of tips for stmt based on tips Id
def GetTipsFromTipsId(env, stmtId, tipsId):
    retTips = []
    if not tipsId:
        return []
    else:
        tipss = GetAllTipsForStmtId(env, stmtId)
        idParts = tipsId[1:].split('.')  # the first character of tipsId is 'h', we skip that        
        for (tips, idTips) in zip(tipss, idParts):            
            if idTips == '0':
                pass
            else:
                ids = idTips.split('!')
                for id in ids:
                    tip = GetTipWithId(tips, id)
                    retTips.append(tip)
    return retTips
    
# from a list of elemenents of type Tip, get a list of displayable tips strings    
def GetTipsDisplayStringsFromTipsList(tips):    
    return RemoveDuplicates([t.GetDisplayableAndString()[1] for t in tips if t.GetDisplayableAndString()[0]])
        
# Returns the tuple <sentence, stmtId, tips, tipsId, combinedId>
# If the tipss is [] then there are no tips, and hence no tipsId
def GenerateSentenceWithTipsAndIDs(env):
    stmt, stmtId = GenerateSentence(env)
    tips_strings = []
    tipsId = ""    
    combinedId = stmtId
    tipss = GetRandomTipsForStmtId_WithSublists(env, stmtId)
    if tipss:
        tipsId = GetTipsIdFromTips(env, tipss)
        combinedId = CombineStmtAndTipsId(stmtId, tipsId)
        tips_strings = GetTipsDisplayStringsFromTipsList([t for tips in tipss for t in tips])
    return stmt, stmtId, tips_strings, tipsId, combinedId
    
# Returns tuble <sentence, stmtId, tips, tipsId>
def GetSentenceAndTipsFromCombinedId(env, combinedId):
    stmtId, tipsId = SeparateIds(combinedId)
    stmt = GenerateSentenceForId(env, stmtId)
    tips_strs = []
    if tipsId:
        tips = GetTipsFromTipsId(env, stmtId, tipsId)
        tips_strs = GetTipsDisplayStringsFromTipsList(tips)
    return stmt, stmtId, tips_strs, tipsId
    
    
def GenEnvFromFile(grammarFilename):
    env = Env()
    with open(grammarFilename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)
        for row in reader:  
            row = filter(lambda r:r != "", row)
            if row != [] and row[0][0] != "#":
                env = ParseRow(env, row)    
    return env       
    
def MainFunc(grammarFilename):    
    env = GenEnvFromFile(grammarFilename)
    return GenerateSentence(env)
    
def Tests(grammarFilename):    
    env = GenEnvFromFile(grammarFilename)
    for i in range(0,1000):
        print "---TEST {0}---".format(i+1)
        stmt, id = GenerateSentence(env)
        print "1. ", stmt, id
        stmt2 = GenerateSentenceForId(env, id)        
        print "2. ", stmt2
        if stmt != stmt2:
            print "MISMATCH!!!"
            break
            
      
         

def TipsTests2(grammarFilename):  
    print "TIPS TESTS:"
    env = GenEnvFromFile(grammarFilename)
    bProblemEnountered = False
    for i in range(0,1000):        
        stmt, stmtId, tips, tipsId, combinedId = GenerateSentenceWithTipsAndIDs(env)
        stmt2, stmtId2, tips2, tipsId2 = GetSentenceAndTipsFromCombinedId(env, combinedId)        

        
        if stmt != stmt2 or stmtId != stmtId2 or tips != tips2 or tipsId != tipsId2 or "[" in stmt or "[" in stmt2:
            bProblemEnountered = True            
          
            print "*** MISMATCH!!! ***"
            print "{0}, {1}, {2}:".format(stmtId, tipsId, combinedId)
            print stmt
            print "Thought Guide:"
            for t in tips:            
                print '* ' + t + '\n'
            
            print ">>> {0}, {1}, {2}:".format(stmtId2, tipsId2, combinedId)
            print ">>> ", stmt2
            print ">>> Thought Guide:"
            for t in tips2:                
                print '>>> * ' + t + '\n'
                
    if not bProblemEnountered:
        print "Passed"
       
    
            
def TestId(grammarFilename, combinedId):
    env = GenEnvFromFile(grammarFilename)
    print id
    stmt, stmtId, tips, tipsId = GetSentenceAndTipsFromCombinedId(env, combinedId)
    print "{0}, {1}, {2}:".format(stmtId, tipsId, combinedId)
    print stmt
    print "Thought Guide:"
    for t in tips:            
        print '* ' + t + '\n'
        
def PrettyPrintSubLists(ls, indentPrefix):
    if not ls:
        print "[]<not ls>"
        return
    print '['
    for l in ls:
        if isinstance(l, list):
            PrettyPrintSubLists(l, indentPrefix + '\t')
        else:
            print indentPrefix, str(l)[:20]
    print ']'
        
def TestTemp(grammarFilename):
    env = GenEnvFromFile(grammarFilename)
    myId="s64.2.3.2.1"
    print "Getting tips for {0} {1}".format(myId, GenerateSentenceForId(env, myId))
    tips = GetAllTipsForStmtId(env, myId)
    if any(not l for l in tips):
        print "There is an empty subList"
    PrettyPrintSubLists(tips, "")
    print "Now Random Tips:"
    tips = GetRandomTipsForStmtId_WithSublists(env, myId)
    PrettyPrintSubLists(tips, "")
        
    
if __name__ == "__main__":
    grammarFilename = sys.argv[1]
#    print MainFunc(grammarFilename)    
#    TestId(grammarFilename, 's57.2.2_h0.0.0.0.0.2!3')
    TipsTests2(grammarFilename)
#    TestTemp(grammarFilename)

    
