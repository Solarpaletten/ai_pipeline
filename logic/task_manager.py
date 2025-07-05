from storage.models import Task

class TaskManager:
    @staticmethod
    def create_task(user_id: int, ai_type: str):
        return Task(user_id=user_id, ai_type=ai_type)
