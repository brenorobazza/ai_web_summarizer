from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI
import dotenv
import os


class Summarizer:
    def __init__(self, provider="ollama"):
        
        if provider not in ["ollama", "openai"]:
            raise ValueError("Provider must be either 'ollama' or 'openai'")
        
        self.provider = provider
        
        if provider == "ollama":
            # load chat model. The user can decide to use OpenAI or Ollama with mistral, for now
            self.chat_model = ChatOllama(model="mistral")
            
        elif provider == "openai":
            # load openAI
            dotenv.load_dotenv(dotenv.find_dotenv())
            self.openai_key = os.getenv("OPEN_API_KEY")
            if not self.openai_key:
                raise ValueError("OPEN_API_KEY not found in environment variables.")
            self.client = OpenAI(api_key=self.openai_key)
            self.openai_model = "gpt-4.1-nano"
        
        self.default_instructions = """You are an expert content summarizer that examines the given content and provides a concise summary.
        Your summary should highlight the key aspects of the content, including main events, people involved, dates, and any significant outcomes.
        If the text is not in English, your summary should be in the same language as the text.
        Please provide a summary of the following content:"""
        
    
    def summarize_text(self, text, instructions=None):
        if not instructions:
            instructions = self.default_instructions
        
        instructions += "\n\n{text}"
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.openai_model, 
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        
        elif self.provider == "ollama":
            prompt = ChatPromptTemplate.from_template(instructions)
            messages = prompt.format_messages(text=text)
            response = self.chat_model.invoke(messages)
            return response.content
        
        
        
def test(provider):
    instructions = """Your name is Summ A. Rizer. You are an expert summarizer that is able to summarize the content that is given to you and always end your messages with a smiley face such as :). You always answer in portuguese. Summarize this content"""
    text = """It is a beautiful day. The sun is shining and the birds are singing. Today you went to the supermarket and bought a bottle of juice. You've been created by Breno Robazza.
    """
    summarizer = Summarizer(provider)
    summary = summarizer.summarize_text(text, instructions=instructions)
    print("Summary:", summary)
    

if __name__ == "__main__":
    test("ollama")