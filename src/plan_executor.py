import time
from plan_manager import load_plan, mark_item_completed, save_plan

def execute_tasks():
    """Execute tasks sequentially from the plan."""
    plan = load_plan()
    tasks = plan.get("tasks", [])

    if not tasks:
        print("No tasks to execute.")
        return

    for task_id in tasks:
        # Simulate task execution
        print(f"Executing task: {task_id}")
        time.sleep(1)  # Simulate time taken to execute a task

        # Mark task as completed
        mark_item_completed(task_id)

    # Save the updated plan
    save_plan(plan)
    print("All tasks executed and marked as completed.")

def main():
    """Main function to execute tasks."""
    print("Starting task execution...")
    execute_tasks()

if __name__ == "__main__":
    main()
