from livekit.agents.llm import FunctionContext, FunctionInfo, FunctionArgInfo
import inspect
import json
from typing import Any

class JSONFunctionContext(FunctionContext):
    def __init__(self, json_definitions: list[dict]):
        super().__init__()
        # Clear out any functions discovered by introspection
        self._fncs.clear()
        # Now load your JSON definitions
        self._load_from_json(json_definitions)

    def _load_from_json(self, json_definitions: list[dict]):
        for fn_def in json_definitions:
            name = fn_def["name"]
            description = fn_def.get("description", "")
            auto_retry = fn_def.get("auto_retry", False)

            # Convert the JSON arguments into FunctionArgInfo
            args_info = {}
            for arg_name, arg_def in fn_def.get("arguments", {}).items():
                python_type = self._json_type_to_python(arg_def["type"])
                args_info[arg_name] = FunctionArgInfo(
                    name=arg_name,
                    description=arg_def.get("description", ""),
                    type=python_type,
                    default=arg_def.get("default", inspect.Parameter.empty),
                    choices=tuple(arg_def["choices"]) if arg_def.get("choices") else None,
                )

            # Create a dummy callable that you can replace with your own logic
            # This could be an HTTP call, a local dispatcher, etc.
            def dynamic_callable(**kwargs):
                # Implement your actual function call logic here
                # For example, send kwargs to a backend system or run local logic
                # returning some result.
                return self._call_external_function(name, kwargs)

            fn_info = FunctionInfo(
                name=name,
                description=description,
                auto_retry=auto_retry,
                callable=dynamic_callable,
                arguments=args_info
            )

            self._fncs[name] = fn_info

    def _json_type_to_python(self, t: str) -> type:
        # Map your JSON types to Python types
        # Example:
        if t == "string":
            return str
        elif t == "int":
            return int
        elif t == "float":
            return float
        elif t == "bool":
            return bool
        elif t == "list_of_strings":
            return list[str]
        # Add more mappings as needed
        else:
            # Default fallback
            return str

    def _call_external_function(self, name: str, kwargs: dict) -> Any:
        # This is the heart of your integration:
        # You must define how to actually call the functions described by the JSON.
        # It could be a call to a microservice, a Python callable in a registry, etc.
        # For now, let's just print and return something mock.
        print(f"Calling external function: {name} with args: {kwargs}")
        # return {"result": f"Mocked result of {name}"}
        return f"I have created a ticket for you with {name}"
    
    def _call_external_function(self, name: str, kwargs: dict) -> str:
        result = self._execute_function(name, kwargs)
        
        # Convert the result to a human-readable string format
        if isinstance(result, (dict, list)):
            formatted_result = json.dumps(result, indent=2)
            return f"Here's the result from {name}:\n{formatted_result}"
        elif isinstance(result, (int, float)):
            return str(result)
        elif result is None:
            return "The operation completed successfully with no return value."
        else:
            return str(result)
        
    def _execute_function(self, name: str, kwargs: dict) -> Any:
        """Execute the actual function logic and return any type of data."""
        print(f"Executing function: {name} with args: {kwargs}")
        if name == "get_ticket_details":
            return {
                "ticket_id": "T-123",
                "status": "open",
                "priority": "high",
                "description": "System outage"
            }
        elif name == "list_open_tickets":
            return [
                {"id": "T-123", "title": "System outage"},
                {"id": "T-124", "title": "Login issues"}
            ]
        elif name == "get_ticket_count":
            return 42
        else:
            return f"Completed operation: {name}"
        
    
