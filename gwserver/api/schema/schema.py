from pydantic import ConstrainedInt


class UID(ConstrainedInt):
    ge = 1
