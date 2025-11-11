# Simple AI Agent - Google 5 Days of AI (Day 1A)

This Python script is converted from the Kaggle notebook "Day 1A - From Prompt to Action" and demonstrates how to create a simple AI agent using Google's Agent Development Kit (ADK).

## Features

- **Simple AI Agent**: Creates an agent that can answer general questions
- **Google Search Integration**: Uses Google Search tool for current information
- **Flexible Authentication**: Works in both Kaggle and local environments
- **Retry Configuration**: Robust error handling and retry logic for API calls

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google API Key

#### For Kaggle Environment:
- Add `GOOGLE_API_KEY` to your Kaggle secrets

#### For Local Environment:
- Set the environment variable:
  ```bash
  export GOOGLE_API_KEY="your_google_api_key_here"
  ```
- Or create a `.env` file with:
  ```
  GOOGLE_API_KEY=your_google_api_key_here
  ```

### 3. Run the Script

```bash
python simpleagent.py
```

## What the Script Does

1. **Authentication Setup**: Automatically detects if running in Kaggle or local environment and sets up the Google API key accordingly
2. **Agent Creation**: Creates a Gemini-powered agent with Google Search capabilities
3. **Example Queries**: Runs two example queries:
   - Information about Google's Agent Development Kit
   - Current weather in London

## Code Structure

- `setup_gemini_api_key()`: Handles API key authentication for different environments
- `main()`: Async function that runs the example queries
- Retry configuration for robust API handling
- Proper error handling and logging

## Original Source

This code is based on the Kaggle notebook: [Day 1A - From Prompt to Action](https://www.kaggle.com/code/kaggle5daysofai/day-1a-from-prompt-to-action/notebook)

## Customization

You can modify the agent by:
- Changing the model (e.g., to `gemini-2.0-pro`)
- Adding more tools
- Modifying the agent's instructions
- Adding more example queries in the `main()` function