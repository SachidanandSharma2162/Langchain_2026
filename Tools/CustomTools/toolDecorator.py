## Custom Tools

from langchain_core.tools import tool

# Step 1 - create a function
# Step 2 - add type hints
# Step 3 - add tool decorator

@tool # tool decorator
def multiply(a: int, b:int) -> int:
    """Multiply two numbers""" # must be given a description.
    return a*b

result = multiply.invoke({"a":3, "b":5})

print(result)
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.args_schema.model_json_schema())

"""
when you sent reequest to LLM through tools it looks like:

{
  "description": "Multiply two numbers",
  "properties": {
    "a": {
      "title": "A",
      "type": "integer"
    },
    "b": {
      "title": "B",
      "type": "integer"
    }
  },
  "required": ["a", "b"],
  "title": "multiply",
  "type": "object"
}
"""