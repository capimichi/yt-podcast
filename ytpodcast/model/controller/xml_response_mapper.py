from xml.etree import ElementTree

from pydantic import BaseModel


class XmlResponseMapper:
    """Build XML responses from controller models."""

    def create_from_response(self, root_name: str, payload: BaseModel) -> str:
        root = ElementTree.Element(root_name)
        for key, value in payload.dict().items():
            child = ElementTree.SubElement(root, key)
            child.text = "" if value is None else str(value)
        return ElementTree.tostring(root, encoding="unicode")
