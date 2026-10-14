from src.Data.Workflow_data_handler import data_handler, step_manager
from pathlib import Path


class ManageWorkflow:
    def __init__(self):
        self.data_handler = Workflow_data_handler.HandleData()
        

    def check_workflow_name(self, workflow_name):
        workflows = self.data_handler.get_workflows()

        for workflow in workflows:
            existing_name = Path(workflow).stem

            if existing_name == workflow_name:
                return True

        return False


    def create_workflow(self, workflow_name):
        if self.check_workflow_name(workflow_name):
            print("Workflow name already exists")
        else:
            data_handler.workflow_creation(workflow_name)

    def select_workflow(self, filename):
        data_handler.open_workflow(filename)