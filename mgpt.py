#!/usr/bin/env python3
import openai
import sys
import os
import subprocess
import json
import re

# Initialize the OpenAI client with the API key from the environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_gpt(prompt, chat_history=None):
    if chat_history is None:
        chat_history = []
    chat_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history,
        max_tokens=150,
        temperature=0.7
    )
    answer = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": answer})
    return answer, chat_history

def call_openmanus(prompt, verbose=False, additional_inputs=None):
    openmanus_path = "/home/jumpmanjr/OpenManus/main.py"
    cmd = ["python", openmanus_path]
    
    # Dynamic additional inputs based on prompt
    if additional_inputs is None:
        if "save" in prompt.lower() and "execute" in prompt.lower():
            additional_inputs = ["yes"]
        elif "save" in prompt.lower():
            additional_inputs = []
        else:
            additional_inputs = ["Hello World", "yes"]
    
    stdin_input = prompt + "\n" + "\n".join(additional_inputs) + "\n"
    
    if verbose:
        print(f"Executing OpenManus command: {' '.join(cmd)} with prompt via STDIN: '{prompt}'")
        print(f"Additional inputs: {additional_inputs}")
    else:
        print("Calling OpenManus...")
    
    if not os.path.exists(openmanus_path):
        return f"Error: OpenManus path {openmanus_path} does not exist."
    
    try:
        result = subprocess.run(
            cmd,
            input=stdin_input,
            capture_output=True,
            text=True,
            check=True,
            timeout=60
        )
        full_output = (result.stdout + result.stderr).strip()
        # Filter and clean output
        output_lines = []
        for line in full_output.splitlines():
            cleaned_line = line.rstrip()  # Clean each line first
            if "Content successfully saved" in cleaned_line:
                output_lines.append(cleaned_line)
            elif "{'observation':" in cleaned_line:
                # Robust extraction of observation
                match = re.search(r"\{'observation':\s*'([^']*)'\}", cleaned_line)
                if match:
                    obs = match.group(1).strip().replace('\\n', '\n')  # Preserve newlines
                    if verbose:
                        print(f"Debug: Raw observation: {repr(match.group(1))}")
                        print(f"Debug: Cleaned observation: {repr(obs)}")
                    output_lines.append(obs)
                else:
                    output_lines.append(cleaned_line)
        if verbose:
            print(f"Debug: Output lines before join: {repr(output_lines)}")
        output = "\n".join([line.strip() for line in output_lines]).rstrip()
        if verbose:
            print(f"OpenManus stdout: '{result.stdout}'")
            print(f"OpenManus stderr: '{result.stderr}'")
            print("OpenManus completed successfully.")
            print(f"Debug: Final output before return: {repr(output)}")
        return output
    except subprocess.TimeoutExpired as e:
        return f"OpenManus timed out after 60 seconds.\nStdout: '{e.stdout}'\nStderr: '{e.stderr}'"
    except subprocess.CalledProcessError as e:
        return f"OpenManus failed with exit code {e.returncode}.\nStdout: '{e.stdout}'\nStderr: '{e.stderr}'"
    except FileNotFoundError:
        return f"Error: 'python' or OpenManus script not found."

def interactive_chat():
    print("Interactive chat mode activated. Type 'exit' to quit.")
    chat_history = []
    while True:
        try:
            prompt = input("You: ").strip()
            if prompt.lower() == "exit":
                print("Chat ended.")
                break
            if not prompt:
                continue
            if prompt.startswith("openmanus:"):
                task = prompt[10:].strip()
                if ";" in task:
                    parts = task.split(";")
                    task = parts[0].strip()
                    additional_inputs = [x.strip() for x in parts[1:]]
                    answer = call_openmanus(task, verbose=True, additional_inputs=additional_inputs)
                else:
                    answer = call_openmanus(task, verbose=True)
                print(f"OpenManus: {answer}")
            else:
                answer, chat_history = query_gpt(prompt, chat_history)
                print(f"Bot: {answer}")
        except KeyboardInterrupt:
            print("\nChat ended (Ctrl+C).")
            break

def show_help():
    help_text = r"""
 _   .-')                 _ (`-.  .-') _   
( '.( OO )_              ( (OO  )(  OO) )  
 ,--.   ,--.) ,----.    _.`     \/     '._ 
 |   `.'   | '  .-./-')(__...--''|'--...__)
 |         | |  |_( O- )|  /  | |'--.  .--'
 |  |'.'|  | |  | .--, \|  |_.' |   |  |   
 |  |   |  |(|  | '. (_/|  .___.'   |  |   
 |  |   |  | |  '--'  | |  |        |  |   
 `--'   `--'  `------'  `--'        `--'   

mgpt - A masterpiece of digital alchemy, distilled from code and AI magic!

Usage:
  mgpt [OPTIONS] [PROMPT]
  cat file.txt | mgpt [OPTIONS] [PROMPT]

Options:
  --help, -h       Show this help text
  --chat, -c       Start interactive chat mode
  --openmanus, -o  Delegate task to OpenManus (requires OpenManus installation)
  --verbose, -v    Show detailed output for OpenManus execution
  [PROMPT]         The prompt as an argument (combined with piped data if present)

Examples:
  mgpt "Hello, how are you?"              - Single request with prompt
  echo "Hello" | mgpt "What is this?"     - Combines STDIN with argument
  mgpt --chat                             - Starts interactive chat
  mgpt --openmanus "Prioritize my tasks"  - Uses OpenManus for automation
  mgpt -o -v "Write a script"             - OpenManus with verbose output
  mgpt -o "Write a script hello world, save it and execute it" - Save and execute
  mgpt --chat "openmanus: Write a script;yes" - OpenManus with custom inputs
  mgpt --help                             - Shows this help text

Notes:
- Set the API key with: export OPENAI_API_KEY="your_key"
- For --openmanus, ensure OpenManus is installed and configured
- In chat mode: type 'exit' or Ctrl+C to quit; use "openmanus: <task>;<input1>;<input2>" for OpenManus tasks with additional inputs
"""
    print(help_text)

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        sys.exit(0)
    if "--chat" in sys.argv or "-c" in sys.argv:
        interactive_chat()
        sys.exit(0)
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    if "--openmanus" in sys.argv or "-o" in sys.argv:
        stdin_input = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
        prompt = stdin_input + " " + " ".join(sys.argv[1:]) if len(sys.argv) > 1 else stdin_input
        for param in ["--chat", "-c", "--help", "-h", "--openmanus", "-o", "--verbose", "-v"]:
            prompt = prompt.replace(param, "").strip()
        if not prompt:
            print("No prompt provided. Use --help for info.", end='')
            sys.exit(1)
        result = call_openmanus(prompt, verbose=verbose)
        print(result, end='')  # No extra newline from print
        sys.exit(0)
    stdin_input = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    prompt = stdin_input + " " + " ".join(sys.argv[1:]) if len(sys.argv) > 1 else stdin_input
    for param in ["--chat", "-c", "--help", "-h", "--openmanus", "-o", "--verbose", "-v"]:
        prompt = prompt.replace(param, "").strip()
    if not prompt:
        print("No prompt provided. Use --help for info.", end='')
        sys.exit(1)
    result, _ = query_gpt(prompt)
    print(result, end='')
