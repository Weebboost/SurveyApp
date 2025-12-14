from ...models.response import Response
from sqlmodel import Session

def submit_response(*, session: Session, response: Response) -> Response:
    session.add(response)
    return response