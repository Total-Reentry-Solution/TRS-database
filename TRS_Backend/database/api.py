from database.mymodels.ReturningCitizen import ReturningCitizen
from database.mymodels.Mentor import Mentor
from database.mymodels.ParoleOfficer import ParoleOfficer
from database.mymodels.Event import Event
from database.mymodels.ParoleAddress import ParoleAddress
from database.mymodels.DailyResponse import DailyResponse
from database.mymodels.TempLogins import TempUserLogin, TempMentorLogin, TempParoleOfficerLogin
from database.mymodels.ApiKeyFor_ import ApiKeyForReturningCitizen, ApiKeyForMentor, ApiKeyForParoleOfficer
from database.mymodels.ThreeDailyActions import ThreeDailyActions
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja_extra import NinjaExtraAPI, route, api_controller
from .schemas import *
from django.utils import timezone
from ninja.errors import HttpError
from django.http import JsonResponse

app = NinjaExtraAPI()


# Helper Functions #

def fetch_all_po_data(self, parole_officer, firstTime):
    parole_officer_data = {
        "po_id": str(parole_officer.parole_officer_id),
        "po_information": {
            "first_Name": parole_officer.first_Name,
            "last_Name": parole_officer.last_Name,
            "phone_number": parole_officer.phone_number,
            "city" : parole_officer.city
        },
        "returning_citizens": []
    }

    for returningCitizen in parole_officer.returning_citizens.all():
        #if not firstTime:
        #userID = "nil"
        #else:
        #userID = str(returningCitizen.userID)

        # Parole Address
        try:
            parole_address_instance = ParoleAddress.objects.get(returning_citizen_id=returningCitizen.userID)
            parole_address_data = model_to_dict(parole_address_instance)
        except ParoleAddress.DoesNotExist:
            parole_address_data = []

        # 3 Daily Actions
        try:
            daily_action_instance = ThreeDailyActions.objects.filter(returning_citizen_id=returningCitizen.userID)
            daily_action_data = [model_to_dict(instance) for instance in daily_action_instance]
        except ThreeDailyActions.DoesNotExist:
            daily_action_data = []

        # Events
        try:
            event_instance = Event.objects.filter(returning_citizen_id=returningCitizen.userID)
            event_data = [model_to_dict(instance) for instance in event_instance]
        except Event.DoesNotExist:
            event_data = []

        # Daily Response
        try:
            daily_response_instance = DailyResponse.objects.filter(returning_citizen_id=returningCitizen.userID)
            daily_response_data = [model_to_dict(instance) for instance in daily_response_instance]
        except DailyResponse.DoesNotExist:
            daily_response_data = []

        # Mentor
        if returningCitizen.myMentor is not None:
            try:
                mentor_data = model_to_dict(Mentor.objects.get(mentor_id=returningCitizen.myMentor.mentor_id))
            except Mentor.DoesNotExist:
                pass

        returning_citizen_data = {
            "userID": str(returningCitizen.userID),
            "returning_citizen": {
                "first_Name": returningCitizen.first_Name,
                "last_Name": returningCitizen.last_Name,
                "MDOC": returningCitizen.MDOC
            },
            "parole_address": parole_address_data,
            "mentor": mentor_data,
            "events": event_data,
            "daily_responses": daily_response_data,
            "daily_actions": daily_action_data,
        }
        parole_officer_data["returning_citizens"].append(returning_citizen_data)


    return parole_officer_data


def fetch_all_mentor_data(self, mentor, firstTime):
    mentor_data = {
        "mentor_id": str(mentor.mentor_id),
        "mentor_information": {
            "first_Name": mentor.first_Name,
            "last_Name": mentor.last_Name,
            "phone_number": mentor.phone_number
        },
        "returning_citizens": []
    }

    
    for returningCitizen in mentor.returning_citizens.all():
        #if not firstTime:
        #userID = "nil"
        #else:
        userID = str(returningCitizen.userID)


        # Parole Address
        try:
            parole_address_instance = ParoleAddress.objects.get(returning_citizen_id=returningCitizen.userID)
            parole_address_data = model_to_dict(parole_address_instance)
        except ParoleAddress.DoesNotExist:
            parole_address_data = []

        # 3 Daily Actions
        try:
            daily_action_instance = ThreeDailyActions.objects.filter(returning_citizen_id=returningCitizen.userID)
            daily_action_data = [model_to_dict(instance) for instance in daily_action_instance]
            
        except ThreeDailyActions.DoesNotExist:
            daily_action_data = []

        # Events
        try:
            event_instance = Event.objects.filter(returning_citizen_id=returningCitizen.userID)
            event_data = [model_to_dict(instance) for instance in event_instance]
        except Event.DoesNotExist:
            event_data = []

        # Daily Response
        try:
            daily_response_instance = DailyResponse.objects.filter(returning_citizen_id=returningCitizen.userID).order_by('date')
            daily_response_data = [model_to_dict(instance) for instance in daily_response_instance]
        except DailyResponse.DoesNotExist:
            daily_response_data = []

        # Parole Officer
        po_data = []
        if returningCitizen.myParoleOfficer:
            try:
                po_instance = ParoleOfficer.objects.get(parole_officer_id=returningCitizen.myParoleOfficer.parole_officer_id)
                po_data = model_to_dict(po_instance)
            except ParoleOfficer.DoesNotExist:
                pass

        returning_citizen_data = {
            "userID": str(returningCitizen.userID),
            "returning_citizen": {
                "first_Name": returningCitizen.first_Name,
                "last_Name": returningCitizen.last_Name,
                "MDOC": returningCitizen.MDOC
            },
            "parole_address": parole_address_data,
            "parole_officer": po_data,
            "events": event_data,
            "daily_responses": daily_response_data,
            "daily_actions": daily_action_data,
        }
        mentor_data["returning_citizens"].append(returning_citizen_data)


    return mentor_data


def fetch_all_rc_data(self, returningCitizen, firstTime):
    ## Parole Address
        try:
            parole_address_instance = ParoleAddress.objects.get(returning_citizen_id=returningCitizen.userID)
            parole_address_data = model_to_dict(parole_address_instance)
        except ParoleAddress.DoesNotExist:
            parole_address_data = None

        ## 3 Daily Actions
        try:
            daily_action_instance = ThreeDailyActions.objects.filter(returning_citizen_id=returningCitizen.userID).order_by('date')
            daily_action_data = [model_to_dict(instance) for instance in daily_action_instance]
            daily_action_data.sort(key=lambda x: x['date'])
        except ThreeDailyActions.DoesNotExist:
            daily_action_data = None
        
        ## Events
        try:
            event_instance = Event.objects.filter(returning_citizen_id=returningCitizen.userID)
            event_data = [model_to_dict(instance) for instance in event_instance]
        except Event.DoesNotExist:
            event_data = None

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
                    "events": event_data,
                    "daily_responses": daily_response_data, 
                    "daily_actions": daily_action_data,}
        else:
            return {"userID" : "nil",
                    "returning_citizen": returningCitizen, 
                    "parole_address": parole_address_data, 
                    "mentor": mentor_data, 
                    "parole_officer": po_data, 
                    "events": event_data,
                    "daily_responses": daily_response_data,
                    "daily_actions": daily_action_data}





# Api #
        
@api_controller('/update', tags=['Add'], permissions=[])
class UpdateController:
    @route.post("/daily_action/", permissions=[])
    def post_daily_action(self, helpers: List[CreateDailyActionHelper]):
        new_daily_actions = []
        returning_citizen = get_object_or_404(ReturningCitizen, userID=helpers[0].returning_citizen_id)
        print(helpers)
        for helper in helpers:
            print(f"Current Daily Action: {helper.description} on {helper.date}")

            new_instance = ThreeDailyActions(
                date_id = helper.date_id,
                date = helper.date,
                description = helper.description,
                returning_citizen = returning_citizen,
                is_completed = helper.is_completed,
                date_only = helper.date.date()
            )


            already_exists = ThreeDailyActions.objects.filter(date_only=new_instance.date_only, date_id=new_instance.date_id)

            if already_exists.exists():
                print("already exists, updated")
                existing_instance = already_exists.first()
                if new_instance.date != existing_instance.date or new_instance.description != existing_instance.description or new_instance.is_completed != existing_instance.is_completed:
                    print("something changed, saving")
                    existing_instance.date = new_instance.date
                    existing_instance.description = new_instance.description
                    existing_instance.is_completed = new_instance.is_completed
                    existing_instance.save()
            else:
                print("doesnt exist, saving")
                print(f"{new_instance.date_only} {new_instance.date_id}")
            print(f"{new_instance.date_only} {new_instance.date_id}")
            new_instance.save()
    
        print("Finished processing daily actions")
        return helpers
    

    @route.post("/event/", permissions=[])
    def post_event(self, helper: CreateEventHelper):

        returning_citizen = get_object_or_404(ReturningCitizen, userID=helper.returning_citizen_id)
        new_event = Event(
            date=helper.date,
            description=helper.description,
            location=helper.location,
            returning_citizen=returning_citizen
        )

        new_event.save()
        return model_to_dict(new_event)
    
    @route.post("/daily_response/", permissions=[])
    def post_daily_response(self, helper: CreateDailyResonseHelper):

        returning_citizen = get_object_or_404(ReturningCitizen, userID=helper.returning_citizen_id)
        new_daily_response = DailyResponse(
            date=helper.date,
            rating=helper.rating,
            returning_citizen=returning_citizen
        )

        new_daily_response.save()
        return model_to_dict(new_daily_response)



@api_controller('/fetch', tags=['Refresh'], permissions=[])
class FetchController:

    @route.get("/community_health_organizations/{apikey}/", response=List[CommunityHealthOrganizationSchema])
    def fetch_cho(self, apikey: str):
        usr = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        if not usr:
           raise HttpError(404, "apikey not valid")
        
        chos = get_list_or_404(CommunityHealthOrganization)
        return chos
        

    @route.get("/events/{apikey}/", response=List[EventSchema])
    def update_daily_actions(self, apikey: str):
        user = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        events = get_list_or_404(Event, returning_citizen=user.returning_citizen)
        return events

    @route.get("/daily_actions/{apikey}/", response=List[ThreeDailyActionsSchema])
    def update_daily_actions(self, apikey: str):
        user = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        daily_actions = get_list_or_404(ThreeDailyActions, returning_citizen=user.returning_citizen)
        return daily_actions
    
    @route.get("/daily_responses/{apikey}/", response=List[DailyResponseSchema])
    def update_daily_responses(self, apikey: str):
        user = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        daily_responses = get_list_or_404(DailyResponse, returning_citizen=user.returning_citizen)
        return daily_responses

@api_controller('/paroleOfficer', tags=['ParoleOfficer'], permissions=[])
class ParoleOfficerLoginController:
    @route.get('/{apikey}/{login}', response=ParoleOfficerLoginSchema)
    def fetch_po_information_first(self, apikey: str, login: str):
        temp = get_object_or_404(TempParoleOfficerLogin, login=login)
        current_time = timezone.now().date()
        parole_officer = get_object_or_404(ParoleOfficer, parole_officer_id=temp.parole_officer.parole_officer_id)

        if not current_time <= temp.valid_until:
            error_message = "Parole Officer login code expired"
            raise HttpError(404, error_message)
        temp.delete()
        log_apikey = ApiKeyForParoleOfficer(apikey=apikey, parole_officer=parole_officer)
        log_apikey.save()

        return fetch_all_po_data(self, parole_officer, firstTime=True)
    
    @route.get('/{apikey}/', response=ParoleOfficerLoginSchema)
    def fetch_po_information(self, apikey: str):
        temp = get_object_or_404(ApiKeyForParoleOfficer, apikey=apikey)
        parole_officer = get_object_or_404(ParoleOfficer, parole_officer_id=temp.parole_officer.parole_officer_id)

        return fetch_all_po_data(self, parole_officer, firstTime=False)




@api_controller('/mentor', tags=['Mentor'], permissions=[])
class MentorLoginController:
    @route.get('/{apikey}/{login}', response=MentorLoginSchema)
    def fetch_mentor_info_first(self, apikey: str, login: str):
        temp = get_object_or_404(TempMentorLogin, login=login)
        current_time = timezone.now().date()
        mentor = get_object_or_404(Mentor, mentor_id=temp.mentor.mentor_id)

        if not current_time <= temp.valid_until:
            error_message = "Mentor login code expired"
            raise HttpError(404, error_message)
        temp.delete()
        log_apikey = ApiKeyForMentor(apikey=apikey, mentor=mentor)
        log_apikey.save()

        return fetch_all_mentor_data(self, mentor, firstTime=True)
    @route.get('/{apikey}/', response=MentorLoginSchema)
    
    def fetch_mentor_information(self, apikey: str):
        temp = get_object_or_404(ApiKeyForMentor, apikey=apikey)
        mentor = get_object_or_404(Mentor, mentor_id=temp.mentor.mentor_id)

        return fetch_all_mentor_data(self, mentor, firstTime=False)



@api_controller('/user', tags=['User'], permissions=[])
class UserLoginController:
    # First Login for new User Loging into their account
    @route.get("/{apikey}/{login}/", response= FirstTimeLoginSchema)
    def first_get(self, apikey: str, login: str):
        temp = get_object_or_404(TempUserLogin, login=login)
        current_time = timezone.now().date()
        returningCitizen = get_object_or_404(ReturningCitizen, userID=temp.returning_citizen.userID)

        if not current_time <= temp.valid_until:
           error_message = "User login code expired."
           raise HttpError(404, error_message)

        temp.delete()
        api_key_entry = ApiKeyForReturningCitizen(apikey=apikey, returning_citizen=returningCitizen)
        api_key_entry.save()

        return fetch_all_rc_data(self, returningCitizen, firstTime=True)
    

    # User getting up to date with any changes made in the database
    @route.get("/{apikey}/", response=FullReturningCitizenSchema)
    def get_citizen(self, apikey:str):
        user = get_object_or_404(ApiKeyForReturningCitizen, apikey=apikey)
        returningCitizen = get_object_or_404(ReturningCitizen, userID=user.returning_citizen.userID)

        ## Error Handling
        if not user.returning_citizen.active:
            error_message = "User is Inactive"
            raise HttpError(404, error_message)
        return fetch_all_rc_data(self, returningCitizen, firstTime=False)


        
app.register_controllers(
    UserLoginController,
    FetchController,
    UpdateController,
    MentorLoginController,
    ParoleOfficerLoginController
)
