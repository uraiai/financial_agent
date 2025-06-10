import base64
import os
import time
from typing import Optional
from uuid import uuid4

from agno.agent import Agent
from agno.media import ImageArtifact
from agno.tools import Toolkit

from tools.thiri import ThiriClient

class ThiriTools(Toolkit):
    def __init__(
        self,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """Initialize Thiri toolkit for code interpretation and running Python code in a sandbox.

        Args:
            api_key: Thiri API key (defaults to THIRI_API_KEY environment variable)
            download_result: Whether to register the download_result function
        """
        super().__init__(name="thiri_tools", **kwargs)

        self.api_key = api_key or os.environ.get("THIRI_API_KEY")
        if not self.api_key:
            raise ValueError("THIRI_API_KEY not set. Please set the THIRI_API_KEY environment variable.")

        # Create the client
        self.client = ThiriClient(api_key=self.api_key)
        self.sandbox = None

        self.last_execution = None

        # Register the functions based on the parameters
        self.register(self.run_python_code)
        self.register(self.download_file_from_sandbox)

    def run_python_code(self, code: str) -> str:
        """
        Run Python code in an isolated Thiri sandbox environment.

        Args:
            code (str): Python code to execute

        Returns:
            str: Execution results or error message
        """
        try:
            if self.sandbox is None:
                self.sandbox = self.client.create_sandbox()
                time.sleep(5)
            # Execute the code in the sandbox
            execution = self.sandbox.run_code(code)
            time.sleep(5)
            self.last_execution = execution

            # Process results
            results = []

            # Add stdout if available
            if execution.logs['stdout']:
                stdout = ''.join(execution.logs['stdout'])
                results.append(f"STDOUT:\n{stdout}")

            # Add stderr if available
            if execution.logs['stderr']:
                stderr = ''.join(execution.logs['stderr'])
                results.append(f"STDERR:\n{stderr}")
            print(results)

            return '\n'.join(results) if results else "Code executed successfully with no output."

        except Exception as e:
            return f"Error executing code: {str(e)}"

    def download_file_from_sandbox(self, agent: Agent, sandbox_path: str) -> str:
        """
        Download a file from the Thiri sandbox and add it as an artifact if it's an image.

        Args:
            agent: The agent to add the image artifact to if applicable
            sandbox_path: Path to the file in the sandbox

        Returns:
            str: Success message or error message
        """
        if not self.last_execution:
            return "No code has been executed yet"
            
        try:
            # Download the file content as base64
            content_base64 = self.last_execution.download_file(sandbox_path)
            
            # Decode the content
            content = base64.b64decode(content_base64)
            
            # Determine file extension
            _, ext = os.path.splitext(sandbox_path)
            ext = ext.lower()
            
            # Save the file locally with the same name
            local_path = os.path.basename(sandbox_path)
            with open(local_path, "wb") as f:
                f.write(content)
                
            # If it's an image, add it as an artifact
            if ext in ['.png', '.jpg', '.jpeg', '.gif']:
                # Generate a file:// URL for the file
                mime_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif'
                }
                mime_type = mime_types.get(ext, 'application/octet-stream')
                data_url = f"data:{mime_type};base64,{content_base64}"
                
                # Add image artifact to the agent
                image_id = str(uuid4())
                agent.add_image(
                    ImageArtifact(
                        id=image_id, 
                        url=data_url, 
                        original_prompt=f"Downloaded from sandbox: {sandbox_path}"
                    )
                )
                
                return f"Image downloaded and added as artifact with ID {image_id}, saved to {local_path}"
            else:
                return f"File downloaded and saved to {local_path}"
                
        except Exception as e:
            return f"Error downloading file: {str(e)}"
