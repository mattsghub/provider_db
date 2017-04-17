from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create a User table
    """
    # Ensures table will be named in plural and not in singular
    # as is the name of the model

    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)

    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Provider(db.Model):
    """
    Create a Provider table
    """

    __tablename__ = 'provider'

    id_provider = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    middle_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(6))
    SSN = db.Column(db.String(9), index=True, unique=True)
    NPI = db.Column(db.String(10), index=True, unique=True)
    CA_DEA = db.Column(db.String(11), index=True, unique=True)
    home_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))
    work_email = db.Column(db.String(120), unique=True)
    personal_email = db.Column(db.String(120), unique=True)
    fax_number = db.Column(db.String(10))
    address = db.Column(db.String(255))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zip = db.Column(db.String(10))

class Provider_Specialty(db.Model):
    """
    Create a Provider Specialty table
    """

    __tablename__ = 'provider_specialty'

    id_provider_specialty = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    id_specialty = db.Column(db.Integer, db.ForeignKey('specialty.id_specialty'))
    board_certified = db.Column(db.Boolean, default=True, nullable=False)
    primary_specialty = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Provider Specialty: {}>'.format(self.name)

class Specialty(db.Model):
    """
    Create a Specialty table
    """

    __tablename__ = 'specialty'

    id_specialty = db.Column(db.Integer, primary_key=True)
    id_specialty_provider = db.Column(db.Integer, db.ForeignKey('provider_specialty.id_provider_specialty'))
    specialty = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<Specialty: {}>'.format(self.name)

class Provider_Education(db.Model):
    """
    Create a Provider Education table
    """

    __tablename__ = 'provider_education'

    id_provider_education = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    type = db.Column(db.String(45))
    school = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zip = db.Column(db.String(10))
    country = db.Column(db.String(255))
    degree = db.Column(db.String(255))
    degree_type = db.Column(db.String(45))
    year_began = db.Column(db.Integer)
    year_complete = db.Column(db.Integer)

    def __repr__(self):
        return '<Provider Education: {}>'.format(self.name)

class Provider_Relationship(db.Model):
    """
    Create a Provider Relationship table
    """

    __tablename__ = 'provider_relationship'

    id_provider_relationship = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    id_referral_source = db.Column(db.Integer, db.ForeignKey('referral_source.id_referral_source'))
    id_relationship_type = db.Column(db.Integer, db.ForeignKey('relationship_type.id_relationship_type'))
    effective_date = db.Column(db.Date)

    def __repr__(self):
        return '<Provider Relationship: {}>'.format(self.name)

class Relationship_Type(db.Model):
    """
    Create a Relationship Type table
    """

    __tablename__ = 'relationship_type'

    id_relationship_type = db.Column(db.Integer, primary_key=True)
    relationship_type = db.Column(db.String(45))

    def __repr__(self):
        return '<Relationship Type: {}>'.format(self.name)

class Referral_Source(db.Model):
    """
    Create a Referral Source table
    """

    __tablename__ = 'referral_source'

    id_referral_source = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    middle_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    company = db.Column(db.String(150))
    work_phone = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(10))
    work_email = db.Column(db.String(120))
    fax_number = db.Column(db.String(10))
    website = db.Column(db.String(255))

    def __repr__(self):
        return '<Referral Source: {}>'.format(self.name)

class Provider_Professional_Liability(db.Model):
    """
    Create a Provider Professional Liability table
    """

    __tablename__ = 'provider_professional_liability'

    id_provider_professional_liability = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    carrier = db.Column(db.String(150))
    effective_date = db.Column(db.Date)
    term_date = db.Column(db.Date)

    def __repr__(self):
        return '<Provider Professional Liability: {}>'.format(self.name)

class Provider_CAQH(db.Model):
    """
    Create a Provider CAQH table
    """

    __tablename__ = 'provider_CAQH'

    id_provider_CAQH = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    auth_received_date = db.Column(db.Date)
    added_date = db.Column(db.Date)
    last_updated_date = db.Column(db.Date)

    def __repr__(self):
        return '<Provider CAQH: {}>'.format(self.name)

class Provider_Employmnt(db.Model):
    """
    Create a Provider Employment table
    """

    __tablename__ = 'provider_employment'

    id_provider_employment = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    id_employer = db.Column(db.Integer, db.ForeignKey('employer.id_employer'))
    effective_date = db.Column(db.Date)
    term_date = db.Column(db.Date)

    def __repr__(self):
        return '<Provider Employer: {}>'.format(self.name)

class Employer(db.Model):
    """
    Create a Employer table
    """

    __tablename__ = 'employer'

    id_employer = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150))
    address = db.Column(db.String(255))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zip = db.Column(db.String(10))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(120))

    def __repr__(self):
        return '<Employer: {}>'.format(self.name)

class Provider_Activities(db.Model):
    """
    Create a Provider Activities table
    """

    __tablename__ = 'provider_activities'

    id_provider_activities = db.Column(db.Integer, primary_key=True)
    id_provider = db.Column(db.Integer, db.ForeignKey('provider.id_provider'))
    id_provider_practice_location = db.Column(db.Integer, db.ForeignKey('provider_practice_locaton.id_provider_practice_location'))
    id_practice_type = db.Column(db.Integer, db.ForeignKey('practice_type.id_practice_type'))
    primary_activities = db.Column(db.Boolean, default=True, nullable=False)
    title = db.Column(db.String(120))
    effective_date = db.Column(db.Date)
    term_date = db.Column(db.Numeric)
    clinical_FTE = db.Column(db.Float)
    admin_FTE = db.Column(db.Float)
    research_FTE = db.Column(db.Float)
    teaching_FTE = db.Column(db.Float)
    weekly_patient_care_hours = db.Column(db.Float)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Provider Activities: {}>'.format(self.name)

class Provider_Practice_Location(db.Model):
    """
    Create a Provider Practice Location table
    """

    __tablename__ = 'provider_practice_locaton'

    id_provider_practice_location = db.Column(db.Integer, primary_key=True)
    id_practice_location = db.Column(db.Integer, db.ForeignKey('practice_locaton.id_practice_location'))
    effective_date = db.Column(db.Date)
    term_date = db.Column(db.Numeric)
    primary_location = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<Provider Practice Location: {}>'.format(self.name)

class Practice_Location(db.Model):
    """
    Create a Practice Location table
    """

    __tablename__ = 'practice_locaton'

    id_practice_location = db.Column(db.Integer, primary_key=True)
    practice_locaton = db.Column(db.String(255))
    practice_type = db.Column(db.String(255))
    cost_center = db.Column(db.String(10))
    region = db.Column(db.String(10))
    CAO = db.Column(db.String(60))
    address = db.Column(db.String(255))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zip = db.Column(db.String(10))

    def __repr__(self):
        return '<Practice Location: {}>'.format(self.name)

class Practice_Type(db.Model):
    """
    Create a Practice Type table
    """

    __tablename__ = 'practice_type'

    id_practice_type = db.Column(db.Integer, primary_key=True)
    practice_type = db.Column(db.String(100))

    def __repr__(self):
        return '<Practice Type: {}>'.format(self.name)