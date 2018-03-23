# Imports
from flask import Flask, redirect, render_template, request, url_for, make_response
from json import dumps, loads
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from function import make_plate, plot_qpcr_data, pipet_scheme, combine_files
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "mysite/static/uploads"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Garp",
    password="random4242",
    hostname="Garp.mysql.pythonanywhere-services.com",
    databasename="Garp$experiment_data",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# the database model of our queries
class ExperimentModel(db.Model):

    __tablename__ = "experiment_data_v3"
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.Text())
    user = db.Column(db.Text())
    samples = db.Column(db.Text())
    genes = db.Column(db.Text())
    status = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    scheme_images = db.Column(db.Text())
    scheme_csv = db.Column(db.Text())
    qpcr_images = db.Column(db.Text())
    qpcr_houskeeping = db.Column(db.Text())
    qpcr_results = db.Column(db.Text())

# the ip database for lookup of logged in users
#class IPLookupModel(db.Model):
#    __tablename__ = "ip_lookup_v1"
#    id = db.Column(db.Integer, primary_key=True)
#    user = db.Column(db.String(4096))
#    ip = db.Column(db.String(4096))
#    login_date = db.Column(db.DateTime())


class AccountModel(db.Model):
    '''A model class to restrict the access to the experiments database.'''
    __tablename__ = "user_data_v1"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(4096))
    pw = db.Column(db.String(4096))
    email = db.Column(db.String(4096))

#class IPLookup:
#    '''The IPLookup class implements basic functionality for checking logged in users.'''


class Account():
    '''The Account class represents user account information and interfaces with the
    user account database.'''

    ADMIN_ACCOUNT = "[ALL_USERS:REQUEST_ADMIN]"

    user = None
    pw = None
    email = None

    def __init__(self, user_name, password, e_mail):
        self.user = user_name.strip()
        self.pw = password
        self.email = e_mail.strip()

    def commit_account(self):
        '''Commit the account information contained in this object to a database
        and return the database id of the submission.'''
        if not self.account_exists():
            acc_model = AccountModel(user = self.user, pw = Account.get_hashed_password(self.pw), email = self.email)
            db.session.add(acc_model)
            db.session.commit()
            return acc_model.id
        else: # return an error code
            return -1

    def get_hashed_password(password):
        '''Returns the password in its' hashed form.'''
        return hashlib.sha512(password.encode()).hexdigest()

    def account_exists(self):
        '''Check if this username is already registered in the database.'''
        info = AccountModel.query.filter_by(user = self.user)
        return info != None and info.count() == 1

    def check_account(username):
        '''Check if the specified user already is registered in the database.'''
        info = AccountModel.query.filter_by(user = username)
        return info != None and info.count() == 1

    def get_account(username):
        '''Get the account belonging to the specified user name.'''
        if Account.check_account(username):
            return AccountModel.query.filter_by(user = username)[0]
        else:
            return None

    def check_password(username, password):
        '''Check if the specified password is correct for the specified user name.'''
        if Account.check_account(username):
            return Account.get_account(username).pw == hashlib.sha512(password.encode()).hexdigest()
        else:
            return False

    def check_password_hash(username, password_hash):
        '''Check if the specified password hash is correct for the specified user name.'''
        if Account.check_account(username):
            return Account.get_account(username).pw == password_hash
        else:
            return False

    def get_user_experiments(self):
        return ExperimentModel.query.filter_by(user = self.user)

class Experiment:
    '''The experiment class represents one defined experiment, containing user data and job data.'''

    DEFAULT_USER = "Default User"
    DEFAULT_JOB_NAME = "No job name specified"

    MAXIMUM_WELLS = 384

    KEY_JOB_NAME = "job"
    KEY_USER_NAME = "user"
    KEY_TEMPLATE = "template"
    KEY_PRIMER = "primer"

    job_name = DEFAULT_JOB_NAME
    user_name = DEFAULT_USER
    sample_names = []
    gene_names = []
    # process indicates the status of the job
    # 0: not processed
    # 1: is currently processed
    # 2 finished
    job_status = 0

    # @param input_data_to_parse a list of strings to parse as experiment information
    def __init__(self, input_data_to_parse = {}):
        self.job_name = input_data_to_parse[self.KEY_JOB_NAME].strip()
        self.user_name = input_data_to_parse[self.KEY_USER_NAME].strip()
        self.sample_names = Experiment.parse_sample_string(input_data_to_parse[self.KEY_TEMPLATE])
        self.gene_names = Experiment.parse_sample_string(input_data_to_parse[self.KEY_PRIMER])

    def create_experiment_from_model(experiment_model):
        '''Create and return a experiment from a database query.'''
        # TODO: finish this function
        if experiment_model != None:
            return Experiment()
        else:
            return None

    def parse_sample_string(sample_string):
        '''Parses a comma delimited string and returns it as list.'''
        if sample_string != None and sample_string != "":
            return [s.strip() for s in sample_string.split(",")]
        else:
            return []

    def compress_list_for_commit(self, string_list):
        '''Compresses a list of strings to a comma separated string in order to
        allow it to be commited to the database.'''
        if len(string_list) > 0:
            return ",".join(string_list)
        else:
            return ""

    def commit_experiment(self):
        '''Commit the experiments information contained in this object to a database
        if a valid user is supplied and return the id of the submission.'''
        exp_model = ExperimentModel(job=self.job_name, user=self.user_name, samples=self.compress_list_for_commit(self.sample_names), genes=self.compress_list_for_commit(self.gene_names), status=self.job_status, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(exp_model)
        db.session.commit()
        return int(exp_model.id)

    def valid_sample_length(self):
        ''' Check that not more samples or genes than wells are entered.'''
        return (len(self.sample_names) + 1) * 3 * len(self.gene_names) <= self.MAXIMUM_WELLS and len(self.sample_names) > 0 and len(self.gene_names) > 0

# Start site
@app.route('/')
def index():
    return render_template("main_page.html", logged_in = cookie_is_logged_in(), user = cookie_get_user())

    #if len(user) > 0:
    #    return redirect(url_for("create_experiment"))
    #else:
    #    return render_template("main_page.html")
@app.route('/info')
def infous():
    return render_template("info.html", logged_in = cookie_is_logged_in(), user = cookie_get_user())
# New experiment creation
@app.route('/newexp', methods=["GET", "POST"])
def create_experiment():
    if request.method == "GET":
        return render_template("newexp.html", user = cookie_get_user(), too_many_samples = False, logged_in = cookie_is_logged_in())
    else: # receive a POST event, meaning data submission
        # do some parsing here with the data
        experiment_data = {Experiment.KEY_USER_NAME:cookie_get_user(), Experiment.KEY_JOB_NAME:request.form["exp name"], Experiment.KEY_TEMPLATE:request.form["samples"], Experiment.KEY_PRIMER:request.form["genes"]}
        # object containing all data about the commited experiment data
        current_experiment = Experiment(experiment_data)
        if (current_experiment.valid_sample_length()):
            # check if an id was supplied in order not to resubmit the data twice on reload from old results
            experiment_id = int(request.form["resubmission"])
            if experiment_id < 0:
                experiment_id = current_experiment.commit_experiment()
            # send the image information to the database
            ExperimentModel.query.get(experiment_id).scheme_csv = pipet_scheme(experiment_id, current_experiment.user_name, current_experiment.job_name, list(current_experiment.sample_names), list(current_experiment.gene_names))
            ExperimentModel.query.get(experiment_id).scheme_images = dumps(make_plate(experiment_id, list(current_experiment.sample_names), list(current_experiment.gene_names)))
            db.session.commit()
            resp = make_response(redirect(url_for("show_results", result_id = experiment_id)))
            return  resp# move to the results page
        else:
            return render_template("newexp.html", user = cookie_get_user(), too_many_samples = True, logged_in = cookie_is_logged_in())

# Here the results are shown
@app.route('/results/<result_id>', methods=["GET", "POST"])
def show_results(result_id):
    if request.method == "GET":
        images = loads(ExperimentModel.query.get(result_id).scheme_images)
        return render_template("results.html", user = cookie_get_user(), genes = Experiment.parse_sample_string(ExperimentModel.query.get(result_id).genes), pipet_scheme = ExperimentModel.query.get(result_id).scheme_csv, image_genes = images[0], image_samples = images[1], logged_in = cookie_is_logged_in())
    else:
        # check if the post request has the file part
        if 'uploadfile' not in request.files:
            # TODO: error handling
            print("")
#            return redirect(request.url)
        file = request.files['uploadfile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '' or file == None:
            # TODO: do some error handling
            print("")
        else:
            # save the Q-PCR results to the disc
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            # commit the qpcr to the database
            # TODO: parse the file to
            # TODO:enter the data into:
            exp = ExperimentModel.query.get(result_id)
            real_data = combine_files(secure_filename(file.filename), exp.scheme_csv, request.form["housekeeper"])
            exp.qpcr_images = dumps(plot_qpcr_data(real_data[1]))
            exp.qpcr_housekeeping = dumps(request.form["housekeeper"])
            exp.qpcr_results = real_data[0]
            db.session.commit()
            return redirect(url_for("show_qpcr_results", qpcr_id = result_id))
        return render_template("main_page.html", user = cookie_get_user(), logged_in = cookie_is_logged_in())

# Here OLD results are shown
@app.route('/oldresults', methods=["GET", "POST"])
def show_all_experiments():
    user_name = cookie_get_user()
    exp = None
    if request.method == "GET":
        if cookie_is_logged_in():
            exp = ExperimentModel.query.filter_by(user = cookie_get_user())
    else: # reveive a POST event
        user_name = request.form["name"]
        if user_name == "[ALL_USERS:REQUEST_ADMIN]":
            exp = ExperimentModel.query.all()
        elif Account.check_password(username = user_name, password = request.form["password"]):
            exp = ExperimentModel.query.filter_by(user = user_name)
    return render_template("oldresults.html", user = user_name, experiments = exp, logged_in = cookie_is_logged_in())

@app.route('/qpcr/<qpcr_id>', methods=["GET", "POST"])
def show_qpcr_results(qpcr_id):
    if request.method == "GET":
        print("")
    return render_template("qpcr.html", images = loads(ExperimentModel.query.get(qpcr_id).qpcr_images), qpcrfile = ExperimentModel.query.get(qpcr_id).qpcr_results, user = cookie_get_user(), logged_in = cookie_is_logged_in())

@app.route("/registration", methods=["GET", "POST"])
def handle_user_registration():
    '''Handle user registration.'''
    user_bool = None
    all_the_accounts = None
    wrong_confirm_pw = False
    if request.method == "POST":
        # check if the submit is correct
        if "name" in request.form and "email" in request.form and "password" in request.form and "password_confirm" in request.form:
            if request.form["password"] == request.form["password_confirm"]:
                user_account = Account(user_name = request.form["name"], password = request.form["password"], e_mail = request.form["email"])
                if user_account.user == "[ALL_USERS:REQUEST_ADMIN]":
                    all_the_accounts = AccountModel.query.all()
                else:
                    # prevent existent or empty usernames
                    user_bool = user_account.account_exists() or user_account.user == None or user_account.user == ""
                    if not user_bool:
                        user_account.commit_account()
            else:
                wrong_confirm_pw = True
    return render_template("registration.html", userExists = user_bool, hacks = all_the_accounts, user = cookie_get_user(), wrong_confirm = wrong_confirm_pw, logged_in = cookie_is_logged_in())

@app.route("/login", methods=["GET", "POST"])
def handle_login():
    '''Handle login.'''
    if request.method == "GET":
        return render_template("login.html", user = cookie_get_user(), logged_in = cookie_is_logged_in())
    else: # reveive a POST event
        user_name = request.form["name"]
        user_password = request.form["password"]
        if user_name == Account.ADMIN_ACCOUNT:
            return render_template("registration.html", userExists = None, hacks = AccountModel.query.all(), logged_in = cookie_is_logged_in())
        else:
            if Account.check_password(username = user_name, password = user_password):
                resp = make_response(redirect(request.form["current_url"]))
                resp.set_cookie('user', user_name)
                resp.set_cookie('pw', Account.get_hashed_password(user_password))
                #request.remote_addr
                return resp
            else:
                return redirect(request.form["current_url"])

@app.route("/logout", methods=["GET", "POST"])
def handle_logout():
    '''Handle logout.'''
    resp = make_response(redirect(request.form["current_url"]))
    cookie_log_off(resp)
    return resp

@app.route("/account", methods=["GET", "POST"])
def manage_account():
    '''Manage the account of the currently logged in user.'''
    user_email = None
    changed_account = None
    if request.method == "GET":
        if Account.check_account(cookie_get_user()):
            user_email = Account.get_account(cookie_get_user()).email
    else: # POST event
        user_account = Account.get_account(cookie_get_user())
        user_email = user_account.email
        changed_account = False
        # do not allow non existent accounts
        if user_account != None:
            if 'email' in request.form:
                    user_email = request.form["email"]
                    user_account.email = user_email
            # check if the from is filled correctly
            if "oldpassword" in request.form and "newpassword1" in request.form and "newpassword2" in request.form:
                changed_account = False
                if Account.check_password(user_account.user, request.form["oldpassword"]):
                    if request.form["newpassword1"] == request.form["newpassword2"]:
                        user_account.pw = Account.get_hashed_password(request.form["newpassword1"])
                        changed_account = True
            # commit the changes
            db.session.commit()
    resp = make_response(render_template("account.html", user = cookie_get_user(), logged_in = cookie_is_logged_in(), email = user_email, change = changed_account))
    # TODO: the website still thinks you are logged out until you reload the page
    if changed_account:
        resp.set_cookie("pw", "", 0)
        resp.set_cookie("pw", Account.get_hashed_password(request.form["newpassword1"]))
    return resp

def cookie_is_logged_in():
    '''Check whether the user is logged in based on cookies. This is not secure!'''
    return Account.check_password_hash(request.cookies.get("user"), request.cookies.get("pw"))

def cookie_get_user():
    '''Get the current user from the cookie.'''
    return request.cookies.get("user")

def cookie_log_off(responseObject):
    '''Log off the user by clearing the cookie information.'''
    responseObject.set_cookie('user', "", expires = 0)
    responseObject.set_cookie('pw', "", expires = 0)
