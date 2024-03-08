from database.mymodels.ReturningCitizen import ReturningCitizen
from database.mymodels.Mentor import Mentor
from database.mymodels.ParoleOfficer import ParoleOfficer
from database.mymodels.DailyAction import DailyAction
from database.mymodels.ParoleAddress import ParoleAddress
from database.mymodels.DailyResponse import DailyResponse
from database.mymodels.TempUserLogin import TempUserLogin
from database.mymodels.ApiKeyForCitizen import ApiKeyForReturningCitizen

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja_extra import NinjaExtraAPI, route, api_controller
from .schemas import *
from django.utils import timezone
from ninja.errors import HttpError
app = NinjaExtraAPI()

def grab_neccessary_info(self, returningCitizen, firstTime):
    ## Parole Address
        try:
            parole_address_instance = ParoleAddress.objects.get(returning_citizen_id=returningCitizen.userID)
            parole_address_data = model_to_dict(parole_address_instance)
        except ParoleAddress.DoesNotExist:
            parole_address_data = None

        ## Daily Action
        try:
            daily_action_instance = DailyAction.objects.filter(returning_citizen_id=returningCitizen.userID)
            daily_action_data = [model_to_dict(instance) for instance in daily_action_instance]
        except DailyAction.DoesNotExist:
            daily_action_data = None

        ## Daily Response
        try:
            daily_response_instance = DailyResponse.objects.filter(returning_citizen_id=returningCitizen.userID)
            daily_response_data = [model_to_dict(instance) for instance in daily_response_instance]
        except DailyResponse.DoesNotExist:
            daily_response_data = None
        
        ## Mentor
        if returningCitizen.myMentor is not None:
            try:
                mentor_data = model_to_dict(Mentor.objects.get(mentor_id=returningCitizen.myMentor.mentor_id))
            except Mentor.DoesNotExist:
                pass

        ## Parole Officer
        if returningCitizen.myParoleOfficer is not None:
            try:
                po_data = model_to_dict(ParoleOfficer.objects.get(parole_officer_id=returningCitizen.myParoleOfficer.parole_officer_id))
            except ParoleOfficer.DoesNotExist:
                pass

        if firstTime:
            return {"userID" : str(returningCitizen.userID),
                    "returning_citizen": returningCitizen, 
                    "parole_address": parole_address_data, 
                    "mentor": mentor_data, 
                    "parole_officer": po_data, 
                    "daily_actions": daily_action_data,
                    "daily_responses": daily_response_data}
        else:
            return {"userID" : "nil",
                    "returning_citizen": returningCitizen, 
                    "parole_address": parole_address_data, 
                    "mentor": mentor_data, 
                    "parole_officer": po_data, 
                    "daily_actions": daily_action_data,
                    "daily_responses": daily_response_data}



@api_controller('/user', tags=['User'], permissions=[])
class TempUserController:
    # First Login for new User Loging into their account
    @route.get("/{apikey}/{login}/", response= FirstTimeLoginSchema)
    def first_get(self, apikey: str, login: str):
        temp = get_object_or_404(TempUserLogin, login=login)
        current_time = timezone.now().date()
        returningCitizen = get_object_or_404(ReturningCitizen, userID=temp.returning_citizen.userID)

        if not current_time <= temp.valid_until:
           error_message = "User expired."
           raise HttpError(404, error_message)

        temp.delete()
        api_key_entry = ApiKeyForReturningCitizen(apikey=apikey, returning_citizen=returningCitizen)
        api_key_entry.save()

        return grab_neccessary_info(self, returningCitizen, firstTime=True)
    
    @route.get("/{apikey}/", response=FullReturningCitizenSchema)
    def get_citizen(self, apikey:str):
        user = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        returningCitizen = get_object_or_404(ReturningCitizen, userID=user.returning_citizen.userID)

        # Error Handling
        if not user.returning_citizen.active:
            error_message = "User is Inactive"
            raise HttpError(404, error_message)

                    # Grab other information from other tables in db  #
        return grab_neccessary_info(self, returningCitizen, firstTime=False)


        


            
app.register_controllers(
    TempUserController,
)
