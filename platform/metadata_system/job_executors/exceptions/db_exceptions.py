from psycopg2.errors import (DatabaseError, DataError, IntegrityError,
                             InterfaceError, InternalError, NotSupportedError,
                             OperationalError, ProgrammingError)


class DBExceptions:
    exceptions = {
        IntegrityError: ("Data Integrity Violation: A Schema Constraint Was Violated"),
        InterfaceError: (
            "Driver Interface Error: Connection Layer Failed On Python Side"
        ),
        ProgrammingError: ("SQL Syntax Error: Incorrect SQL Syntax"),
        OperationalError: (
            "Operational Disruption: Network/Connection Gave Out Mid-Way"
        ),
        NotSupportedError: ("Unsupported Feature Error: Feature Not In Support"),
        DataError: ("Data Format Error: Invalid Content Provided"),
        InternalError: ("Database Internal Error: Internal Crash or Glitch"),
        DatabaseError: ("Un"),
    }
