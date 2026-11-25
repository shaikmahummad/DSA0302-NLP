import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import run_assignment as a

class TestAssignment(unittest.TestCase):
    def test_segment(self):
        self.assertEqual(len(a.segment("The road is closed. Therefore use the bypass.")),2)
    def test_frame(self):
        s,msg=a.frame_manager("I am near Market Road")
        self.assertIn("location",s)
    def test_realizer(self):
        self.assertEqual(a.realize({"type":"road","name":"East Bridge","status":"closed"}),"East Bridge is closed.")
    def test_ibm1(self):
        r=a.ibm1_one_iteration("road closed","சாலை மூடப்பட்டது")
        self.assertTrue(r["probabilities"])
    def test_cancel(self):
        s,msg=a.frame_manager("cancel")
        self.assertEqual(s["status"],"cancelled")

if __name__=="__main__": unittest.main()
