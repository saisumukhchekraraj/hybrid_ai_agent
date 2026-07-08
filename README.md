# Hybrid AI Agent

A production-oriented **Hybrid Intelligent Healthcare Agent** that combines:

- Local ML Intent Classification *(coming in later phases)*
- Google Gemini for natural language reasoning
- LangChain for tool integration
- LangGraph for workflow orchestration and agent state management
- FastAPI backend services
- SQLite database
- Structured business-rule execution

The project simulates an intelligent hospital assistant capable of interacting naturally with users while maintaining deterministic workflow logic for patient lookup, appointment scheduling, and booking.

---

# 📁 Project Structure

```text
hybrid_ai_agent/
│
├── app/
│   │
│   ├── api/
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   └── patients.py              # LangChain tool wrappers
│   │   │
│   │   ├── __init__.py
│   │   └── language_chain.py            # Gemini + LangChain configuration
│   │
│   ├── classifier/
│   │   └── __init__.py                  # Reserved for local ML intent classifier
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── sqlite.py
│   │   ├── sqlite_patients.py
│   │   ├── sqlite_docs.py
│   │   └── sqlite_appointments.py
│   │
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── graph.py                     # LangGraph workflow
│   │   ├── nodes.py                     # Workflow nodes
│   │   └── state.py                     # AgentState definition
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── data_generator.py
│   │   └── hugging_face.py
│   │
│   └── crud_demo/
│       ├── chat_db.py
│       └── crud_demo.py
│
├── data/
│   ├── patients.csv
│   ├── doctors.csv
│   ├── doctors_schedules.csv
│   └── appointments.csv
│
├── images/
│
├── hospital_records.db
├── generate_csv.py
├── import_csv.py
├── main.py
├── tests.py                            # Interactive LangGraph terminal agent
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# ✅ Phase 1 — Backend Development

## Features

- SQLite relational database
- Faker-based synthetic hospital dataset generation
- CSV generation and SQLite import
- Modular database architecture
- FastAPI CRUD APIs
- Patient lookup endpoint
- Doctor availability endpoint
- Appointment booking endpoint
- Swagger API documentation

---

## Implemented APIs

### Patient Lookup

`POST /patients/lookup`

---

### Create Patient

`POST /patients/new`

---

### Doctor Availability

`POST /doctors/availability`

---

### Appointment Booking

`POST /appointments/book`

---

# ✅ Phase 2 — AI Agent Integration

Phase 2 transformed the backend into an AI-powered assistant.

## Features

- LangChain integration
- Google Gemini 2.5 Flash integration
- LangChain tool calling
- AI-powered patient lookup
- AI-powered doctor availability
- AI-powered appointment booking
- Interactive terminal agent
- Multi-tool reasoning
- End-to-end backend verification

---

## Available AI Tools

### lookup_patient

Looks up an existing patient.

---

### create_patient

Creates a new patient record.

---

### get_doctor_availability

Retrieves available appointment slots.

---

### book_appointment

Books an appointment for an existing patient.

---

# ✅ Phase 3 — LangGraph Workflow Orchestration

Phase 3 transforms the project from a **ReAct Tool Calling Agent** into a **Workflow-Oriented AI Agent**.

Instead of allowing the LLM to control the complete execution, LangGraph now orchestrates the workflow while AgentState stores structured application memory.

---

## Workflow Architecture

```text
User
   │
   ▼
Gemini
   │
   ▼
ToolNode
   │
   ▼
Workflow State Synchronization
   │
   ▼
Business Rule Nodes
   │
   ▼
Gemini
```

---

## Phase 3 Features

### LangGraph Integration

- StateGraph implementation
- Workflow orchestration
- Conditional routing
- ToolNode integration
- Graph compilation

---

### AgentState

Structured workflow memory introduced.

Current workflow state stores

- Conversation history
- Patient ID
- Patient status
- Appointment duration
- Department
- Appointment date
- Available slots
- Booking status

---

### Workflow Nodes

Implemented workflow nodes including

- LLM reasoning node
- Workflow synchronization node
- Duration business-rule node

---

### Tool Synchronization

Workflow automatically synchronizes

#### Tool Outputs

- Patient lookup results
- Patient creation results
- Available doctor slots
- Booking confirmation

#### Tool Arguments

Gemini's structured tool arguments are synchronized into AgentState.

Currently synchronized:

- Department
- Appointment Date

This avoids natural language parsing and keeps workflow memory synchronized with the agent's reasoning.

---

### Business Rules

Deterministic business logic has been separated from the LLM.

Implemented rule:

- New Patient → 60 minute appointment
- Returning Patient → 30 minute appointment

Appointment duration is now determined by workflow state rather than by Gemini.

---

### Multi-turn Conversation

The agent now supports

- Natural conversation
- Multi-step reasoning
- Multiple tool calls
- Stateful execution
- Workflow-aware decision making

---

### Interactive Terminal Agent

An interactive terminal interface was developed for testing.

Supports

- Continuous conversation
- Live LangGraph execution
- Workflow state inspection
- AgentState debugging
- Tool execution tracing

---

# Current Architecture

```text
                User
                  │
                  ▼
             Google Gemini
                  │
                  ▼
          LangGraph Workflow
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
 Business Rules          LangChain ToolNode
      │                       │
      └───────────┬───────────┘
                  ▼
            FastAPI Backend
                  │
                  ▼
             SQLite Database
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- SQLite
- Pydantic

## AI

- Google Gemini 2.5 Flash
- LangChain
- LangGraph

## Database

- SQLite
- Faker
- Pandas

## Development

- Uvicorn
- Swagger UI
- Git
- VS Code

---

# Current Progress

| Phase | Status |
|--------|--------|
| Backend APIs | ✅ Complete |
| SQLite Database | ✅ Complete |
| LangChain Integration | ✅ Complete |
| Gemini Tool Calling | ✅ Complete |
| ReAct Agent | ✅ Complete |
| LangGraph Integration | ✅ Complete |
| AgentState | ✅ Complete |
| Workflow Synchronization | ✅ Complete |
| Business Rule Nodes | ✅ Complete |
| Multi-turn Workflow | ✅ Complete |

---

