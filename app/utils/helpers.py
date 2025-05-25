from datetime import datetime, timezone, tzinfo


def time_utcnow() -> datetime:
    return datetime.now(timezone.utc)


def time_now(tz: tzinfo | None = None) -> datetime:
    now = time_utcnow()
    if tz is None:
        return now.replace(tzinfo=None)
    return now.astimezone(tz)
