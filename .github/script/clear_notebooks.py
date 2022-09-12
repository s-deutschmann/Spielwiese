import argparse
from nbconvert.preprocessors import ClearOutputPreprocessor, ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
import nbformat

def process_notebook(filename, execute=True):
    '''Checks if an IPython notebook runs without error from start to finish. If so, writes the notebook to HTML (with outputs) and overwrites the .ipynb file (without outputs).
    '''
    with open(filename) as f:
        nb = nbformat.read(f, as_version=4)
        
    clear = ClearOutputPreprocessor()
    
    try:
        if execute:
            # Check that the notebook runs
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            ep.preprocess(nb, {'metadata': {'path': ''}})

        msg = ''

    except CellExecutionError:
        msg = f'\n  Error executing the notebook "{filename}".\n'
        msg += f'  See notebook "{filename}" for the traceback.'
        
    # Clear notebook outputs and save as .ipynb
    with open(filename, mode='w', encoding='utf-8') as f:
        nbformat.write(nb, f)
         
    print(f"Processed {filename}{msg}")

    return


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='read some files')
    parser.add_argument('file',
                        metavar='File',
                        type=str, 
                        nargs='+',
                        help='Files')

    args = parser.parse_args()
    file = args.file

    file[:] = [x for x in file if x.endswith('.ipynb')]

    for fn in file:
        if not fn.endswith('.ipynb'):
            print(f'Error: file {fn} is not an IPython notebook.')
            raise IOError
        
    for fn in file:
        process_notebook(fn, execute=False)
    