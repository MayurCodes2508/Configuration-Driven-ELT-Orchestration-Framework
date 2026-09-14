from builtins import (
    AttributeError,
    Exception,
    FileNotFoundError,
    ImportError,
    KeyError,
    ModuleNotFoundError,
    OSError,
    PermissionError,
    RuntimeError,
    TimeoutError,
    TypeError,
    ValueError,
)
from json.decoder import JSONDecodeError
from subprocess import CalledProcessError, SubprocessError, TimeoutExpired

from google.api_core.exceptions import (
    Forbidden,
    GoogleAPICallError,
    NotFound,
    TooManyRequests,
)
from google.auth.exceptions import DefaultCredentialsError, RefreshError
from jsonschema import SchemaError, ValidationError
from psycopg2 import (
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from psycopg2 import (
    Error as Psycopg2Error,
)
from requests.exceptions import HTTPError, RequestException, Timeout

EXCEPTION_DESCRIPTIONS = {
    Exception: "An unexpected error occurred.",
    AttributeError: "The requested attribute does not exist.",
    FileNotFoundError: "The specified file or directory was not found.",
    ImportError: "Failed to import a module or object.",
    ModuleNotFoundError: "The required Python module could not be found.",
    KeyError: "The requested key does not exist.",
    OSError: "An operating system error occurred.",
    PermissionError: "Permission was denied while accessing the resource.",
    RuntimeError: "A runtime error occurred.",
    TimeoutError: "The operation exceeded the allowed timeout.",
    TypeError: "An object or argument has an invalid type.",
    ValueError: "An object or argument has an invalid value.",
    JSONDecodeError: "Failed to decode JSON data.",
    SubprocessError: "A subprocess execution error occurred.",
    CalledProcessError: "The subprocess exited with a non-zero exit status.",
    TimeoutExpired: "The subprocess execution exceeded the configured timeout.",
    ValidationError: "The provided configuration failed schema validation.",
    SchemaError: "The provided schema is invalid.",
    RequestException: "An HTTP request failed.",
    HTTPError: "The HTTP request returned an error response.",
    Timeout: "The HTTP request timed out.",
    DefaultCredentialsError: "Google Cloud credentials could not be loaded.",
    RefreshError: "Google Cloud credentials could not be refreshed.",
    GoogleAPICallError: "A Google Cloud API request failed.",
    NotFound: "The requested Google Cloud resource was not found.",
    Forbidden: "Access to the requested Google Cloud resource was denied.",
    TooManyRequests: "The request exceeded the allowed rate limit.",
    Psycopg2Error: "A PostgreSQL database error occurred.",
    DatabaseError: "A database operation failed.",
    OperationalError: "A database operational error occurred.",
    IntegrityError: "A database integrity constraint was violated.",
    ProgrammingError: "A database programming error occurred.",
}
