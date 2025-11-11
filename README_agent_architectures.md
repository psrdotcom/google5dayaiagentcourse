# 🤖 Agent Architectures Interactive Demo

An interactive Python script that demonstrates different multi-agent architecture patterns using Google's Agent Development Kit (ADK). This script converts the Kaggle notebook "Day 1B - Agent Architectures" into an executable format with a user-friendly menu system.

## 🎯 What This Demo Covers

### Four Core Agent Architecture Patterns:

1. **🔍 Multi-Agent Research & Summarization System**
   - LLM-orchestrated workflow with specialized agents
   - Research Agent + Summarizer Agent + Root Coordinator
   - Dynamic decision making by the LLM

2. **✍️ Sequential Blog Post Creation Pipeline**
   - Fixed order execution: Outline → Write → Edit
   - Guaranteed step-by-step processing
   - Predictable and deterministic workflow

3. **⚡ Parallel Multi-Topic Research**
   - Concurrent execution for independent tasks
   - Tech + Health + Finance researchers running simultaneously
   - Aggregator combines all results

4. **➰ Loop-based Story Refinement**
   - Iterative improvement with feedback cycles
   - Writer → Critic → Refiner loop until approved
   - Quality refinement through multiple iterations

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

### 3. Run the Interactive Demo

```bash
python agent_architectures_interactive.py
```

## 🎮 How to Use

The script provides an interactive menu where you can:

1. **Choose a demo** - Select from 4 different architecture patterns
2. **Customize inputs** - Enter your own topics, prompts, or use defaults
3. **See real results** - Watch agents collaborate in real-time
4. **Learn architecture patterns** - Built-in guide helps you choose the right pattern

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

Enter a topic to research (or press Enter for default): machine learning trends 2024

🔍 Researching: machine learning trends 2024
[Agent execution output...]
📋 Final Summary: [Generated summary]
```

## 🏗️ Architecture Decision Guide

| Pattern | When to Use | Example | Key Benefit |
|---------|-------------|---------|-------------|
| **LLM-Orchestrated** | Dynamic decisions needed | Research + Summarize | Flexible, adaptive |
| **Sequential** | Order matters, linear pipeline | Outline → Write → Edit | Predictable, deterministic |
| **Parallel** | Independent tasks, speed matters | Multi-topic research | Fast, concurrent execution |
| **Loop** | Iterative improvement needed | Write → Critique → Improve | High quality through refinement |

### Quick Decision Tree:
- Need guaranteed order? → **Sequential**
- Independent tasks? → **Parallel**
- Need improvement cycles? → **Loop**
- Dynamic decisions? → **LLM-Orchestrated**

## 📁 File Structure

```
Google5dayAIagent/
├── agent_architectures_interactive.py  # Main interactive script
├── simpleagent.py                     # Simple agent from Day 1A
├── requirements.txt                   # Dependencies
├── README.md                         # Documentation for simple agent
├── .env.example                      # Environment variables template
└── day-1b-agent-architectures.ipynb  # Original notebook
```

## 🛠️ Technical Details

### Key Components:

- **AgentArchitecturesDemo Class**: Main demo controller with interactive menu
- **Extract Response Text**: Helper function to clean up API responses
- **Error Handling**: Graceful handling of API limits and interruptions
- **Async Support**: Proper async/await for concurrent operations

### Agent Types Used:

- `Agent`: Basic LLM-powered agent with tools
- `SequentialAgent`: Runs sub-agents in fixed order
- `ParallelAgent`: Runs sub-agents concurrently
- `LoopAgent`: Runs sub-agents in cycles with termination conditions
- `AgentTool`: Wraps agents to make them callable as tools
- `FunctionTool`: Wraps Python functions as agent tools

## 🔧 Customization

You can easily modify the script to:

1. **Change Models**: Replace `gemini-2.5-flash-lite` with other models
2. **Add New Demos**: Create additional architecture patterns
3. **Modify Instructions**: Customize agent behaviors and outputs
4. **Add Tools**: Integrate additional tools beyond Google Search
5. **Adjust Parameters**: Change iteration limits, retry options, etc.

## 🎓 Learning Outcomes

After using this demo, you'll understand:

- ✅ When to use each multi-agent architecture pattern
- ✅ How to orchestrate agent workflows
- ✅ State management between agents using `output_key`
- ✅ Tool integration with `AgentTool` and `FunctionTool`
- ✅ Error handling and retry strategies
- ✅ Real-world applications of each pattern

## 🚨 Troubleshooting

### Common Issues:

1. **API Rate Limits (429 errors)**:
   - Run demos one at a time
   - Wait between executions
   - Check your API quota

2. **Import Errors**:
   - Ensure `google-adk` is installed
   - Check Python version (3.7+ required)

3. **Authentication Errors**:
   - Verify your API key is set correctly
   - Check permissions on your API key

4. **Slow Performance**:
   - This is normal for complex multi-agent workflows
   - Parallel demos will be faster than sequential ones

## 📚 Original Source

Based on the Kaggle notebook: [Day 1B - Agent Architectures](https://www.kaggle.com/code/kaggle5daysofai/day-1b-agent-architectures/notebook)

## 🤝 Contributing

Feel free to:
- Add new architecture patterns
- Improve error handling
- Add more interactive features
- Submit bug fixes

## 📄 License

Licensed under the Apache License, Version 2.0 - same as the original Kaggle notebook.