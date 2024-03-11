from ninja import ModelSchema, Schema
from .mymodels.Event import Event
from .mymodels.DailyResponse import DailyResponse
from .mymodels.Mentor import Mentor
from .mymodels.ParoleAddress import ParoleAddress
from .mymodels.ParoleOfficer import ParoleOfficer
from .mymodels.ReturningCitizen import ReturningCitizen
from .mymodels.TempUserLogin import TempUserLogin
from .mymodels.ThreeDailyActions import ThreeDailyActions
from typing import Optional, List
from datetime import datetime


#GET
class ThreeDailyActionsSchema(ModelSchema):
    class Meta:
        model = ThreeDailyActions
        fields = ('date_id', 'date', 'description', 'is_completed')

class EventSchema(ModelSchema):
    class Meta:
        model = Event
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

#Schemas Returned from the LoginController
        
class FullReturningCitizenSchema(Schema):
    userID: str
    returning_citizen: ReturningCitizenSchema
    parole_address: Optional[ParoleAddressSchema] = []
    mentor: Optional[MentorSchema] = []
    parole_officer: Optional[ParoleOfficerSchema] = []
    events: Optional[List[EventSchema]] = []
    daily_responses: Optional[List[DailyResponseSchema]] = []
    daily_actions: Optional[List[ThreeDailyActionsSchema]] = []

class FirstTimeLoginSchema(Schema):
    userID: str
    returning_citizen: ReturningCitizenSchema
    parole_address: Optional[ParoleAddressSchema] = []
    mentor: Optional[MentorSchema] = []
    parole_officer: Optional[ParoleOfficerSchema] = []
    events: Optional[List[EventSchema]] = []
    daily_responses: Optional[List[DailyResponseSchema]] = []
    daily_actions: Optional[List[ThreeDailyActionsSchema]] = []

#POST

class CreateDailyActionHelper(Schema):
    date_id: int
    date: datetime
    description: str
    is_completed: bool
    returning_citizen_id: str
    

#
class CreateEventHelper(Schema):
    date: datetime
    location: str
    description: str
    returning_citizen_id: str


#
class CreateDailyResonseHelper(Schema):
    date: datetime
    rating: str
    returning_citizen_id: str
