from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from datetime import datetime


class Rank(Enum):
    CADET = "Cadet"
    OFFICER = "Officer"
    LIEUTENANT = "Lieutenant"
    CAPTAIN = "Captain"
    COMMANDER = "Commander"


class CrewMember(BaseModel):
    member_id: Annotated[str, Field(min_length=3, max_length=10)]
    name: Annotated[str, Field(min_length=2, max_length=50)]
    rank: Rank
    age: Annotated[int, Field(ge=18, le=80)]
    specialization: Annotated[str, Field(min_length=3, max_length=30)]
    years_experience: Annotated[int, Field(ge=0, le=50)]
    is_active: Annotated[bool, Field(default=True)]


class SpaceMission(BaseModel):
    mission_id: Annotated[str, Field(min_length=5, max_length=15)]
    mission_name: Annotated[str, Field(min_length=3, max_length=100)]
    destination: Annotated[str, Field(min_length=3, max_length=50)]
    launch_date: datetime
    duration_days: Annotated[int, Field(ge=1, le=3650)]
    crew: Annotated[list[CrewMember], Field(min_length=1, max_length=12)]
    budget_millions: Annotated[float, Field(ge=1.0, le=10000.0)]

    @model_validator(mode="after")
    def check(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("mission_id must start with 'M'\n")

        for member in self.crew:
            if member.rank == Rank.COMMANDER or member.rank == Rank.CAPTAIN:
                break
        else:
            raise ValueError("Mission must have at least one " +
                             "Commander or Captain\n")

        if self.duration_days > 365:
            count = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    count += 1
            if count < len(self.crew) // 2 + len(self.crew) % 2:
                raise ValueError("Long missions must have at least " +
                                 "half the crew with 5+ years experience\n")

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active\n")
        return self


def show_mission(mission: SpaceMission) -> None:
    print(f"ID: {mission.mission_id}\n" +
          f"Name: {mission.mission_name}\n" +
          f"Destination: {mission.destination}\n" +
          f"Launch Date: {mission.launch_date.strftime('%d-%m-%Y')}\n" +
          f"Duration: {mission.duration_days} days\n" +
          f"Budget: ${mission.budget_millions} million\n" +
          f"Crew Count: {len(mission.crew)}\n" +
          "Crew Members:\n", end="")
    for member in mission.crew:
        print(f"- {member.name}, " +
              f"({member.rank.value}) " +
              f"- {member.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================\n")
    crew = [
        CrewMember(
            member_id="CM001",
            name="Alice Johnson",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Pilot",
            years_experience=20,
            is_active=True
        ),
        CrewMember(
            member_id="CM002",
            name="Bob Smith",
            rank=Rank.OFFICER,
            age=38,
            specialization="Engineer",
            years_experience=10,
            is_active=True
        ),
        CrewMember(
            member_id="CM003",
            name="Charlie Lee",
            rank=Rank.LIEUTENANT,
            age=30,
            specialization="Scientist",
            years_experience=5,
            is_active=True
        )
    ]

    mission = SpaceMission(
        mission_id="M2024_001",
        mission_name="Mars Exploration",
        destination="Mars",
        launch_date=datetime(2024, 7, 1),
        duration_days=300,
        crew=crew,
        budget_millions=500.0
    )
    print("Valid mission created:")
    show_mission(mission)
    print("========================================\n")
    print("Expected validation error:")
    crew = [
        CrewMember(
            member_id="CM001",
            name="Alice Johnson",
            rank=Rank.LIEUTENANT,
            age=45,
            specialization="Pilot",
            years_experience=20,
            is_active=True
        ),
        CrewMember(
            member_id="CM002",
            name="Bob Smith",
            rank=Rank.OFFICER,
            age=38,
            specialization="Engineer",
            years_experience=10,
            is_active=True
        ),
        CrewMember(
            member_id="CM003",
            name="Charlie Lee",
            rank=Rank.LIEUTENANT,
            age=30,
            specialization="Scientist",
            years_experience=5,
            is_active=True
        )
    ]
    try:
        mission2 = SpaceMission(
            mission_id="M2024_001",
            mission_name="Mars Exploration",
            destination="Mars",
            launch_date=datetime(2024, 7, 1),
            duration_days=300,
            crew=crew,
            budget_millions=500.0
        )
        show_mission(mission2)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
