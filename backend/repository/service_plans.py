from sqlalchemy.orm import Session
from models.index import ServicePlanModel, UserModel


def create(plan_id:int, plan_nameame: str, rate_limit:int, db: Session):
    try:
        if not db.query(ServicePlanModel).filter(ServicePlanModel.planName == plan_nameame).count():
            new_plan = ServicePlanModel(id = plan_id, planName = plan_nameame, requestLimit = rate_limit)
            db.add(new_plan)
            db.commit()
            db.refresh(new_plan)
            return True
    except Exception as e:
        print(e)
        return False
    

def get_plans(db: Session):
    plans = db.query(ServicePlanModel).all()

    return plans

def get_plan_by_user_id(user_id:int, db: Session):

    user: UserModel = db.query(UserModel).filter(UserModel.id == user_id).join(ServicePlanModel).first()

    return user.plan

