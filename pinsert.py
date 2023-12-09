import re
from tabulate import tabulate
from operator import itemgetter

def line_col(str, idx):
    """
    Convert index in string to it's line and column.
    """
    line = str.count('\n', 0, idx) + 1
    col = idx - str.rfind('\n', 0, idx)
    return f'{line}:{col}'

def pinsert(filename: str, 
            variables: dict, 
            output_file = None, 
            crash_on_error = True, 
            show_usages = True, 
            warn_unused = True, 
            regex=r'@(\w+?)@'):
    """
    Replaces placeholders in a file with corresponding values from a dictionary.

    @param filename The path to the file that needs placeholder replacement.
    @param variables A dictionary containing key-value pairs for placeholders and their corresponding values.
    @param output_file (Optional) Output file name. If not given the new file will be filename.formatted
    @param crash_on_error (Optional) Whether to stop if placeholder wasn't found in dictionary.
    @param show_usages (Optional) Whether to print a table showing the usages of each placeholder and its value. Default is True.
    @param warn_unused (Optional) Whether to print a table showing placeholders that were not used. Default is True.
    @param regex (Optional) Custom regex to find placeholders. By default it looks for @placeholder@.
    @returns None 
    """
    with open(filename, 'r') as f:
        contents = ''.join(f.readlines())

    failed_to_match = []
    statistics = {key: 0 for key in variables.keys()}
    
    def replacer(match):
        try:
            statistics[match.group(1)]+=1
            return str(variables[match.group(1)])
        except KeyError as e:
            position = line_col(contents, match.start())
            failed_to_match.append((match.group(1),position))
            return f'\\textbf{{ variable "{match.group(1)}" not found }}'

    contents=re.sub(regex, replacer, contents)
    def print_errors():
        for fail, pos in failed_to_match:
            print(f'Key "{fail}" at {filename}:{pos} was not found in dictionary')
        
    got_errors = len(failed_to_match) > 0
    if got_errors and crash_on_error:
        print('Stopping because of errors:')
        print_errors()
        print('No output file produced')
        return
    
    if got_errors:
        print('Following errors occured during processing:')
        print_errors()
    else:
        print('All placeholders replaced properly')
    if show_usages:
        print('Usages:')
        table = sorted([[k,variables[k],v] for k,v in statistics.items()], key=itemgetter(2,0), reverse=True)
        # print(keys, values)
        print(tabulate(table, ['key','value', 'usages'], tablefmt='rounded_outline'))
    if warn_unused:
        if 0 in statistics.values():
            print('Note that some values left unused:')
        table = [[key, variables[key]] for key,usages in statistics.items() if usages==0]
        print(tabulate(table, ['key','value'], tablefmt='rounded_outline'))
    new_name = filename+'.formatted' if output_file is None else output_file
    with open(new_name, 'w') as f:
        f.write(contents)
    print(f'Formatted file saved as "{new_name}"')

v=10
s=30
t=s/v
vars = {
    'velocity': v,
    'time': t,
    'distance': s,
    'name': 'andrey'
}

pinsert('tex/test.tex', vars, crash_on_error=False)




