Overview


This project presents a context-bounded Clinical AI Assistant designed for preliminary cardiovascular health assessment in Bangladesh. Rather than relying on a general-purpose chatbot prone to hallucination, the system implements a Retrieval-Augmented Generation (RAG) architecture on top of Google's Gemini 2.5 Flash LLM — ensuring every response is strictly grounded in a curated local medical knowledge base.
The application also integrates a Patient Metrics Engine that computes BMI and BMR (Mifflin-St Jeor Equation) to deliver personalized — not generic — health assessments.
The knowledge base (data/disease_info.txt) covers 6 major cardiovascular and pulmonary conditions with Bangladesh-specific emergency protocols:
Hypertension (উচ্চ রক্তচাপ)

Coronary Artery Disease (করোনারি ধমনী রোগ)

Stroke (স্ট্রোক)

Heart Failure (হার্ট ফেইলিওর)

Pulmonary Artery Disease (পালমোনারি ধমনী রোগ)

Pulmonary Embolism (পালমোনারি এম্বোলিজম)

Each entry includes: Identifying Characteristics, user matrics, Treatment advices, and Local Action Protocols (CMCH, Anderkilla General Hospital, Hotline: 16263).

AI Approach flowchart:
[User Input: Symptoms + Patient Metrics]

              │
              ▼
              
[Ingestion Layer: Normalize & Tokenize Input]

              │
              ▼
              
[Retrieval Layer: Keyword-Based RAG Scan → disease_info.txt]

              │
              ▼
              
[Generation Layer: Token-Optimized Prompt Boundary]

              │
              ▼
              
[Engine: Gemini 2.5 Flash API — In-Context Learning]

              │
              ▼
              
[Output UI: Streamlit Streamed Markdown + Medical Disclaimer]

Key Design Choice: No model fine-tuning. All domain-specific behavior is enforced entirely through Prompt Engineering + ICL (In-Context Learning) at inference time.

CUETAI-SCIBLITZ2026/

│

├── app.py                  # Main Streamlit application

├── requirements.txt        # Python dependencies

│
├── data/

│   └── disease_info.txt    # Curated cardiovascular knowledge base

│

└── README.md

Limitations

API rate limits restrict concurrent multi-user access

Keyword-based retrieval may miss relevant sections when user input uses indirect phrasing or synonyms not present in the database

Occasional 503 server errors during Google Cloud peak load periods

Knowledge base currently scoped to 6 conditions due to free-tier token constraints




Future Work

Vector Search Integration — ChromaDB / Pinecone for semantic retrieval supporting 70+ diseases

Hardware-AI Co-Design — RTL modeling and FPGA deployment as an offline Edge-AI medical device

Formal Verification — SystemVerilog / UVM framework for healthcare logic reliability testing

Expanded Knowledge Base — Broader disease categories across infectious, metabolic, and neurological conditions



License
Non-commercial use only. Covered under Google AI Studio Terms of Service for developer usage.

