"""
Seed the database with sample tasks for testing the concentric circle UI.
"""

from datetime import datetime, timezone, timedelta
import random

from core.models import Node, NodeType, Stage, Quadrant, CognitiveLoad
from core.storage import Repository


def create_sample_tasks(repo: Repository):
    """Create sample tasks across different phases and quadrants."""
    
    sample_tasks = [
        # Backlog tasks
        {
            "title": "Write blog post",
            "type": NodeType.ACTION,
            "stage": Stage.BACKLOG,
            "quadrant": Quadrant.NOT_URGENT_IMPORTANT,
            "load": CognitiveLoad.MEDIUM,
            "desc": "Create content for company blog"
        },
        {
            "title": "Research competitors",
            "type": NodeType.ACTION,
            "stage": Stage.BACKLOG,
            "quadrant": Quadrant.NOT_URGENT_NOT_IMPORTANT,
            "load": CognitiveLoad.LOW,
            "desc": "Analyze market competition"
        },
        
        # Planning tasks
        {
            "title": "Plan Q4 roadmap",
            "type": NodeType.INITIATIVE,
            "stage": Stage.PLANNING,
            "quadrant": Quadrant.URGENT_IMPORTANT,
            "load": CognitiveLoad.HIGH,
            "desc": "Define strategic initiatives for Q4"
        },
        {
            "title": "Design system architecture",
            "type": NodeType.DELIVERABLE,
            "stage": Stage.PLANNING,
            "quadrant": Quadrant.NOT_URGENT_IMPORTANT,
            "load": CognitiveLoad.DEEP,
            "desc": "Create technical architecture document"
        },
        
        # Executing tasks
        {
            "title": "Build MVP feature",
            "type": NodeType.EFFORT,
            "stage": Stage.EXECUTING,
            "quadrant": Quadrant.URGENT_IMPORTANT,
            "load": CognitiveLoad.DEEP,
            "desc": "Implement core functionality"
        },
        {
            "title": "Client presentation",
            "type": NodeType.ACTION,
            "stage": Stage.EXECUTING,
            "quadrant": Quadrant.URGENT_NOT_IMPORTANT,
            "load": CognitiveLoad.MEDIUM,
            "desc": "Prepare slides for client meeting"
        },
        {
            "title": "Code review",
            "type": NodeType.ACTION,
            "stage": Stage.EXECUTING,
            "quadrant": Quadrant.NOT_URGENT_IMPORTANT,
            "load": CognitiveLoad.MEDIUM,
            "desc": "Review pull requests"
        },
        
        # Review/Waiting tasks
        {
            "title": "Wait for API access",
            "type": NodeType.ACTION,
            "stage": Stage.REVIEW,
            "quadrant": Quadrant.URGENT_IMPORTANT,
            "load": CognitiveLoad.LOW,
            "desc": "Blocked until API credentials received"
        },
        {
            "title": "Stakeholder feedback",
            "type": NodeType.ACTION,
            "stage": Stage.REVIEW,
            "quadrant": Quadrant.NOT_URGENT_IMPORTANT,
            "load": CognitiveLoad.LOW,
            "desc": "Awaiting feedback on proposal"
        },
        
        # Acceptance tasks
        {
            "title": "Final QA testing",
            "type": NodeType.ACTION,
            "stage": Stage.ACCEPTANCE,
            "quadrant": Quadrant.URGENT_IMPORTANT,
            "load": CognitiveLoad.HIGH,
            "desc": "Complete acceptance criteria verification"
        },
        {
            "title": "Documentation review",
            "type": NodeType.ACTION,
            "stage": Stage.ACCEPTANCE,
            "quadrant": Quadrant.NOT_URGENT_IMPORTANT,
            "load": CognitiveLoad.MEDIUM,
            "desc": "Review user documentation"
        },
    ]
    
    # Create nodes with varied ages
    now = datetime.now(timezone.utc)
    
    for i, task_data in enumerate(sample_tasks):
        # Vary creation time to show different ages
        days_ago = random.randint(0, 25)
        created_at = now - timedelta(days=days_ago)
        
        node = Node(
            type=task_data["type"],
            title=task_data["title"],
            description=task_data["desc"],
            stage=task_data["stage"],
            quadrant=task_data["quadrant"],
            cognitive_load=task_data["load"],
            last_touched_at=created_at,
            last_progress_at=created_at + timedelta(days=random.randint(1, 5)),
        )
        
        repo.upsert_node(node)
        print(f"Created: {node.title} ({node.stage.value}, {node.quadrant.value})")
    
    # Add one completed task (should not appear in UI)
    completed_node = Node(
        type=NodeType.ACTION,
        title="Completed setup",
        description="Initial project setup",
        stage=Stage.COMPLETED,
        quadrant=Quadrant.NOT_URGENT_IMPORTANT,
        cognitive_load=CognitiveLoad.LOW,
        completed_at=now - timedelta(days=2),
    )
    repo.upsert_node(completed_node)
    print(f"Created: {completed_node.title} (completed - hidden from UI)")
    
    print(f"\nTotal tasks created: {len(sample_tasks) + 1}")


if __name__ == "__main__":
    repo = Repository("data/workos.sqlite3")
    create_sample_tasks(repo)
    print("\nDatabase seeded successfully!")
