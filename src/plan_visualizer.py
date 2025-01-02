import json
import plotly.express as px
import pandas as pd
from datetime import datetime

def read_plan(file_path='plan.json'):
    """Read the plan data from a JSON file."""
    with open(file_path, 'r') as file:
        plan = json.load(file)
    return plan

def generate_gantt_chart(plan):
    """Generate a Gantt chart from the plan data."""
    tasks = []
    for task_id, task_info in plan.items():
        if task_id not in ['tasks', 'completed_tasks']:
            start_date = datetime.strptime(task_info['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(task_info['due_date'], '%Y-%m-%d')
            tasks.append({
                'Task': task_id,
                'Start': start_date,
                'Finish': end_date,
                'Resource': 'Completed' if task_id in plan['completed_tasks'] else 'Pending'
            })

    df = pd.DataFrame(tasks)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource", title="Software Development Plan")
    fig.update_yaxes(categoryorder="total ascending")
    fig.show()

def main():
    """Main function to read the plan and generate a Gantt chart."""
    plan = read_plan()
    generate_gantt_chart(plan)

if __name__ == "__main__":
    main()
