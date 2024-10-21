from helper import get_empty_leg_position

class LegRules:
    def __init__(self):
        self.previous_left_knee = None
        self.previous_right_knee = None
        self.previous_left_foot = None
        self.previous_right_foot = None

    def extract_leg_rules(self, landmarks):
        # Get empty leg position dictionary
        leg_positions = get_empty_leg_position()

        # Extract knee and foot landmarks for both legs
        left_knee = landmarks.get('left_knee', None)
        right_knee = landmarks.get('right_knee', None)
        left_foot = landmarks.get('left_foot', None)
        right_foot = landmarks.get('right_foot', None)

        # Process left knee
        if left_knee:
            leg_positions['left_knee']['position'] = self.get_position_state(left_knee)
            if self.previous_left_knee is not None:
                leg_positions['left_knee']['motion'] = self.detect_motion(self.previous_left_knee, left_knee)
            self.previous_left_knee = left_knee
        
        # Process right knee
        if right_knee:
            leg_positions['right_knee']['position'] = self.get_position_state(right_knee)
            if self.previous_right_knee is not None:
                leg_positions['right_knee']['motion'] = self.detect_motion(self.previous_right_knee, right_knee)
            self.previous_right_knee = right_knee

        # Process left foot
        if left_foot:
            leg_positions['left_foot']['position'] = self.get_position_state(left_foot)
            if self.previous_left_foot is not None:
                leg_positions['left_foot']['motion'] = self.detect_motion(self.previous_left_foot, left_foot)
            self.previous_left_foot = left_foot

        # Process right foot
        if right_foot:
            leg_positions['right_foot']['position'] = self.get_position_state(right_foot)
            if self.previous_right_foot is not None:
                leg_positions['right_foot']['motion'] = self.detect_motion(self.previous_right_foot, right_foot)
            self.previous_right_foot = right_foot

        return leg_positions

    def get_position_state(self, landmark):
        #TODO polish this
        if landmark['y'] > 0.5:  # Example condition
            return ["flat", "on ground"]
        else:
            return ["raised"]

    def detect_motion(self, previous, current):
        # Check for motion between frames (flexion, extension, stationary)
        if current['y'] > previous['y']:
            return ["extension"]
        elif current['y'] < previous['y']:
            return ["flexion"]
        else:
            return ["stationary"]
