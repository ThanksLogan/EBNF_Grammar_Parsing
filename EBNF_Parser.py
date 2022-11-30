
import re
from functools import *

"""

A LL(1) recursive descent parser for validating simple expressions.

******************************************************
GRAMMAR SET:
<exp> ::= <term> { op <term> | ( <exp> ) } | ( <exp> )
<term> ::= relop <int> | <int> - <int> 
<int> ::= 0-9999999999
<relop> ::= > | < | >= | <= | == | not 
<-> ::= - (dash)
******************************************************


"""

class recDescent:

    # IMPORTANT:
    # MUST NOT change the signatures of 
    # the constructor, lex(self) and validate(self)
    # Otherwise, auto-tests will FAIL

    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):

        self.expr = expr # string to be parsed
        self.valid = False # Global boolean to detect grammar-rule breaking
        self.tokens = [] # tokens from lexer tokenization of the expression
        self.index = 0 # Indexer for tokens list
        self.pCount = 0 # (invalid) Parenthesis counter: used to check for an invalid ")"

    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    def lex(self):
        self.tokens = re.findall("[-\(\)]|[!<>=]=|[<>]|\w+|[^ +]\W+", self.expr)
        # transform tokens to lower case, and filter out possible spaces in the tokens
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    

    # ----------------------------------------------------------------------------------------
    # Helper Functions
    # ----------------------------------------------------------------------------------------
    def isLast(self):
        return(self.index + 1 >= len(self.tokens)) # True if we're at the end of self.tokens' list

    def advance(self):
        if(self.isLast() == False):
            self.index += 1
    
    def current(self):
        return self.tokens[self.index] 

    def isRelop(self, token):
        return (token == ">" or token == "<" or token == ">=" or token == "<=" or token == "==" or token == "!=" or token == "not")

    def isOp(self, token):
        return (token == "and" or token == "or" or token == "nand" or token == "xor" or token == "xnor")

    def isDash(self, token):
        return (token == "-")
    

    # -----------------------------------------------------------------------------------------
    # Recursive Expression and Term parsers - determine if the input expression is valid or not
    # -----------------------------------------------------------------------------------------

    # EXPRESSION FUNCTION  :: Gets called recursively
    # <exp> ::= <term> { op <term> | <exp> } | ( <exp> )
    def expression(self):
        
        if(self.isLast()):
            return self.valid # Breaks out of expression recursion when we're at the end 
        else:
            # 1.) if its a left parenthesis, we must advance to check within that expression(recursive) <exp> := ( <exp> )    
            # CHECKING for ( <exp> )    
            if(self.current() == "("): 
                self.pCount += 1 # Used to check for random closing parenthesis validating an expression
                self.advance()
                if(self.isLast()): # Checking to see invalid parenthesis usage: example: "(4"
                    self.valid = False
                    return self.valid # Breaks out of expression call with valid flag as False

                if(self.expression() == False): # Recursively calls itself to check inside parenthesis for valid <exp>/<term> usage (could be any definition)
                    self.valid = False # Flag valid as false if expression checking fails, if not we can pass on to check R. Parenthesis
                    return False 
                #self.advance() # Moves up after completing expression to detect closing parenthesis
                if(self.current() != ")"): # Since <exp> inside parenthesis finished, must find R. Paren (however deep we are in the recursion)
                    self.valid = False
                    return False #REASON: did not find a closing matching parenthesis
                else: 
                    #Successfully identified an expression inside parenthesis: ( <exp> ), now move to handle next
                    self.advance() # Advances to token after closing parenthesis
                    # If we were able to advance, we need to check for a symbol in the incorrect place
                    # Example: "(>=5)and", or "(<7)>=", or "(==8)-", or "(>=9)9" 
                    if((self.isOp(self.current()) or self.isRelop(self.current()) or self.isDash(self.current()) or self.current().isdigit()) and self.isLast()):
                        self.valid = False # REASON: illegal symbol directly following right parenthesis; such as: '(>=5)and'
                        return self.valid 
                    if(self.isLast()):
                       self.valid = True # Marks valid flag as true since no ( <exp> ) rules broken
                       return self.valid # Here we return/recur back up  

            # CHECKING <term>
            # we check for a <term> calling term(), and then call isOp() to check for an operator. 
            # if isOp() returns true, then we need to check the following <term> for validity
            else:
                # Currently at the token immediately following parenthesis if we were called recursively, will now call term() 
                # Else, we are at a basic token NOT inside parenthesis but will still check the term()
                if(self.term() == False): # Running term() to check for valid dash or relop usage to come back to  
                    self.valid = False
                    return False 
                # Passes through here if term identification returned True (self.valid == True)
                # Now, we should be checking the token immediately after the term() for and op (can occur multiple times)

                # {op <term> | ( <exp> )}
                # Here, we're checking for a valid term or exp with parenthesis directly following an Operator
                if(self.isOp(self.current())):
                    # If we indeed see an Operator, we need to advance to check the next token for validity
                    # We also need to check if we're at the end for an invalid Operator usage
                    if(self.isLast()):
                        self.valid = False
                        return False # FAILED - thinks were at the end when we're not
                    else: self.advance()
                    # Here, we now recursively call expression to check for a valid <term> or <(exp)> post-Operator
                    # If it's a <term> it will go into this same else block where it will check for term validity
                    #  and then return back right here to finish the isOp check with self.valid as true
                    if(self.expression() == False):
                        return False
                if(self.current() == ")" and self.pCount == 0):
                    self.valid = False
                    return False
                return self.valid


    def term(self):
        # <term> ::= <int> - <int> | relop <int>

        # Checking for: relop <int>
        if(self.isRelop(self.current())):
            if(self.isLast() or self.isRelop(self.tokens[self.index + 1])):
                self.valid = False
                return False # REASON: a relational operator without an <int> to the right of it. example: "><" or ">"
            self.advance() # Should advance to an <int> directly to right of operator
            if(self.current().isdigit()):
                # Successfully found "relop <int>"  
                self.valid = True
                self.advance() 
                return True # Should return back up main signalling VALID, even if we reached the end of the list
            else:
                self.valid = False 
                return False #REASON: relop missing an int

        # Checking for: <int> - <int>
        elif(self.current().isdigit()):
            if(self.isRelop(self.tokens[self.index + 1])):
                self.valid = False
                return False # REASON: cannot have an <int> relop
            self.advance()
            if(self.isLast()):
                self.valid = False
                return False # REASON: cannot have an <int> be last on its own inside parenthesis
            if(self.isDash(self.current())):
                if(self.isLast()):
                    self.valid=False
                    return False #REASON: cannot end on a <int> - (incomplete)
                self.advance()
                if(self.current().isdigit()):
                    # Successfully found <int> - <int>
                    self.valid = True
                    self.advance() 
                    return True # Should return back up main signalling VALID, even if we reached the end of the list
                else: 
                    self.valid = False
                    return False #REASON: <int> - missing final int
            else: 
                self.valid = False
                return False #REASON: <int> missing dash
        else: 
            self.valid = False
            return False #REASON: nothing inside

    # validate() function will return True if the expression is valid, False otherwise 
    def validate(self):
        # Using the tokens from lex() tokenization,
        # this validate would first call lex() to tokenize the expression,
        # then call the top level parsing procedure for the outermost rule and go from there
        self.lex()   
        self.expression()
        return self.valid

 
print("\nTesting a true and false example -->\n")
# positive tests: validation of the expression returns True
# negative tests: validation of the expression returns False 

print("The following should print True...")
r = recDescent('(5 - 100) and (not 50) or (>= 130 or (2 - 4))') 
print("Validation: ", r.validate())


print("The following should print False...")
r = recDescent('>= 5) xnor < 10') 
print("Validation: ", r.validate())





