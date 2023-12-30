# Python Recursive Descent Parser for EBNF Grammars

## Overview
This project implements a simple recursive descent parser in Python to validate expressions based on Extended Backus-Naur Form (EBNF) grammars. It uses a LL(1) parsing technique with one parsing procedure for each specified grammar rule. The parser can recursively invoke these procedures, handling circular references between grammar rules and validating expressions accordingly.

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Ensure Python 3.x is installed on your machine.
2. Clone or download this repository to your local machine.

### Running the Program
Execute the script using Python:
```
python recursive_descent_parser.py
```

## Code Description

### `recursive_descent_parser.py`
- **Key Components**:
  - Lexical Analysis: Tokenizes the input expression into a list of tokens.
  - Recursive Descent Parsing: Validates the expression based on the EBNF grammar rules.

- **Grammar Rules (EBNF)**:
<exp> ::= <term> { op <term> | ( <exp> ) } | ( <exp> )
<term> ::= relop <int> | <int> - <int>
<int> ::= 0-9999999999
<relop> ::= > | < | >= | <= | == | not
<-> ::= - (dash)


- **Classes and Methods**:
- `recDescent`: Main class for the parser.
  - `lex()`: Tokenizes the expression.
  - `expression()`, `term()`: Parsing procedures for the respective grammar rules.
  - `validate()`: Initiates the parsing process and returns the validity of the expression.

- **Parsing Logic**:
- The parser handles each grammar rule with a dedicated function.
- It employs recursion to manage nested expressions and to navigate the parse tree.

## Testing
- The script includes test cases to demonstrate the validation of expressions.
- Both positive and negative test cases are provided to show correct parser behavior.

## Disclaimer
This project is intended for educational purposes to demonstrate recursive descent parsing and should not be used for production-level parsing tasks.

## Author
- ThanksLogan


