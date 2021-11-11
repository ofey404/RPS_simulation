import sympy
import pickle

with open("./matrix-eigens-4.pkl", "rb") as f:
    eigens = pickle.load(f)
    sympy.pprint(eigens)
    # print(eigens)

