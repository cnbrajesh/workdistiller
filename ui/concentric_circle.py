"""
Rich Concentric Circle UI for WorkOS MVP

This module provides a PyQt5-based radial visualization of tasks organized by:
- Phases (concentric rings): Backlog, Planning Review, Executing, Waiting for inputs, Acceptance Review, Completed
- Priority wedges (Eisenhower Matrix quadrants): Urgent/Important combinations
- Bubble size: Linear mapping to complexity number
- Task age: Shown via progress ring around bubble

Completed tasks disappear from the visualization.
"""

from __future__ import annotations

import math
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from PyQt5.QtCore import (
    QPointF, QRectF, Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
)
from PyQt5.QtGui import (
    QColor, QFont, QPainter, QPen, QBrush, QPalette, QWheelEvent, QMouseEvent
)
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsObject,
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFrame,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QSlider, QGroupBox, QFormLayout, QScrollArea, QToolBar,
    QAction, QMenu, QSystemTrayIcon, QDialog, QDialogButtonBox
)

from core.models import Node, Stage, Quadrant, NodeType, CognitiveLoad
from core.storage import Repository


# ============================================================================
# Configuration Constants
# ============================================================================

PHASES = [
    Stage.BACKLOG,
    Stage.PLANNING,
    Stage.EXECUTING,
    Stage.REVIEW,  # "Waiting for inputs" maps to review stage
    Stage.ACCEPTANCE,  # Will add this to models
    Stage.COMPLETED,
]

# Eisenhower Matrix quadrants (4 wedges)
QUADRANTS = [
    Quadrant.URGENT_IMPORTANT,
    Quadrant.NOT_URGENT_IMPORTANT,
    Quadrant.URGENT_NOT_IMPORTANT,
    Quadrant.NOT_URGENT_NOT_IMPORTANT,
]

# Visual configuration
MIN_RING_RADIUS = 80
RING_SPACING = 70
MAX_COMPLEXITY = 10
MIN_BUBBLE_RADIUS = 15
MAX_BUBBLE_RADIUS = 60
WEDGE_COUNT = 4  # Eisenhower quadrants

# Color scheme
PHASE_COLORS = {
    Stage.BACKLOG: QColor(128, 128, 128, 180),  # Gray
    Stage.PLANNING: QColor(52, 152, 219, 180),  # Blue
    Stage.EXECUTING: QColor(46, 204, 113, 180),  # Green
    Stage.REVIEW: QColor(241, 196, 15, 180),  # Yellow
    Stage.ACCEPTANCE: QColor(155, 89, 182, 180),  # Purple
    Stage.COMPLETED: QColor(39, 174, 96, 180),  # Dark Green
}

QUADRANT_COLORS = {
    Quadrant.URGENT_IMPORTANT: QColor(231, 76, 60, 100),  # Red
    Quadrant.NOT_URGENT_IMPORTANT: QColor(52, 152, 219, 100),  # Blue
    Quadrant.URGENT_NOT_IMPORTANT: QColor(243, 156, 18, 100),  # Orange
    Quadrant.NOT_URGENT_NOT_IMPORTANT: QColor(149, 165, 166, 100),  # Gray
}

COMPLEXITY_COLOR_SCALE = [
    QColor(46, 204, 113),  # Low complexity - Green
    QColor(241, 196, 15),  # Medium - Yellow
    QColor(230, 126, 34),  # High - Orange
    QColor(192, 57, 43),   # Very high - Red
]


# ============================================================================
# Helper Functions
# ============================================================================

def get_complexity_score(node: Node) -> float:
    """Extract complexity score from node's cognitive load or other attributes."""
    # Map cognitive load to numeric complexity
    load_map = {
        CognitiveLoad.LOW: 2.0,
        CognitiveLoad.MEDIUM: 5.0,
        CognitiveLoad.HIGH: 7.5,
        CognitiveLoad.DEEP: 10.0,
    }
    return load_map.get(node.cognitive_load, 5.0)


def polar_to_cartesian(center_x: float, center_y: float, radius: float, angle_degrees: float) -> QPointF:
    """Convert polar coordinates to Cartesian."""
    angle_radians = math.radians(angle_degrees - 90)  # -90 to start from top
    x = center_x + radius * math.cos(angle_radians)
    y = center_y + radius * math.sin(angle_radians)
    return QPointF(x, y)


def get_quadrant_angle_range(quadrant: Quadrant, wedge_count: int = 4) -> Tuple[float, float]:
    """Get the start and end angles for a quadrant."""
    # Eisenhower matrix layout:
    # Q1 (Urgent+Important): Top-right (0° to 90°)
    # Q2 (Not Urgent+Important): Bottom-right (90° to 180°)
    # Q3 (Urgent+Not Important): Top-left (270° to 360°)
    # Q4 (Not Urgent+Not Important): Bottom-left (180° to 270°)
    
    ranges = {
        Quadrant.URGENT_IMPORTANT: (0, 90),
        Quadrant.NOT_URGENT_IMPORTANT: (90, 180),
        Quadrant.NOT_URGENT_NOT_IMPORTANT: (180, 270),
        Quadrant.URGENT_NOT_IMPORTANT: (270, 360),
    }
    return ranges.get(quadrant, (0, 90))


def calculate_bubble_radius(complexity: float, min_radius: float = MIN_BUBBLE_RADIUS, 
                           max_radius: float = MAX_BUBBLE_RADIUS, 
                           max_complexity: float = MAX_COMPLEXITY) -> float:
    """Calculate bubble radius based on complexity (linear scaling)."""
    normalized = min(max(complexity / max_complexity, 0.0), 1.0)
    return min_radius + (max_radius - min_radius) * normalized


def get_task_age_days(node: Node) -> float:
    """Calculate task age in days."""
    now = datetime.now(timezone.utc)
    created = node.last_touched_at or now
    delta = now - created
    return delta.total_seconds() / 86400.0  # Convert to days


def get_progress_from_age(age_days: float, max_age: float = 30.0) -> float:
    """Convert task age to progress value (0.0 to 1.0)."""
    return min(age_days / max_age, 1.0)


# ============================================================================
# Graphics Items
# ============================================================================

class PhaseRing(QGraphicsItem):
    """Represents a concentric ring for a phase."""
    
    def __init__(self, inner_radius: float, outer_radius: float, 
                 phase: Stage, parent=None):
        super().__init__(parent)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.phase = phase
        self.setZValue(-2)
        
    def boundingRect(self) -> QRectF:
        return QRectF(-self.outer_radius, -self.outer_radius,
                     self.outer_radius * 2, self.outer_radius * 2)
    
    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw ring background
        color = PHASE_COLORS.get(self.phase, QColor(128, 128, 128, 100))
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        
        # Draw annulus (ring)
        path = painter.path()
        path.addEllipse(QRectF(-self.outer_radius, -self.outer_radius,
                              self.outer_radius * 2, self.outer_radius * 2))
        path.addEllipse(QRectF(-self.inner_radius, -self.inner_radius,
                              self.inner_radius * 2, self.inner_radius * 2))
        painter.drawPath(path)
        
        # Draw phase label
        painter.setPen(QColor(255, 255, 255, 200))
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)
        label_y = -(self.inner_radius + self.outer_radius) / 2
        painter.drawText(QRectF(-self.outer_radius, label_y - 10,
                               self.outer_radius * 2, 20),
                        Qt.AlignCenter, self.phase.value.replace('_', ' ').title())


class QuadrantWedge(QGraphicsItem):
    """Represents a priority wedge (quadrant)."""
    
    def __init__(self, start_angle: float, span_angle: float, 
                 quadrant: Quadrant, max_radius: float, parent=None):
        super().__init__(parent)
        self.start_angle = start_angle
        self.span_angle = span_angle
        self.quadrant = quadrant
        self.max_radius = max_radius
        self.setZValue(-1)
        
    def boundingRect(self) -> QRectF:
        return QRectF(-self.max_radius, -self.max_radius,
                     self.max_radius * 2, self.max_radius * 2)
    
    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw wedge background
        color = QUADRANT_COLORS.get(self.quadrant, QColor(128, 128, 128, 50))
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        
        # Draw pie slice
        painter.drawPie(QRectF(-self.max_radius, -self.max_radius,
                              self.max_radius * 2, self.max_radius * 2),
                       int(self.start_angle * 16),
                       int(self.span_angle * 16))
        
        # Draw quadrant label
        painter.setPen(QColor(255, 255, 255, 180))
        font = QFont("Arial", 9, QFont.Bold)
        painter.setFont(font)
        
        mid_angle = self.start_angle + self.span_angle / 2
        label_radius = self.max_radius * 0.7
        label_pos = polar_to_cartesian(0, 0, label_radius, mid_angle)
        
        label_text = {
            Quadrant.URGENT_IMPORTANT: "Q1\nUrgent &\nImportant",
            Quadrant.NOT_URGENT_IMPORTANT: "Q2\nImportant\nNot Urgent",
            Quadrant.URGENT_NOT_IMPORTANT: "Q3\nUrgent\nNot Important",
            Quadrant.NOT_URGENT_NOT_IMPORTANT: "Q4\nNot Urgent\nNot Important",
        }.get(self.quadrant, "")
        
        painter.drawText(int(label_pos.x() - 40), int(label_pos.y() - 30), 80, 60,
                        Qt.AlignCenter, label_text)


class TaskBubble(QGraphicsObject):
    """Represents a task as a bubble in the radial grid."""
    
    clicked = pyqtSignal(object)  # Emits the node when clicked
    
    def __init__(self, node: Node, phase_index: int, quadrant: Quadrant,
                 inner_radius: float, outer_radius: float,
                 start_angle: float, span_angle: float, parent=None):
        super().__init__(parent)
        self.node = node
        self.phase_index = phase_index
        self.quadrant = quadrant
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.span_angle = span_angle
        
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        
        self.complexity = get_complexity_score(node)
        self.radius = calculate_bubble_radius(self.complexity)
        self.target_pos = self._calculate_position()
        self.setPos(self.target_pos)
        
        self.hovered = False
        self.age_progress = get_progress_from_age(get_task_age_days(node))
        
    def _calculate_position(self) -> QPointF:
        """Calculate position within the sector."""
        # Radial position: middle of the ring
        radial_pos = (self.inner_radius + self.outer_radius) / 2
        
        # Angular position: middle of the wedge
        angular_pos = self.start_angle + self.span_angle / 2
        
        return polar_to_cartesian(0, 0, radial_pos, angular_pos)
    
    def boundingRect(self) -> QRectF:
        margin = 2
        return QRectF(-self.radius - margin, -self.radius - margin,
                     (self.radius + margin) * 2, (self.radius + margin) * 2)
    
    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Main bubble color based on complexity
        color_index = min(int(self.complexity / (MAX_COMPLEXITY / len(COMPLEXITY_COLOR_SCALE))),
                         len(COMPLEXITY_COLOR_SCALE) - 1)
        base_color = COMPLEXITY_COLOR_SCALE[color_index]
        
        if self.hovered:
            base_color = base_color.lighter(120)
        
        # Draw progress ring (age indicator)
        if self.age_progress > 0:
            pen = QPen(base_color.darker(150), 3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            # Draw full circle background
            painter.drawEllipse(QPointF(0, 0), self.radius, self.radius)
            
            # Draw progress arc
            span_angle = int(-self.age_progress * 360 * 16)  # Negative for clockwise
            painter.drawArc(QRectF(-self.radius, -self.radius,
                                  self.radius * 2, self.radius * 2),
                           90 * 16, span_angle)
        
        # Draw main bubble
        painter.setBrush(QBrush(base_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(0, 0), self.radius - 2, self.radius - 2)
        
        # Draw title (truncated if needed)
        painter.setPen(QColor(255, 255, 255, 255) if self.hovered else QColor(0, 0, 0, 200))
        font = QFont("Arial", 8, QFont.Bold if self.hovered else QFont.Normal)
        painter.setFont(font)
        
        title = self.node.title
        if len(title) > 15:
            title = title[:12] + "..."
        
        painter.drawText(QRectF(-self.radius, -self.radius,
                               self.radius * 2, self.radius * 2),
                        Qt.AlignCenter, title)
    
    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()
        super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.node)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        # Check if dropped in a new sector
        pos = self.pos()
        distance = math.sqrt(pos.x()**2 + pos.y()**2)
        angle = math.degrees(math.atan2(pos.y(), pos.x())) + 90
        if angle < 0:
            angle += 360
        
        # Determine new phase and quadrant
        new_phase_index = int((distance - MIN_RING_RADIUS) / RING_SPACING)
        new_phase_index = max(0, min(new_phase_index, len(PHASES) - 2))  # Exclude completed
        
        quadrant_angles = [(0, 90), (90, 180), (180, 270), (270, 360)]
        new_quadrant = None
        for i, (start, end) in enumerate(quadrant_angles):
            if start <= angle < end:
                new_quadrant = QUADRANTS[i]
                break
        
        if new_quadrant and (new_phase_index != self.phase_index or new_quadrant != self.quadrant):
            # Update node
            self.node.stage = PHASES[new_phase_index]
            self.node.quadrant = new_quadrant
            
            # Emit signal for external handling
            self.clicked.emit(self.node)
        
        super().mouseReleaseEvent(event)


class RadialGridScene(QGraphicsScene):
    """Main scene containing the radial grid and tasks."""
    
    task_clicked = pyqtSignal(object)
    task_moved = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-500, -500, 1000, 1000)
        self.setBackgroundBrush(QColor(30, 30, 30))
        
        self.nodes: Dict[str, TaskBubble] = {}
        self.repository: Optional[Repository] = None
        
        self._draw_grid()
        
    def set_repository(self, repo: Repository):
        self.repository = repo
        self.refresh()
    
    def _draw_grid(self):
        """Draw the concentric rings and wedges."""
        # Draw phase rings
        for i, phase in enumerate(PHASES[:-1]):  # Exclude completed
            inner_r = MIN_RING_RADIUS + i * RING_SPACING
            outer_r = inner_r + RING_SPACING
            ring = PhaseRing(inner_r, outer_r, phase)
            ring.setPos(0, 0)
            self.addItem(ring)
        
        # Draw quadrant wedges
        max_radius = MIN_RING_RADIUS + (len(PHASES) - 1) * RING_SPACING
        for i, quadrant in enumerate(QUADRANTS):
            start_angle = i * 90
            wedge = QuadrantWedge(start_angle, 90, quadrant, max_radius)
            wedge.setPos(0, 0)
            self.addItem(wedge)
    
    def refresh(self):
        """Reload all nodes from repository."""
        if not self.repository:
            return
        
        # Remove existing bubbles
        for bubble in list(self.nodes.values()):
            self.removeItem(bubble)
        self.nodes.clear()
        
        # Load nodes and create bubbles
        all_nodes = self.repository.all_nodes()
        
        for node in all_nodes:
            # Skip completed tasks
            if node.stage == Stage.COMPLETED:
                continue
            
            # Find phase index
            try:
                phase_index = PHASES.index(node.stage)
            except ValueError:
                phase_index = 0
            
            # Get quadrant angles
            start_angle, span_angle = get_quadrant_angle_range(node.quadrant)
            
            # Calculate ring radii
            inner_r = MIN_RING_RADIUS + phase_index * RING_SPACING
            outer_r = inner_r + RING_SPACING
            
            # Create bubble
            bubble = TaskBubble(
                node, phase_index, node.quadrant,
                inner_r, outer_r, start_angle, span_angle
            )
            bubble.clicked.connect(self._on_task_clicked)
            self.nodes[node.id] = bubble
            self.addItem(bubble)
    
    def _on_task_clicked(self, node: Node):
        """Handle task click - save changes and emit signal."""
        if self.repository:
            self.repository.upsert_node(node)
        self.task_clicked.emit(node)


# ============================================================================
# Side Panel Editor
# ============================================================================

class TaskEditorPanel(QWidget):
    """Side panel for editing task details."""
    
    task_saved = pyqtSignal(str)  # Emits node ID when saved
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_node: Optional[Node] = None
        self.repository: Optional[Repository] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("Task Details")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(title_label)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(8)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Title field
        self.title_edit = QLineEdit()
        self.title_edit.setStyleSheet("""
            QLineEdit {
                background: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        form_layout.addRow("Title:", self.title_edit)
        
        # Description field
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        self.desc_edit.setStyleSheet("""
            QTextEdit {
                background: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        form_layout.addRow("Description:", self.desc_edit)
        
        # Stage combo
        self.stage_combo = QComboBox()
        for stage in PHASES[:-1]:  # Exclude completed
            self.stage_combo.addItem(stage.value.replace('_', ' ').title(), stage.value)
        self.stage_combo.setStyleSheet("""
            QComboBox {
                background: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        form_layout.addRow("Phase:", self.stage_combo)
        
        # Quadrant combo
        self.quadrant_combo = QComboBox()
        for quad in QUADRANTS:
            display = quad.value.replace('_', ' ').title()
            self.quadrant_combo.addItem(display, quad.value)
        self.quadrant_combo.setStyleSheet("""
            QComboBox {
                background: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        form_layout.addRow("Priority:", self.quadrant_combo)
        
        # Cognitive load combo
        self.load_combo = QComboBox()
        for load in CognitiveLoad:
            self.load_combo.addItem(load.value.title(), load.value)
        self.load_combo.setStyleSheet("""
            QComboBox {
                background: #2a2a2a;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        form_layout.addRow("Cognitive Load:", self.load_combo)
        
        # Complexity slider
        self.complexity_slider = QSlider(Qt.Horizontal)
        self.complexity_slider.setMinimum(1)
        self.complexity_slider.setMaximum(10)
        self.complexity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #444;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        self.complexity_value_label = QLabel("5")
        self.complexity_value_label.setStyleSheet("color: white; min-width: 20px;")
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(self.complexity_slider)
        complexity_layout.addWidget(self.complexity_value_label)
        form_layout.addRow("Complexity:", complexity_layout)
        
        # Save button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:pressed {
                background: #1f618d;
            }
        """)
        self.save_btn.clicked.connect(self._save_changes)
        layout.addWidget(self.save_btn)
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # Connect slider to label
        self.complexity_slider.valueChanged.connect(
            lambda v: self.complexity_value_label.setText(str(v))
        )
        
        self.setStyleSheet("""
            QWidget {
                background: #1e1e1e;
            }
        """)
    
    def set_repository(self, repo: Repository):
        self.repository = repo
    
    def load_node(self, node: Node):
        """Load node data into the editor."""
        self.current_node = node
        
        self.title_edit.setText(node.title)
        self.desc_edit.setText(node.description)
        
        # Set stage
        for i in range(self.stage_combo.count()):
            if self.stage_combo.itemData(i) == node.stage.value:
                self.stage_combo.setCurrentIndex(i)
                break
        
        # Set quadrant
        for i in range(self.quadrant_combo.count()):
            if self.quadrant_combo.itemData(i) == node.quadrant.value:
                self.quadrant_combo.setCurrentIndex(i)
                break
        
        # Set cognitive load
        for i in range(self.load_combo.count()):
            if self.load_combo.itemData(i) == node.cognitive_load.value:
                self.load_combo.setCurrentIndex(i)
                break
        
        # Set complexity (map from cognitive load)
        complexity = int(get_complexity_score(node))
        self.complexity_slider.setValue(complexity)
    
    def _save_changes(self):
        """Save changes back to repository."""
        if not self.current_node or not self.repository:
            return
        
        # Update node
        self.current_node.title = self.title_edit.text()
        self.current_node.description = self.desc_edit.toPlainText()
        
        stage_value = self.stage_combo.currentData()
        for stage in PHASES:
            if stage.value == stage_value:
                self.current_node.stage = stage
                break
        
        quadrant_value = self.quadrant_combo.currentData()
        for quad in QUADRANTS:
            if quad.value == quadrant_value:
                self.current_node.quadrant = quad
                break
        
        load_value = self.load_combo.currentData()
        for load in CognitiveLoad:
            if load.value == load_value:
                self.current_node.cognitive_load = load
                break
        
        # Save to repository
        self.repository.upsert_node(self.current_node)
        self.task_saved.emit(self.current_node.id)


# ============================================================================
# Panchangam Widget (Phase 2 placeholder)
# ============================================================================

class PanchangamWidget(QDialog):
    """Simple Panchangam display dialog (Phase 2 feature)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Daily Panchangam")
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🕉️ Daily Panchangam")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #f39c12; padding: 10px;")
        layout.addWidget(title)
        
        # Placeholder content
        info = QLabel(
            "<h3>Today's Details</h3>"
            "<p><b>Tithi:</b> Calculated locally</p>"
            "<p><b>Vara:</b> Day of week</p>"
            "<p><b>Nakshatra:</b> Lunar mansion</p>"
            "<p><b>Rahu Kala:</b> Inauspicious time</p>"
            "<p><b>Amruta Kala:</b> Auspicious time</p>"
            "<hr>"
            "<p><i>Note: Full offline calculation will be implemented in Phase 2.</i></p>"
        )
        info.setStyleSheet("color: white; padding: 10px; line-height: 1.6;")
        layout.addWidget(info)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setStyleSheet("background: #1e1e1e;")


# ============================================================================
# Main Application Window
# ============================================================================

class WorkOSMainWindow(QWidget):
    """Main application window."""
    
    def __init__(self, db_path: str = "data/workos.sqlite3"):
        super().__init__()
        self.repository = Repository(db_path)
        self.setWindowTitle("WorkOS - Concentric Circle UI")
        self.setMinimumSize(1200, 800)
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Radial visualization
        self.scene = RadialGridScene()
        self.scene.set_repository(self.repository)
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setStyleSheet("""
            QGraphicsView {
                background: #1a1a1a;
                border: none;
            }
        """)
        
        # Add toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setStyleSheet("""
            QToolBar {
                background: #2a2a2a;
                border: none;
                padding: 5px;
            }
            QToolButton {
                background: transparent;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QToolButton:hover {
                background: #3498db;
            }
        """)
        
        # Panchangam action
        panchangam_action = QAction("🕉️ Panchangam", self)
        panchangam_action.triggered.connect(self._show_panchangam)
        toolbar.addAction(panchangam_action)
        
        toolbar.addSeparator()
        
        # Refresh action
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.scene.refresh)
        toolbar.addAction(refresh_action)
        
        # Layout for view with toolbar
        view_container = QWidget()
        view_layout = QVBoxLayout(view_container)
        view_layout.setContentsMargins(0, 0, 0, 0)
        view_layout.setSpacing(0)
        view_layout.addWidget(toolbar)
        view_layout.addWidget(self.view)
        
        splitter.addWidget(view_container)
        
        # Right: Task editor panel
        self.editor = TaskEditorPanel()
        self.editor.set_repository(self.repository)
        self.editor.setMinimumWidth(300)
        self.editor.setMaximumWidth(400)
        splitter.addWidget(self.editor)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        
        main_layout.addWidget(splitter)
        
        self.setStyleSheet("""
            QWidget {
                background: #1e1e1e;
            }
        """)
    
    def _connect_signals(self):
        self.scene.task_clicked.connect(self.editor.load_node)
        self.editor.task_saved.connect(lambda: self.scene.refresh())
    
    def _show_panchangam(self):
        dialog = PanchangamWidget(self)
        dialog.exec_()


# ============================================================================
# Entry Point
# ============================================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(42, 42, 42))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, Qt.black)
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    window = WorkOSMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
