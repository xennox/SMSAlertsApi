from pydantic import BaseModel


class Client(BaseModel):
    id: int
    tel: int
    tag: int
    note: str
    timebelt: str

class Malling(BaseModel):
    id: int
    datetimestart: str
    datetimeend: str
    smstext: str
    tag: int
