from helper import get_empty_torso_position

class TorsoRules:
    def __init__(self):
        self.previous_torso = None

    def extract_torso_rules(self, landmarks):
        # Get empty torso position dictionary
        torso_position = get_empty_torso_position()

        # Extract torso landmarks
        torso = landmarks.get('torso', None)

        # Process torso position and motion
        if torso:
            torso_position['torso']['position'] = self.get_position_state(torso)
            if self.previous_torso is not None:
                torso_position['torso']['motion'] = self.detect_motion(self.previous_torso, torso)
            self.previous_torso = torso

        return torso_position

    def get_position_state(self, landmark):
        # TODO POLISH this
        if landmark['y'] > 0.5:  # Example condition
            return ["neutral spine", "on bench"]
        else:
            return ["leaning forward"]

    def detect_motion(self, previous, current):
        # Check for motion between frames (extension, flexion, stationary)
        if current['y'] > previous['y']:
            return ["extension"]
        elif current['y'] < previous['y']:
            return ["flexion"]
        else:
            return ["stationary"]
