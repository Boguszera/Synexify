def project_to_dict(project):
    return {
        "id": project.get_id(),
        "name": project.get_name(),
        "description": project.get_description(),
        "member_ids": project.get_member_ids(),
        "task_ids": project.get_task_ids(),
        "sprint_ids": project.get_sprint_ids(),
        "archived": project.get_archived(),
    }
