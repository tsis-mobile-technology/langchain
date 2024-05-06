import nbformat as nbf

# Read the Python file
with open('./langchain_tut_04.py', 'r', encoding='utf-8') as f:
    py_content = f.read()

# Split the file into cells on '# %%' and create a new notebook cell for each
cells = []
for cell_content in py_content.split('# %%'):
    cells.append(nbf.v4.new_code_cell(cell_content))

# Create a new notebook
nb = nbf.v4.new_notebook(cells=cells)

# Write the notebook to a new .ipynb file
with open('langchain_tut_04.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)