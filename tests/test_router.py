import unittest
from core.router import AIRouter

class TestRouter(unittest.TestCase):
    def test_route_analysis(self):
        self.assertEqual(AIRouter().route_task("Анализ данных"), "claude")
        self.assertEqual(AIRouter().route_task("Напиши код"), "deepseek")

if __name__ == "__main__":
    unittest.main()
