import json
from pathlib import Path


class HandleData:
    def get_workflow_folder(self):
        current_file = Path(__file__).resolve()

        project_folder = current_file.parents[2]
        return project_folder / "workflows"


    def get_workflow_path(self, workflow_name):
        return self.get_workflow_folder() / f"{workflow_name}.json"


    def open_workflow(self, filename):
        path = self.get_workflow_path(filename)

        if not path.exists():
            raise FileNotFoundError(f"Workflow file {filename} does not exist")

        with open(path, "r", encoding="utf-8") as file:
            self.workflow = json.load(file)

        self.workflow_name = filename


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
        if self.get_workflow_path(workflow_name).exists():
            raise FileExistsError(f"Workflow {workflow_name} already exists")

        workflow_creation_data = {
            "current_step": "root",
            "root": {
                "id": "root",
                "module": None,
                "children": []
            }
        }

        self.write_in_workflow(workflow_name, workflow_creation_data)


