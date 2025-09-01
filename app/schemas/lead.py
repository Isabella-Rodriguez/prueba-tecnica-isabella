from pydantic import BaseModel, Field

class LeadCreate(BaseModel):
    id: int = Field(..., ge=1)
    name: str
    location: str
    budget: int = Field(..., ge=0)

class LeadOut(BaseModel):
    id: int
    name: str
    location: str
    budget: int
    class Config:
        from_attributes = True
