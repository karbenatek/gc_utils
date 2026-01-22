import __main__, os

# get directory of the main script being run
try:
    script_dir_path = os.path.dirname(os.path.abspath(__main__.__file__))
except AttributeError:
    # or the working directory if run in interactive mode or when using python -c "do something"
    script_dir_path = os.getcwd()

# global variable for directory of gc_utils    
gc_utils_dir = os.path.dirname(__file__)
