"""Module for ytpodcast.model.controller.xml_response_mapper."""

from xml.etree import ElementTree

from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class XmlResponseMapper:
    """Build XML responses from controller models."""

    def create_from_response(self, root_name: str, response_model: BaseModel) -> str:
        """Serialize a response model into XML."""
        root_element: ElementTree.Element = ElementTree.Element(root_name)
        for key, value in response_model.dict().items():
            child_element: ElementTree.Element = ElementTree.SubElement(root_element, key)
            child_element.text = "" if value is None else str(value)
        xml_body: str = ElementTree.tostring(root_element, encoding="unicode")
        return xml_body
