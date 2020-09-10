"""Application constants file
"""
import os

APP_LOG_FORMAT = "[%(asctime)s %(filename)s:%(lineno)s %(levelname)-2s %(funcName)20s()] %(message)s"
APP_PATH = os.path.dirname(os.path.abspath(__file__))
APP_PATH = APP_PATH.replace("config", "")
APP_LOG_FILENAME = APP_PATH + "log/application.log"
CANDIDATES = "Candidates"
NEO_BATCHES = "NeoBatches"
CANDIDATE_REG_ENROLL_DETAILS = "CandidateRegEnrollDetails"
CANDIDATE_REG_ENROLL_NON_MANDATORY_DETAILS = "CandidateRegEnrollNonMandatoryDetails"
CANDIDATE_INTERVENTIONS = "CandidateInterventions"
CANDIDATE_INTERVENTION_TRACKER = "CandidateInterventionTracker"
MAP_CANDIDATE_INTERVENTION_SKILLING = "MapCandidateInterventionSkilling"
ECP_COUNT = "ECPCount"
CANDIDATE_AGE_RANGE = "CandidateAgeRange"
CUSTOMER_CANDIDATE_DATA = "CustomerCandidateData"
