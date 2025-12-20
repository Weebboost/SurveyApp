from sqlalchemy.exc import SQLAlchemyError
from ..core.exceptions import DatabaseError, CouldNotCreateResource, NotFoundError
from functools import wraps

def transactional(refresh_returned_instance: bool = False):

    def decoratotr(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = kwargs.get("session")
            print(f"Starting transaction for function: {func.__name__}")
            print("Kwargs:", kwargs)
            print("Args:", args)
            try:
                result = func(*args, **kwargs)
                print("Session:",  session)
                if session is not None:
                    session.commit()
                    print("Transaction committed successfully.")
                    if refresh_returned_instance and result is not None:

                        if hasattr(result, "__table__"):
                            session.refresh(result)

                        elif isinstance(result, (list, tuple, set)):
                            for item in result:
                                if hasattr(item, "__table__"):
                                    session.refresh(item)
                else:
                    raise DatabaseError("No session provided to transactional function")
                
                return result   
        
            
            except CouldNotCreateResource:
                if session:
                    session.rollback()
                raise   
            
            except NotFoundError:
                if session:
                    session.rollback()
                raise   

            except SQLAlchemyError as e:
                print(f"Database error occurred in function {func.__name__}: {e}")
                if session:
                    session.rollback()
                raise DatabaseError("Database error") from e
            
        return wrapper
    
    return decoratotr

