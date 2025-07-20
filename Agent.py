__all__ = ["Agent"]

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI
import dotenv
import os

class Agent:
    def __init__(self, provider="ollama", instructions=None):
        
        if not instructions:
            raise ValueError("Instructions must not be empty. Give your agent some context")
        
        if provider not in ["ollama", "openai"]:
            raise ValueError("Provider must be either 'ollama' or 'openai'")
        
        self.instructions = instructions
        self.provider = provider
        
        # load chat model. The user can decide to use OpenAI or Ollama, for now
        if provider == "ollama":
            self.chat_model = ChatOllama(model="llama3.2")
            
        elif provider == "openai":
            # load openAI
            dotenv.load_dotenv(dotenv.find_dotenv())
            self.openai_key = os.getenv("OPENAI_API_KEY")
            if not self.openai_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            self.client = OpenAI(api_key=self.openai_key)
            self.openai_model = "gpt-4.1-nano"
        
    
    def invoke(self, prompt):
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.openai_model, 
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        
        elif self.provider == "ollama":
            chat_prompt = ChatPromptTemplate.from_messages([
             ("system", self.instructions),
             ("user", "{user_prompt}")   
            ])
            messages = chat_prompt.format_messages(user_prompt=prompt)
            response = self.chat_model.invoke(messages)
            return response.content

        
def test(provider):
    instructions = """Your name is Summ A. Rizer. You are an expert summarizer that is able to summarize the content that is given to you and always end your messages with a smiley face such as :). You always answer in portuguese and in a professional way. You've been created by Breno Robazza. Summarize the given to you"""
    
    prompt = """Let us not wallow in the valley of despair, I say to you today, my friends. So even though we face the difficulties of today and tomorrow, I still have a dream. It is a dream deeply rooted in the American dream. I have a dream that one day this nation will rise up and live out the true meaning of its creed: We hold these truths to be self-evident, that all men are created equal.
    """
    summarizer = Agent(provider, instructions)
    summary = summarizer.invoke(prompt=prompt)
    print("Summary:", summary)
    

if __name__ == "__main__":
    test("ollama")