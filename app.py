from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

def detect_scopes(code):
    tree = ast.parse(code)
    scopes = []

    def extract_scopes(node, parent_scope=None):
        if isinstance(node, ast.FunctionDef):
            scope_type = "Function"
            scope_name = node.name
            scope_contents = ast.get_source_segment(code, node)
            scopes.append({"Type": scope_type, "Name": scope_name, "Contents": scope_contents})
        elif isinstance(node, ast.ClassDef):
            scope_type = "Class"
            scope_name = node.name
            inner_scopes = []
            for child_node in node.body:
                extract_scopes(child_node, parent_scope=scope_name)
            scope_contents = [scope["Name"] for scope in inner_scopes]
            scopes.append({"Type": scope_type, "Name": scope_name, "Contents": scope_contents})
            return
        for child_node in ast.iter_child_nodes(node):
            extract_scopes(child_node, parent_scope=parent_scope)

    extract_scopes(tree)

    return scopes

@app.route('/detect_scopes', methods=['POST'])
def handle_detect_scopes():
    data = request.get_json()
    code = data.get('code', '')
    if code:
        scopes = detect_scopes(code)
        return jsonify({"scopes": scopes})
    else:
        return jsonify({"error": "No code provided."}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
