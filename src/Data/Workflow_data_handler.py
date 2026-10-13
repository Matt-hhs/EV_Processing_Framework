import json
from pathlib import Path


class HandleData:
    def get_workflow_folder(self):
        current_file = Path(__file__).resolve()

        project_folder = current_file.parents[2]
        return project_folder / "workflows"


    def write_in_workflow(self, workflow_name, data):
        with workflow_name.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


    def get_workflows(self):
        workflow_files = []

        workflows_folder = self.get_workflow_folder()

        for file in workflows_folder.iterdir():
            workflow_files.append(file)

        return workflow_files


    def workflow_creation(self, workflow_name):
        workflow = workflow_name + ".json"

        file_path = self.get_workflow_folder() / workflow
        workflow_creation_data = {}

        self.write_in_workflow(file_path, workflow_creation_data)