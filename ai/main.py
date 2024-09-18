import asyncio
from gemini_chat import GeminiChat, genai
from config_reader import JSONConfigReader
from utils import CONFIG_PATH, ROLE_PROMPT, END_PROGRAM, END_PROMPT


def setup(config_path: str, role_prompt: str) -> genai.ChatSession:
    """Creates an active chat with gemini model.

    Args:
        config_path (str): path to configuration file.
        role_prompt (str): prompt to set the role of the model before the users interaction.

    Returns:
        genai.ChatSession: open and active chat session.
    """
    api_key = JSONConfigReader.get_config_value(config_path, "API_KEY")
    if not api_key:
        print("API key not found in configuration file. Exiting...")
        exit(1)
    
    gen_chat = GeminiChat(api_key)
    gen_chat.start_new_chat(role_prompt)
    return gen_chat


async def main() -> None:
    """Main function for user interaction."""
    gen_chat = setup(CONFIG_PATH, ROLE_PROMPT)
    print("System is ready. Enter your text:\n")

    prompt = ""
    while True:
        if not prompt:
            prompt = input()
        
        response = await gen_chat.get_chat_response(prompt)
        if response is not None:
            print(response)

        added = input(f"\n{prompt}")
        
        if added.strip() == END_PROMPT:
            prompt = ""
        
        elif added.strip() == END_PROGRAM:
            print("Exit...")
            return
        
        else:
            prompt += added


if __name__ == "__main__":
    print("System is booting. Please wait...\n")
    asyncio.run(main())