from ninja import ModelSchema, Schema
from .mymodels.DailyAction import DailyAction
from .mymodels.DailyResponse import DailyResponse
from .mymodels.Mentor import Mentor
from .mymodels.ParoleAddress import ParoleAddress
from .mymodels.ParoleOfficer import ParoleOfficer
from .mymodels.ReturningCitizen import ReturningCitizen
from .mymodels.TempUserLogin import TempUserLogin
from typing import Optional, List

#Schema Templates for use below
class DailyActionSchema(ModelSchema):
    class Meta:
        model = DailyAction
        fields = ('date', 'location', 'description')

class DailyResponseSchema(ModelSchema):
    class Meta:
        model = DailyResponse
        fields = ('date', 'rating')
    
class MentorSchema(ModelSchema):
    class Meta:
        model = Mentor
        fields = ('first_Name', 'last_Name', 'phone_number')

class ParoleAddressSchema(ModelSchema):
    class Meta:
        model = ParoleAddress
        fields = ('address', 'city', 'state', 'zip_code')

class ParoleOfficerSchema(ModelSchema):
    class Meta:
        model = ParoleOfficer
        fields = ('first_Name', 'last_Name', 'city', 'phone_number')

class ReturningCitizenSchema(ModelSchema):
    class Meta:
        model = ReturningCitizen
        fields = ('first_Name', 'last_Name', 'MDOC')
    
class TempUserLoginSchema(ModelSchema):
    class Meta:
        model = TempUserLogin
        fields = ("returning_citizen",)

#Schemas Returned from the API
        
class FullReturningCitizenSchema(Schema):
    userID: str
    returning_citizen: ReturningCitizenSchema
    parole_address: Optional[ParoleAddressSchema] = []
    mentor: Optional[MentorSchema] = []
    parole_officer: Optional[ParoleOfficerSchema] = []
    daily_actions: Optional[List[DailyActionSchema]] = []
    daily_responses: Optional[List[DailyResponseSchema]] = []

class FirstTimeLoginSchema(Schema):
    userID: str
    returning_citizen: ReturningCitizenSchema
    parole_address: Optional[ParoleAddressSchema] = []
    mentor: Optional[MentorSchema] = []
    parole_officer: Optional[ParoleOfficerSchema] = []
    daily_actions: Optional[List[DailyActionSchema]] = []
    daily_responses: Optional[List[DailyResponseSchema]] = []
