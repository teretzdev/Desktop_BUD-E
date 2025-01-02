import json
import os

PLAN_FILE_PATH = 'plan.json'

def initialize_plan():
    """Initialize a new plan."""
    plan = {
        "tasks": [],
        "completed_tasks": []
    }
    save_plan(plan)
    print("New plan initialized.")

def save_plan(plan):
    """Save the plan to a JSON file."""
    with open(PLAN_FILE_PATH, 'w') as file:
        json.dump(plan, file, indent=4)

def load_plan():
    """Load the plan from a JSON file."""
    if not os.path.exists(PLAN_FILE_PATH):
        return {"tasks": [], "completed_tasks": []}
    with open(PLAN_FILE_PATH, 'r') as file:
        return json.load(file)

def mark_item_completed(task_id):
    """Mark a task as completed."""
    plan = load_plan()
    if task_id in plan["tasks"]:
        plan["tasks"].remove(task_id)
        plan["completed_tasks"].append(task_id)
        save_plan(plan)
        print(f"Task '{task_id}' marked as completed.")
    else:
        print(f"Task '{task_id}' not found in the plan.")

def update_plan(task_id, task_info):
    """Update the plan with new information."""
    plan = load_plan()
    if task_id not in plan["tasks"]:
        plan["tasks"].append(task_id)
    plan[task_id] = task_info
    save_plan(plan)
    print(f"Task '{task_id}' updated.")

def get_plan():
    """Retrieve the current state of the plan."""
    plan = load_plan()
    print("Current plan state:")
    print(json.dumps(plan, indent=4))
    return plan

def export_plan_to_visualizer_format():
    """Convert the plan data into a format suitable for visualization."""
    plan = load_plan()
    tasks = []
    for task_id, task_info in plan.items():
        if task_id not in ['tasks', 'completed_tasks']:
            task_info['task_id'] = task_id
            tasks.append(task_info)
    return tasks

def export_plan_to_visualizer_format():
    """Convert the plan data into a format suitable for visualization."""
    plan = load_plan()
    tasks = []
    for task_id, task_info in plan.items():
        if task_id not in ['tasks', 'completed_tasks']:
            task_info['task_id'] = task_id
            tasks.append(task_info)
    return tasks

# Example usage
if __name__ == "__main__":
    initialize_plan()
    update_plan("task1", {"description": "Complete the project", "due_date": "2023-12-31"})
    mark_item_completed("task1")
    get_plan()