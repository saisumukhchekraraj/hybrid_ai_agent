from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
import random
import torch
MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

model.eval()

SYMPTOM_DURATION = [
    "since yesterday",
    "since this morning",
    "for two days",
    "for three days",
    "for about a week",
    "for ten days",
    "for two weeks",
    "for three weeks",
    "for a month",
    "for six weeks",
    "for two months",
    "for three months",
    "for six months",
    "for almost a year",
    "on and off for a few months",
]
 
# {SYMPTOM_SEVERITY}
SYMPTOM_SEVERITY = [
    "mild",
    "moderate",
    "severe",
    "occasional",
    "constant",
    "unbearable",
    "manageable",
    "worsening",
    "intermittent",
    "persistent",
]
OCCUPATION = [
    "office worker",
    "teacher",
    "construction worker",
    "nurse",
    "delivery rider",
    "student",
    "software engineer",
    "farmer",
    "chef",
    "shopkeeper",
    "factory worker",
    "athlete",
    "homemaker",
    "retired government employee",
    "salesperson",
    "accountant",
    "police officer",
    "long-distance driver",
]
 
# {BODY_PART}
BODY_PART = [
    "lower back",
    "upper back",
    "right knee",
    "left knee",
    "right shoulder",
    "left shoulder",
    "chest",
    "stomach",
    "lower abdomen",
    "right ear",
    "left ear",
    "right eye",
    "left eye",
    "throat",
    "neck",
    "right wrist",
    "left ankle",
    "head",
    "jaw",
    "right hip",
    "left elbow",
    "right foot",
]
 
# {LIFESTYLE}
LIFESTYLE = [
    "sedentary",
    "very active",
    "smoking",
    "heavy drinking",
    "poor sleep",
    "high-stress",
    "frequent traveling",
    "irregular eating",
    "night-shift",
    "vegetarian",
    "gym-focused",
    "desk-bound",
]
 
# {PATIENT_TYPE}
PATIENT_TYPE = [
    "new",
    "returning",
    "walk-in",
    "referred",
    "follow-up",
    "self-referred",
    "insurance-covered",
    "emergency",
    "routine check-up",
]
 
# {SEASON}
SEASON = [
    "summer",
    "winter",
    "monsoon",
    "spring",
    "autumn",
    "rainy season",
    "flu season",
    "allergy season",
]
 
prompts = [

    # Generic
    "Write one short sentence a patient says to a doctor about a health problem. First person, simple words, no diagnosis, no treatment: I",
    "Apatient sits down with the doctor and says: I have been",
    "Write a short, natural, everyday sentence describing a common complaint. No medical terms, no diagnosis: Lately, I",
    "The doctor asks what's wrong. The patient replies in one plain sentence, no diagnosis: I've been",

    # Age-aware
    "A {AGE}-year-old patient tells the doctor about a problem. One first-person sentence, no diagnosis: I",
    "The patient, {AGE} years old, opens the visit by saying: My",
    "Write a natural sentence a {AGE}-year-old might say out loud to a doctor. Simple words, no advice: For the past few days, I",
    "The nurse asks the {AGE}-year-old patient what's wrong. Patient replies: I",

    # Gender-aware
    "A {GENDER} patient describes a symptom. One first-person sentence, simple words, no diagnosis: I",
    "The {GENDER} patient turns to the doctor and says: My",
    "Write a short, natural complaint a {GENDER} patient might share, no medical terms: Since last week, I",
    "Asked how they're feeling, the {GENDER} patient answers in one sentence: I've been",

    # Department-aware
    "A patient visiting {DEPARTMENT} describes a problem typical for that department. One sentence, no diagnosis: I",
    "At the clinic, the patient tells the doctor: I've been",
    "Write a one-sentence complaint a patient would bring to {DEPARTMENT}. Simple words, no medical jargon: My",
    "The patient sits with the specialist in {DEPARTMENT} and says: I have",

    # Severity-aware
    "A patient describes a {SYMPTOM_SEVERITY} symptom. One first-person sentence, no diagnosis: I have",
    "The patient tells the nurse the problem is {SYMPTOM_SEVERITY} and says: It",
    "Write a natural sentence where the patient calls their symptom {SYMPTOM_SEVERITY}, no advice: Lately, my",
    "Asked how bad it is, the patient says it's {SYMPTOM_SEVERITY} and adds: I",

    # Duration-aware
    "A patient has had a problem in the {BODY_PART} for {SYMPTOM_DURATION}. One sentence, no diagnosis: I've had",
    "The patient tells the doctor: For {SYMPTOM_DURATION} now, I",
    "Write a short complaint mentioning the symptom has lasted {SYMPTOM_DURATION}. Simple words, no advice: My",
    "The doctor asks how long this has been going on. Patient replies: This has been going on for {SYMPTOM_DURATION}, and",

    # Lifestyle-aware
    "A patient with a {LIFESTYLE} lifestyle describes a symptom. One sentence, no diagnosis: I",
    "The patient mentions their {LIFESTYLE} routine and says: My",
    "Write a natural complaint that fits someone with a {LIFESTYLE} routine, no medical terms: Lately, I",
    "Asked about their habits, the patient with a {LIFESTYLE} lifestyle says: I",

    # Occupation-aware
    "A patient who works as a {OCCUPATION} describes a symptom. One sentence, no diagnosis: I",
    "The patient, a {OCCUPATION}, tells the doctor: My",
    "Write a natural complaint a {OCCUPATION} might bring to the doctor, simple words: Because of my job, I",
    "The doctor asks what the patient does for work. The {OCCUPATION} patient replies, then adds: I",

    # Elderly patient
    "An elderly {AGE}-year-old patient describes a health problem. One sentence, simple words, no diagnosis: I",
    "The elderly patient sits down slowly and says: Lately, my",
    "Write a natural complaint an elderly patient in their {AGE}s might say, no advice: These days, I",
    "The nurse asks the elderly {GENDER} patient how they've been. Patient answers: I've been",

    # Child (spoken by parent)
    "A parent describes their {AGE}-year-old child's symptom. One sentence spoken by the parent, no diagnosis: My child",
    "The worried parent tells the pediatrician: For the past few days, my child",
    "Write a natural sentence a parent says about their child's health, simple words: My {AGE}-year-old has been",
    "The doctor asks the parent what's wrong with the child. Parent replies: My child keeps",

    # Sports injury
    "A patient injured while playing sports describes the problem. One sentence, no diagnosis: I hurt my",
    "The patient tells the doctor: While playing sports, I",
    "Write a natural complaint about a sports injury to the {BODY_PART}, simple words, no advice: My {BODY_PART}",
    "Asked what happened, the patient says it was during a game and adds: My {BODY_PART}",

    # Seasonal illness
    "A patient describes a common {SEASON} illness. One sentence, no diagnosis: I",
    "The patient tells the doctor: Now that it's {SEASON}, I",
    "Write a natural complaint typical during {SEASON}, simple words, no advice: Every {SEASON}, I",
    "The patient blames the {SEASON} weather and says: Ever since it turned {SEASON}, I",

    # Follow-up visit
    "A patient returning for a follow-up describes how they feel now. One sentence, no diagnosis: Since my last visit, I",
    "The patient at a follow-up appointment tells the doctor: I'm back because",
    "Write a short, natural update a patient gives at a follow-up, simple words: My symptom",
    "The doctor asks if things have improved. The patient replies: It's",

    # Chronic symptom
    "A patient describes a symptom that keeps coming back. One sentence, no diagnosis: I keep getting",
    "The patient tells the doctor: Every few weeks, I",
    "Write a natural complaint about a long-lasting, recurring symptom, simple words: On and off for a while now, I",
    "Asked if this has happened before, the patient says: Yes, this keeps happening, and",

    # Sudden symptom
    "A patient describes a symptom that started suddenly. One sentence, no diagnosis: Suddenly, I",
    "The patient tells the doctor: Out of nowhere, I",
    "Write a natural complaint about a symptom that came on all at once, simple words: It happened all of a sudden, and",
    "Asked when it started, the patient says: Just this morning, I",

    # Mild symptom
    "A patient describes a mild, minor symptom. One sentence, no diagnosis: I have a slight",
    "The patient shrugs and tells the doctor: It's not too bad, but I",
    "Write a natural complaint about a mild symptom that isn't very concerning, simple words: Just a bit of",
    "Asked how they're feeling, the patient says: Nothing serious, but my",

    # Moderate symptom
    "A patient describes a moderate symptom that's starting to bother them. One sentence, no diagnosis: I",
    "The patient tells the doctor: It's uncomfortable and I",
    "Write a natural complaint about a moderate symptom that's hard to ignore, simple words: It's not unbearable, but my",
    "Asked how bad it is, the patient says: It's noticeable now, and",

    # Severe symptom
    "A patient describes a severe symptom that's hard to bear. One sentence, no diagnosis: I have severe",
    "The patient tells the doctor: The pain is so bad that I",
    "Write a natural complaint about a severe symptom, simple words, no advice: My {BODY_PART}",
    "Visibly in pain, the patient tells the doctor: I can barely",

    # Emergency-like (without diagnosis)
    "A patient rushed in urgently describes what's wrong. One sentence, no diagnosis: I suddenly",
    "The patient, clearly in distress, tells the doctor: Right now, I",
    "Write a short, urgent-sounding complaint a patient says in an emergency, no diagnosis, no advice: I can't",
    "Rushed into {DEPARTMENT}, the patient gasps: It started a few minutes ago and I",

    # Multi-symptom (maximum two symptoms)
    "A patient describes two symptoms together in one sentence, no diagnosis, no more than two symptoms: I have",
    "The patient tells the doctor: For the past {SYMPTOM_DURATION}, I've had",
    "Write a natural complaint mentioning exactly two symptoms, simple words, no diagnosis: Along with the pain, I've also had",
    "Asked if anything else is bothering them, the patient adds: My {BODY_PART} and",

]
departments = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology", "Gastroenterology", "Oncology", "Ophthalmology", "Psychiatry", "Urology"]
   
def generate_complaint(age, gender):
    prompt = prompts[random.randint(0, len(prompts) - 1)].format(
        AGE=age,
        GENDER=gender,
        DEPARTMENT=random.choice(departments),
        SYMPTOM_DURATION=random.choice(SYMPTOM_DURATION),
        BODY_PART=random.choice(BODY_PART),
        SYMPTOM_SEVERITY=random.choice(SYMPTOM_SEVERITY),
        LIFESTYLE=random.choice(LIFESTYLE),
        OCCUPATION=random.choice(OCCUPATION),
        SEASON=random.choice(SEASON)
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
            temperature=0.2,
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