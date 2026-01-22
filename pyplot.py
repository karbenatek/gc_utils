import matplotlib.pyplot as plt
from matplotlib import rc

def set_font_and_fig():
    rc('font',**{'family':'serif','serif':['Computer Modern']})
    rc('text', usetex=True)
    plt.rcParams['figure.figsize'] = (8, 4.5)  # Default figure size in inches (width, height)
    plt.rcParams['figure.dpi'] = 200  # Default dots per inch (DPI)