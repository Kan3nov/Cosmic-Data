from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional, Annotated


class SpaceStation(BaseModel):
    station_id: Annotated[str, Field(min_length=3, max_length=10)]
    name: Annotated[str, Field(min_length=1, max_length=50)]
    crew_size: Annotated[int, Field(ge=1, le=20)]
    power_level: Annotated[float, Field(ge=0, le=100)]
    oxygen_level: Annotated[float, Field(ge=0, le=100)]
    last_maintenance: datetime
    is_operational: Annotated[bool, Field(default=True)]
    notes: Optional[Annotated[str, Field(max_length=200)]] = None


def main() -> None:
    print("Space Station Data Validation")
    print("========================================\n")
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now(),
        is_operational=True,
        notes=None
    )

    print("Valid station created:")
    print(f"ID: {station.station_id}\nName: {station.name}\n" +
          f"Crew Size: {station.crew_size}people\n" +
          f"Power Level: {station.power_level}%\n" +
          f"Oxygen Level: {station.oxygen_level}%\n" +
          f"Last Maintenance: {station.last_maintenance.
                               strftime('%d-%m-%Y %H:%M')}\n" +
          f"Operational: {station.is_operational}\n" +
          f"Notes: {station.notes}")

    print("========================================\n")
    print("Expected validation error:")
    try:
        station2 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=26,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
        )
        print(station2)
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
