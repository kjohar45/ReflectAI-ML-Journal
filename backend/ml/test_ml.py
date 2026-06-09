import unittest
from predict import clean_text, predict_emotion

class TestMLPipeline(unittest.TestCase):
    def test_clean_text(self):
        # Test lowercase
        self.assertEqual(clean_text("HELLO"), "hello")
        
        # Test punctuation removal
        self.assertEqual(clean_text("hello, world!"), "hello world")
        
        # Test stopword removal
        self.assertEqual(clean_text("this is a test sentence"), "test sentence")

    def test_predict_emotion_structure(self):
        # Test result structure on a sample
        res = predict_emotion("I feel great today!")
        
        # Check output keys
        self.assertIn("predicted_emotion", res)
        self.assertIn("confidence_score", res)
        self.assertIn("emotion_probabilities", res)
        
        # Check mapped emotion types
        self.assertIsInstance(res["predicted_emotion"], str)
        self.assertIsInstance(res["confidence_score"], float)
        self.assertIsInstance(res["emotion_probabilities"], dict)
        
        # Verify emotion mapping labels
        expected_emotions = ["sadness", "joy", "love", "anger", "fear", "surprise"]
        for emotion in expected_emotions:
            if res["predicted_emotion"] != "neutral":  # If model is loaded
                self.assertIn(emotion, res["emotion_probabilities"])
                self.assertIsInstance(res["emotion_probabilities"][emotion], float)

if __name__ == "__main__":
    unittest.main()
