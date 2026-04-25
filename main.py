import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Assistant")
    parser.add_argument("user_prompt", type=str, help="User prompt to send to Gemeni")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    

    client = genai.Client(api_key=api_key)

    for _ in range(20):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )

            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)
            
            if response.usage_metadata is None:
                raise RuntimeError(
                    "Failed to get usage metadata from Gemini API response. "
                    "This usually indicates the request failed or was blocked."
                )
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            print("Response:")
            function_results = []

            if response.function_calls != None:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, args.verbose)
                    if function_call_result.parts == []:
                        raise Exception("types.Content object is Empty")
                    if function_call_result.parts[0].function_response == None:
                        raise Exception("Function Response Property is None")
                    if function_call_result.parts[0].function_response.response == None:
                        raise Exception("None Response")


                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    
                messages.append(types.Content(role="user", parts=function_results))

                    # print(f"Calling function: {function_call.name}({function_call.args})")
            else:
                print(response.text)
                return

        except Exception as e:
            print(f"Error in generate_content: {e}")
        
        print(f"Maximum iterations reached")
        sys.exit(1)


if __name__ == "__main__":
    main()
