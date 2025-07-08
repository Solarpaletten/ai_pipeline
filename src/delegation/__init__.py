"""
Level 7: Inter-Agent Delegation System
Модульная система делегирования задач между AI агентами
"""
__version__ = "1.0.0"
__level__ = 7

from .engine.delegation_engine import DelegationEngine
from .orchestrator.workflow_orchestrator import WorkflowOrchestrator
from .monitoring.delegation_monitor import DelegationMonitor

__all__ = ["DelegationEngine", "WorkflowOrchestrator", "DelegationMonitor"]
