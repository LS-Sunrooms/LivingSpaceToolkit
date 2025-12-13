import logging

from livingspacetoolkit.views.studio_view import Studio
from livingspacetoolkit.lib.livingspacetoolkit_enums import PitchType, SunroomType

logger = logging.getLogger(__name__)


class StudioController:
    def __init__(self, view: Studio):
        self.view = view
        self.pitch = view.sunroom_roof.pitch

        # Connect signals
        self.pitch.radio_ratio.clicked.connect(lambda: self.handle_pitch_type_click(PitchType.RATIO, SunroomType.STUDIO))
        self.pitch.radio_angle.clicked.connect(lambda: self.handle_pitch_type_click(PitchType.ANGLE, SunroomType.STUDIO))

    def handle_pitch_type_click(self, pitch_type: PitchType, sunroom: SunroomType):
        logger.debug("Studio pitch radio button clicked.")
        self.pitch.update_pitch_text(pitch_type, sunroom)
