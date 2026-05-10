from langchain_community.tools import ShellTool

shell_tool = ShellTool()

results = shell_tool.invoke('git status')

print(results)


"""
ShellTool is a built-in LangChain tool that allows 
an LLM agent to execute shell/terminal commands on
the machine where your Python app is running.
"""