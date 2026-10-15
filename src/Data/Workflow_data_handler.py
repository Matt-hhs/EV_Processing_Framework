import json
from pathlib import Path


class HandleData:
    def __init__(self):
        self.workflow = None
        self.workflow_name = None


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
        with open(self.get_workflow_path(workflow_name), "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        self.workflow = data
        self.workflow_name = workflow_name


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


class ManageSteps:
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager


    def get_workflow(self):
        return self.workflow_manager.workflow

    
    def create_step(self):
        workflow = self.get_workflow()

        if workflow is None:
            raise ValueError(f"No workflow selected! Select a workflow first by typing: select_workflow <workflow_name>")
        
        parent = self.find_step(workflow["current_step"])

        if parent is None:
            raise ValueError(f"Current step {workflow['current_step']} does not exist")

        number = len(parent["children"]) + 1

        if parent["id"] == "root":
            step_id = str(number)
        else:
            step_id = parent["id"] + "." + str(number)

        parent["children"].append({
            "id": step_id,
            "module": None,
            "status": "Open",
            "children": []
        })

        workflow["current_step"] = step_id

        self.workflow_manager.write_in_workflow(self.workflow_manager.workflow_name, workflow)


    def set_step_status(self, status):
        statuses = ["Success", "Processing", "Open", "Failed"]

        if status not in statuses:
            raise ValueError(f"Status needs to be one of {statuses}, {status} is not in there!")
        
        workflow = self.get_workflow()
        print(f"selected workflow: {workflow}")
        step_id = workflow["current_step"]
        step = self.find_step(step_id)
        print(f"step id is {step_id}")

        if step is None:
            raise ValueError(f"Step {step_id} does not exist")

        step["status"] = status

        self.workflow_manager.write_in_workflow(self.workflow_manager.workflow_name, workflow)


    def set_step_module(self, module_name):
        workflow = self.get_workflow()
        step_id = workflow["current_step"]
        step = self.find_step(step_id)

        if step is None:
            raise ValueError(f"Step {step_id} does not exist")

        step["module"] = module_name

        self.workflow_manager.write_in_workflow(self.workflow_manager.workflow_name, workflow)


    def set_step_output_type(self, output_type):
        workflow = self.get_workflow()
        step = self.find_step(workflow["current_step"])

        if step is None:
            raise ValueError(f"Step {workflow['current_step']} does not exist")

        step["output_type"] = output_type

        self.workflow_manager.write_in_workflow(self.workflow_manager.workflow_name, workflow)


    def get_parent_output_type(self):
        workflow = self.get_workflow()
        step_id = workflow["current_step"]

        if "." in step_id:
            parent = self.find_step(step_id.rsplit(".", 1)[0])
        else:
            parent = self.find_step("root")

        return parent.get("output_type")


    def find_step(self, step_id):
        node = self.get_workflow()["root"]

        if step_id == "root":
            return node

        for number in step_id.split("."):
            index = int(number) - 1

            if not 0 <= index and index < len(node["children"]):
                return None

            node = node["children"][index]

        return node


data_handler = HandleData()
step_manager = ManageSteps(data_handler)