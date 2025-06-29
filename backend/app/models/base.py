from sqlalchemy.orm import declarative_base

# The base class for all our models.
# By placing this in its own file, we prevent circular import issues.
Base = declarative_base()
