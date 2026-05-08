import pickle
from random import choice, randint
from pathlib import Path
import condition_lists as conditions
from error import error


class Database:
    """Stores and manages the in-game time and weather state for a campaign."""

    def __init__(self) -> None:
        """Initialises a new Database with default time and weather values."""
        print("Initalising database...")
        self.version: str = "v0.9.0"

        self.day_raw: int = 0
        self.day: int = 1
        self.hour: int = 0
        self.tenday: int = 1
        self.month_raw: int = 0
        self.month: list = [self.month_raw+1, conditions.months[self.month_raw]]
        self.year: int = 1491
        self.precipitation: str = choice(conditions.precipitation)
        self.wind_dir: str = choice(conditions.wind_dir)
        self.windspeed: str = choice(conditions.wind_speed)
        self.temperature: str = choice(conditions.temp)
        self.RAW: bool = False

        self.reminders: list = []
        self.session_num: int = 1

    def _next_day(self, days: int = 1) -> None:
        """Advances weather and calendar state by the given number of days.

        Args:
            days: Number of days to advance. Negative values go backwards.
        """
        if self.RAW:
            prob=0
        else:
            prob=5

        for _ in range(abs(days)):
            change_rolls=[randint(0,prob) for _ in range(4)]
            if change_rolls[0]==0:
                self.precipitation=choice(conditions.precipitation)
            if change_rolls[1]==0:
                self.wind_dir=choice(conditions.wind_dir)
            if change_rolls[2]==0:
                self.windspeed=choice(conditions.wind_speed)
            if change_rolls[3]==0:
                self.temperature=choice(conditions.temp)

        self.day=self.day_raw%30+1
        self.tenday=int((self.day_raw%30)/10)+1
        self.month_raw=int((self.day_raw%360)/30)
        self.month=[self.month_raw+1,conditions.months[self.month_raw]]
        self.year=int(self.day_raw/360)+1491

    def change_day(self, days: int) -> None:
        """Increments the raw day counter and updates the calendar.

        Args:
            days: Number of days to add (can be negative).
        """
        try:
            self.day_raw+=int(days)
            if int(days)!=0:
                self._next_day(int(days))

        except TypeError as e:
            print("INVALID TIME INCREMENT")

    def change_hour(self, hours: int) -> None:
        """Increments the hour counter, rolling over into new days as needed.

        Args:
            hours: Number of hours to add (can be negative).
        """
        try:
            self.hour+=int(hours)
            while self.hour>=24:
                self.hour-=24
                self.day_raw+=1
                self._next_day()
            while self.hour<0:
                self.hour+=24
                self.day_raw-=1
                self._next_day(-1)
            print(f"Time: {self.hour}:00")
        except TypeError as e:
            print("INVALID TIME INCREMENT")

    def time_data(self) -> tuple[int, int, int, int]:
        """Returns the current time as a tuple.

        Returns:
            A tuple of (hour, day, month_number, year).
        """
        return (self.hour,self.day,self.month[0],self.year)


def pickler(path: str | Path, obj: object) -> None:
    """Serialises an object to a file using pickle.

    Args:
        path: Destination file path.
        obj: The object to serialise.
    """
    path = Path(path)
    with path.open('wb') as f:
        pickle.dump(obj, f)
    print(f"{path} pickled")

def unpickle(path: str | Path) -> object:
    """Deserialises an object from a pickle file.

    Args:
        path: Path to the pickle file.

    Returns:
        The deserialised object, or None if the file does not exist.
    """
    try:
        path = Path(path)
        with path.open('rb') as f:
            obj = pickle.load(f)
        print(f"{path} unpickled")
        return obj
    except FileNotFoundError:
        return None

def time_comparison(time0: tuple[int, ...], time1: tuple[int, ...]) -> bool:
    """Compares two in-game timestamps to determine if time1 has been reached.

    Args:
        time0: Current time as (hour, day, month, year).
        time1: Target time as (hour, day, month, year).

    Returns:
        True if time0 >= time1, False otherwise.
    """
    if len(time0)!=len(time1):
        error("time_comparison length error")
        return

    for i in range(len(time0)):
        print(time0[-i-1],time1[-i-1])
        if time0[-i-1]>time1[-i-1]:
            return True
        elif time0[-i-1]<time1[-i-1]:
            return False
    print("equal")
    return True

def time_increment(start_time: tuple[int, ...], increment: tuple[int, ...]) -> list[int]:
    """Adds a time increment to a start time, carrying over unit boundaries.

    Args:
        start_time: Base time as (hour, day, month, year).
        increment: Amount to add in each unit as (hour, day, month, year).

    Returns:
        The resulting time as a list of integers.
    """
    new_time=[i+j for i,j in zip(start_time, increment)]
    limits=[24, 30, 12, 1e99]
    new_time[0]+=1
    for i in range(len(new_time)-1):
        limit=limits[i]
        while new_time[i]>limit:
            print(0)
            new_time[i]%=limit
            new_time[i+1]+=int(new_time[i]/limit)+1
    new_time[0]-=1
    return new_time

# Backwards compatibility alias for pickle deserialization
db = Database
