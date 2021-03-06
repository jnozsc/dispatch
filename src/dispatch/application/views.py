from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from dispatch.database import get_db, search_filter_sort_paginate
from dispatch.search.service import search

from .models import (
    Application,
    ApplicationCreate,
    ApplicationPagination,
    ApplicationRead,
    ApplicationUpdate,
)
from .service import create, delete, get, get_all, update

router = APIRouter()


@router.get("/", response_model=ApplicationPagination)
def get_applications(
    db_session: Session = Depends(get_db),
    page: int = 1,
    items_per_page: int = Query(5, alias="itemsPerPage"),
    query_str: str = Query(None, alias="q"),
    sort_by: List[str] = Query(None, alias="sortBy[]"),
    descending: List[bool] = Query(None, alias="descending[]"),
    fields: List[str] = Query(None, alias="field[]"),
    ops: List[str] = Query(None, alias="op[]"),
    values: List[str] = Query(None, alias="value[]"),
):
    """
    Get all applications, or only those matching a given search term.
    """
    return search_filter_sort_paginate(
        db_session=db_session,
        model="Application",
        query_str=query_str,
        page=page,
        items_per_page=items_per_page,
        sort_by=sort_by,
        descending=descending,
        fields=fields,
        values=values,
        ops=ops,
    )


@router.get("/{app_id}", response_model=ApplicationRead)
def get_application(*, db_session: Session = Depends(get_db), app_id: str):
    """
    Given its unique ID, retrieve details about a single application.
    """
    app = get(db_session=db_session, app_id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="The requested application does not exist.")
    return app


@router.post("/", response_model=ApplicationRead)
def create_application(*, db_session: Session = Depends(get_db), app_in: ApplicationCreate):
    """
    Create a new application.
    """
    app = create(db_session=db_session, app_in=app_in)
    return app


@router.put("/{app_id}", response_model=ApplicationRead)
def update_application(
    *, db_session: Session = Depends(get_db), app_id: int, app_in: ApplicationUpdate
):
    """
    Given its unique ID, update details of an application.
    """
    app = get(db_session=db_session, app_id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="An application with this ID does not exist.")
    app = update(db_session=db_session, app=app, app_in=app_in)
    return app


@router.delete("/{app_id}")
def delete_application(*, db_session: Session = Depends(get_db), app_id: int):
    """
    Delete an application, returning only an HTTP 200 OK if successful.
    """
    app = get(db_session=db_session, app_id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="An application with this ID does not exist.")
    delete(db_session=db_session, app_id=app_id)
