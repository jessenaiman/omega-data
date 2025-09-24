from sqlalchemy.orm import Session
from src.models.feature_specification import FeatureSpecification
import uuid
from typing import Optional, List, Dict, Any


class FeatureService:
    def __init__(self, db: Session):
        self.db = db

    def create_feature_specification(self, name: str, description: str) -> FeatureSpecification:
        """
        Create a new feature specification
        """
        feature_spec = FeatureSpecification(
            name=name,
            description=description,
            status="Draft"
        )
        self.db.add(feature_spec)
        self.db.commit()
        self.db.refresh(feature_spec)
        return feature_spec

    def get_feature_specification(self, feature_id: uuid.UUID) -> Optional[FeatureSpecification]:
        """
        Retrieve a feature specification by ID
        """
        return self.db.query(FeatureSpecification).filter(
            FeatureSpecification.id == feature_id
        ).first()

    def update_feature_specification(self, feature_id: uuid.UUID, **kwargs) -> Optional[FeatureSpecification]:
        """
        Update a feature specification
        """
        feature_spec = self.get_feature_specification(feature_id)
        if feature_spec:
            for key, value in kwargs.items():
                setattr(feature_spec, key, value)
            self.db.commit()
            self.db.refresh(feature_spec)
        return feature_spec

    def delete_feature_specification(self, feature_id: uuid.UUID) -> bool:
        """
        Delete a feature specification
        """
        feature_spec = self.get_feature_specification(feature_id)
        if feature_spec:
            self.db.delete(feature_spec)
            self.db.commit()
            return True
        return False