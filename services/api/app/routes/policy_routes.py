import os
import shutil
import tempfile
from typing import List
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from services.api.app.services.gemini_file_rag import gemini_file_rag

router = APIRouter(prefix="/api/v1/policies", tags=["Policy Documents (Google File Search API)"])


class PolicyQueryRequest(BaseModel):
    query: str


class PolicyDeleteRequest(BaseModel):
    file_ids: List[str]


@router.get("")
async def get_policies():
    """List all policy documents in Google Gemini storage."""
    return gemini_file_rag.list_policies()


@router.post("/upload")
async def upload_policies(files: List[UploadFile] = File(...)):
    """Uploads one or more policy documents (PDF / DOCX / MD / TXT / CSV / RTF / HTML) to Google Gemini File API."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided for upload.")

    results = []
    temp_dir = tempfile.mkdtemp()
    try:
        for file in files:
            safe_filename = os.path.basename(file.filename) if file.filename else "unnamed_document.pdf"
            temp_path = os.path.join(temp_dir, safe_filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_info = gemini_file_rag.upload_policy(
                file_path=temp_path,
                display_name=safe_filename
            )
            results.append(uploaded_info)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return {
        "status": "success",
        "uploaded": results,
        "count": len(results),
        "message": f"Successfully uploaded {len(results)} document(s) to Gemini File storage."
    }


@router.post("/delete")
async def delete_policies(body: PolicyDeleteRequest):
    """Batch delete policy documents from Google Gemini storage and cache."""
    if not body.file_ids:
        raise HTTPException(status_code=400, detail="No file IDs provided for deletion.")

    deleted_count = 0
    for fid in body.file_ids:
        if gemini_file_rag.delete_policy(fid):
            deleted_count += 1

    remaining_policies = gemini_file_rag.list_policies()
    return {
        "status": "success",
        "deleted_count": deleted_count,
        "deleted_ids": body.file_ids,
        "remaining_count": len(remaining_policies),
        "message": f"Successfully deleted {deleted_count} document(s)."
    }


@router.post("/ask")
async def ask_policy(body: PolicyQueryRequest):
    """Queries uploaded school policies using Google File Search RAG."""
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    return gemini_file_rag.ask_policy(body.query)
