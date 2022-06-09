from Dairy.data.data import Sessions
from Dairy.models.key import Key


def get_key(value: str):
    with Sessions() as session:
        key = session.query(Key).filter_by(value=value).first()
        return key
