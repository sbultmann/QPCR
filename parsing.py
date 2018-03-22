#from OpenTrons_app import db


class Experiment:
    '''The experiment class represents one defined experiment, containing user data and job data.'''

    #__tablename__ = "sequences"
    #id = db.Column(db.Integer, primary_key=True)
    #sequence = db.Column(db.String(4096))
    #rev_com = db.Column(db.String(4096))
    #gc = db.Column(db.Float())
    #date = db.Column(db.DateTime())

    DEFAULT_USER = "Default User"
    DEFAULT_JOB_NAME = "No job name specified"

    KEY_JOB_NAME = "job"
    KEY_USER_NAME = "user"
    KEY_TEMPLATE = "template"
    KEY_PRIMER = "primer"

    job_name = DEFAULT_JOB_NAME
    user_name = DEFAULT_USER
    template_name = []
    primer_pair_name = []
    # process indicates the status of the job
    # 0: not processed
    # 1: is currently processed
    # 2 finished
    job_status = 0

    # @param input_data_to_parse a list of strings to parse as experiment information
    def __init__(self, input_data_to_parse):
        self.job_name = self.parse_sample_string(input_data_to_parse[self.KEY_JOB])
        self.user_name = self.parse_sample_string(input_data_to_parse[self.KEY_USER])
        self.template_name = self.parse_sample_string(input_data_to_parse[self.KEY_TEMPLATE])
        self.primer_pair_name = self.parse_sample_string(input_data_to_parse[self.KEY_PRIMER])

    def parse_sample_string(self, sample_string):
        return sample_string.split(",")

