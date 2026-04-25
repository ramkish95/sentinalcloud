from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime

# Base class for our classes to inherit from (OOPs: Inheritance)
Base = declarative_base()

class Server(Base):
    """
    DBMS: Primary Table (The '1' in a 1:N relationship)
    """
    __tablename__ = "servers"

    # DBMS: Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Logic: Unique constraint ensures no duplicate hostnames
    hostname = Column(String, unique=True, nullable=False)
    ip_address = Column(String, nullable=False)
    
    # OOPs: Composition 
    # A Server 'has' many metrics. 
    # 'cascade' ensures if a server is deleted, its logs are too (Memory Management).
    metrics = relationship("Metric", back_populates="owner", cascade="all, delete")

class Metric(Base):
    """
    DBMS: Normalized Table (The 'N' in a 1:N relationship)
    This follows 3NF (Third Normal Form) because it removes transitive dependencies.
    """
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    
    # DBMS: Foreign Key (linking the metric to a specific server)
    server_id = Column(Integer, ForeignKey("servers.id"))
    
    cpu_usage = Column(Float)
    ram_usage = Column(Float)
    
    # Operating Systems: Timestamping for time-series analysis
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Creating the reverse relationship
    owner = relationship("Server", back_populates="metrics")