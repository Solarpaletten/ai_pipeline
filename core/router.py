class AIRouter:
    def __init__(self):
        self.routes = {'analysis': 'claude', 'coding': 'deepseek'}

    def route_task(self, text: str) -> str:
        return self.routes['analysis'] if 'анализ' in text.lower() else self.routes['coding']
