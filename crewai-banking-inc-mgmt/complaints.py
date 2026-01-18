COMPLAINTS = [
    "Card transaction declined despite having sufficient balance",
    "Unauthorized transactions detected but credit not reversed for 2 weeks",
    "Mobile app freezes during payment processing",
    "Interest rate increased without prior notification",
    "Credit score dropped after paying off balance"
]

COMPLAINT_TEXT = "\n".join([f"- {c}" for c in COMPLAINTS])
