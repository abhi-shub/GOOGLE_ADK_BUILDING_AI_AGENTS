import time
import json
from datetime import datetime
from typing import Optional, Dict, Any
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai.types import Content

class CallbackLogger:
    """
    ADK-compliant Callback handler that logs details at each stage of the agent lifecycle.
    """
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        # Store state by invocation ID for tracking execution details like start time
        self.execution_states: Dict[str, Any] = {}

    def log_event(self, invocation_id: str, event_type: str, details: Optional[Dict[str, Any]] = None):
        """Log an event to the log file."""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "invocation_id": invocation_id,
            "event_type": event_type,
            "details": details or {}
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def log_completion(self, invocation_id: Optional[str], final_response_text: str, session_id: str = 'N/A', user_id: str = 'N/A', agent_name: str = 'UnknownAgent'):
        """Fallback method for run_end logging (call from main.py if callback doesn't fire)."""
        if invocation_id is None:
            # Pop the last active state (for demo; assumes single invocation)
            if self.execution_states:
                invocation_id = next(iter(self.execution_states))
                state = self.execution_states.pop(invocation_id)
                session_id = state.get('session_id', session_id)
                user_id = state.get('user_id', user_id)
                agent_name = state.get('agent_name', agent_name)
                start_time = state['start_time']
            else:
                # No state; estimate time as 0
                start_time = time.time()
                invocation_id = 'fallback-' + str(int(time.time()))
        else:
            state = self.execution_states.pop(invocation_id, None)
            start_time = state['start_time'] if state else time.time()
        
        execution_time = time.time() - start_time
        
        self.log_event(invocation_id, "run_end", {
            "user_id": user_id,
            "session_id": session_id,
            "agent_name": agent_name,
            "execution_time_seconds": execution_time,
            "agent_response_length": len(final_response_text),
            "agent_response_preview": final_response_text[:100]
        })
        
        print(f"[Callback] Run end: {invocation_id[:8]}... Time = {execution_time:.2f} seconds")

    # --- Agent Lifecycle Callbacks ---

    async def before_agent_callback(self, callback_context: CallbackContext) -> Optional[Content]:
        """Called before the agent starts processing."""
        invocation_id = callback_context.invocation_id
        session_id = callback_context.session.id if hasattr(callback_context.session, 'id') else 'N/A'
        user_id = callback_context.session.user_id if hasattr(callback_context.session, 'user_id') else 'N/A'
        agent_name = getattr(callback_context, 'agent_name', 'UnknownAgent')
        
        # Initialize execution tracking
        self.execution_states[invocation_id] = {
            "start_time": time.time(),
            "session_id": session_id,
            "user_id": user_id,
            "agent_name": agent_name
        }

        # Extract the user message from user_content in context
        user_message = (
            callback_context.user_content.parts[0].text 
            if hasattr(callback_context, 'user_content') and callback_context.user_content and callback_context.user_content.parts 
            else 'No message found'
        )
        
        self.log_event(invocation_id, "run_start", {
            "user_id": user_id,
            "session_id": session_id,
            "agent_name": agent_name,
            "user_message": user_message
        })
        
        print(f"[Callback] Run start: {invocation_id[:8]}... Message='{user_message[:30]}...'")
        return None  # Proceed normally

    async def after_agent_callback(self, callback_context: CallbackContext, result: Any, **kwargs) -> Optional[Content]:
        """Called after the agent completes processing."""
        invocation_id = callback_context.invocation_id
        state = self.execution_states.pop(invocation_id, None)

        # Extract response (handle Content, Event, or other)
        if isinstance(result, Content):
            agent_response = next((part.text for part in result.parts if hasattr(part, 'text') and part.text), 'No response text')
        elif hasattr(result, 'content') and isinstance(result.content, Content):
            agent_response = next((part.text for part in result.content.parts if hasattr(part, 'text') and part.text), 'No response text')
        else:
            agent_response = str(result)[:100] if result else 'No response'

        if state:
            execution_time = time.time() - state['start_time']
            session_id = state['session_id']
            user_id = state['user_id']
            agent_name = state['agent_name']
            
            self.log_event(invocation_id, "run_end", {
                "user_id": user_id,
                "session_id": session_id,
                "agent_name": agent_name,
                "execution_time_seconds": execution_time,
                "agent_response_length": len(agent_response),
                "agent_response_preview": agent_response[:100]
            })
            
            print(f"[Callback] Run end: {invocation_id[:8]}... Time = {execution_time:.2f} seconds")
        else:
            # Fallback if state missing
            self.log_event(invocation_id, "run_end_fallback", {"note": "No state; agent completed", "kwargs_keys": list(kwargs.keys())})

        return None  # Use the original result
        
    # --- LLM Interaction Callbacks ---
    
    async def before_model_callback(self, callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
        """Called before sending a request to the LLM."""
        invocation_id = callback_context.invocation_id
        agent_name = getattr(callback_context, 'agent_name', 'UnknownAgent')

        # Prompt length: Sum text lengths across all contents
        prompt_length = sum(
            len(part.text or '') for content in llm_request.contents 
            for part in content.parts if hasattr(part, 'text')
        )

        self.log_event(invocation_id, "llm_call", {
            "agent_name": agent_name,
            "prompt_length": prompt_length
        })
        
        print(f"[Callback] LLM call: Agent = {agent_name}, Prompt length = {prompt_length} chars")
        return None

    async def after_model_callback(self, callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
        """Called after receiving a response from the LLM."""
        invocation_id = callback_context.invocation_id
        agent_name = getattr(callback_context, 'agent_name', 'UnknownAgent')
        
        # Response length: Include str() for non-text parts like function calls
        response_length = sum(
            len(str(part)) for part in llm_response.content.parts 
        )

        self.log_event(invocation_id, "llm_response", {
            "agent_name": agent_name,
            "response_length": response_length
        })
        
        print(f"[Callback] LLM response: Agent = {agent_name}, Response length = {response_length} chars")
        return None
        
    # --- Tool Execution Callbacks ---
    
    async def before_tool_callback(self, tool_context: ToolContext, **kwargs) -> Optional[Dict[str, Any]]:
        """Called before executing a tool."""
        invocation_id = tool_context.invocation_id
        agent_name = getattr(tool_context, 'agent_name', 'UnknownAgent')
        tool_input = kwargs.get('args', {})  # ADK passes tool input as 'args' kwarg
        tool = kwargs.get('tool')  # ADK passes tool instance as 'tool' kwarg
        tool_name = getattr(tool, 'name', 'UnknownTool') if tool else 'UnknownTool'

        session_id = tool_context.session.id if hasattr(tool_context.session, 'id') else 'N/A'
        user_id = tool_context.session.user_id if hasattr(tool_context.session, 'user_id') else 'N/A'

        self.log_event(invocation_id, "tool_call", {
            "user_id": user_id,
            "session_id": session_id,
            "agent_name": agent_name,
            "tool_name": tool_name,
            "tool_params": tool_input
        })
        
        print(f"[Callback] Tool call: Agent = {agent_name}, Tool = {tool_name}, Params = {tool_input}")
        return None

    async def after_tool_callback(self, tool_context: ToolContext, **kwargs) -> Optional[Dict[str, Any]]:
        """Called after receiving a response from a tool."""
        invocation_id = tool_context.invocation_id
        agent_name = getattr(tool_context, 'agent_name', 'UnknownAgent')
        # ADK passes raw tool result as 'tool_response' kwarg
        actual_output = kwargs.get('tool_response', {})
        tool = kwargs.get('tool')
        tool_name = getattr(tool, 'name', 'UnknownTool') if tool else 'UnknownTool'

        session_id = tool_context.session.id if hasattr(tool_context.session, 'id') else 'N/A'
        user_id = tool_context.session.user_id if hasattr(tool_context.session, 'user_id') else 'N/A'

        self.log_event(invocation_id, "tool_response", {
            "user_id": user_id,
            "session_id": session_id,
            "agent_name": agent_name,
            "tool_name": tool_name,
            "tool_response_summary": str(actual_output)[:100]
        })
        
        print(f"[Callback] Tool response: Agent = {agent_name}, Tool = {tool_name}, Output preview: {str(actual_output)[:50]}")
        return None