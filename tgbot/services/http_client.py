import aiohttp


_SESSIONS = {}


def get_shared_session(name: str, *, headers=None, timeout=None) -> aiohttp.ClientSession:
    """Возвращает переиспользуемую aiohttp-сессию по имени."""
    session = _SESSIONS.get(name)
    if session is None or session.closed:
        session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        _SESSIONS[name] = session
    return session


async def close_shared_sessions():
    """Закрывает все переиспользуемые сессии."""
    for key, session in list(_SESSIONS.items()):
        if not session.closed:
            await session.close()
        _SESSIONS.pop(key, None)
