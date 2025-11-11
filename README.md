# 🤖 Google 5 Days of AI - Agent Development Course

A comprehensive collection of AI agent demonstrations using Google's Agent Development Kit (ADK), covering both simple single-agent systems and complex multi-agent architectures. This repository contains Python scripts converted from Kaggle notebooks for Days 1A and 1B of the Google 5 Days of AI course.

## 📚 What's Included

### 🔧 Simple AI Agent (Day 1A)
- **Single-Agent System**: Basic Gemini-powered agent with Google Search capabilities
- **Authentication Handling**: Works in both Kaggle and local environments
- **Error Recovery**: Robust retry logic for API calls
- **Real-World Examples**: Weather queries and tech information retrieval

### 🏗️ Agent Architectures (Day 1B)
- **Four Architecture Patterns**: Interactive demos of different multi-agent systems
- **Production-Ready Examples**: Real implementations you can modify and extend
- **Interactive Menu System**: User-friendly interface to explore each pattern
- **Architecture Decision Guide**: Help choosing the right pattern for your use case

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google API Key

#### For Local Environment:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

Or create a `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

#### For Kaggle Environment:
Add `GOOGLE_API_KEY` to your Kaggle secrets.

### 3. Run the Demos

#### Simple Agent:
```bash
python simpleagent.py
```

#### Agent Architectures Interactive Demo:
```bash
python agent_architectures_interactive.py
```

## 🎯 Agent Architecture Patterns

### 1. 🔍 Multi-Agent Research & Summarization System
- **Pattern**: LLM-orchestrated workflow with specialized agents
- **Components**: Research Agent + Summarizer Agent + Root Coordinator
- **Use Case**: When you need dynamic decision making and flexible workflows
- **Benefits**: Adaptive, intelligent routing of tasks

### 2. ✍️ Sequential Blog Post Creation Pipeline
- **Pattern**: Fixed order execution (Outline → Write → Edit)
- **Components**: Sequential processing with guaranteed step order
- **Use Case**: When order matters and you need predictable workflows
- **Benefits**: Deterministic, reliable processing pipeline

### 3. ⚡ Parallel Multi-Topic Research
- **Pattern**: Concurrent execution for independent tasks
- **Components**: Tech + Health + Finance researchers + Aggregator
- **Use Case**: When tasks are independent and speed matters
- **Benefits**: Fast execution, efficient resource utilization

### 4. ➰ Loop-based Story Refinement
- **Pattern**: Iterative improvement with feedback cycles
- **Components**: Writer → Critic → Refiner loop with termination conditions
- **Use Case**: When you need iterative improvement and quality refinement
- **Benefits**: High-quality outputs through multiple iterations

## 🏗️ Architecture Decision Guide

| Pattern | When to Use | Best For | Key Benefit |
|---------|-------------|----------|-------------|
| **LLM-Orchestrated** | Dynamic decisions needed | Research + Analysis | Flexible, adaptive routing |
| **Sequential** | Order matters, dependencies exist | Content creation pipelines | Predictable, deterministic |
| **Parallel** | Independent tasks, speed critical | Multi-domain research | Fast, concurrent execution |
| **Loop** | Quality improvement needed | Creative tasks, refinement | High quality through iteration |

### Quick Decision Tree:
- Need guaranteed execution order? → **Sequential**
- Have independent parallel tasks? → **Parallel**
- Need iterative improvement cycles? → **Loop**
- Require dynamic decision making? → **LLM-Orchestrated**

## 📁 Project Structure

```
google5dayaiagentcourse/
├── simpleagent.py                     # Day 1A: Simple agent implementation
├── agent_architectures_interactive.py  # Day 1B: Multi-agent architectures
├── requirements.txt                   # Python dependencies
├── README.md                         # This comprehensive guide
├── README_agent_architectures.md     # Detailed architecture documentation
├── LICENSE                           # Apache 2.0 license
└── run_demo.sh                      # Quick start script
```

## 🎮 Interactive Demo Features

The agent architectures demo provides:

1. **Menu-Driven Interface**: Easy navigation between different patterns
2. **Custom Input Support**: Enter your own topics and prompts
3. **Real-Time Execution**: Watch agents collaborate live
4. **Built-in Architecture Guide**: Learn when to use each pattern
5. **Error Handling**: Graceful handling of API limits and failures

### Example Session:
```
🤖 AGENT ARCHITECTURES INTERACTIVE DEMO
Choose a demo to run:

1. 🔍 Multi-Agent Research & Summarization System
2. ✍️ Sequential Blog Post Creation Pipeline  
3. ⚡ Parallel Multi-Topic Research
4. ➰ Loop-based Story Refinement
5. 📖 Show Architecture Guide
6. ❌ Exit

Select an option (1-6): 1
Enter a topic to research: "latest AI developments 2024"
🔍 Researching: latest AI developments 2024
[Real-time agent execution...]
📋 Final Summary: [Generated comprehensive summary]
```

## 🛠️ Technical Architecture

### Core Components:
- **Agent Types**: Basic, Sequential, Parallel, Loop agents
- **Tool Integration**: Google Search, custom function tools
- **State Management**: Inter-agent communication using `output_key`
- **Error Handling**: Retry logic, graceful degradation
- **Async Support**: Proper concurrency for parallel operations

### Agent Framework Components:
- `Agent`: Basic LLM-powered agent with tools
- `SequentialAgent`: Executes sub-agents in fixed order
- `ParallelAgent`: Runs sub-agents concurrently
- `LoopAgent`: Iterative execution with termination conditions
- `AgentTool`: Wraps agents as callable tools
- `FunctionTool`: Wraps Python functions as agent tools

## 🔧 Customization & Extension

### Simple Agent Modifications:
- Change models (e.g., `gemini-2.0-pro`, `gemini-1.5-pro`)
- Add custom tools and integrations
- Modify agent instructions and behavior
- Add new example queries and use cases

### Architecture Pattern Extensions:
1. **Add New Patterns**: Create custom multi-agent workflows
2. **Tool Integration**: Add databases, APIs, external services
3. **Model Switching**: Use different models for different agents
4. **Custom Logic**: Implement domain-specific processing
5. **Monitoring**: Add logging, metrics, and observability

## 🎓 Learning Outcomes

After working through these demos, you'll understand:

### Fundamental Concepts:
- ✅ Single vs. multi-agent system trade-offs
- ✅ When and how to orchestrate multiple agents
- ✅ State management and inter-agent communication
- ✅ Tool integration and custom function wrapping

### Architecture Patterns:
- ✅ LLM-orchestrated dynamic workflows
- ✅ Sequential processing pipelines
- ✅ Parallel execution for independent tasks
- ✅ Loop-based iterative improvement systems

### Production Considerations:
- ✅ Error handling and retry strategies
- ✅ API rate limiting and quota management
- ✅ Authentication and security best practices
- ✅ Performance optimization for multi-agent systems

## 🚨 Troubleshooting

### Common Issues & Solutions:

**API Rate Limits (429 errors)**:
- Run demos sequentially, not concurrently
- Implement exponential backoff (already included)
- Monitor your API quota usage
- Consider using different API keys for different agents

**Authentication Errors**:
- Verify `GOOGLE_API_KEY` is set correctly
- Check API key permissions and quotas
- Ensure the key has access to required services

**Performance Issues**:
- Multi-agent workflows are inherently slower
- Parallel patterns are fastest for independent tasks
- Sequential patterns provide most predictable timing
- Loop patterns may require multiple iterations

**Import/Dependency Errors**:
- Ensure `google-adk` is properly installed
- Check Python version compatibility (3.7+)
- Verify all requirements.txt dependencies are installed

## 📚 Original Sources & References

- **Day 1A**: [From Prompt to Action](https://www.kaggle.com/code/kaggle5daysofai/day-1a-from-prompt-to-action/notebook)
- **Day 1B**: [Agent Architectures](https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures/notebook)
- **Google ADK Documentation**: Official Google Agent Development Kit docs
- **Best Practices**: Production multi-agent system patterns

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- **New Architecture Patterns**: Implement additional multi-agent patterns
- **Tool Integrations**: Add support for more external services
- **Error Handling**: Improve robustness and recovery mechanisms
- **Documentation**: Expand examples and use cases
- **Performance**: Optimize execution speed and resource usage
- **Testing**: Add comprehensive test suites

## 📄 License

Licensed under the Apache License, Version 2.0 - consistent with the original Kaggle notebooks.

## 🔗 Quick Links

- [Simple Agent Demo](simpleagent.py) - Start here for basic concepts
- [Multi-Agent Architectures](agent_architectures_interactive.py) - Advanced patterns
- [Requirements](requirements.txt) - All dependencies
- [Detailed Architecture Docs](README_agent_architectures.md) - In-depth technical details

---

*This repository provides hands-on experience with Google's Agent Development Kit, from basic single agents to sophisticated multi-agent architectures. Perfect for developers looking to understand and implement production-ready AI agent systems.*