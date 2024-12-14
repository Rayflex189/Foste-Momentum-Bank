from .decorators import *
from .forms import *
from .models import *

def validate_imf(input_imf, user_profile):
    # Compare the input OTP with the OTP stored in the user profile
    return input_imf == user_profile.imf_code

def validate_aml(input_aml, user_profile):
    # Compare the input OTP with the OTP stored in the user profile
    return input_aml == user_profile.aml_code

def validate_tac(input_tac, user_profile):
    # Compare the input OTP with the OTP stored in the user profile
    return input_tac == user_profile.tac_code

def validate_linking_code(input_linking_code, user_profile):
    # Compare the input OTP with the OTP stored in the user profile
    return input_linking_code == user_profile.linking_code