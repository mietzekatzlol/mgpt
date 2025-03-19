# mgpt - A Command-Line AI Assistant
## mgpt – a command-line AI sidekick that blends OpenAI smarts with OpenManus magic. 

Crafted by Marco, with a tiny assist from the Grok-ulator :-)

Think piping data into it for quick AI insights, generating Python scripts on demand, and automating tasks like a pro – all from your terminal. 

Took some late-night debugging, but it’s alive and kicking! 

Hack it, tweak it, clone it, nuke it – it’s all yours to play with! ^^

## Features

• Interactive chat mode with GPT-4o.

• Delegate tasks to OpenManus for script generation and execution.

• Supports piping input and verbose debugging.

• Customizable via environment variables.

## Prerequisites

Before installing mgpt, ensure you have the following:

• Python 3.6+: Installed on your system.

• pip: Python package manager.

• Git: For cloning the repository (optional).

• OpenAI API Key: Required for GPT functionality.

• OpenManus: Optional, for script automation features.

## Installation

### 1. Clone the Repository (Optional)

If you’re installing from GitHub: 

```bash
git clone https://github.com/mietzekatzlol/mgpt.git
```
```bash
cd mgpt
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install openai
```

The openai package is the only direct dependency for basic functionality. If you use OpenManus, additional dependencies may be required (see OpenManus section below).

### 3. Download or Create mgpt.py

• If cloned from GitHub, the script is already in the repository.

• Otherwise, copy the mgpt.py script into your working directory (e.g., ~/mgpt/).

### 4. Make the Script Executable

Set execute permissions: 

```bash
chmod +x mgpt.py
```

## Configuration

### 1. Set Up OpenAI API Key

mgpt requires an OpenAI API key for GPT functionality. Set it as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

• Replace your_openai_api_key_here with your actual key from OpenAI.

• To make this permanent, add the line to your ~/.bashrc, ~/.zshrc, or equivalent shell configuration file.

### 2. Define an Alias in .bashrc

To run mgpt conveniently without typing ./mgpt.py every time, define an alias in your ~/.bashrc:

Open the file:

```bash
nano ~/.bashrc
```

• Add this line at the end (adjust the path to where mgpt.py is located):

```bash
alias mgpt='python3 /home/yourusername/mgpt/mgpt.py'
```

Replace /home/yourusername/mgpt/mgpt.py with the actual path to your mgpt.py.

• Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

• Apply the changes: source ~/.bashrc

Now you can simply type mgpt to run the script from anywhere!

### 3. (Optional) Configure OpenManus

If you want to use OpenManus for script generation and execution:

• Install OpenManus: Follow the official OpenManus documentation to install it. Typically, it’s a Python script (main.py) that you place in a directory (e.g., ~/OpenManus/).

• Update Path: Ensure the openmanus_path variable in mgpt.py points to your OpenManus main.py. Default is:

openmanus_path = "/home/jumpmanjr/OpenManus/main.py"

Edit this line if your path differs:

```bash
nano mgpt.py
```

• Dependencies: OpenManus may require additional packages (e.g., shutil, psutil). Install them as needed:

```bash
pip install psutil
```

### 4. Test the Setup

Verify everything works (after setting the alias):

```bash
mgpt "Hello, how are you?" 
```

Expected output: A response from GPT-4o, like "I'm doing great, thanks! How about you?"

Basic GPT Query

```bash
mgpt "Write a haiku about space" 
```

Output: A haiku generated by GPT-4o.

Interactive Chat Mode

```bash
mgpt --chat
```

OpenManus Task

Generate and execute a script: 

```bash
mgpt -o "write a simple python script that checks disk usage and prints the results, save it as check_disk_usage.py, and execute it"
```

Output:

Content successfully saved to check_disk_usage.py

Total: 343.19 GB

Used: 48.04 GB

Free: 277.65 GB

Add -v for detailed debugging: mgpt -o -v "write a simple python script that says hello, save it, and execute it"

## Notes

• Ensure your OpenAI API key is set before running GPT commands.

• For OpenManus features, confirm the script path and dependencies are correctly configured.

• The script assumes a Unix-like environment (Linux/macOS). For Windows, adjust paths and commands accordingly (e.g., use python mgpt.py instead of mgpt).

## Troubleshooting

• API Key Error: Verify OPENAI_API_KEY is set (echo $OPENAI_API_KEY).

• OpenManus Not Found: Check the openmanus_path in mgpt.py.

• Alias Not Working: Ensure the path in the alias is correct and run source ~/.bashrc.

• No Output: Use -v to debug OpenManus execution.

## Contributing

Feel free to fork this repository, submit issues, or send pull requests on GitHub!

License This project is open-source under the MIT License. Use it freely

