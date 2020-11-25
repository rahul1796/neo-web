displaymsg=""

Base_URL="https://neo.labournet.in"
#Base_URL="http://127.0.0.1:5000"
app_host = "127.0.0.1"
app_port = "5000"

################ live
conn_str = "DRIVER={SQL SERVER};server=EC2AMAZ-0UO2K5U\SQLEXPRESS;database=NEO;uid=sa;pwd=p@$$w0rd"
SessionTimeOut=50

secret_key = 'LN-NEO-Skills-Web-Structured_UAT'

tma_stage_log_image_path='{}/data/TMA/trainer_stage_images/'.format(Base_URL)
tma_candidate_image_path='{}/data/TMA/attendance_images/'.format(Base_URL)

neo_report_file_path = 'C:/SITES/NEO_SKILLS/'
neo_report_file_path_web = '{}/report file/'.format(Base_URL)

UAP_API_BASE_URL ='https://uap-api.certiplate.com/json/syncreply/'
NAVRITI_SPOC_EMAIL = 'naveen.r@navriti.com'
NAVRITI_ASSESSMENT_EMAIL_CC = ['prathanickam.d@labournet.in','vinod.p@labournet.in','neo.helpdesk@labournet.in','baibhaw.p@navriti.com','arun.paul@navriti.com']

html_email_msg_uap_batch_creation = '''
    <div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">Dear <b>{},</b><br>
    <br>
    Greetings from LabourNet!
    <br><br>
    An assessment is scheduled and the details are below,
    <br><br>
    UAP Request ID : <b>{}</b>
    <br>
    Batch ID : <b>{}</b>
    <br>
    Center : <b>{}</b>
    <br>
    Course : <b>{}</b>
    <br>
    Customer : <b>{}</b>
    <br>
    Assessment proposed date : <b>{}</b>
    <br><br>
    For any further details visit the URL <b>https://uap.certiplate.com/</b> or contact LN POC.
    </p>
    </div>
    <br>

    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">
    Best Regards,<br>
    <b>LN Assessment Team</b> </p>
    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>

    <div>
    <!--p style="font-size:12pt;font-family:Times New Roman,serif;margin:0 0 12pt 0;">&nbsp;</p-->
    <p align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <i>This is an auto generated e-mail. Please do not reply to this mail.</i></p>
    </div>
    <br>
    '''


    ############################################################################3 
html_email_msg_certification_stage_change= '''
    <div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">Dear <b>{},</b><br>
    <br>
    Greetings from NEO Team!
    <br><br>
    Certification Stage is changed for the batch <b>{}</b> to <b>{}</b> by <b>{}</b> ,
    <br><br>
   
    For any further details visit the URL <b>https://neo.labourmet.in/</b> .
    </p>
    </div>
    <br>

    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">
    Best Regards,<br>
    <b>NEO Team</b> </p>
    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>

    <div>
    <!--p style="font-size:12pt;font-family:Times New Roman,serif;margin:0 0 12pt 0;">&nbsp;</p-->
    <p align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <i>This is an auto generated e-mail. Please do not reply to this mail.</i></p>
    </div>
    <br>
    '''

bulk_upload_path = 'C:/SITES/NEO_SKILLS/Bulk Upload/'

DownloadcandidateResultPathLocal='C:/SITES/NEO_SKILLS/Downloads/Candidates/'
DownloadcandidateResultPathWeb='{}/Downloads/Candidates/'.format(Base_URL)
AssessmentCandidateResult="Assessment_Candidate_Result_"
AssessmentCandidateResultUploadTemplate="Assessment_Result_Upload_Template_"
BatchReportFileName="Customer_Contract_Report_"
BatchStatusReportFileName="Batch_Status_Report_"
OpsProductivityFileName='Ops_Productivity_Report_'
RegionProductivityFileName='Region_Productivity_Report_'
CustomerTargetFileName='Customer-Wise_Productivity_Report_'
CandidateDataFileName="Candidate_Data_"

ReportDownloadPathLocal='C:/SITES/NEO_SKILLS/'
ReportDownloadPathWeb='{}/data/'.format(Base_URL)

DownloadPathLocal='C:/SITES/NEO_SKILLS/Downloads/'
DownloadPathWeb='{}/Downloads/'.format(Base_URL)

DumpFileName="NEO_Master_Data_"
DumpFilesList=  {
                  "Customer_List":"[masters].[sp_get_customer_list_for_dump]",
                  "Contract_List":"[masters].[sp_get_contract_list_for_dump]",
                  "Project_List":"[masters].[sp_get_project_list_for_dump]",
                  "Center_List":"[masters].[sp_get_center_list_for_dump]"
                 }
                 
html_email_msg = '''
    <div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">Dear <b>{},</b><br>
    <br>
    Greeting from NEO team!
    <br><br>
    We got your request for forgot password.
    <br><br>
    Your current password is <b>{}</b>
    <br><br>
    If you have not raised this request, kindly contact the support team immediately.
    </p>
    </div>
    <br>

    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>
    <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">
    Best Regards,<br>
    <b>NEO Team</b> </p>
    <div align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <hr align="center" width="100%" size="2">
    </div>

    <div>
    <!--p style="font-size:12pt;font-family:Times New Roman,serif;margin:0 0 12pt 0;">&nbsp;</p-->
    <p align="center" style="font-size:12pt;font-family:Times New Roman,serif;text-align:center;margin:0;">
    <i>This is an auto generated e-mail. Please do not reply to this mail.</i></p>
    </div>
    <br>
    '''


    ############################################################################3 
DATABASE="NEO"
SQL_GENERAL_TABLES = [
    # "{}.candidate_details.tbl_candidates".format(DATABASE),
    # "{}.candidate_details.tbl_candidate_reg_enroll_details".format(DATABASE),
    # "{}.candidate_details.tbl_candidate_reg_enroll_non_mandatory_details".format(DATABASE),
    # "{}.candidate_details.tbl_candidate_interventions".format(DATABASE),
    # "{}.candidate_details.tbl_candidate_intervention_tracker".format(DATABASE),
    # "{}.candidate_details.tbl_map_candidate_intervention_skilling".format(DATABASE),
    "{}.assessments.tbl_batch_assessments".format(DATABASE),
    "{}.assessments.tbl_map_assessment_candidates".format(DATABASE),
    "{}.batches.tbl_batches".format(DATABASE),
    "{}.masters.tbl_block".format(DATABASE),
    "{}.masters.tbl_bu".format(DATABASE),
    "{}.masters.tbl_category_type".format(DATABASE),
    "{}.masters.tbl_center".format(DATABASE),
    "{}.masters.tbl_center_category".format(DATABASE),
    "{}.masters.tbl_center_type".format(DATABASE),
    "{}.masters.tbl_cluster".format(DATABASE),
    "{}.masters.tbl_contract".format(DATABASE),
    "{}.masters.tbl_contract_stages".format(DATABASE),
    "{}.masters.tbl_countries".format(DATABASE),
    "{}.masters.tbl_courses".format(DATABASE),
    "{}.masters.tbl_customer".format(DATABASE),
    "{}.masters.tbl_customer_address".format(DATABASE),
    "{}.masters.tbl_customer_group".format(DATABASE),
    "{}.masters.tbl_customer_spoc".format(DATABASE),
    "{}.masters.tbl_districts".format(DATABASE),
    "{}.masters.tbl_entity".format(DATABASE),
    "{}.masters.tbl_funding_source".format(DATABASE),
    "{}.masters.tbl_industry_type".format(DATABASE),
    "{}.masters.tbl_map_course_center".format(DATABASE),
    "{}.masters.tbl_practice".format(DATABASE),
    "{}.masters.tbl_product".format(DATABASE),
    "{}.masters.tbl_project_group".format(DATABASE),
    "{}.masters.tbl_project_type".format(DATABASE),
    "{}.masters.tbl_projects".format(DATABASE),
    "{}.masters.tbl_qp".format(DATABASE),
    "{}.masters.tbl_question_type".format(DATABASE),
    "{}.masters.tbl_region".format(DATABASE),
    "{}.masters.tbl_sales_category".format(DATABASE),
    "{}.masters.tbl_sector".format(DATABASE),
    "{}.masters.tbl_states".format(DATABASE),
    "{}.masters.tbl_sub_center".format(DATABASE),
    "{}.masters.tbl_sub_projects".format(DATABASE),
    "{}.masters.tbl_target_type".format(DATABASE),
    "{}.masters.tbl_tma_candidate_attendance".format(DATABASE),
    "{}.masters.tbl_tma_trainer_stage_log".format(DATABASE),
    "{}.users.tbl_users".format(DATABASE),
    "{}.users.tbl_user_details".format(DATABASE),
    "{}.users.tbl_map_user_employee_department".format(DATABASE)
    #"{}.batches.vw_enrolled_dropped_certifed_placed_cnt_total".format(DATABASE)
    #"{}.candidate_details.tbl_candidates_age_range_view".format(DATABASE)
]

SQL_CANDIDATES_TABLE = [
    "{}.candidate_details.tbl_candidates".format(DATABASE)
]

CANDIDATE_REG_ENROLL_DETAILS_TABLE = [
    "{}.candidate_details.tbl_candidate_reg_enroll_details".format(DATABASE)
]

CANDIDATE_REG_ENROLL_NON_MANDATORY_DETAILS_TABLE = [
    "{}.candidate_details.tbl_candidate_reg_enroll_non_mandatory_details".format(DATABASE)
]

CANDIDATE_INTERVENTIONS_TABLE = [
    "{}.candidate_details.tbl_candidate_interventions".format(DATABASE)
]

CANDIDATE_INTERVENTION_TRACKER_TABLE = [
    "{}.candidate_details.tbl_candidate_intervention_tracker".format(DATABASE)
]

MAP_CANDIDATE_INTERVENTION_SKILLING_TABLE = [
    "{}.candidate_details.tbl_map_candidate_intervention_skilling".format(DATABASE)
]

CUSTOMER_CANDIDATE_DATA_TABLE = [
    "{}.candidate_details.tbl_customer_candidate_view".format(DATABASE)
]

ECP_COUNT_TABLE = [
    "{}.batches.vw_enrolled_dropped_certifed_placed_cnt_total".format(DATABASE)
]

CANDIDATE_AGE_RANGE_TABLE = [
    "{}.candidate_details.tbl_candidates_age_range_view".format(DATABASE)
]

REPLACE_EMPTY_STRING_TABLES = [
    "{}.users.tbl_users".format(DATABASE),
    "{}.users.tbl_user_details".format(DATABASE),
    "{}.users.tbl_map_user_employee_department".format(DATABASE)
]

postgre_SERVER = "localhost"  #pgsql:host=
postgre_DATABASE = "neo_jobs_live"
postgre_USER = "postgres"
postgre_PASSWORD = "p@$$w0rd"


GENERAL_TABLES = [
    "{}.neo_customer.companies".format(postgre_DATABASE),
    "{}.neo_customer.opportunities".format(postgre_DATABASE),
    "{}.neo_customer.lead_logs".format(postgre_DATABASE),
    "{}.neo_customer.customers".format(postgre_DATABASE),
    "{}.neo_job.candidate_placement".format(postgre_DATABASE),
    "{}.neo_job.candidates_jobs".format(postgre_DATABASE),
    "{}.neo_job.candidates_jobs_logs".format(postgre_DATABASE),
    "{}.neo_job.jobs".format(postgre_DATABASE),
    "{}.neo_job.jobs_statuses_logs".format(postgre_DATABASE),
    "{}.neo_job.jobs_users".format(postgre_DATABASE),
    "{}.neo_user.users".format(postgre_DATABASE),
    "{}.neo_user.user_roles".format(postgre_DATABASE),
    "{}.neo_user.centers".format(postgre_DATABASE),
    "{}.neo_user.user_logs".format(postgre_DATABASE),
    "{}.neo_master.business_practices".format(postgre_DATABASE),
    "{}.neo_master.business_verticals".format(postgre_DATABASE),
    "{}.neo_master.candidate_sources".format(postgre_DATABASE),
    "{}.neo_master.candidate_stages".format(postgre_DATABASE),
    "{}.neo_master.candidate_statuses".format(postgre_DATABASE),
    "{}.neo_master.candidate_types".format(postgre_DATABASE),
    "{}.neo_master.caste_categories".format(postgre_DATABASE),
    "{}.neo_master.clcs_qps".format(postgre_DATABASE),
    "{}.neo_master.commercial_remark_types".format(postgre_DATABASE),
    "{}.neo_master.country".format(postgre_DATABASE),
    "{}.neo_master.districts".format(postgre_DATABASE),
    "{}.neo_master.document_types".format(postgre_DATABASE),
    "{}.neo_master.education_temp".format(postgre_DATABASE),
    "{}.neo_master.educations".format(postgre_DATABASE),
    "{}.neo_master.employment_type".format(postgre_DATABASE),
    "{}.neo_master.functional_areas".format(postgre_DATABASE),
    "{}.neo_master.genders".format(postgre_DATABASE),
    "{}.neo_master.industries".format(postgre_DATABASE),
    "{}.neo_master.job_open_types".format(postgre_DATABASE),
    "{}.neo_master.job_priority_levels".format(postgre_DATABASE),
    "{}.neo_master.job_statuses".format(postgre_DATABASE),
    "{}.neo_master.labournet_entities".format(postgre_DATABASE),
    "{}.neo_master.lead_sources".format(postgre_DATABASE),
    "{}.neo_master.lead_statuses".format(postgre_DATABASE),
    "{}.neo_master.lead_type".format(postgre_DATABASE),
    "{}.neo_master.learning_types".format(postgre_DATABASE),
    "{}.neo_master.locations".format(postgre_DATABASE),
    "{}.neo_master.marital_statuses".format(postgre_DATABASE),
    "{}.neo_master.qualification_packs".format(postgre_DATABASE),
    "{}.neo_master.region".format(postgre_DATABASE),
    "{}.neo_master.religions".format(postgre_DATABASE),
    "{}.neo_master.sectors".format(postgre_DATABASE),
    "{}.neo_master.skilling_types".format(postgre_DATABASE),
    "{}.neo_master.states".format(postgre_DATABASE),
    "{}.neo_master.work_authorizations".format(postgre_DATABASE)
]

CANDIDATES_TABLE = [
    "{}.neo.candidates".format(postgre_DATABASE)
]

NEO_BATCHES_TABLE = [
    "{}.neo.neo_batches".format(postgre_DATABASE)
]

API_secret_key='navriti@123'
API_secret_id = 'athira'
candidate_xmlPath = 'C:/SITES/NEO_SKILLS/XML file/'
candidate_xml_weburl = 'https://neo.certiplate.com/Data/skills_app_files/xml/'

upload_data_path = '/data/'
tmapath = 'C:/SITES/NEO_SKILLS/data/TMA/'
CandidateAttendanceImagePathLocal='C:/SITES/NEO_SKILLS/data/TMA/attendance_images/'
TrainerLogImagesPathLocal='C:/SITES/NEO_SKILLS/data/TMA/trainer_stage_images/'


aws_location = 'neo_skills/live/'  #live uat qa
COL_URL = 'https://col-neo.labournet.in/'  # 'http://127.0.0.2:5000/'   'http://3.6.31.28:5000/'  'https://col-neo.labournet.in/'
neo_certiplate = 'https://neo.certiplate.com/Data/skills_app_files/img/' # 'https://neo.certiplate.com/Data/skills_app_files/img/'  skills_app_files_demo
dell_type_customer = '305'  # '305,339'
