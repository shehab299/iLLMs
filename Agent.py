from typing import List
import Tool
import json

class Agent:

    def __init__(
            self, 
            client, 
            name: str, 
            role: str, 
            system_message_file: str, 
            tools: List[Tool.Tool] = None
        ):
        
        self.name = name
        self.role = role

        self.tools = tools if tools is not None else []
        self.tools_dict = {tool.func.__name__: tool for tool in self.tools}
        
        self.system_message_template = self.load_system_message(system_message_file)
        self.system_message = self.system_message_template.format(
            agent_info=f"Name: {self.name}\nRole: {self.role}", 
            tools_info="\n".join(tool.info for tool in self.tools)
        )

        self.messages = []
        self.messages.append({
            "role": "system",
            "content": self.system_message
        })

        self.client = client

    def load_system_message(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"System message file '{filename}' not found.")

    def add_tool(self, tool):

        if isinstance(tool, Tool.Tool):

            self.tools.append(tool)
            self.tools_dict[tool.func.__name__] = tool
            
            self.system_message = self.system_message_template.format(
                agent_info=f"Name: {self.name}\nRole: {self.role}", 
                tools_info="\n".join(tool.info for tool in self.tools)
            )

            self.messages[0]["content"] = self.system_message

        else:
            raise TypeError("Tool must be an instance of Tool class.")
        
    def call_tool(self, tool_name, args):

        if tool_name in self.tools_dict:
            tool = self.tools_dict[tool_name]
            try:
                result = tool(*args)
                return result
            except Exception as e:
                return f"Error calling tool '{tool_name}': {str(e)}"
        
        return "Tool not found! Please find another tool or check the tool name."
    
    def __call__(self, message, max_iterations=10):
         
        if message:
            self.messages.append({"role": "user", "content": message})

        counter = 0

        while counter < max_iterations:

            result = self.execute()

            if self.verbose:
                print(f"Iteration {counter + 1}: {result}")
            
            self.messages.append({"role": "assistant", "content": result}) 

            try:
                result_obj = json.loads(result)
            except json.JSONDecodeError as e:
                result_obj = {"state": "Nothing"}

            if result_obj["state"] == "Answer":
                return result_obj["payload"]
            
            elif result_obj["state"] == "Action":

                observation = self.call_tool(result_obj["payload"], result_obj.get("args") or [])

                if self

                self.messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "state": "Observation",
                        "payload": observation
                    })
                })

            counter += 1    

        raise RuntimeError("Max iterations exceeded without reaching an Answer.")

    def execute(self):

        completetion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama3-70b-8192"
        )

        return completetion.choices[0].message.content
    