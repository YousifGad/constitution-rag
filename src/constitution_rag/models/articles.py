from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Article(BaseModel):
    model_config = ConfigDict(extra="forbid")
    article_id: str
    lineage_id: str | None = None
    version: Literal["2014-original", "2014-amended-2019"]
    number: int = Field(gt=0)
    suffix: str | None = None
    text_ar: str
    text_ar_search: str
    start_page: int = Field(gt=0)
    end_page: int = Field(gt=0)
    status: str | None = None
    refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_page_range(self):
        if self.end_page < self.start_page:
            raise ValueError("end_page cannot be smaller than start_page")
        return self