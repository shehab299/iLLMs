import inspect
from typing import Any, get_type_hints

class Tool:

    def __init__(self, func):
        self.func = func
        self.info = self.getToolInfo(func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)  
            
    def getToolInfo(self, func):
    
        sig = inspect.signature(func)
        hints = get_type_hints(func)
    
        desc = func.__doc__ or "No description available."
    
        params = " \n\t " + " \n\t ".join(
            f"{name}: {hints.get(name, Any).__name__ if hasattr(hints.get(name, Any), '__name__') else str(hints.get(name, Any))}"
            for name in sig.parameters
        )

        return_type = hints.get("return", Any)
        return_type_str = return_type.__name__ if hasattr(return_type, "__name__") else str(return_type)

        return f"""Function Name: {func.__name__}
    Description: {desc}
    Parameters: {params}
    Return Type: {return_type_str}
    Example Usage: {func.__name__}({', '.join(sig.parameters.keys())})
    """


def tool(func):
    return Tool(func)





