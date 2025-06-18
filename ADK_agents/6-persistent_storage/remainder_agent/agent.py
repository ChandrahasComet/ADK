from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


# Tools
# Add remainder
def add_remainder(remainder:str, tool_context: ToolContext) -> dict:
    """
    Add a new remainder to the remainder list
    Args:
        remainder: The remainder to add
        tool_context: Context for accessing and updating the session state
    
    Returns:
    A confirmation message
    """
    # get current remainders from state
    remainders = tool_context.state.get("remainders",[])
    # add new remainder to the list
    remainders.append(remainder)
    # update the state
    tool_context.state["remainders"] = remainders
    return {
        "action": "add_remainder",
        "remainder": remainder,
        "message": f"Added remainder: {remainder}"
    }

# View remainder tool

def view_remainders(tool_context: ToolContext) -> dict:
    """
    View the current remainders
    Args:
        tool_context: Context for accessing and updating the session state

    Returns:
    A list of remainders
    """
    # get current remainders from state
    remainders = tool_context.state.get("remainders",[])
    return {
        "action": "view_remainders",
        "remainders": remainders,
        "message": f"Current remainders: {remainders}",
        "count": len(remainders)
    }

#update remainder tool
def update_remainder(index:int, updated_text:str, tool_context: ToolContext) -> dict:
    """
    Update a remainder in the remainder list
    Args:
        index: The 1-based index of the remainder to update
        updated_text: The updated text for the remainder
        tool_context: Context for accessing and updating the session state
    Returns:
    A confirmation message
    """
    # get current remainders from state
    remainders = tool_context.state.get("remainders",[])
    # check if index is valid
    if not remainders or index < 1 or index > len(remainders):
        return {
            "action": "update_remainder",
            "status": "error",
            "message": "Could not find remainder at position {index}"
        }
    
    #update the remainder(adjusting for 0-based indices)
    old_remainder = remainders[index - 1]
    remainders[index - 1] = updated_text

    #Update state with the modified list
    tool_context.state["remainders"] = remainders

    return {
        "action": "update_remainder",
        "index": index,
        "old_remainder": old_remainder,
        "updated_text": updated_text,
        "message": f"Updated remainder at position {index} from '{old_remainder}' to '{updated_text}'"
    }

# Delete remainder tool
def delete_remainder(index:int, tool_context: ToolContext) -> dict:
    """
    Update a remainder in the remainder list
    Args:
        index: The 1-based index of the remainder to update
        tool_context: Context for accessing and updating the session state
    Returns:
    A confirmation message
    """
    #get current remainders from state
    remainders = tool_context.state.get("remainders",[])
    #check if index is valid
    if not remainders or index < 1 or index > len(remainders):
        return {
            "action": "delete_remainder",
            "status": "error",
            "message": "Could not find remainder at position {index}"
            }
    #delete the remainder(adjusting for 0-based indices)
    delete_remainder = remainders.pop(index - 1)
    #update state with the modified list
    tool_context.state["remainders"] = remainders
    return {
        "action": "delete_remainder",
        "index": index,
        "deleted_remainder": delete_remainder,
        "message": f"Deleted remainder at position {index}: {delete_remainder}"
    }

#update username
def update_username(name:str, tool_context: ToolContext) -> dict:
    """
    Update the user's name
    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating the session state
    Returns:
    A confirmation message
    """
    #get curretn aname from state
    old_name = tool_context.state.get("user_name", "")

    #update the name
    tool_context.state["user_name"] = name

    return {
        "action": "update_username",
        "old_name": old_name,
        "name": name,
        "message": f"Updated user's name to {name}"
    }

        
        
        
        
        
remainder_agent = Agent(
    name = "remainder_agent",
    model = "gemini-2.0-flash",
    description = "A remainder agent that views, updates, adds, and deletes remainder from the database",
    instruction = """
    You are a helpful AI assistant that helps manages the remainder of the users.
    You have the funtionality of viewing, updating, adding, and deleting remainder from the user's own database/collection.

    Here are some of the details of the user
    Users name is : {user_name}
    and his remainders are ; {user_remainders}

    Your main job is to manage the remainders of the user based on their query
    You have the following capabilities:
    1. Add new remainders
    2. View existing remainders
    3. Update remainders
    4. Delete remainders
    5. Update the username

    Always be friendly and address the user by their name. 

    **REMINDER MANAGEMENT GUIDELINES:**
    
    When dealing with reminders, you need to be smart about finding the right reminder:
    
    1. When the user asks to update or delete a reminder but doesn't provide an index:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"), 
         look through the reminders to find a match
       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on
    
    4. For viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some
    
    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" → add_reminder("buy milk"))
    
    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which reminder the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
""",
    tools = [
        add_remainder,
        view_remainders,
        update_remainder,
        delete_remainder,
        update_username
    ]
)