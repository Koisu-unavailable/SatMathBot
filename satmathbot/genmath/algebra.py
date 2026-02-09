import satmathbot.genmath.ProblemGenerator as ProbGen
import satmathbot.utils

class AlgebraGen(ProbGen.ProblemGenerator):
    def __init__(self):
        super().__init__()
    
    def generate_problem(self):
        """Returns the path to an image of the generated problem"""
        return satmathbot.utils.render_latex(r'\frac{a}{b}')