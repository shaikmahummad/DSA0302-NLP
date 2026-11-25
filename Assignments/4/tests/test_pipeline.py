import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import run_assignment as a
class PipelineTests(unittest.TestCase):
 def test_inference(self): self.assertIn("PensionBeneficiary(F1)",a.infer_service())
 def test_service_threshold(self): self.assertIn("ServiceConditionMet(E1)",a.infer_service())
 def test_lesk(self): self.assertEqual(a.lesk("qualifying employment pension years","service")["selected"],"qualifying_service")
 def test_retrieval(self): self.assertEqual(a.search("commutation pension",a.build_index(a.DOCS))[0][1],"CIRC_03")
 def test_ner(self): self.assertTrue(a.ner("Employee E-104")["EMPLOYEE_ID"])
if __name__=="__main__": unittest.main()
