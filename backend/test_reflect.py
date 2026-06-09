import unittest
import math
from reflect import (
    calculate_asp,
    classify_emotion,
    calculate_eds,
    calculate_evi,
    detect_cognitive_distortions,
    calculate_eri
)

class TestReflectAI(unittest.TestCase):

    def test_asp_no_history(self):
        # Default global thresholds
        mean, std_dev, t_pos, t_neg = calculate_asp([])
        self.assertEqual(mean, 0.0)
        self.assertEqual(std_dev, 1.0)
        self.assertEqual(t_pos, 0.1)
        self.assertEqual(t_neg, -0.1)

    def test_asp_with_history(self):
        # Suppose a user is generally positive
        scores = [0.8, 0.7, 0.9, 0.8]
        mean, std_dev, t_pos, t_neg = calculate_asp(scores)
        self.assertEqual(mean, 0.8)
        self.assertTrue(std_dev > 0)
        # T_pos will be capped at 0.8, T_neg at some value
        self.assertTrue(t_pos <= 0.8)
        self.assertTrue(t_neg < mean)
        
    def test_classify_emotion(self):
        t_pos, t_neg = 0.5, -0.5
        self.assertEqual(classify_emotion(0.6, t_pos, t_neg), "Happy")
        self.assertEqual(classify_emotion(-0.6, t_pos, t_neg), "Sad")
        self.assertEqual(classify_emotion(-0.2, t_pos, t_neg), "Anxious")
        self.assertEqual(classify_emotion(0.2, t_pos, t_neg), "Neutral")

    def test_eds(self):
        mean = 0.5
        std_dev = 0.2
        # current score = 0.9, drift = |0.9 - 0.5| / 0.2 = 2.0
        eds = calculate_eds(0.9, mean, std_dev)
        self.assertAlmostEqual(eds, 2.0)

    def test_evi_stable(self):
        emotions = ["Happy", "Happy", "Happy", "Happy"]
        evi = calculate_evi(emotions)
        # max probability of staying in same state is P(Happy, Happy) = 1.0
        # EVI = 1 - 1 = 0
        self.assertEqual(evi, 0.0)

    def test_evi_volatile(self):
        emotions = ["Happy", "Sad", "Happy", "Sad"]
        evi = calculate_evi(emotions)
        # probabilities: Happy->Sad, Sad->Happy. P(i,i) = 0
        # EVI = 1 - 0 = 1.0
        self.assertEqual(evi, 1.0)
        
    def test_cognitive_distortions(self):
        text = "I always fail and this is a terrible disaster. I am worthless."
        count, words = detect_cognitive_distortions(text)
        self.assertTrue(count >= 3)
        self.assertTrue("always" in words)
        self.assertTrue("terrible" in words)
        self.assertTrue("disaster" in words)
        self.assertTrue("fail" in words)
        self.assertTrue("worthless" in words)

    def test_calculate_eri(self):
        # 100% negative entries, high EDS, high distortions
        emotions = ["Sad", "Anxious", "Sad", "Sad"]
        eri = calculate_eri(emotions, d_avg=2.0, k_risk_ratio=1.0)
        # F_neg = 1.0
        # ERI = 0.4*1.0 + 0.3*min(2.0/2, 1.0) + 0.3*1.0 = 1.0
        self.assertAlmostEqual(eri, 1.0)
        
        # 0% negative entries
        emotions_pos = ["Happy", "Happy", "Neutral"]
        eri_low = calculate_eri(emotions_pos, d_avg=0.0, k_risk_ratio=0.0)
        self.assertAlmostEqual(eri_low, 0.0)

    def test_reflection_output_high_eri(self):
        from reflect import generate_reflect_feedback
        feedback = generate_reflect_feedback(eri=0.8, eds=1.0, cpd_count=0, found_distortions=[])
        self.assertIn("Reflection:", feedback)
        self.assertIn("high emotional risk", feedback)

    def test_reflection_output_distortions(self):
        from reflect import generate_reflect_feedback
        feedback = generate_reflect_feedback(eri=0.5, eds=1.0, cpd_count=2, found_distortions=["always", "never"])
        self.assertIn("Reflection:", feedback)
        self.assertIn("absolute thinking", feedback)
        self.assertIn("always", feedback)

    def test_reflection_output_high_eds(self):
        from reflect import generate_reflect_feedback
        feedback = generate_reflect_feedback(eri=0.3, eds=2.0, cpd_count=0, found_distortions=[])
        self.assertIn("Reflection:", feedback)
        self.assertIn("significant shift", feedback)

    def test_reflection_output_stable(self):
        from reflect import generate_reflect_feedback
        feedback = generate_reflect_feedback(eri=0.1, eds=0.5, cpd_count=0, found_distortions=[])
        self.assertEqual("", feedback)

if __name__ == '__main__':
    unittest.main()
