from google.adk import Agent
from pydantic import BaseModel

class EmailContent(BaseModel):
    subject: str
    body: str

email_agent = Agent(
    name= "email_agent", 
    model= "gemini-2.5-flash-lite",
    description= "An email generation assistant",
    instruction= """
    You are an email generation assistant. You always write professional emails based on the user's request.
    
    Guidelines for writing emails:
    1. Create a concise and relevant subject line
    2. Write a professional email body with a greeting, clear message, and appropriate closing
    3. Keep the tone business-friendly and formal
    4. Be concise but complete
    
    IMPORTANT: Always return your response as a JSON object with the following structure:
    {
        "subject": "The email subject line",
        "body": "The full email body"
    }
    """,
    output_schema= EmailContent,
    output_key= "email"
)

root_agent = email_agent

