__all__ = ["Agent"]

from openai import OpenAI
import dotenv
import os

class Agent:
    def __init__(self, provider="openai", instructions=None):
        if not instructions:
            raise ValueError("Instructions must not be empty. Give your agent some context")
        if provider not in ["ollama", "openai"]:
            raise ValueError("Provider must be either 'ollama' or 'openai'")
        self.instructions = instructions
        self.provider = provider
        dotenv.load_dotenv(dotenv.find_dotenv())
        openai_key = os.getenv("OPENAI_API_KEY")
        if provider == "ollama":
            self.api_key = "ollama"
            self.base_url = "http://localhost:11434/v1"
            self.model = "gemma3"
        elif provider == "openai":
            if not openai_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            self.api_key = openai_key
            self.base_url = "https://api.openai.com/v1"
            self.model = "gpt-4.1-nano"
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
    
    def invoke(self, prompt):
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input = prompt,
            previous_response_id = self.response_id if hasattr(self, 'response_id') else None
        )
        self.response_id = response.id
        return response.output_text

        
def test(provider):
    instructions = """Your name is Summ A. Rizer. You are an expert summarizer that is able to summarize the content that is given to you and always end your messages with a smiley face such as :). You always answer in portuguese and in a professional way. You've been created by Breno Robazza. Summarize the given to you"""
    prompt = """Let us not wallow in the valley of despair, I say to you today, my friends. So even though we face the difficulties of today and tomorrow, I still have a dream. It is a dream deeply rooted in the American dream. I have a dream that one day this nation will rise up and live out the true meaning of its creed: We hold these truths to be self-evident, that all men are created equal.
    """
    summarizer = Agent(provider, instructions)
    summary = summarizer.invoke(prompt=prompt)
    print("Summary:", summary)

if __name__ == "__main__":
    test("openai")