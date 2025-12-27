"""Data models for ISRO launch records."""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class PSLVLaunch(BaseModel):
    """Data model for PSLV launch records."""
    
    flight_number: str = Field(..., description="Flight number")
    date_time_utc: Optional[str] = Field(None, description="Launch date/time UTC")
    rocket_configuration: Optional[str] = Field(None, description="Rocket variant")
    launch_site: Optional[str] = Field(None, description="Launch site")
    payload: str = Field(..., description="Payload name(s)")
    payload_mass: Optional[str] = Field(None, description="Payload mass")
    orbit: Optional[str] = Field(None, description="Target orbit")
    user: Optional[str] = Field(None, description="Customer/Organization")
    launch_outcome: Optional[str] = Field(None, description="Outcome")
    remarks: Optional[str] = Field(None, description="Mission notes")
    
    @field_validator('payload_mass')
    @classmethod
    def validate_mass(cls, v: Optional[str]) -> Optional[str]:
        """Validate mass contains numeric values."""
        if v is None or v.strip() == '':
            return None
        if re.search(r'\d', v):
            return v.strip()
        return None


class GSLVLaunch(BaseModel):
    """Data model for GSLV launch records."""
    
    flight_number: str = Field(..., description="Flight number")
    date_time_utc: Optional[str] = Field(None, description="Launch date/time UTC")
    rocket_configuration: Optional[str] = Field(None, description="Rocket variant")
    launch_site: Optional[str] = Field(None, description="Launch site")
    payload: str = Field(..., description="Payload name(s)")
    payload_mass: Optional[str] = Field(None, description="Payload mass")
    orbit: Optional[str] = Field(None, description="Target orbit")
    user: Optional[str] = Field(None, description="Customer/Organization")
    launch_outcome: Optional[str] = Field(None, description="Outcome")
    remarks: Optional[str] = Field(None, description="Mission notes")
    
    @field_validator('payload_mass')
    @classmethod
    def validate_mass(cls, v: Optional[str]) -> Optional[str]:
        """Validate mass contains numeric values."""
        if v is None or v.strip() == '':
            return None
        if re.search(r'\d', v):
            return v.strip()
        return None


class LVM3Launch(BaseModel):
    """Data model for LVM3 launch records."""
    
    flight_number: str = Field(..., description="Flight number")
    date_time_utc: Optional[str] = Field(None, description="Launch date/time UTC")
    launch_site: Optional[str] = Field(None, description="Launch site")
    payload: str = Field(..., description="Payload name(s)")
    payload_mass: Optional[str] = Field(None, description="Payload mass with units")
    regime: Optional[str] = Field(None, description="Orbital regime")
    operator: Optional[str] = Field(None, description="Operator/Organization")
    function: Optional[str] = Field(None, description="Mission function")
    status: Optional[str] = Field(None, description="Launch status")
    remarks: Optional[str] = Field(None, description="Mission notes")
    
    @field_validator('payload_mass')
    @classmethod
    def validate_mass(cls, v: Optional[str]) -> Optional[str]:
        """Validate mass contains numeric values."""
        if v is None or v.strip() == '':
            return None
        if re.search(r'\d', v):
            return v.strip()
        return None
