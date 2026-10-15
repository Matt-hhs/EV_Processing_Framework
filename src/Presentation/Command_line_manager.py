from src.Businesslogic.Module_manager import RunCustomModule
from src.Businesslogic.Module_manager import GetFromRegistry
from src.Businesslogic.Workflow_manager import ManageWorkflow

import cmd


class ProcessStatusManager(cmd.Cmd):
    intro = "Running EV_Processing_Framework. For available commands, type help."
    prompt = "> "


    def __init__(self, get_from_registry, run_custom_module, manage_workflow):
        super().__init__()
        self.get_from_registry = get_from_registry
        self.run_custom_module = run_custom_module
        self.manage_workflow = manage_workflow


    def do_pause(self, arg):
        "Pause the current process."
        self.run_custom_module.pause()

    
    def do_resume(self, arg):
        "Resume a paused process."
        self.run_custom_module.resume()


    def do_stop(self, arg):
        "Stop the running process."
        self.run_custom_module.stop()


    def do_exit(self, arg):
        "Stop the running process and exit framework."
        if self.run_custom_module.is_alive():
            self.run_custom_module.stop()
        return True

    do_EOF = do_exit


    def do_get_custom_modules(self, arg):
        "Returns custom modules found in dedicated folder(s)."
        custom_modules = self.get_from_registry.get_custom_module_names_from_registry()

        if not custom_modules:
            print("No modules found!")
            return

        for module in custom_modules:
            print(f"- {module}")


    def do_run_module(self, arg):
        """Run a custom module located in the custom_modules folder by typing: run_module <module_name>"""
        module_name = arg.strip()

        if module_name:
            self.run_custom_module.start(module_name)
        

    def do_create_workflow(self, arg):
        """Create a new workflow with custom name by typing: create_workflow <workflow_name>"""
        workflow_name = arg.strip()

        if not workflow_name:
            return

        self.manage_workflow.create_workflow(workflow_name)
        self.manage_workflow.select_workflow(workflow_name)


    def do_create_step(self, arg):
        """Create a new step continueing from your current step inside the current workflow"""
        self.manage_workflow.create_step()


    def do_select_workflow(self, arg):
        """Select a the workflow you want to work in by typing: select_workflow <workflow_name>"""
        workflow_name = arg.strip()

        if not workflow_name:
            return

        self.manage_workflow.select_workflow(workflow_name)


def main():
    run_custom_module = RunCustomModule()
    manage_workflow = ManageWorkflow()
    get_from_registry = GetFromRegistry()

    ProcessStatusManager(get_from_registry, run_custom_module, manage_workflow).cmdloop()

if __name__ == "__main__":
    main()