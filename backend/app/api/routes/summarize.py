from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from starlette.concurrency import run_in_threadpool

from app.schemas.summary import SummaryResponse
from app.services.document_extractor import DocumentExtractionError, extract_text

router = APIRouter()


@router.post("/summarize", response_model=SummaryResponse)
async def summarize(
    request: Request,
    text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
):
    # Exactly one input method must be supplied.
    has_text = text is not None and bool(text.strip())
    has_file = file is not None

    if has_text == has_file:
        raise HTTPException(
            status_code=400,
            detail="Provide exactly one input: either 'text' or a document 'file'.",
        )

    if has_text:
        source_text = text.strip()
        source_type = "text"
        source_name = None
    else:
        filename = file.filename or "uploaded-document"
        content = await file.read()
        max_bytes = request.app.state.settings.max_upload_size_mb * 1024 * 1024

        if len(content) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds the {request.app.state.settings.max_upload_size_mb} MB upload limit.",
            )

        try:
            source_text = extract_text(filename, content)
        except DocumentExtractionError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        source_type = "document"
        source_name = filename

    if len(source_text) > request.app.state.settings.max_document_characters:
        raise HTTPException(
            status_code=413,
            detail=(
                "Document text is too large. Maximum supported size is "
                f"{request.app.state.settings.max_document_characters:,} characters."
            ),
        )

    service = request.app.state.summarization_service
    try:
        result = await run_in_threadpool(service.summarize, source_text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        # Keep internal stack traces out of the API response.
        raise HTTPException(
            status_code=500,
            detail="Summarization failed. Check backend logs for details.",
        ) from exc

    return SummaryResponse(
        **result,
        source_type=source_type,
        source_name=source_name,
        source_characters=len(source_text),
    )
