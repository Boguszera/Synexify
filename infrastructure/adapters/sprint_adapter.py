# infrastructure/adapters/sprint_adapter.py
def sprint_to_dict(sprint):
    return {
        "id": sprint.get_id(),
        "name": sprint.get_name(),
        "start_date": getattr(sprint, "_start_date", None),
        "end_date": getattr(sprint, "_end_date", None),
        "project_id": sprint.get_project_id(),
        "task_ids": sprint.get_task_ids(),
    }
