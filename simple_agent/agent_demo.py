# agent_demo.py

from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from .tools import WikipediaTool, CalculatorTool
import openai
import sys
import os
import time
from typing import List, Optional, Any, Dict
from uuid import UUID

def main() -> None:
    """
    Main function that sets up and runs a LangChain agent with Wikipedia and Calculator tools.
    
    This function:
    1. Checks for the OpenAI API key in environment variables
    2. Sets up the language model with OpenAI
    3. Initializes the Wikipedia and Calculator tools
    4. Creates a zero-shot agent with these tools
    5. Runs a set of predefined questions through the agent
    6. Handles various OpenAI API errors gracefully
    
    Returns:
        None
    
    Exits:
        With status code 1 if API key is missing or authentication fails
    """
    # Print header
    print("\n")
    print("🤖 Simple Agent Demo (LangChain with OpenAI Compatible LLM)")
    print("-" * 50)
    
    # Initialize statistics tracking
    stats: Dict[str, int] = {
        "wiki_queries": 0,
        "calculator_calls": 0,
        "openai_queries": 0
    }
    start_time = time.time()
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in the .env file or export it in your shell.")
        sys.exit(1)
        
    try:
        # Create a callback handler to track tool usage
        class ToolTracker(BaseCallbackHandler):
            def __init__(self, stats):
                super().__init__()
                self.stats = stats
                
            def on_tool_start(
                self, 
                serialized: Dict[str, Any], 
                input_str: str, 
                *, 
                run_id: UUID, 
                parent_run_id: Optional[UUID] = None,
                tags: Optional[List[str]] = None,
                metadata: Optional[Dict[str, Any]] = None,
                **kwargs: Any
            ) -> None:
                tool_name = serialized.get("name", "")
                if tool_name == "wikipedia":
                    self.stats["wiki_queries"] += 1
                elif tool_name == "calculator":
                    self.stats["calculator_calls"] += 1
                    
            def on_llm_start(
                self, 
                serialized: Dict[str, Any], 
                prompts: List[str], 
                *, 
                run_id: UUID,
                parent_run_id: Optional[UUID] = None,
                tags: Optional[List[str]] = None,
                metadata: Optional[Dict[str, Any]] = None,
                **kwargs: Any
            ) -> None:
                self.stats["openai_queries"] += 1

        tool_tracker = ToolTracker(stats)

        # 1) LLM setup - Add the callback handler to the LLM
        llm: OpenAI = OpenAI(temperature=0, callbacks=[tool_tracker])  # Add callbacks here

        # 2) Wrap tools into LangChain's Tool format
        wiki_tool: WikipediaTool = WikipediaTool()
        calc_tool: CalculatorTool = CalculatorTool()

        tools: List[Tool] = [
            Tool(
                name=wiki_tool.name,
                func=wiki_tool.run,
                description=wiki_tool.description
            ),
            Tool(
                name=calc_tool.name,
                func=calc_tool.run,
                description=calc_tool.description
            ),
        ]

        # 3) Initialize a zero-shot-react-description style agent
        # Using invoke instead of run to address deprecation warning
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,  
            callbacks=[tool_tracker]  # Make sure callback is here too
        )

        # 4) Let's ask a couple of questions
        questions: List[str] = [
            "Who was Ada Lovelace and why is she important?",
            "Calculate 17 * (24 - 5)",  
            "Calculate the square root of 144",  
            "Tell me something about Art Deco jewelry.",
        ]

        for q in questions:
            print("\n" + "-" * 40)
            print(f"Question: {q}")
            try:
                # Use invoke instead of run to address deprecation warning
                # Add callbacks to each invoke call as well
                answer: str = agent.invoke({"input": q}, config={"callbacks": [tool_tracker]})["output"]
                print(f"Answer:\n{answer}")
            except openai.AuthenticationError:
                print("Error: Authentication failed. Check your OpenAI API key.")
                break
            except openai.RateLimitError:
                print("Error: OpenAI API rate limit exceeded. Please try again later.")
                continue
            except openai.APIError as e:
                print(f"OpenAI API Error: {e}")
                continue
            except openai.APIConnectionError:
                print("Error: OpenAI service is currently unavailable. Please try again later.")
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                continue
        
        # Print statistics
        elapsed_time = time.time() - start_time
        
        print("\n")
        print("-" * 50)
        print("\n📊 Statistics:")
        
        print(f"- Runtime..............: {elapsed_time:.2f} seconds")
        print(f"- OpenAI API calls.....: {stats['openai_queries']}")
        print(f"- Wikipedia tool calls.: {stats['wiki_queries']}")
        print(f"- Calculator tool calls: {stats['calculator_calls']}")
        print("\n")
                
    except openai.AuthenticationError:
        print("Error: Authentication failed. Check your OpenAI API key.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()