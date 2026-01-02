from typing import Dict
from livingspacetoolkit.models.toolkit_state_model import ToolkitStateModel
from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.lib.toolkit_enums import RoofingType



class RoofModel:
    """Used to generate the items in the thickness combo box."""
    def __init__(self, toolkit_state_model: ToolkitStateModel):
        self.toolkit_state_model = toolkit_state_model

    @staticmethod
    def set_thickness_combo_dict(roof_type: RoofingType) -> Dict[str, str]:
        combo_item_dict: Dict = {}
        match roof_type:
            case RoofingType.ALUMINUM:
                combo_item_dict.update(
                    {
                        '3"': '3"',
                        '6"': '6"'
                    }
                )
            case RoofingType.ECO_GREEN:
                combo_item_dict.update(
                    {
                        '6"': '6"',
                        '8"': '8.25"',
                        '10"': '10.25"',
                        '12"': '12.25"'
                    }
                )
        return combo_item_dict