import re


# Keywords
keywords = frozenset(['abstract', 'assert', 'boolean', 'break', 'byte', 'case',
                  'catch', 'char', 'class', 'const', 'continue', 'default',
                  'do', 'double', 'else', 'enum', 'extends', 'exports', 'final',
                  'finally', 'float', 'for', 'goto', 'if', 'implements',
                  'import', 'instanceof', 'int', 'interface', 'long', 'native',
                  'module', 'new', 'package', 'private', 'protected', 'public', 
                  'return', 'requires', 'short', 'static', 'strictfp', 'super', 
                  'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
                  'try', 'var','void', 'volatile', 'while', 'true', 'false', 'null'])


# holds known non-user-defined functions; immutable set
main_set = frozenset({'main'})
# arguments in main function; immutable set
main_args = frozenset({'args'})

# input is a list of string lines
def clean_gadget(gadget):
    # dictionary; map function name to symbol name + number
    fun_symbols = {}
    # dictionary; map variable name to symbol name + number
    var_symbols = {}

    fun_count = 1
    var_count = 1

    # regular expression to catch multi-line comment
    rx_comment = re.compile('\*/\s*$')
    # regular expression to find function name candidates
    rx_fun = re.compile(r'\b([_A-Za-z]\w*)\b(?=\s*\()')
    # regular expression to find variable name candidates
    #rx_var = re.compile(r'\b([_A-Za-z]\w*)\b(?!\s*\()')
    rx_var = re.compile(r'\b([_A-Za-z]\w*)\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()')

    # final cleaned gadget output to return to interface
    cleaned_gadget = []

    for line in gadget:
        # process if not the header line and not a multi-line commented line
        if rx_comment.search(line) is None:
            # remove all string literals (keep the quotes)
            nostrlit_line = re.sub(r'".*?"', '""', line)
            # remove all character literals
            nocharlit_line = re.sub(r"'.*?'", "''", nostrlit_line)
            # replace any non-ASCII characters with empty string
            ascii_line = re.sub(r'[^\x00-\x7f]', r'', nocharlit_line)

            # return, in order, all regex matches at string list; preserves order for semantics
            user_fun = rx_fun.findall(ascii_line)
            user_var = rx_var.findall(ascii_line)

            # Could easily make a "clean gadget" type class to prevent duplicate functionality
            # of creating/comparing symbol names for functions and variables in much the same way.
            # The comparison frozenset, symbol dictionaries, and counters would be class scope.
            # So would only need to pass a string list and a string literal for symbol names to
            # another function.
            for fun_name in user_fun:
                if len({fun_name}.difference(main_set)) != 0 and len({fun_name}.difference(keywords)) != 0:
                    # check to see if function name already in dictionary
                    if fun_name not in fun_symbols.keys():
                        fun_symbols[fun_name] = 'FUN' + str(fun_count)
                        fun_count += 1
                    # ensure that only function name gets replaced (no variable name with same
                    # identifier); uses positive lookforward
                    ascii_line = re.sub(r'\b(' + fun_name + r')\b(?=\s*\()', fun_symbols[fun_name], ascii_line)

            for var_name in user_var:
                # next line is the nuanced difference between fun_name and var_name
                if len({var_name}.difference(keywords)) != 0 and len({var_name}.difference(main_args)) != 0:
                    # check to see if variable name already in dictionary
                    if var_name not in var_symbols.keys():
                        var_symbols[var_name] = 'VAR' + str(var_count)
                        var_count += 1
                    # ensure that only variable name gets replaced (no function name with same
                    # identifier); uses negative lookforward
                    ascii_line = re.sub(r'\b(' + var_name + r')\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()', \
                                        var_symbols[var_name], ascii_line)

            cleaned_gadget.append(ascii_line)
    # return the list of cleaned lines
    return cleaned_gadget