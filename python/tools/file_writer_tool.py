import os
import asyncio
from dataclasses import dataclass
from python.helpers.tool import Tool, Response
from python.helpers import files
from python.helpers.print_style import PrintStyle

@dataclass
class State:
    pass

class FileWriter(Tool):

    async def execute(self, **kwargs):
        await self.agent.handle_intervention()  # wait for intervention and handle it, if paused

        file_path = self.args['file_path']
        content = self.args['content']

        if file_path.startswith('/'):
            return Response(message="Error: file_path must not start with a '/'.", break_loop=False)

        root_path = files.get_abs_path("work_dir")
        full_path = os.path.join(root_path, file_path)
        PrintStyle(font_color="#FF0000", bold=True).print("root path is %s" % root_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        PrintStyle(font_color="#FF0000", bold=True).print("full path is %s" % full_path)

        with open(full_path, 'w') as file:
            file.write(content)

        response = f"Content successfully written to {file_path}"
        return Response(message=response, break_loop=False)

    async def before_execution(self, **kwargs):
        await self.agent.handle_intervention()  # wait for intervention and handle it, if paused
        PrintStyle(font_color="#1B4F72", padding=True, background_color="white", bold=True).print(f"{self.agent.agent_name}: Using tool '{self.name}':")
        self.log = self.agent.context.log.log(type="file_write", heading=f"{self.agent.agent_name}: Using tool '{self.name}':", content="", kvps=self.args)
        if self.args and isinstance(self.args, dict):
            for key, value in self.args.items():
                PrintStyle(font_color="#85C1E9", bold=True).stream(self.nice_key(key)+": ")
                PrintStyle(font_color="#85C1E9", padding=isinstance(value,str) and "\n" in value).stream(value)
                PrintStyle().print()

    async def after_execution(self, response, **kwargs):
        msg_response = self.agent.read_prompt("fw.tool_response.md", tool_name=self.name, tool_response=response.message)
        await self.agent.append_message(msg_response, human=True)