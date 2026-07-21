from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class WorkflowNode:
    id: str
    label: str
    agent: str
    description: str = ""


@dataclass
class WorkflowGraph:
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    edges: List[tuple[str, str]] = field(default_factory=list)

    def add_node(self, node_id: str, label: str, agent: str, description: str = "") -> None:
        self.nodes[node_id] = WorkflowNode(node_id, label, agent, description)

    def add_edge(self, from_id: str, to_id: str) -> None:
        if from_id in self.nodes and to_id in self.nodes:
            self.edges.append((from_id, to_id))

    def to_dict(self) -> Dict[str, object]:
        return {
            "nodes": [{"id": n.id, "label": n.label, "agent": n.agent, "description": n.description} for n in self.nodes.values()],
            "edges": [{"from": s, "to": t} for s, t in self.edges],
        }

    def render_html(self) -> str:
        lines = ["<div style='background:#0f172a;border:1px solid rgba(255,255,255,0.08);padding:1rem;border-radius:16px;'>"]
        lines.append("<h3 style='color:#ffffff;margin-bottom:0.75rem;'>Agent Workflow Graph</h3>")
        lines.append("<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0.75rem;'>")
        for node in self.nodes.values():
            lines.append(
                f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.05);padding:1rem;border-radius:14px;'>"
                f"<div style='font-size:0.8rem;color:#94a3b8;margin-bottom:0.5rem;'>{node.agent}</div>"
                f"<div style='font-weight:700;color:#ffffff;margin-bottom:0.4rem;'>{node.label}</div>"
                f"<div style='font-size:0.78rem;color:#cbd5e1;'>{node.description}</div>"
                "</div>"
            )
        lines.append("</div>")
        if self.edges:
            lines.append("<div style='color:#94a3b8;margin-top:1rem;font-size:0.8rem;'>Workflow transitions:</div>")
            for source, target in self.edges:
                lines.append(
                    f"<div style='color:#cbd5e1;font-size:0.8rem;'>• {self.nodes[source].label} → {self.nodes[target].label}</div>"
                )
        lines.append("</div>")
        return "\n".join(lines)
