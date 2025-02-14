import ctypes

# Load the Go shared library
lib = ctypes.CDLL('./libhtmlparser.so')

# Define function signatures for Go functions in Python
lib.ParseHTML.argtypes = [ctypes.c_char_p]
lib.ParseHTML.restype = ctypes.c_void_p

lib.GetInnerText.argtypes = [ctypes.c_void_p]
lib.GetInnerText.restype = ctypes.c_char_p

lib.GetFirstChild.argtypes = [ctypes.c_void_p]
lib.GetFirstChild.restype = ctypes.c_void_p

lib.GetNextSibling.argtypes = [ctypes.c_void_p]
lib.GetNextSibling.restype = ctypes.c_void_p

lib.GetParent.argtypes = [ctypes.c_void_p]
lib.GetParent.restype = ctypes.c_void_p

# Node class to wrap pointers and methods in Python
class Node:
    def __init__(self, node_ptr):
        self.node_ptr = node_ptr

    def inner_text(self):
        """Returns the inner text of the node."""
        text = lib.GetInnerText(self.node_ptr)
        return ctypes.cast(text, ctypes.c_char_p).value.decode('utf-8')

    def first_child(self):
        """Returns the first child node, or None if no child exists."""
        child_ptr = lib.GetFirstChild(self.node_ptr)
        return Node(child_ptr) if child_ptr else None

    def next_sibling(self):
        """Returns the next sibling node, or None if no sibling exists."""
        sibling_ptr = lib.GetNextSibling(self.node_ptr)
        return Node(sibling_ptr) if sibling_ptr else None

    def parent(self):
        """Returns the parent node, or None if no parent exists."""
        parent_ptr = lib.GetParent(self.node_ptr)
        return Node(parent_ptr) if parent_ptr else None

# Example usage
HTML_CONTENT = ''' <html>
						<body>
                        	<p>Hello World</p>
                            <p>Another paragraph</p>
                        </body>
                    </html> 
            	'''

root = Node(lib.ParseHTML(HTML_CONTENT.encode('utf-8')))

# Accessing nodes and getting their text
first_child = root.first_child()  # First child of <html>, should be <body>
if first_child:
    #print("First Child Inner Text:", first_child.inner_text())  # Outputs inner text of <body>

    first_para = first_child.first_child()  # First child of <body>, should be <p>Hello World</p>
    if first_para:
        print("First Paragraph Text: ", first_para.inner_text())  # Outputs: "Hello World"

        next_para = first_para.next_sibling()  # Get the next sibling, the second <p>
        if next_para:
            print("Next Paragraph Text: ", next_para.inner_text())  # Outputs: "Another paragraph"
