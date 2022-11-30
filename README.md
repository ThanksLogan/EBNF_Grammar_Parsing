# EBNF_Grammar_Parsing
A program built to parse a token list based on a set of grammar rules in the Extended Backus-Naur Form (EBNF) for describing the syntax of expressions.
Uses Python3 to implement a simple recursive descent parser for validating expressions based on the grammars designated.
The essence of the recursive descent parsing is to have ONE parsing procedure for each specified grammar rule (or non-terminal) starting from the outermost grammar rule,
and parsing procedures can be invoked recursively based on the circular references between grammar rules.



