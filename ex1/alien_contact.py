from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: Annotated[str, Field(min_length=5, max_length=15)]
    timestamp: datetime
    location: Annotated[str, Field(min_length=3, max_length=100)]
    contact_type: ContactType
    signal_strength: Annotated[float, Field(ge=0, le=10)]
    duration_minutes: Annotated[int, Field(ge=1, le=1440)]
    witness_count: Annotated[int, Field(ge=1, le=100)]
    message_received: Optional[Annotated[str, Field(max_length=500)]] = None
    is_verified: Annotated[bool, Field(default=False)]

    @model_validator(mode="after")
    def check(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contacts must be verified")
        if self.contact_type == ContactType.TELEPATHIC and \
           self.witness_count < 3:
            raise ValueError("Telepathic contacts must have at " +
                             "least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals must have a message received")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("========================================\n")
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 6, 1, 14, 30),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}\n" +
          f"Timestamp: {contact.timestamp.strftime('%d-%m-%Y %H:%M')}\n" +
          f"Location: {contact.location}\n" +
          f"Contact Type: {contact.contact_type.value}\n" +
          f"Signal Strength: {contact.signal_strength}\n" +
          f"Duration: {contact.duration_minutes} minutes\n" +
          f"Witness Count: {contact.witness_count}\n" +
          f"Message Received: {contact.message_received}\n" +
          f"Verified: {contact.is_verified}")

    print("========================================\n")
    print("Expected validation error:")
    try:
        contact2 = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 6, 1, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
        print(contact2)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
