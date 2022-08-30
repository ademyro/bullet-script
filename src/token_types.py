import string

NUMBERS         = '1234567890'
CHARACTERS      = string.ascii_letters + '_' + NUMBERS
        
INT             = '<integer>' # número inteiro
FLOAT           = '<float>' # número com valor decimal.
STRING          = '<str>'
PLUS            = '+'
MINUS           = '-'
MULTI           = '*'
DIVIS           = '/'
POW             = '^'
DOT             = '.'
QUESTION        = '?'
OPEN_PAREN      = '('
CLOSE_PAREN     = ')'
OPEN_BRACE      = '{'
CLOSE_BRACE     = '}'
OPEN_BRACKET    = '['
CLOSE_BRACKET   = ']'
COMMA           = ','
COLON           = ':'
ASSIGNMENT      = '='
LOG_EQ          = '=='
LOG_NEQ         = '!='
LOG_GT          = '>'
LOG_GTE         = '>='
LOG_LT          = '<'
LOG_LTE         = '<='
LOG_NOT         = 'not'
LOG_AND         = 'and'
LOG_OR          = 'or'
LOG_IN          = 'in'
KEYWORD         = '<kw>'
IDENTIFIER      = '<id>'
NEWLINE         = '<newln>'
EOF             = '<eof>' # fim do arquivo

KEYWORDS = [
    'if',
    'else',
    'while',
    'for',
    'in',
    'fn',
    'return',
    'break',
    'continue',
    'load',
    'switch',
    'case',
    'default'
]

PRIMITIVE_FUNCTIONS = [
    'print',
    'println',
    'readln',
    'instanceof',
    'range'
]