from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler


class AgentDebugCallback(BaseCallbackHandler):
    """Simple console callback to observe agent/tool execution."""

    def _stamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def on_tool_start(self, serialized, input_str, **kwargs):
        name = serialized.get("name", "unknown_tool")
        print(f"\n[{self._stamp()}] TOOL START -> {name}")
        print(f"[{self._stamp()}] TOOL INPUT -> {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"[{self._stamp()}] TOOL OUTPUT -> {output}")

    def on_tool_error(self, error, **kwargs):
        print(f"[{self._stamp()}] TOOL ERROR -> {error}")

    def on_chain_error(self, error, **kwargs):
        print(f"[{self._stamp()}] AGENT/CHAIN ERROR -> {error}")
