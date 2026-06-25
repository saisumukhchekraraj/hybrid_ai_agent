# hybrid-ai-agent
Hybrid Intelligent Agent combining local ML intent classification with LLM reasoning and tool orchestration.

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
