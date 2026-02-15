from __future__ import annotations

from typing import Callable, Literal, Optional
import copy

class Node:
    def __init__(self, value, child) -> None:
        self.value = value
        self.child = child

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


class UnaryOperationNode(OperationNode):
    def __init__(
        self, value: Callable[[float], float], child: NumberNode | VariableNode
    ) -> None:
        super().__init__(value, child)  # type: ignore


class TreeCollapser:
    """TreeCollapser.collapse is part of a class to keep track of state during recursive function calls.
    """
    def __init__(self) -> None:
        self.seen = []
    def collapse(
        self, node: Node, previous_level: Optional[Node], first_call: bool = False
    ):
        print("=========================")
        if first_call:
            self.seen = []
        self.seen.append(copy.deepcopy(node))
        if node is not OperationNode and first_call:
            raise TypeError("First node must be an operation node")
        print("NODE: ", node)
        print("CHILD: ", node.child)
        print("PREV: ", previous_level)
        if (
            node.child is not None
        ): # only operation nodes have children
            if isinstance(node, UnaryOperationNode):
                result = NumberNode(node.value(node.child.value))
                if previous_level.child == node: 
                    previous_level.child = result
                else: # it's a list
                    print(previous_level.child)
                    index_of_node = previous_level.child.index(node)
                    previous_level.child[index_of_node] = result
                print("SEEN: ", self.seen)
                if len(self.seen) < 3:
                    return self.collapse(previous_level, None)
                else:
                    self.collapse(previous_level, self.seen[-3])
            else:
                if not isinstance(node.child[0], NumberNode):
                    return self.collapse(node.child[0], node)
                if not isinstance(node.child[1], NumberNode):
                    return self.collapse(node.child[1], node)
                else:
                    result = NumberNode(
                        node.value(node.child[0].value, node.child[1].value)
                    )
                    if previous_level is None:
                        print("Skjsk")
                        return result
                    if previous_level.child[0] == node:
                        previous_level.child = [result, previous_level.child[1]]
                        return self.collapse(previous_level, self.seen[-2])
                    else:
                        previous_level.child = [previous_level.child[0], result]
                    return self.collapse(previous_level, self.seen[-2])
        elif node is VariableNode:
            raise TypeError(f"Cannot evaluate variable node: {node} of unknown value")
        else:
            pass


beginning = OperationNode(
    (lambda x, y: x + y),
    [NumberNode(9), UnaryOperationNode(lambda x: x**0.5, NumberNode(64))],
)

treeCollapser = TreeCollapser()
print("SKSK: ", treeCollapser.collapse(beginning, previous_level=None))
