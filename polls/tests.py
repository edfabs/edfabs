from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for question whose pub_date
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
