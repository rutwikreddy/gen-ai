import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
MODEL = "gpt-4o-mini"

# Organization Context
ORG_CONTEXT = {
    "product": "FinCore Banking Platform (Mobile + Web + ATM)",
    "stack": {
        "backend": "Java Spring Boot + Oracle DB + Redis Cache",
        "transactions": "Real-time payment processing + Visa/Mastercard integration",
        "security": "2FA + Biometric auth + Encryption at rest",
        "fraud": "ML-based fraud detection + Manual review queue",
        "observability": "ELK Stack + Splunk + DataDog",
    },
    "recent_changes": [
        {
            "date": "2026-01-15",
            "release": "v5.2.0",
            "notes": [
                "Upgraded transaction processing engine for real-time settlement",
                "New fraud detection ML model deployed with stricter thresholds",
                "Mobile app UI redesign with new payment flow",
                "Interest rate calculation algorithm refactored for accuracy",
            ],
        }
    ],
    "known_incidents": [
        {
            "date": "2025-12-20",
            "summary": "Fraud detection flagging legitimate transactions during peak hours",
            "mitigation": "Lowered ML model thresholds but caused delayed reversals",
        },
        {
            "date": "2026-01-05",
            "summary": "Transaction processing delays due to Visa gateway connectivity issues",
            "mitigation": "Added fallback to Mastercard but not all merchant terminals updated",
        }
    ],
    "sla_targets": {
        "transaction_settlement_s": "<5s",
        "card_decline_rate": "<0.5%",
        "fraud_detection_accuracy": ">=95%",
        "dispute_resolution_days": "<=14",
        "app_availability_pct": ">=99.9%",
    }
}
