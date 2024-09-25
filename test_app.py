import unittest
import json
from unittest.mock import patch
from main import app
from pydantic import BaseModel, ConfigDict
from content_generator import Article

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.article = None  # Initialize instance variable for article

    @patch('content_generator.openai.Completion.create')
    def test_generate_article(self, mock_openai):
        
        
        # Mock the response from OpenAI API
        mock_openai.return_value = {
            'choices': [
                {'text': 'Generated article content here...'}
            ]
        }

        payload = {
            "topic": "The Future of Renewable Energy",
            "target_audience": "Environmental policymakers and activists",
            "audience_questions": "What are the latest advancements? How can we implement these technologies?",
            "purpose": "To inform about emerging trends and encourage adoption",
            "detail_info": "Include statistics on solar and wind energy growth",
            "length": "800 words",
            "style": "Persuasive"
        }

        response = self.app.post('/generate_article',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.article = Article(**data)  # Store the Article object in the instance variable

            # Mock the response from OpenAI API
        mock_openai.return_value = {
            'choices': [
                {'text': 'Feedback from reviewer...'}
            ]
        }

        # review and edit article
        # feedback from persona
        payload = {
            "article": self.article.model_dump(),
            "persona": "Environmental Scientist",
            "job_description": "Researches and develops sustainable energy solutions"
        }

        response = self.app.post('/provide_feedback',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        # update article from feedback request and use for edit request
        data = json.loads(response.get_data(as_text=True))
        self.article = Article(**data)  # Store the Article object in the instance variable

        payload = {
            "article": self.article.model_dump(),
            "guidance": "Simplify technical terms and focus on actionable steps",
            
        }

        response = self.app.post('/edit_article',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()