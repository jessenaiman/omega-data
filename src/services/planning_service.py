from sqlalchemy.orm import Session
from src.models.implementation_plan import ImplementationPlan
import uuid
from typing import Optional, List, Dict, Any


class PlanningService:
    def __init__(self, db: Session):
        self.db = db

    def create_implementation_plan(self, feature_id: uuid.UUID, technical_context: Dict[str, Any], 
                                   project_structure: str, phases: List[str]) -> ImplementationPlan:
        """
        Create a new implementation plan
        """
        plan = ImplementationPlan(
            feature_id=feature_id,
            technical_context=technical_context,
            project_structure=project_structure,
            phases=phases
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_implementation_plan(self, plan_id: uuid.UUID) -> Optional[ImplementationPlan]:
        """
        Retrieve an implementation plan by ID
        """
        return self.db.query(ImplementationPlan).filter(
            ImplementationPlan.id == plan_id
        ).first()

    def get_implementation_plan_by_feature(self, feature_id: uuid.UUID) -> Optional[ImplementationPlan]:
        """
        Retrieve an implementation plan by feature ID
        """
        return self.db.query(ImplementationPlan).filter(
            ImplementationPlan.feature_id == feature_id
        ).first()

    def update_implementation_plan(self, plan_id: uuid.UUID, **kwargs) -> Optional[ImplementationPlan]:
        """
        Update an implementation plan
        """
        plan = self.get_implementation_plan(plan_id)
        if plan:
            for key, value in kwargs.items():
                setattr(plan, key, value)
            self.db.commit()
            self.db.refresh(plan)
        return plan

    def delete_implementation_plan(self, plan_id: uuid.UUID) -> bool:
        """
        Delete an implementation plan
        """
        plan = self.get_implementation_plan(plan_id)
        if plan:
            self.db.delete(plan)
            self.db.commit()
            return True
        return False