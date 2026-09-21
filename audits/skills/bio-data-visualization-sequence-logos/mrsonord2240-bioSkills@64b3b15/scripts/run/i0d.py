import logomaker, inspect
print(logomaker.__version__)
print(inspect.signature(logomaker.transform_matrix))
print(inspect.getsource(logomaker.transform_matrix)[:6000])
print(inspect.signature(logomaker.Logo.__init__))
