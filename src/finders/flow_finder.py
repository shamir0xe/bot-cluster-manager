from typing import List
from src.models.conditional_proposition import ConditionalProposition
from src.models.page import Page
from src.types.flow_types import FlowTypes


class FlowFinder:
    @staticmethod
    def with_page(page: Page, flow_type: FlowTypes) -> List[ConditionalProposition]:
        if not page.flow:
            return []
        if flow_type is FlowTypes.PHOTO:
            if page.flow.photo:
                return page.flow.photo 
        elif flow_type is FlowTypes.VIDEO:
            if page.flow.video:
                return page.flow.video
        elif flow_type is FlowTypes.AUDIO:
            if page.flow.audio:
                return page.flow.audio
        elif flow_type is FlowTypes.TEXT:
            if page.flow.text:
                return page.flow.text
        elif flow_type is FlowTypes.LOCATION:
            if page.flow.location:
                return page.flow.location
        return []

