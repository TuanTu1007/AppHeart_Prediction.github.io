import ast

def extract_docstrings(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    docstrings = {}
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                name = node.name if hasattr(node, 'name') else 'module'
                docstrings[name] = docstring
                
    return docstrings

file_path = r"D:\Subject\IE221_Python\DoAn\Front-end\login.py"
docstrings = extract_docstrings(file_path)
for name, doc in docstrings.items():
    print(f"{name}:\n{doc}\n")