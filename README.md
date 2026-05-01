# GraphRAG-LangGraph-Neo4j-Travel-Assistant

## 🚀 Overview
An intelligent travel assistant combining GraphRAG, Neo4j, LangGraph agents, and LLMs to generate optimized travel plans.

## 🧠 How It Works
User query → Agents → Neo4j (graph data) + Mock APIs (RAG) → Reasoning → Ranking → LLM → Response

## 📁 Project Structure

I will add this shortly after completion and running it successfuly on local

## 🌐 Mock API Setup (Using Mocki)
1. Go to https://mocki.io/
2. Paste JSON
3. Generate endpoint
4. Use in code

Example:
https://mocki.io/v1/your-endpoint-id

## 🧪 Sample Flight JSON

```
{
  "flight_no": "AI101",
  "airline": "Air India",
  "from": "Delhi",
  "to": "Mumbai",
  "departure_time": "2026-06-01T08:00:00",
  "arrival_time": "2026-06-01T10:10:00",
  "duration_minutes": 130,
  "price": 5500,
  "currency": "INR",
  "aircraft": "Airbus A320",
  "seat_class": ["Economy", "Business"],
  "available_seats": {
    "Economy": 25,
    "Business": 5
  },
  "baggage": {
    "cabin": "7kg",
    "check_in": "15kg"
  },
  "on_time_performance": 0.92,
  "cancellation_probability": 0.03,
  "rating": 4.2,
  "reviews_count": 1240,
  "amenities": ["WiFi", "Meal", "USB Charging"],
  "layovers": [],
  "is_direct": true,
  "carbon_emission_kg": 120,
  "fare_rules": {
    "refundable": false,
    "change_fee": 1500
  },
  "dynamic_pricing_factor": 1.1,
  "demand_score": 0.78,
  "tags": ["fastest", "popular", "morning"]
}

```

## 💡 Why Rich Data Matters
- Better graph reasoning
- Smarter ranking
- Stronger LLM explanations
- Realistic demo

## 💡 Benefits of having this architecture

- separation of concerns
- agent orchestration
- hybrid retrieval
- reasoning layer

## 🧑‍💻 Author


| Name              | Details                             |
|-------------------|-------------------------------------|
| **👨‍💻 Developer**  | Sachin Arora                      |
| **📧 Email**      | [sachnaror@gmail.com](mailto:sacinaror@gmail.com) |
| **📍 Location**   | Noida, India                       |
| **📂 GitHub**     | [Link](https://github.com/sachnaror) |
| **🌐 Youtube**    | [Link](https://www.youtube.com/@sachnaror4841/videos) |
| **🌐 Blog**       | [Link](https://medium.com/@schnaror) |
| **🌐 Website**    | [Link](https://about.me/sachin-arora) |
| **🌐 Twitter**    | [Link](https://twitter.com/sachinhep) |
| **📱 Phone**      | [+91 9560330483](tel:+919560330483) |


------------------------------------------------------------------------
