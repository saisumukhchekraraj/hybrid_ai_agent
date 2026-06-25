# hybrid-ai-agent
Hybrid Intelligent Agent combining local ML intent classification with LLM reasoning and tool orchestration.
## 📁 Project Structure

 The following is the folder-map of the structure of this repository, to be used to navigate through the files as needed.
```text
hybrid-ai-agent/
│
├── app/
│   │
│   ├── api/
│   │   └── __init__.py              # API package
│   │
│   ├── classifier/
│   │   └── __init__.py              # Reserved for intent classifier (Phase 2)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── sqlite.py                # SQLite connection, schema and business logic
│   │
│   ├── orchestrator/
│   │   └── __init__.py              # Reserved for AI agent orchestration
│   │
│   ├── ui/
│   │   └── __init__.py              # Reserved for future UI
│   │
│   ├── data_generator.py            # Generates synthetic hospital records using Faker
│   └── hugging_face.py              # Hugging Face model loading and inference
│
├── crud_demo/                       # FastAPI CRUD practice project (learning)
│
├── data/
│   ├── patients.csv                 # Generated patient dataset
│   ├── doctors.csv                  # Generated doctor dataset
│   └── appointments.csv             # Generated appointment dataset
│
├── images/                          # Swagger API screenshots used in README
│
├── tests/                           # Reserved for future testing
│
├── generate_csv.py                  # Generates CSV datasets
├── import_csv.py                    # Imports CSV data into SQLite database
├── hospital_records.db              # SQLite database
├── main.py                          # FastAPI application and API endpoints
├── requirements.txt                 # Project dependencies
├── README.md                        # Project documentation
├── LICENSE                          # Project license
└── .gitignore                       # Git ignore configuration
```
## Phase One

## ✅ Phase One Features

- SQLite database with relational schema
- Synthetic hospital dataset generation using Faker
- CSV generation and import into SQLite
- Patient lookup
- Doctor availability check
- Appointment booking
- Interactive Swagger API documentation

---

## 📌 API Endpoints

### Patient Lookup

`POST /patients/lookup`

**Input**

![Patient Lookup Input](images/patients_lookup_input.png)

**Output**

![Patient Lookup Output](images/patients_lookup_output.png)

---

### Doctor Availability

`POST /doctors/availability`

**Input**

![Doctor Input](images/docs_input.png)

**Output**

![Doctor Output](images/docs_output.png)

---

### Appointment Booking

`POST /appointments/book`

**Successful Booking**

**Input**

![Appointment Input](images/appoint_1_input.png)

**Output**

![Appointment Output](images/appoint_1_output.png)

**Invalid Booking**

![Invalid Booking](images/booking_appointment_2.png)

--
##Phase one - Complete
---
