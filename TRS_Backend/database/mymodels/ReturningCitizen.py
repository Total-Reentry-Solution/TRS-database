from django.db import models
import uuid
from django.core.exceptions import ValidationError
from .Mentor import Mentor
from .ParoleOfficer import ParoleOfficer
from .ParoleAddress import ParoleAddress
from datetime import date


class ReturningCitizen(models.Model):
    userID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_Name = models.CharField(max_length=32)
    last_Name = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    date_activated = models.DateField(blank = True, null = True)
    date_deactivated = models.DateField(blank = True, null = True)
    MDOC = models.CharField(max_length=6)
    # Mentor Information # =====================================================================================================
    myMentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, null=True, blank=True, related_name='mentor', to_field='mentor_id')    
    def addMentor(self):
        if self.myMentor is not None:
            mentor_instance = Mentor.objects.get(mentor_id=self.myMentor.mentor_id)
            mentor_instance.returning_citizens.add(self)
            mentor_instance.save()
    
    def switchMentor(self, original_user):
        if original_user.myMentor is not None:
            originalmyMentor = Mentor.objects.get(mentor_id=original_user.myMentor.mentor_id)
            originalmyMentor.returning_citizens.remove(self)
            originalmyMentor.save()
        self.addMentor()
    
    def removeMentor(self):
        if self.myMentor is not None:
            mentor_instance = Mentor.objects.get(mentor_id=self.myMentor.mentor_id)
            mentor_instance.returning_citizens.remove(self)
            self.myMentor = None
            self.save()
    # ==========================================================================================================================
    # |
    # |
    # |
    # Parole Officer Information #  --------------------------------------------------------------------------------------------
    myParoleOfficer = models.ForeignKey('ParoleOfficer', on_delete=models.SET_NULL, null=True, blank=True, related_name='parole_officer', to_field='parole_officer_id')

    def addPO(self):
        if self.myParoleOfficer is not None:
            po_instance = ParoleOfficer.objects.get(parole_officer_id=self.myParoleOfficer.parole_officer_id)
            po_instance.returning_citizens.add(self)
            po_instance.save()
    
    def switchPO(self, original_user):
        if original_user.myParoleOfficer is not None:
            original_po = ParoleOfficer.objects.get(parole_officer_id=original_user.myParoleOfficer.parole_officer_id)
            original_po.returning_citizens.remove(self)
            original_po.save()
        self.addPO()
    
    def removePO(self):
        if self.myParoleOfficer is not None:
            po_instance = ParoleOfficer.objects.get(parole_officer_id=self.myParoleOfficer.parole_officer_id)
            po_instance.returning_citizens.remove(self)
            self.myParoleOfficer = None
            self.save()
    # --------------------------------------------------------------------------------------------------------------------------
    # |
    # |
    # |
    # Universal Functions
    def addAll(self):
        self.addMentor()
        self.addPO()
    def removeAll(self):
        self.removeMentor()
        self.removePO()

    def clean(self):
        if not self.active and (self.myMentor or self.myParoleOfficer):
            if self.pk is None or (self.pk is not None and ReturningCitizen.objects.get(pk=self.pk).active == self.active):
                raise ValidationError("An inactive user cannot have a mentor/parole officer assigned.")
        
        if not self.myMentor or not self.myParoleOfficer:
            raise ValidationError("A user must have a Mentor and/or Parole Officer Assigned")



    def save(self, *args, **kwargs):
        if self.pk:
            try:
                original_user = ReturningCitizen.objects.get(pk=self.pk)

                #### -- REMEMBER TO UPDATE ADD ALL / REMOVE ALL #####
                if self.active and (self.myMentor != original_user.myMentor):
                    self.switchMentor(original_user) # Check Mentor Attributes
                if self.active and (self.myParoleOfficer != original_user.myParoleOfficer): 
                    self.switchPO(original_user) # Check Parole Officer Attributes
                #####                                           #####
                if not original_user.active and self.active:
                    self.date_activated = date.today()
                    self.date_deactivated = None

                if original_user.active and not self.active:
                    self.removeAll()
            except ReturningCitizen.DoesNotExist:
                self.addAll()
                pass 
        else:
            super().save(*args, **kwargs)
            self.addAll()
            self.date_activated = date.today()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}"