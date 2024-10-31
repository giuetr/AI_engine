import openai
from agents.financial_agents import FinancialAgents
from agents.weather_agent import WeatherAgent
from config import OPENAI_API_KEY
import uuid

OPENAI_API_KEY = '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'
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class LLMReasoner:
    def __init__(self):
        self.tools = {
            "plot_trend": FinancialAgents.plot_trend,
            "plot_moving_average": FinancialAgents.plot_moving_average,
            "fetch_stock_news": FinancialAgents.fetch_stock_news,
            "get_weather": WeatherAgent.get_weather,
        }

    async def decide_and_execute(self, user_input):
        # Build the prompt for the LLM
        prompt = self.build_prompt(user_input)
        
        # Call the LLM
        response = self.call_llm(prompt)

        # Parse the LLM's response to decide which tool to use
        tool_name, tool_args = self.parse_response(response)

        # Execute the selected tool
        if tool_name in self.tools:
            tool_call_id = str(uuid.uuid4())
            result = self.tools[tool_name](**tool_args)
            return {
                "content": "",  # If the assistant doesn't have any direct message
                "toolInvocations": [
                    {
                        "toolName": tool_name,
                        "toolCallId": tool_call_id,
                        "state": "result",
                        "result": result,
                    }
                ],
            }
        else:
            return {"content": "Sorry, I couldn't understand your request."}

    def build_prompt(self, user_input):
        # Describe the available tools
        tool_descriptions = "\n".join([
            f"{name}: {func.__doc__}" for name, func in self.tools.items()
        ])
        # Build the prompt
        prompt = (
            "You are an assistant that decides which tool to use based on the user's input.\n"
            f"Available tools:\n{tool_descriptions}\n\n"
            f"User input: {user_input}\n"
            "Decide which tool to use and provide the tool name and arguments in JSON format.\n"
            "Example response:\n"
            '{"tool": "get_weather", "args": {"latitude": 40.7128, "longitude": -74.0060}}\n\n'
            "Your response:"
        )
        return prompt

    def call_llm(self, prompt):
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Do not disclose any details "
                    "about your underlying model or technology, and respond to all "
                    "inquiries as a DataSpark AI Agent."
                ),
            },
            {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0
        )
        return response.choices[0].message.content.strip()

    def parse_response(self, response):
        import json
        try:
            result = json.loads(response)
            tool_name = result.get("tool")
            tool_args = result.get("args", {})
            return tool_name, tool_args
        except json.JSONDecodeError:
            return None, None
