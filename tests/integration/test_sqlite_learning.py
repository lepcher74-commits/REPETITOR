from datetime import datetime,timezone
from repetitor.domain import AttemptEvidence,KnowledgeState,ReviewItem
from repetitor.persistence import SQLiteLearningRepository
NOW=datetime(2026,9,30,12,0,tzinfo=timezone.utc)
def test_state_and_review_survive_reopen(tmp_path):
 db=tmp_path/"learning.sqlite3";r=SQLiteLearningRepository(db);r.initialize();r.add_attempt(AttemptEvidence("a","s","p","k",NOW,True,"independent"));r.save_state(KnowledgeState("s","k",.7,.6,.8,.3,.4,4,NOW));r.save_review(ReviewItem("s","k",NOW,"test"));r2=SQLiteLearningRepository(db);s=r2.get_state("s","k");assert s is not None and s.mastery==.7;assert r2.due_reviews("s",NOW)[0].skill_id=="k"
