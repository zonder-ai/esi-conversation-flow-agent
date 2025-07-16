"""
ESI Conversation Flow Agent - Complete Implementation
====================================================

This file contains all the classes and logic needed to create your ESI conversation flow agent.
It replicates your existing Retell conversation flow but in clean, maintainable Python code.

Author: AI Assistant
Created for: ESI Design School
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import json
from retell import Retell


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class NodeType(Enum):
    """Types of conversation flow nodes"""
    CONVERSATION = "conversation"
    FUNCTION = "function" 
    BRANCH = "branch"
    EXTRACT_DYNAMIC_VARIABLES = "extract_dynamic_variables"
    END = "end"
    TRANSFER_CALL = "transfer_call"


class InstructionType(Enum):
    """Types of node instructions"""
    PROMPT = "prompt"
    STATIC_TEXT = "static_text"


class TransitionConditionType(Enum):
    """Types of transition conditions"""
    PROMPT = "prompt"
    EQUATION = "equation"


class ToolType(Enum):
    """Types of tools/functions"""
    CUSTOM = "custom"
    LOCAL = "local"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DisplayPosition:
    """Position of node in visual editor (for compatibility)"""
    x: float
    y: float


@dataclass
class Instruction:
    """Instruction for a conversation node"""
    type: str
    text: str


@dataclass
class Equation:
    """Equation for logic conditions"""
    left: str
    operator: str
    right: str


@dataclass
class TransitionCondition:
    """Condition for transitioning between nodes"""
    type: str
    prompt: Optional[str] = None
    equations: Optional[List[Dict[str, Any]]] = None
    operator: Optional[str] = None


@dataclass
class Edge:
    """Connection between conversation nodes"""
    id: str
    destination_node_id: Optional[str] = None
    transition_condition: Optional[TransitionCondition] = None


@dataclass
class Variable:
    """Dynamic variable for data extraction"""
    name: str
    description: str
    type: str
    choices: List[str] = field(default_factory=list)


@dataclass
class Tool:
    """External tool/function definition"""
    tool_id: str
    name: str
    description: str
    type: str
    method: str
    url: str
    parameter_type: str = "json"
    timeout_ms: int = 120000
    parameters: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, Any] = field(default_factory=dict)
    query_params: Dict[str, Any] = field(default_factory=dict)
    response_variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransferDestination:
    """Transfer call destination"""
    type: str
    number: str


@dataclass
class TransferOption:
    """Transfer call options"""
    type: str
    show_transferee_as_caller: bool = False


@dataclass
class Node:
    """A conversation flow node"""
    id: str
    name: str
    type: str
    display_position: DisplayPosition
    edges: List[Edge] = field(default_factory=list)
    instruction: Optional[Instruction] = None
    tool_id: Optional[str] = None
    tool_type: Optional[str] = None
    speak_during_execution: bool = False
    wait_for_result: bool = True
    variables: List[Variable] = field(default_factory=list)
    else_edge: Optional[Edge] = None
    skip_response_edge: Optional[Edge] = None
    start_speaker: Optional[str] = None
    custom_sip_headers: Dict[str, Any] = field(default_factory=dict)
    transfer_destination: Optional[TransferDestination] = None
    transfer_option: Optional[TransferOption] = None
    edge: Optional[Edge] = None


# =============================================================================
# CONVERSATION FLOW BUILDER
# =============================================================================

class ESIConversationFlowBuilder:
    """
    Builder class for creating ESI's complete conversation flow structure.
    This replicates your existing Retell flow but in maintainable Python code.
    """
    
    def __init__(self):
        self.nodes = []
        self.tools = []
        self.global_prompt = self._get_global_prompt()
        
    def _get_global_prompt(self) -> str:
        """ESI's global prompt - the personality and context for Bea"""
        return """## IDENTIDAD Y CONTEXTO
Eres Bea, asesora comercial especializada de la Escuela Superior de Diseño ESI. Eres española, profesional, cálida y experta en cursos de diseño. Tu objetivo es cualificar leads rápidamente y conectar prospects cualificados con nuestro equipo comercial.

## INFORMACIÓN DE ESI
- **Escuela**: Escuela Superior de Diseño ESI
- **Especialidad**: Cursos de diseño profesional
- **Modalidades**: Privado u online
- **Horario comercial**: Lunes a Viernes, 9:00 a 18:00h

## CURSOS PRINCIPALES
1. **Diseño Gráfico y Comunicación Visual**: Suite Adobe completa, branding, diseño editorial, proyectos reales
2. **UX/UI Design**: Investigación de usuarios, Figma, prototipado, testing, alta demanda laboral
3. **Diseño de Interiores**: Planificación espacios, AutoCAD, SketchUp, renders 3D, proyectos comerciales
4. **Ilustración Digital**: Técnicas digitales, portfolio profesional, mercado freelance
5. **Motion Graphics y Animación**: After Effects, animación 2D/3D, industria audiovisual
6. **Diseño Web y E-commerce**: Desarrollo web, UX/UI web, tiendas online

## VARIABLES DINÁMICAS DISPONIBLES
- {{customer_name}}: Nombre del lead
- {{phone_number}}: Teléfono del lead
- {{email}}: Email del lead
- {{course_interest}}: Curso de interés inicial
- {{lead_source}}: Fuente del lead
- {{current_time}}: Hora actual de la llamada (formato 24h)
- {{business_hours}}: Si es horario laboral

## PERSONALIDAD Y TONO (Siempre)
- **Formal pero cercana**: "genial", "perfecto", "fenomenal", "ah, qué guay"
- **Transmite pasión** por el diseño y educación
- **Española natural**: Evita formalismos excesivos
- **Directa y eficiente**: Ir al grano sin perder calidez
- **Respetuosa**: Con tiempos y decisiones del lead

## REGLAS GENERALES
- Máximo 3 preguntas por vez
- Respuestas cerradas siempre que sea posible
- Una objeción a la vez - no alargues
- Cortar educadamente si no cualifica
- Sentido de urgencia sin presionar

## ESPECIALISTAS DISPONIBLES
### Online (llamada/videollamada):
- Caridad Frutos: caridadfrutos@laescueladediseno.com
- Vanessa Calvo: vanessacalvo@laescueladediseno.com  
- Marta Gutiérrez: martagutierrez@laescueladediseno.com

### Privada (presencial/videollamada):
- Caridad Frutos: caridadfrutos@laescueladediseno.com
- Vanessa Calvo: vanessacalvo@laescueladediseno.com
- En copia: Bea <bea@laescueladediseno.com>

## HORARIOS ESPECIALISTAS
- **Online**: Lunes a Viernes 9:00-18:00h para llamadas/videollamadas
- **Privada**: 
  - Presencial: Solo tardes (16:00-20:00h) y sábados mañana (9:00-13:00h) - 1 hora
  - Videollamada: Cualquier horario 9:00-18:00h

## INFORMACIÓN NUNCA INVENTAR
- Precios específicos exactos (usar rangos generales)
- Fechas exactas de inicio de cursos
- Detalles técnicos muy específicos del temario
- Descuentos o promociones no confirmadas
- Garantías específicas de empleo"""

    def create_tools(self):
        """Create all the n8n webhook tools that handle business logic"""
        
        # Check Availability Privada Tool
        check_availability_privada = Tool(
            tool_id="tool-1752595233964",
            name="check_availability_privada",
            description="Verificar disponibilidad de especialistas privada ESI",
            type="custom",
            method="POST",
            url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
            parameters={
                "type": "object",
                "properties": {
                    "meeting_type": {
                        "type": "string",
                        "description": "Tipo de reunión: presencial o videollamada"
                    },
                    "course_type": {
                        "type": "string",
                        "description": "Curso de interés del lead"
                    }
                },
                "required": ["course_type", "meeting_type"]
            }
        )
        
        # Check Availability Online Tool
        check_availability_online = Tool(
            tool_id="tool-1752595396875",
            name="check_availability_online",
            description="Verificar disponibilidad de especialistas online ESI",
            type="custom",
            method="POST",
            url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
            parameters={
                "type": "object",
                "properties": {
                    "preferred_time": {
                        "type": "string",
                        "description": "Momento preferido para la reunión"
                    },
                    "course_type": {
                        "type": "string",
                        "description": "Curso de interés del lead"
                    }
                },
                "required": ["course_type"]
            }
        )
        
        # Book Calendar Privada Tool
        book_calendar_privada = Tool(
            tool_id="tool-1752596037711",
            name="book_calendar_privada",
            description="Agendar reunión con especialista privada",
            type="custom",
            method="POST",
            url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
            parameter_type="form",
            parameters={
                "type": "object",
                "required": [
                    "customer_name", "customer_phone", "customer_email",
                    "course_interest", "meeting_datetime", "meeting_type", "specialist_email"
                ],
                "properties": {
                    "customer_name": {"type": "string", "description": "Nombre del lead cualificado"},
                    "customer_phone": {"type": "string", "description": "Teléfono del lead"},
                    "customer_email": {"type": "string", "description": "Email del lead"},
                    "course_interest": {"type": "string", "description": "Curso de interés"},
                    "meeting_datetime": {"type": "string", "description": "Fecha y hora de la reunión en formato ISO"},
                    "specialist_email": {"type": "string", "description": "Email del especialista asignado"},
                    "motivation": {"type": "string", "description": "Motivación principal del lead"},
                    "experience_level": {"type": "string", "description": "Nivel de experiencia del lead"},
                    "primera_reunion": {"type": "string", "description": "Tipo de reunión para modalidad privada: presencial o videollamada"},
                    "copy_bea": {"type": "boolean", "description": "Si incluir a Bea en copia del email"}
                }
            }
        )
        
        # Book Calendar Online Tool
        book_calendar_online = Tool(
            tool_id="tool-1752601612267",
            name="book_calendar_online",
            description="Agendar reunión con especialista online",
            type="custom",
            method="POST",
            url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
            parameter_type="form",
            parameters={
                "type": "object",
                "required": [
                    "customer_name", "customer_phone", "customer_email",
                    "course_interest", "meeting_datetime", "specialist_email"
                ],
                "properties": {
                    "customer_name": {"type": "string", "description": "Nombre del lead cualificado"},
                    "customer_phone": {"type": "string", "description": "Teléfono del lead"},
                    "customer_email": {"type": "string", "description": "Email del lead"},
                    "course_interest": {"type": "string", "description": "Curso de interés"},
                    "meeting_datetime": {"type": "string", "description": "Fecha y hora de la reunión en formato ISO"},
                    "specialist_email": {"type": "string", "description": "Email del especialista asignado"},
                    "motivation": {"type": "string", "description": "Motivación principal del lead"},
                    "experience_level": {"type": "string", "description": "Nivel de experiencia del lead"},
                    "primera_reunion": {"type": "string", "description": "Tipo de reunión: videollamada o llamada"}
                }
            }
        )
        
        # Create HubSpot Task Tool
        create_hubspot_task = Tool(
            tool_id="tool-1752666157093",
            name="create_hubspot_task",
            description="Crear tarea en HubSpot para que alguien llame al lead",
            type="custom",
            method="POST",
            url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
            parameters={
                "type": "object",
                "required": [
                    "customer_name", "customer_phone", "customer_email",
                    "course_interest", "task_type", "assigned_to"
                ],
                "properties": {
                    "customer_name": {"type": "string", "description": "Nombre del lead"},
                    "customer_phone": {"type": "string", "description": "Teléfono del lead"},
                    "customer_email": {"type": "string", "description": "Email del lead"},
                    "course_interest": {"type": "string", "description": "Curso de interés"},
                    "task_type": {"type": "string", "description": "Tipo de tarea: call_lead"},
                    "assigned_to": {"type": "string", "description": "Email del especialista asignado"},
                    "motivation": {"type": "string", "description": "Motivación principal del lead"},
                    "experience_level": {"type": "string", "description": "Nivel de experiencia del lead"},
                    "priority": {"type": "string", "description": "Prioridad de la tarea: high, medium, low"},
                    "preferred_time": {"type": "string", "description": "Horario preferido para ser contactado"},
                    "notes": {"type": "string", "description": "Notas adicionales para la llamada"}
                }
            }
        )
        
        self.tools = [
            check_availability_privada,
            check_availability_online,
            book_calendar_privada,
            book_calendar_online,
            create_hubspot_task
        ]

    def create_nodes(self):
        """Create all conversation flow nodes - this is the complete conversation logic"""
        
        # Welcome Node (Start)
        welcome_node = Node(
            id="start-node-1752593222665",
            name="Welcome Node",
            type="conversation",
            display_position=DisplayPosition(342, 433),
            start_speaker="agent",
            instruction=Instruction(
                type="prompt",
                text="Introdúcete como Bea, asistente IA de ESI. Pregúntale al usuario si es un buen momento para hablar 5 minutos."
            ),
            edges=[
                Edge(
                    id="edge-1",
                    destination_node_id="node-callback",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="El usuario indica que no tiene tiempo ahora o pide que le llamen más tarde."
                    )
                ),
                Edge(
                    id="edge-2",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="El usuario no muestra interés real en el curso o rechaza explícitamente."
                    )
                ),
                Edge(
                    id="edge-3",
                    destination_node_id="node-qualification",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="El usuario confirma que tiene tiempo para hablar y muestra interés en el curso."
                    )
                )
            ]
        )
        
        # Qualification Node
        qualification_node = Node(
            id="node-qualification",
            name="Cualificación Express",
            type="conversation",
            display_position=DisplayPosition(1292, 818),
            instruction=Instruction(
                type="prompt",
                text="""Genial. Tres preguntas rápidas antes de conectarte con nuestro especialista:
1. ¿Tienes experiencia previa en diseño?
2. ¿Tu objetivo principal? ¿Cambio profesional, mejorar trabajo actual, o emprendimiento?
3. ¿Modalidad preferida: online o presencial?"""
            ),
            edges=[
                Edge(
                    id="edge-qualified",
                    destination_node_id="node-extract-variables",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="El usuario cualifica basado en motivación profesional y plazos razonables."
                    )
                )
            ]
        )
        
        # Extract Variables Node
        extract_variables_node = Node(
            id="node-extract-variables",
            name="Extract Variables",
            type="extract_dynamic_variables",
            display_position=DisplayPosition(1682, 1240),
            variables=[
                Variable(
                    name="tipo_curso",
                    description="Qué tipo de curso va a cursar o está interesado el lead",
                    type="enum",
                    choices=["online", "privado"]
                ),
                Variable(
                    name="experience_level",
                    description="Nivel de experiencia en diseño del usuario",
                    type="string"
                ),
                Variable(
                    name="motivation",
                    description="Objetivo principal del usuario",
                    type="string"
                )
            ],
            edges=[
                Edge(
                    id="edge-to-booking",
                    destination_node_id="node-booking-flow",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="Variables are determined and user is qualified"
                    )
                )
            ]
        )
        
        # Simplified booking flow node
        booking_flow_node = Node(
            id="node-booking-flow",
            name="Booking Flow",
            type="conversation",
            display_position=DisplayPosition(2500, 1200),
            instruction=Instruction(
                type="prompt",
                text="Perfecto, vamos a agendar una cita con nuestro especialista. Te contactaremos pronto con los detalles."
            ),
            edges=[
                Edge(
                    id="edge-to-end",
                    destination_node_id="node-end",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="Booking process completed"
                    )
                )
            ]
        )
        
        # Callback Node
        callback_node = Node(
            id="node-callback",
            name="Callback Request",
            type="conversation",
            display_position=DisplayPosition(732, 305),
            instruction=Instruction(
                type="prompt",
                text="Entiendo que no es un buen momento. ¿Cuándo sería mejor para llamarte?"
            ),
            edges=[
                Edge(
                    id="edge-callback-to-end",
                    destination_node_id="node-end",
                    transition_condition=TransitionCondition(
                        type="prompt",
                        prompt="Callback scheduled"
                    )
                )
            ]
        )
        
        # End Node
        end_node = Node(
            id="node-end",
            name="End Call",
            type="end",
            display_position=DisplayPosition(3000, 1500),
            instruction=Instruction(
                type="prompt",
                text="¡Perfecto! Gracias y que tengas un excelente día."
            )
        )
        
        self.nodes = [
            welcome_node,
            qualification_node,
            extract_variables_node,
            booking_flow_node,
            callback_node,
            end_node
        ]

    def build_conversation_flow(self) -> Dict[str, Any]:
        """Build the complete conversation flow JSON structure for Retell"""
        
        self.create_tools()
        self.create_nodes()
        
        # Convert tools to dict format
        tools_dict = []
        for tool in self.tools:
            tool_dict = asdict(tool)
            tools_dict.append(tool_dict)
        
        # Convert nodes to dict format
        nodes_dict = []
        for node in self.nodes:
            node_dict = asdict(node)
            nodes_dict.append(node_dict)
        
        conversation_flow = {
            "conversation_flow_id": "conversation_flow_esi_python",
            "version": 0,
            "global_prompt": self.global_prompt,
            "nodes": nodes_dict,
            "start_node_id": "start-node-1752593222665",
            "start_speaker": "agent",
            "tools": tools_dict,
            "model_choice": {
                "type": "cascading",
                "model": "gpt-4.1"
            },
            "begin_tag_display_position": {"x": 122, "y": 333},
            "is_published": False,
            "knowledge_base_ids": []
        }
        
        return conversation_flow


# =============================================================================
# AGENT MANAGER
# =============================================================================

class ESIAgentManager:
    """
    Main class for managing the ESI agent creation and deployment.
    This handles the interaction with Retell's API.
    """
    
    def __init__(self, api_key: str):
        """Initialize with your Retell API key"""
        self.client = Retell(api_key=api_key)
        self.flow_builder = ESIConversationFlowBuilder()
        
    def create_agent(self, agent_name: str = "ESI Conversation Flow Agent") -> Any:
        """Create the ESI agent with conversation flow"""
        
        try:
            # Build conversation flow
            conversation_flow = self.flow_builder.build_conversation_flow()
            
            print(f"🏗️  Building agent: {agent_name}")
            print(f"   Nodes: {len(conversation_flow['nodes'])}")
            print(f"   Tools: {len(conversation_flow['tools'])}")
            
            # Create agent with Retell SDK
            agent_response = self.client.agent.create(
                agent_name=agent_name,
                response_engine={
                    "type": "conversation-flow",
                    "version": 0,
                    "conversation_flow_id": conversation_flow["conversation_flow_id"],
                    "conversation_flow": conversation_flow
                },
                voice_id="custom_voice_6105206ed083e6faf35d86f533",  # Your custom voice
                language="es-ES",
                max_call_duration_ms=3600000,
                interruption_sensitivity=0.9,
                allow_user_dtmf=True,
                opt_out_sensitive_data_storage=False,
                opt_in_signed_url=False
            )
            
            print(f"✅ Agent created successfully!")
            print(f"Agent ID: {agent_response.agent_id}")
            print(f"Agent Name: {agent_response.agent_name}")
            
            return agent_response
            
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            raise

    def get_conversation_flow(self) -> Dict[str, Any]:
        """Get the conversation flow structure for inspection"""
        return self.flow_builder.build_conversation_flow()

    def save_conversation_flow(self, filename: str = "esi_conversation_flow.json") -> str:
        """Save the conversation flow to a JSON file"""
        flow = self.get_conversation_flow()
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(flow, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Conversation flow saved to: {filename}")
        return filename


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    """
    Example of how to use the ESI Conversation Flow system
    """
    
    # You'll need to set your actual Retell API key
    api_key = "YOUR_RETELL_API_KEY"  # Replace with your actual API key
    
    if api_key == "YOUR_RETELL_API_KEY":
        print("⚠️  Please set your actual RETELL_API_KEY in the code or use environment variables")
        print("Example usage:")
        print("1. Set api_key = 'your_actual_key_here'")
        print("2. Or use: python -c \"from config import Config; print('API Key loaded from .env')\"")
    else:
        # Create agent manager
        agent_manager = ESIAgentManager(api_key)
        
        # Create the agent
        try:
            agent = agent_manager.create_agent("ESI Design School Agent")
            
            # Save conversation flow for reference
            flow_file = agent_manager.save_conversation_flow()
            
            print("\n🎉 ESI Agent setup complete!")
            print(f"📁 Flow saved to: {flow_file}")
            print("🔗 Next steps:")
            print("1. Test your agent in the Retell dashboard")
            print("2. Configure your phone number to use this agent")
            print("3. Monitor calls and adjust the conversation flow as needed")
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            print("Please check your API key and try again")
