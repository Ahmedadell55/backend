from business.models.graph import City

_city_instance: City = None


def init_city():
    global _city_instance
    if _city_instance is None:
        _city_instance = City()


def get_city() -> City:
    if _city_instance is None:
        raise Exception("City not initialized. Call init_city() first.")
    return _city_instance