from google.adk import Agent
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Category(str, Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    ACCOUNT = "account"
    GENERAL = "general"

class SupportTicket(BaseModel):
    title: str = Field(description="A concise summary of the issue")
    description: str = Field(description="Detailed description of the problem")
    priority: Priority = Field(description="The ticket priority level")
    category: Category = Field(description="The department this ticket belongs to")
    steps_to_reproduce: Optional[List[str]] = Field(
        description="Steps to reproduce the issue (for technical problems)",
        default=None
    )
    customer_contact: Optional[str] = Field(
        description="Customer's preferred contact method",
        default=None
    )

ticket_agent = Agent(
    name="ticket_agent",
    model="gemini-2.5-flash-lite",
    description="A support ticket creation assistant",
    instruction="""
    You are a support ticket creation assistant. You help users create well-structured support tickets from their issues.
    
    For each ticket request:
    1. Extract the key issue from the user's description
    2. Create a concise but descriptive title
    3. Format a detailed description
    4. Determine the appropriate priority level and category
    5. For technical issues, list steps to reproduce
    6. Include customer contact information if provided
    
    IMPORTANT: Return your response as a JSON object matching this structure:
    {
        "title": "Brief issue summary",
        "description": "Detailed issue description",
        "priority": "low|medium|high|critical",
        "category": "technical|billing|account|general",
        "steps_to_reproduce": ["Step 1", "Step 2", ...] (optional),
        "customer_contact": "Contact information" (optional)
    }
    """,
    output_schema=SupportTicket,
    output_key="ticket"
)

root_agent = ticket_agent

