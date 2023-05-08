from datetime import datetime, timedelta

from app import schemas, services
from app.dependencies import get_db, get_current_provider
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import pandas as pd

router = APIRouter()
router.tags = ["reporting"]


@router.get("/reporting", response_class=StreamingResponse)
def get_reporting(
    db: Session = Depends(get_db),
    provider=Depends(get_current_provider),
    start_date: float = (datetime.now() - timedelta(days=1 * 365)).timestamp(),
    end_date: float = datetime.now().timestamp(),
):
    data = services.get_reporting_events(
        db,
        provider_id=provider.id,
        start_date=start_date,
        end_date=end_date,
    )

    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"

    return response
