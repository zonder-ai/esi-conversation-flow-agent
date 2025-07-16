"""
Configuration management for ESI Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for ESI Conversation Flow Agent"""
    
    # API Configuration
    RETELL_API_KEY = os.getenv("RETELL_API_KEY")
    AGENT_NAME = os.getenv("AGENT_NAME", "ESI Design School Agent")
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://n8n.zonder.ai/webhook/retell-zonder-esi")
    
    # ESI Specific Settings
    CUSTOM_VOICE_ID = "custom_voice_6105206ed083e6faf35d86f533"
    LANGUAGE = "es-ES"
    MAX_CALL_DURATION_MS = 3600000
    INTERRUPTION_SENSITIVITY = 0.9
    
    # Specialist Emails
    ONLINE_SPECIALISTS = [
        "caridadfrutos@laescueladediseno.com",
        "vanessacalvo@laescueladediseno.com",
        "martagutierrez@laescueladediseno.com"
    ]
    
    PRIVATE_SPECIALISTS = [
        "caridadfrutos@laescueladediseno.com",
        "vanessacalvo@laescueladediseno.com"
    ]
    
    BEA_EMAIL = "bea@laescueladediseno.com"
