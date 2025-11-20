from fastapi import HTTPException
from sqlmodel import select
from models import Company, Employee, Team, Teams_to_employee


def create_team_in_db(team, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    if team.name == 'string':
        raise HTTPException(status_code=400, detail="Enter team name")
    if team.description == 'string':
        raise HTTPException(status_code=400, detail="Enter team description")
    if team.team_lead_id == 0:
        raise HTTPException(status_code=400, detail="Enter team lead id")
    if team.company_id == 0:
        raise HTTPException(status_code=400, detail="Enter company id")
    if team.company_id != company.company_id:
        raise HTTPException(status_code=400, detail="No company Exist with this id")
    team_lead = session.exec(select(Employee).where(Employee.id == team.team_lead_id,
                                                    Employee.company_id == team.company_id)).first()
    if not team_lead:
        raise HTTPException(status_code=404, detail="No Employee Exist with this id")
    existing = session.exec(select(Team).where(Team.team_lead_id == team.team_lead_id,
                                                Team.company_id == team.company_id))
    if existing:
        raise HTTPException(status_code=409, detail="Team lead is already leading a team")
    team = Team.model_validate(team)
    session.add(team)
    session.commit()
    team_lead.team = team.id
    team_lead.designation = 'Team Lead'
    team_to_employee = Teams_to_employee(
        team_id = team.id,
        team_lead_id = team_lead.id
    )
    session.add()(team_to_employee)
    session.commit()
    session.refresh(team)
    session.refresh(team_lead)
    session.refresh(team_to_employee)
    return team

def get_team_by_id_in_db(team_id, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    team = session.exec(select(Team).where(Team.id == team_id,
                                            Team.company_id == company.company_id)).first()
    if not team:
        raise HTTPException(status_code=404, detail='Team with given id does not exist.')
    return team

def edit_team_in_db(team, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    existing = session.exec(select(Team).where(Team.id == team.id,
                                            Team.company_id == company.company_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail='Team with given id does not exist.')
    if team.name != 'string':
        existing.name = team.name
    if team.description != 'string':
        existing.description = team.description
    if team.team_lead_id != 0:
        if team.company_id != 'string':
            team_lead = session.exec(select(Employee).where(Employee.id == team.team_lead_id,
                                                            Employee.company_id == team.company_id)).first()
            if not team_lead:
                raise HTTPException(status_code=404, detail="No Employee Exist with this id")
            existing.company_id = team.company_id
        else:
            team_lead = session.exec(select(Employee).where(Employee.id == team.team_lead_id,
                                                            Employee.company_id == existing.company_id)).first()
            if not team_lead:
                raise HTTPException(status_code=404, detail="No Employee Exist with this id")
        existing.team_lead_id = team.team_lead_id
    session.commit()
    session.refresh(existing)
    return