# ESI Conversation Flow Agent

A Python implementation of the ESI Design School conversation flow agent using Retell AI SDK.

## 🎯 Overview

This project converts your existing ESI conversation flow from Retell's visual interface into clean, maintainable Python code. You get all the power of code (version control, testing, automation) while keeping all your existing n8n integrations working exactly as they do now.

## ✨ Features

- ✅ **Clean Python Architecture**: Well-organized, maintainable code
- ✅ **Retell SDK Integration**: Uses official Retell Python SDK
- ✅ **Conversation Flow Builder**: Programmatically creates complex conversation flows
- ✅ **n8n Integration**: Keeps all your existing webhook integrations
- ✅ **Spanish Language Support**: Configured for Spanish (es-ES)
- ✅ **Custom Voice Support**: Uses your existing custom voice
- ✅ **Environment Configuration**: Easy configuration via .env files
- ✅ **Testing Suite**: Built-in tests for validation
- ✅ **Deployment Scripts**: Simple deployment and management

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/zonder-ai/esi-conversation-flow-agent.git
cd esi-conversation-flow-agent
```

### 2. Setup

```bash
# Run automated setup
python setup.py
```

This will:
- Check Python version compatibility
- Install all dependencies
- Create your `.env` file from template

### 3. Configure

```bash
# Edit your environment file
cp .env.example .env
# Add your Retell API key to .env
```

Example `.env`:
```bash
RETELL_API_KEY=your_actual_retell_api_key_here
AGENT_NAME=ESI Design School Agent
N8N_WEBHOOK_URL=https://n8n.zonder.ai/webhook/retell-zonder-esi
```

### 4. Deploy

```bash
# Test the configuration
python test_agent.py

# Deploy your agent
python run.py
```

## 📁 Project Structure

```
esi-conversation-flow-agent/
├── esi_conversation_flow.py  # 🧠 Main conversation flow classes
├── config.py                 # ⚙️  Configuration management  
├── setup.py                  # 🛠️  Automated setup script
├── run.py                    # 🚀 Simple deployment runner
├── test_agent.py             # 🧪 Testing utilities
├── requirements.txt          # 📦 Dependencies
├── .env.example             # 🔐 Environment template
└── README.md                # 📖 This file
```

## 🎪 How It Works

### **The Magic: Conversation Flow as Code**

Instead of dragging boxes in Retell's visual interface, you describe your conversation flow in Python:

```python
# Your visual "Welcome Node" becomes:
welcome_node = Node(
    name="Welcome Node",
    instruction="Introdúcete como Bea, asesora comercial de ESI...",
    edges=[
        Edge(destination="qualification", condition="User says yes"),
        Edge(destination="callback", condition="User says no time")
    ]
)

# Your n8n webhooks become:
Tool(
    name="book_calendar_privada",
    url="https://n8n.zonder.ai/webhook/retell-zonder-esi",  # Same URL!
    parameters={"customer_name": "...", "meeting_datetime": "..."}  # Same params!
)
```

### **Complete Flow Process**

1. **Build Flow**: Python creates your conversation structure
2. **Deploy to Retell**: Uses SDK to upload agent configuration  
3. **Agent Goes Live**: Ready to take calls with your n8n integrations intact

## 🔧 Usage Examples

### Basic Usage

```python
from config import Config
from esi_conversation_flow import ESIAgentManager

# Create and deploy agent
agent_manager = ESIAgentManager(Config.RETELL_API_KEY)
agent = agent_manager.create_agent("My ESI Agent")
print(f"Agent ID: {agent.agent_id}")
```

### Advanced Customization

```python
from esi_conversation_flow import ESIConversationFlowBuilder

# Create custom flow
builder = ESIConversationFlowBuilder()

# Modify global prompt
builder.global_prompt = "Your custom prompt here..."

# Add custom nodes
custom_node = Node(
    name="Custom Question",
    instruction="Ask about their portfolio",
    edges=[Edge(destination="next_node", condition="User responds")]
)
builder.nodes.append(custom_node)

# Build and deploy
flow = builder.build_conversation_flow()
```

## 🧪 Testing

```bash
# Run all tests
python test_agent.py

# Output:
# ✅ All conversation flow structure tests passed!
# ✅ All tool parameter tests passed!
# ✅ JSON serialization test passed!
# 🎉 All tests passed! Your conversation flow is ready to deploy.
```

## 🛠️ Customization

### Adding New Conversation Nodes

```python
# In esi_conversation_flow.py, add to create_nodes():
portfolio_node = Node(
    id="node-portfolio-check",
    name="Portfolio Check",
    type="conversation",
    display_position=DisplayPosition(1500, 800),
    instruction=Instruction(
        type="prompt",
        text="¿Tienes algún portfolio de diseño que puedas mostrarnos?"
    ),
    edges=[
        Edge(
            id="edge-has-portfolio",
            destination_node_id="node-next-step",
            transition_condition=TransitionCondition(
                type="prompt",
                prompt="El usuario tiene portfolio"
            )
        )
    ]
)

self.nodes.append(portfolio_node)
```

### Adding New n8n Functions

```python
# In create_tools() method:
send_email_tool = Tool(
    tool_id="tool-send-welcome-email",
    name="send_welcome_email",
    description="Enviar email de bienvenida al lead",
    type="custom",
    method="POST",
    url="https://n8n.zonder.ai/webhook/retell-zonder-esi",
    parameters={
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "Email del lead"},
            "template": {"type": "string", "description": "Template de email"}
        },
        "required": ["email", "template"]
    }
)

self.tools.append(send_email_tool)
```

## 🔗 Integration Details

### n8n Webhooks
All your existing n8n workflows continue working unchanged:
- **Same URLs**: `https://n8n.zonder.ai/webhook/retell-zonder-esi`
- **Same Parameters**: `customer_name`, `meeting_datetime`, etc.
- **Same Logic**: Calendar booking, HubSpot tasks, email notifications

### Retell Configuration
- **Voice**: Your custom voice (`custom_voice_6105206ed083e6faf35d86f533`)
- **Language**: Spanish (es-ES)
- **Flow Type**: `conversation-flow` with programmatic generation

### ESI Business Logic
- **Qualification**: Express and detailed lead qualification
- **Scheduling**: Private (presencial/video) and online courses
- **Specialist Assignment**: Automatic based on course type and availability
- **Business Hours**: Time-based routing for optimal lead handling

## 📊 Monitoring & Analytics

After deployment:
- **Retell Dashboard**: Monitor calls and performance
- **n8n Workflows**: All existing integrations continue working
- **Conversation Logs**: Track flow transitions and function calls
- **Agent Analytics**: Call success rates, conversion metrics

## 🆘 Troubleshooting

### Common Issues

**API Key Error**
```bash
❌ Error: RETELL_API_KEY not found
```
**Solution**: Make sure your `.env` file has the correct `RETELL_API_KEY`

**Import Error**
```bash
❌ No module named 'retell'
```
**Solution**: Run `python setup.py` or `pip install -r requirements.txt`

**n8n Webhook Error**
```bash
❌ Webhook call failed
```
**Solution**: Verify your n8n webhook URL is accessible and accepts POST requests

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test conversation flow structure
from test_agent import validate_json_output
validate_json_output()
```

## 🔄 Migration Benefits

### Before (Visual Editor)
- ❌ Drag boxes, connect arrows
- ❌ Hard to backup/version
- ❌ Complex to modify at scale
- ❌ Manual deployment process

### After (Python Code)
- ✅ Describe flow in Python classes
- ✅ Easy Git backup and versioning
- ✅ Simple to modify and test
- ✅ One-command deployment
- ✅ Automated testing and validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [Retell AI Docs](https://docs.retellai.com)
- **n8n Integration**: [n8n Documentation](https://docs.n8n.io)
- **Issues**: [Create an issue](https://github.com/zonder-ai/esi-conversation-flow-agent/issues)

## 🎯 What's Next?

1. **Test your agent** in the Retell dashboard
2. **Configure your phone number** to use this agent
3. **Monitor calls** and optimize the conversation flow
4. **Scale your operation** with programmatic conversation management

---

**Built with ❤️ for ESI Design School**

Transform your voice agents from visual configuration to code-powered automation while keeping all your existing integrations intact.
