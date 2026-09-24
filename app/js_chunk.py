from tree_sitter_language_pack import get_parser
from tree_sitter import Query, QueryCursor

parser = get_parser("javascript")

def extract_js_chunk(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    chunks = [] 
    # for tree sitter we need to convert code into bytes(it only handles the text in form of bytes not as string or anything)
    code_bytes = bytes(code, "utf8")

    # formation of an structured tree
    tree = parser.parse(code_bytes)
    query_string = """
    (function_declaration
        name: (identifier) @function.name) @function.def

    (method_definition
        name: (property_identifier) @function.name) @function.def

    (variable_declarator
        name: (identifier) @function.name
        value: (arrow_function) @function.def)
        
    """
    
    function_query  = Query(parser.language, query_string)
    function_cursor = QueryCursor(function_query)
    function_matches = function_cursor.matches(tree.root_node)
    # query finds only function declaration not classes(method_definition)

    # print(function_matches)

    class_query_string = """
        (class_declaration
            name: (identifier) @class.name) @class.def
    """

    class_query = Query(parser.language, class_query_string)
    class_cursor = QueryCursor(class_query)
    class_matches = class_cursor.matches(tree.root_node)

    classes_info = []

    for match in class_matches:
        captures = match[1]
        class_node = captures["class.def"][0]
        class_name_node = captures["class.name"][0]

        class_name = class_name_node.text.decode("utf8")

        classes_info.append({
            "name": class_name,
            "start": class_node.start_byte,
            "end": class_node.end_byte
        })

        

    # print(class_matches)

    for match in function_matches:
        captures = match[1]
        function_node = captures["function.def"][0]
        name_node = captures["function.name"][0]

        function_name = name_node.text.decode("utf8")    
        # we get this iN form of bytes then decode this to turn this in string format

        function_code = function_node.text.decode("utf8")

        class_name = None
        for cls in classes_info:
            if function_node.start_byte >= cls["start"] and function_node.end_byte <= cls["end"]:
                class_name = cls["name"]
                break

        if class_name is not None:
            final_name = class_name + "." + function_name
        else:
            final_name = function_name

        # print(function_code)
        # print(function_name)

        chunks.append({
            "name": final_name,
            "code": function_code,
            "file": file_path,
            "start_line": function_node.start_point[0] + 1,
            "end_line": function_node.end_point[0] + 1,
        })

    # print(tree.root_node)

    return chunks

    








