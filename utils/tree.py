from __future__ import annotations

from typing import Callable, Optional
import copy



class Node:
    def __init__(self, value, child) -> None:
        self.value = value
        self.child = child
        self.parent = None
    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__} {{value: {self.value}, child: {self.child}}}"


class ValueNode(Node):
    def __init__(self, value: float) -> None:
        super().__init__(value, None)


class NumberNode(Node):
    def __init__(self, value: float) -> None:
        super().__init__(value, None)


class VariableNode(Node):
    def __init__(self, value: str) -> None:
        super().__init__(value, None)


class OperationNode(Node):
    def __init__(
        self,
        value: Callable[[float, float], float],
        child: list[Node],
    ) -> None:
        super().__init__(value, child)
        for child in self.child:
            child.parent = self


class UnaryOperationNode(Node):
    def __init__(
        self, value: Callable[[float], float], child: NumberNode | VariableNode
    ) -> None:
        super().__init__(value, child)  # type: ignore
        self.child.parent = self


def print_tree(node, indent="", is_last=True):
    """Pretty-print the AST as a tree."""
    branch = "└── " if is_last else "├── "
    print(indent + branch + node_label(node))

    # Prepare indentation for children
    if is_last:
        new_indent = indent + "    "
    else:
        new_indent = indent + "│   "

    # Handle leaf nodes
    if not hasattr(node, "child") or node.child is None:
        return

    # Normalize children into a list
    children = node.child if isinstance(node.child, list) else [node.child]

    # Print children
    for i, child in enumerate(children):
        print_tree(child, new_indent, i == len(children) - 1)


def node_label(node):
    """Return a readable label for each node type."""
    if isinstance(node, ValueNode):
        return f"Value({node.value})"
    if isinstance(node, NumberNode):
        return f"Number({node.value})"
    if isinstance(node, VariableNode):
        return f"Var({node.value})"
    if isinstance(node, UnaryOperationNode):
        return f"UnaryOp({node.value.__name__})"
    if isinstance(node, OperationNode):
        return f"Op({node.value.__name__})"
    return f"Node({node.value})"


class TreeCollapser:
    """TreeCollapser.collapse is part of a class to keep track of state during recursive function calls."""

    def __init__(self) -> None:
        self.seen = []
        self.seen_ref = []
        self.start : OperationNode
        self.iters = 0
    def collapse(
        self, node: Node, previous_level: Optional[Node], first_call: bool = False
    ):
        self.iters+=1
        if node is None:
            print("Reached None node — stopping collapse")
            return None

        print(self.iters, " ", "=========================")

        if first_call:
            self.seen = []
            self.start = node
        print("Current Node: ", node_label(node))
        print_tree(self.start, is_last=False)
        self.seen.append(copy.deepcopy(node))
        self.seen_ref.append(node)

        if not isinstance(node, OperationNode) and first_call:
            raise TypeError("First node must be an operation node")

        print("NODE: ", node)
        print("CHILD: ", node.child)
        print("PREV: ", previous_level)
        if isinstance(node, UnaryOperationNode):
            if not isinstance(node.child, NumberNode):
                return self.collapse(node.child, node)
            result = NumberNode(node.value(node.child.value))
            if previous_level.child == node:
                previous_level.child = result
            else:  # it's a list
                index_of_node = previous_level.child.index(node)
                previous_level.child[index_of_node] = result
            print("SEEN: ", self.seen)
            if len(self.seen) < 3:
                return self.collapse(previous_level, None)
            else:
                # if self.seen[-3].child == previous_level:
                #     self.seen_ref[-3].child = previous_level
                # else:
                #     if self.seen[-3].child[0] == node:
                #         self.seen_ref[-3].child = [previous_level, self.seen[-3].child[1]]
                #     else:
                #         self.seen_ref[-3].child = [self.seen[-3].child[0], previous_level]
                return self.collapse(previous_level, previous_level.parent)
        else:  # is opeation node
            if not isinstance(node.child[0], NumberNode):
                return self.collapse(node.child[0], node)
            if not isinstance(node.child[1], NumberNode):
                return self.collapse(node.child[1], node)
            result = NumberNode(
                node.value(node.child[0].value, node.child[1].value)
            )
            if previous_level is None:
                return result
            print("RESULT: ", result)
            # if not  isinstance(previous_level.child, list):
            #     previous_level.child = result
            #     return self.collapse(previous_level, self.seen[-2])
            if isinstance(previous_level, UnaryOperationNode):
                previous_level.child = node
            else:
                if previous_level.child[0] == node:
                    previous_level.child = [result, previous_level.child[1]]
                else:
                    previous_level.child = [previous_level.child[0], result]
            print(self.seen[-2] == previous_level, "JSJIKDDDDDDDDDDDDDDDDDD")
            return self.collapse(previous_level, previous_level.parent)


beginning = OperationNode(
    (lambda x, y: x + y),
    [
        OperationNode((lambda x, y: x * y), [NumberNode(9), NumberNode(2)]),
        OperationNode(
            (lambda x, y: x * y),
            [
                OperationNode((lambda x, y: x**y), [NumberNode(2), NumberNode(2)]),
                OperationNode(
                    (lambda x, y: x - y),
                    [
                        UnaryOperationNode(lambda x: x ** (1 / 2), NumberNode(233333333333)),
                        NumberNode(2),
                    ],
                ),
            ],
        ),
    ],
)

treeCollapser = TreeCollapser()
print("SKSK: ", treeCollapser.collapse(beginning, previous_level=None, first_call=True))
