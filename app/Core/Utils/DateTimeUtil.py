from datetime import datetime, timedelta, timezone

class DateTimeUtil:

    @staticmethod
    def UtcNow() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def AfterMinutes(minutes: int) -> datetime:
        return DateTimeUtil.UtcNow() + timedelta(minutes=minutes)

    @staticmethod
    def AfterDays(days: int) -> datetime:
        return DateTimeUtil.UtcNow() + timedelta(days=days)
