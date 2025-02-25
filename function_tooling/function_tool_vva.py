from livekit.agents.llm import FunctionContext, FunctionInfo, FunctionArgInfo
import inspect
from typing import Any
import json

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  
from function_tooling.function_handelling import function_handler


'''
Called by Agent(TTS/S2S) to pass the JSON definition function
We also pass the user phone-number during initialization 
'''


class ServiceDeskFunctionContext(FunctionContext):
    def __init__(self, json_definitions: list[dict], phone_number: str = None, servicenow=None, ms365group=None):
        super().__init__()
        self._fncs.clear()
        self._phone_number = phone_number
        
        from function_tooling.function_handelling import init_function_handler
        init_function_handler(servicenow, ms365group)

        self._load_from_json(json_definitions)
        

    def _load_from_json(self, json_definitions: list[dict]):
        for fn_def in json_definitions:
            name = fn_def["name"]
            description = fn_def.get("description", "")

            # Add auto_retry with a default value of False if not specified
            auto_retry = fn_def.get("auto_retry", False)
            
            # Handle parameters if they exist
            args_info = {}
            if "parameters" in fn_def:
                properties = fn_def["parameters"].get("properties", {})
                required = fn_def["parameters"].get("required", [])
                
                for arg_name, arg_def in properties.items():
                    python_type = self._json_type_to_python(arg_def["type"])
                    default = inspect.Parameter.empty if arg_name in required else None
                    
                    args_info[arg_name] = FunctionArgInfo(
                        name=arg_name,
                        description=arg_def.get("description", ""),
                        type=python_type,
                        default=default,
                        choices=tuple(arg_def.get("enum", [])) if "enum" in arg_def else None
                    )

            # Create a closure to capture the correct name
            def create_callable(func_name: str):
                async def dynamic_callable(**kwargs):
                    return await self._call_external_function(func_name, kwargs)
                return dynamic_callable

            fn_info = FunctionInfo(
                name=name,
                description=description,
                auto_retry=auto_retry,  
                callable=create_callable(name),
                arguments=args_info
            )

            self._fncs[name] = fn_info


    def _json_type_to_python(self, t: str) -> type:
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        return type_mapping.get(t, str)

    async def _call_external_function(self, name: str, kwargs: dict) -> str:
        """Execute the function and format the response appropriately."""
        kwargs['phone_number'] = self._phone_number
        result = await self._execute_function(name, kwargs)
        return self._format_response(name, result)
    

    async def _execute_function(self, name: str, kwargs: dict) -> Any:        
        print(f"Executing {name} with arguments: {kwargs}")
        responce = await function_handler(name, kwargs)

        return str(responce)

    def _format_response(self, name: str, result: Any) -> str:
        if isinstance(result, dict):
            formatted_result = json.dumps(result, indent=2)
            return f"Result from {name}:\n{formatted_result}"
        elif isinstance(result, list):
            if name.startswith("get_") and name.endswith("_troubleshooting"):
                return "Here are the troubleshooting steps:\n" + "\n".join(result)
            return f"Results from {name}:\n" + "\n".join(f"- {item}" for item in result)
        else:
            return str(result)