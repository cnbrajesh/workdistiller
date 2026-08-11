from core.models import Node, NodeType, Stage


def test_node_creation():
    node = Node(
        type=NodeType.ACTION,
        title="Test action",
    )

    assert node.type == NodeType.ACTION
    assert node.stage == Stage.BACKLOG
    assert node.progress == 0.0
    assert node.postpone_count == 0
