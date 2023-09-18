from fastapi import HTTPException, status


def not_found_exception(id, model):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{model} with {id} not found.')
