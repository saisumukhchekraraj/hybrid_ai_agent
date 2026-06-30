from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
import random
import torch
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)
model.eval()
prompts=[
    
    # Reception desk
    "A {age}-year-old {gender} patient walks up to the {department} reception desk and says: I",
    "At {department} reception, the {gender} patient, age {age}, tells the receptionist: My",
    "{age}-year-old {gender} patient leans over the {department} counter and says: I have",
    "A {age}-year-old {gender} approaches {department} reception and says: Since yesterday, I",
    "{department} reception desk. A {age}-year-old {gender} patient walks in. Patient says:",
    "At the {department} front desk, a {age}-year-old {gender} tells the staff: I've been",
    "A {age}-year-old {gender} patient stops at {department} reception. Patient:",
    "{age}-year-old {gender} patient checks in at {department} reception. My",
    "At {department} reception, a {age}-year-old {gender} patient explains: I have",
    "A {age}-year-old {gender} walks into {department} reception and tells the clerk: I've been",

    # Nurse triage
    "A nurse asks a {age}-year-old {gender} patient in {department} what's wrong. Patient says:",
    "During triage in {department}, the {gender} patient, age {age}, tells the nurse: I",
    "{age}-year-old {gender} patient sits with the {department} triage nurse and says: I have",
    "The {department} nurse asks what brought the {age}-year-old {gender} patient in today. My",
    "At {department} triage, a {age}-year-old {gender} patient tells the nurse: I've been",
    "{age}-year-old {gender} patient describes the problem to the {department} nurse: Since yesterday, I",
    "The triage nurse in {department} listens to the {age}-year-old {gender} patient. Patient:",
    "A {age}-year-old {gender} patient tells the {department} triage nurse: I have",
    "{department} triage. The {gender} patient, {age} years old, says: My",
    "The nurse in {department} asks the {age}-year-old {gender} patient to explain. Patient says:",

    # Walk-in consultation
    "A {age}-year-old {gender} walks into {department} for a consultation and tells the doctor: I",
    "During a walk-in visit to {department}, the {age}-year-old {gender} patient says: I have",
    "{age}-year-old {gender} patient walks into {department} without an appointment. I've been",
    "The doctor in {department} greets a {age}-year-old {gender} walk-in patient. Patient says:",
    "A {age}-year-old {gender} shows up at {department} unannounced and tells the doctor: My",
    "Walking into {department}, the {age}-year-old {gender} patient tells the doctor: Since yesterday, I",
    "{age}-year-old {gender} patient takes a seat in {department}. Patient:",
    "A {age}-year-old {gender} patient enters {department} for a same-day visit and says: I have",
    "The {department} doctor asks the walk-in {age}-year-old {gender} patient what's wrong. My",
    "{age}-year-old {gender} patient sits across from the {department} doctor and says: I've been",

    # OPD registration
    "At {department} OPD registration, a {age}-year-old {gender} patient tells the clerk: I",
    "{age}-year-old {gender} patient fills out the {department} OPD form and says: I have",
    "During OPD registration in {department}, the {gender} patient, age {age}, says: My",
    "A {age}-year-old {gender} patient at {department} OPD tells the registrar: I've been",
    "{department} OPD desk. A {age}-year-old {gender} patient. Since yesterday, I",
    "At {department} OPD, a {age}-year-old {gender} patient is asked why they came. Patient says:",
    "{age}-year-old {gender} patient registers at {department} OPD. Patient:",
    "A {age}-year-old {gender} patient waits to register at {department} OPD and says: I have",
    "At {department} OPD registration, the {gender} patient, age {age}, begins: My",
    "{age}-year-old {gender} patient hands over their {department} OPD slip and says: I've been",

    # Telephone appointment
    "A {age}-year-old {gender} calls {department} to book an appointment and says: I",
    "On the phone with {department}, a {age}-year-old {gender} patient explains: I have",
    "{age}-year-old {gender} patient calls the {department} clinic and tells the receptionist: I've been",
    "Calling {department} for an appointment, the {gender} patient, age {age}, says: My",
    "A {age}-year-old {gender} phones {department} and tells the staff: Since yesterday, I",
    "{department} clinic gets a call from a {age}-year-old {gender} patient. Patient says:",
    "On a call to {department}, a {age}-year-old {gender} patient. Patient:",
    "A {age}-year-old {gender} dials {department} to ask for a slot and says: I have",
    "Over the phone, a {age}-year-old {gender} patient tells {department} staff: I've been",
    "{age}-year-old {gender} patient calls {department} and begins: My",

    # Follow-up visit
    "Back in {department} for a follow-up, the {age}-year-old {gender} patient says: I",
    "{age}-year-old {gender} patient returns to {department} and tells the doctor: I have",
    "At a {department} follow-up visit, the {gender} patient, age {age}, says: I've been",
    "A {age}-year-old {gender} patient comes back to {department} and says: Since yesterday, I",
    "During a {department} check-up, the {age}-year-old {gender} patient mentions: My",
    "{age}-year-old {gender} patient at a {department} follow-up appointment. Patient:",
    "Returning to {department}, a {age}-year-old {gender} patient tells the nurse: I",
    "A {age}-year-old {gender} patient back in {department} this week says: I have",
    "At the {department} follow-up, the {gender} patient, age {age}, begins: I've been",
    "{age}-year-old {gender} patient revisits {department} and tells the doctor: My",

    # New patient visit
    "A new {age}-year-old {gender} patient at {department} tells the doctor: I",
    "On their first {department} visit, the {age}-year-old {gender} patient says: I have",
    "{age}-year-old {gender} patient, new to {department}, tells the staff: I've been",
    "A first-time {department} patient, age {age}, {gender}, says: Since yesterday, I",
    "{department} welcomes a new {age}-year-old {gender} patient. Patient says:",
    "On a first visit to {department}, a {age}-year-old {gender} patient. Patient:",
    "A new patient in {department}, {age} years old, {gender}, says: I have",
    "{age}-year-old {gender} patient, visiting {department} for the first time, says: I've been",
    "A first-time {gender} patient, age {age}, at {department} tells the doctor: My",
    "New to {department}, a {age}-year-old {gender} patient explains: Since yesterday, I",

    # Emergency arrival
    "A {age}-year-old {gender} patient rushed into {department} says: I",
    "Brought into {department} urgently, the {age}-year-old {gender} patient says: I have",
    "{age}-year-old {gender} patient arrives at {department} in distress and says: I've been",
    "Rushed to {department}, a {age}-year-old {gender} patient tells the doctor: My",
    "An emergency case in {department}, the {gender} patient, age {age}, says: Since yesterday, I",
    "{department} emergency entrance. A {age}-year-old {gender} patient arrives. Patient says:",
    "A {age}-year-old {gender} patient brought into {department} urgently. Patient:",
    "Arriving at {department} in a hurry, the {age}-year-old {gender} patient says: I have",
    "{age}-year-old {gender} patient rushed to {department} tells the staff: I've been",
    "An urgent {department} case, the {gender} patient, age {age}, begins: My",

    # Conversation starter
    "A {age}-year-old {gender} patient in {department} starts the conversation: I",
    "{age}-year-old {gender} patient turns to the {department} doctor and says: I have",
    "Starting the visit in {department}, the {gender} patient, age {age}, says: I've been",
    "A {age}-year-old {gender} patient breaks the ice in {department} by saying: My",
    "{age}-year-old {gender} patient opens up in {department} and says: Since yesterday, I",
    "In {department}, a {age}-year-old {gender} patient is asked to explain. Patient says:",
    "A {age}-year-old {gender} patient starts off in {department}. Patient:",
    "{age}-year-old {gender} patient kicks off the {department} visit and says: I have",
    "Beginning the {department} appointment, the {gender} patient, age {age}, says: I've been",
    "A {age}-year-old {gender} patient opens the conversation in {department}: My",

    # Patient introduction
    "Introducing themselves in {department}, a {age}-year-old {gender} patient says: I",
    "A {age}-year-old {gender} patient introduces their visit to {department} and says: I have",
    "{age}-year-old {gender} patient, here for {department}, says: I've been",
    "A {age}-year-old {gender} patient steps into {department} and introduces the problem: My",
    "Meeting the {department} doctor, a {age}-year-old {gender} patient says: Since yesterday, I",
    "{department} visit begins. The {age}-year-old {gender} patient enters. Patient says:",
    "A {age}-year-old {gender} patient greets the {department} doctor. Patient:",
    "{age}-year-old {gender} patient meets the {department} team and says: I have",
    "Introducing the visit, a {age}-year-old {gender} patient in {department} says: I've been",
    "A {age}-year-old {gender} patient sits down in {department} and says: My",

]
departments = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology", "Gastroenterology", "Oncology", "Ophthalmology", "Psychiatry", "Urology"]
   
def generate_complaint(age, gender):
    prompt = prompts[random.randint(0, len(prompts) - 1)].format(
        age=age,
        gender=gender,
        department=departments[random.randint(0, len(departments) - 1)]
    )


    inputs = tokenizer(
    prompt,
    return_tensors="pt"
)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=True,
            early_stopping=True,
            temperature=0.8,
            top_k=50,
            top_p=0.95
)
    response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)    
    
    complaint = response
    return complaint
if __name__ == "__main__":
    age=random.randint(1, 100)
    gender=random.choice(["male", "female"])
    complaint = generate_complaint(age, gender)
    print(type(complaint))
    print(complaint)