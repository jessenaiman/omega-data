from pydantic import BaseModel, validator
from typing import List, Optional
import re


class FeatureCreateRequest(BaseModel):
    feature_description: str

    @validator('feature_description')
    def validate_feature_description(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Feature description cannot be empty')
        if len(v) > 500:
            raise ValueError('Feature description cannot exceed 500 characters')
        return v.strip()


class FeatureCreateResponse(BaseModel):
    branch_name: str
    spec_file_path: str
    status: str

    @validator('branch_name')
    def validate_branch_name(cls, v):
        # Branch name should follow format: NNN-feature-name
        if not re.match(r'^\d{3}-[a-z0-9-]+$', v):
            raise ValueError('Branch name must follow format: NNN-feature-name')
        return v


class PlanCreateResponse(BaseModel):
    plan_file_path: str
    status: str
    artifacts: List[str]


class TasksCreateResponse(BaseModel):
    tasks_file_path: str
    status: str
    task_count: int

    @validator('task_count')
    def validate_task_count(cls, v):
        if v < 0:
            raise ValueError('Task count cannot be negative')
        return v