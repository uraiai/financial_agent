import os
import time
import base64
import json
import requests
import sseclient
import threading
from agno.utils.log import log_info, log_debug, log_error

class ThiriClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.thiri_base_url = os.environ.get('THIRI_API_BASE', 'https://api.thiri.dev/api')
    
    def url_for(self, path):
        return f"{self.thiri_base_url}{path}"
    
    # This method is kept for API compatibility but not used internally
    def make_request(self, path, options=None):
        if options is None:
            options = {}
        
        url = self.url_for(path)
        
        headers = {
            'Content-Type': 'application/json',
            'X-THIRI-KEY': self.api_key
        }
        
        if 'headers' in options:
            headers.update(options['headers'])
        
        method = options.get('method', 'GET')
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=options.get('body'),
                params=options.get('params')
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as error:
            raise error
    
    def create_sandbox(self):
        response = requests.post(
            self.url_for('/vms'),
            headers={
                'Content-Type': 'application/json',
                'X-THIRI-KEY': self.api_key
            }
        )
        
        if not response.ok:
            raise Exception(f"Failed to create sandbox: {response.status_code} {response.reason}")
        
        result = response.json()
        
        # Wait a moment for the sandbox to initialize
        time.sleep(1)
        
        return Sandbox(result['id'], self)


class Sandbox:
    def __init__(self, id, client):
        self.id = id
        self.client = client
        self.execution = None
    
    # run code in the sandbox
    def run_code(self, code):
        code64 = base64.b64encode(code.encode()).decode()
        
        response = requests.post(
            self.client.url_for(f"/vms/{self.id}/gateway/execute"),
            headers={
                'Content-Type': 'application/json',
                'X-THIRI-KEY': self.client.api_key
            },
            json={
                'code': code64
            }
        )
        
        if not response.ok:
            raise Exception(f"Failed to run code: {response.status_code} {response.reason}")
        
        data = response.json()
        
        # Create execution object
        execution = Execution(data['execution_id'], self)
        
        # Handle SSE for stdout and stderr in a separate thread
        try:
            def listen_for_events(execution):
                log_info("Listening for events...")
                time.sleep(1)
                headers = {'X-THIRI-KEY': self.client.api_key}
                url = self.client.url_for(f"/vms/{self.id}/gateway/executions/{data['execution_id']}/events")
                
                response = requests.get(url, headers=headers, stream=True)
                client = sseclient.SSEClient(response)
                
                for event in client.events():
                    if event.event == 'stdout' and execution:
                        log_debug(f"stdout: {event.data}")
                        execution.logs['stdout'].append(event.data)
                    elif event.event == 'stderr' and execution:
                        log_debug(f"stderr: {event.data}")
                        execution.logs['stderr'].append(event.data)
            
            # Start event listener in a separate thread
            thread = threading.Thread(target=listen_for_events, args=[execution])
            thread.daemon = True
            thread.start()
            
        except Exception as error:
            print(f"Error setting up event source: {error}")
        
        return execution


class Execution:
    def __init__(self, id, sandbox):
        self.id = id
        self.sandbox = sandbox
        self.logs = {
            'stdout': [],
            'stderr': []
        }
    
    # Returns file content as base64
    def download_file(self, path):
        url = self.sandbox.client.url_for(f"/vms/{self.sandbox.id}/gateway/executions/{self.id}/download/{path}")
        
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'X-THIRI-KEY': self.sandbox.client.api_key
            }
        )
        
        if not response.ok:
            raise Exception(f"Failed to download file: {response.status_code} {response.reason}")
        
        resp_content = response.json()
        return resp_content['content']
