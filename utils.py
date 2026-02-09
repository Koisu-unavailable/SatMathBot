import matplotlib.pyplot as plt
import io

def render_latex(latex_string):
    plt.rcParams['text.usetex'] = True
    a = '\\frac{a}{b}'  #notice escaped slash
    plt.text(0.5, 0.5, f"${a}$", fontsize=20, ha='center')
    plt.axis('off')

    buf = io.BytesIO() 
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)   
