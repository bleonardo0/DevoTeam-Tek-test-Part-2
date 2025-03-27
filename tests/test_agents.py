import unittest
from agents.multi_agent import demander_agent

class TestAgents(unittest.TestCase):

    def test_programme_formation(self):
        question = "Quels programmes de formation sont adaptés pour améliorer le leadership ?"
        response = demander_agent(question)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

    def test_meilleures_pratiques(self):
        question = "Quelles sont les meilleures pratiques pour la gestion du temps ?"
        response = demander_agent(question)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

    def test_etudes_de_cas(self):
        question = "Peux-tu me donner un exemple réel d'optimisation des coûts opérationnels ?"
        response = demander_agent(question)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

if __name__ == '__main__':
    unittest.main()
