//go:build linux
package main

// #include <stdlib.h>
import "C"

import (
	"golang.org/x/net/html"
	"strings"
	"unsafe"
)

// Export ParseHTML function to parse HTML and return the root node's pointer.
//export ParseHTML
func ParseHTML(htmlStr *C.char) uintptr {
	htmlContent := C.GoString(htmlStr)
	node, err := html.Parse(strings.NewReader(htmlContent))
	if err != nil {
		return 0 
	}
	return uintptr(unsafe.Pointer(node)) // Return the root node's address
}

// Export GetInnerText function to retrieve the inner text of a node.
//export GetInnerText
func GetInnerText(nodePtr uintptr) *C.char {
	node := (*html.Node)(unsafe.Pointer(nodePtr))
	var innerText strings.Builder

	// Helper function to recursively collect text
	var collectText func(n *html.Node)
	collectText = func(n *html.Node) {
		if n.Type == html.TextNode {
			innerText.WriteString(n.Data)
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			collectText(c)
		}
	}

	collectText(node)
	return C.CString(innerText.String())
}

// Export GetFirstChild to get the first child of the node.
//export GetFirstChild
func GetFirstChild(nodePtr uintptr) uintptr {
	node := (*html.Node)(unsafe.Pointer(nodePtr))
	if node.FirstChild == nil {
		return 0
	}
	return uintptr(unsafe.Pointer(node.FirstChild))
}

// Export GetNextSibling to get the next sibling of the node.
//export GetNextSibling
func GetNextSibling(nodePtr uintptr) uintptr {
	node := (*html.Node)(unsafe.Pointer(nodePtr))
	if node.NextSibling == nil {
		return 0
	}
	return uintptr(unsafe.Pointer(node.NextSibling))
}

// Export GetParent to get the parent of the node.
//export GetParent
func GetParent(nodePtr uintptr) uintptr {
	node := (*html.Node)(unsafe.Pointer(nodePtr))
	if node.Parent == nil {
		return 0
	}
	return uintptr(unsafe.Pointer(node.Parent))
}

func main() {}
