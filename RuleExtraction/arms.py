from helper import *

class ArmRules:
    def __init__(self):
        self.previous_left_elbow = None
        self.previous_right_elbow = None
        self.previous_left_hand = None
        self.previous_right_hand = None
        self.previous_left_shoulder = None
        self.previous_right_shoulder = None

    def extract_arm_rules(self, landmarks):
        # Get empty arm position dictionary
        arm_positions = get_empty_arm_position()

        # Extract elbow and hand landmarks for both arms
        left_elbow = landmarks.get('left_elbow', None)
        right_elbow = landmarks.get('right_elbow', None)
        left_hand = landmarks.get('left_hand', None)
        right_hand = landmarks.get('right_hand', None)
        left_shoulder = landmarks.get('left_shoulder',None)
        right_shoulder = landmarks.get('right_shoulder',None)

        # Process left elbow
        if left_elbow:
            arm_positions['left_elbow']['position'] = self.get_position_state('left_elbow',landmark=landmarks)
            if self.previous_left_elbow is not None:
                arm_positions['left_elbow']['motion'] = self.detect_motion(self.previous_left_elbow, left_elbow)
            self.previous_left_elbow = left_elbow
        
        # Process right elbow
        if right_elbow:
            arm_positions['right_elbow']['position'] = self.get_position_state('right_elbow',landmarks)
            if self.previous_right_elbow is not None:
                arm_positions['right_elbow']['motion'] = self.detect_motion(self.previous_right_elbow, right_elbow)
            self.previous_right_elbow = right_elbow

        # Process left hand
        if left_hand:
            arm_positions['left_hand']['position'] = self.get_position_state('left_hand',landmarks)
            if self.previous_left_hand is not None:
                arm_positions['left_hand']['motion'] = self.detect_motion(self.previous_left_hand, left_hand)
            self.previous_left_hand = left_hand

        # Process right hand
        if right_hand:
            arm_positions['right_hand']['position'] = self.get_position_state('right_hand',landmarks)
            if self.previous_right_hand is not None:
                arm_positions['right_hand']['motion'] = self.detect_motion(self.previous_right_hand, right_hand)
            self.previous_right_hand = right_hand

        self.previous_right_shoulder = right_shoulder
        self.previous_left_shoulder = left_shoulder
        return arm_positions

    def get_position_state(self, keyword, landmarks, eqpt_center_list):
        """
        Determine the position for a given landmark (keyword)
        """
        results = []
        side, joint= keyword.split('_')
        match joint:
            case "elbow":
                #close to torso, flexed, extended, slightly flexed, slightly extended, bent at 90 degrees
                elbow_angle = calculate_angle(landmarks[f'{side}_shoulder'],landmarks[f'{side}_elbow'],landmarks[f'{side}_shoulder'])
                elbow_shoulder_dif = landmarks[f'{side}_elbow'] - landmarks[f'{side}_shoulder'] #elbow - shoulder, be careful when used for different sides of the body
                if 0.1 > elbow_shoulder_dif[1]:
                    results.append['close to torso']

                if elbow_angle<30:
                    results.append['flexed']
                elif elbow_angle<80:
                    results.append['slightly flexed']
                elif elbow_angle<100:
                    results.append['bent a t 90 degrees']
                elif elbow_angle<150:
                    results.append['slightly extended']
                else: 
                    results.append['extended']
                
            case "hand":
                # "holding equipment","horizontal outward","horizontal inward","vertical upward","vertical downward""vertical upward","vertical downward","over chest","over head"
                horizontal_diff = hand[0] - elbow[0]
                vertical_diff = hand[1]-elbow[1]
                if abs(vertical_diff)>abs(horizontal_diff):
                    # more significant vertically:
                    if horizontal_diff>0: 
                        results.append['vertical upward']
                    else:
                        results.append['vertical downward']
                else:
                    if (side == 'left' and horizontal_diff<0) or (side == 'right' and horizontal_diff>0):
                        results.append['horizontal inward']
                    else:
                        results.append['horizontal outward']

                if any(calculate_distance(hand,curr_eqpt)<0.05) for curr_eqpt in eqpt_center_list:
                    #TODO change threshold
                    results.append['holding equipment']
                
                return results
        
    def detect_motion(self, keyword: str, previous_dist, current_dist, threshold: float):
        '''
        Detect motion based on keyword side, remember that left side of the img is the right side of the body

        Parameters:
        keyword (str): 'l' or 'r'
        previous_dist (float,float): previous difference between landmark and shoulder
        current_dist (float,float): current difference between landmark and shoulder
        threshold (float): abs value in distance difference to clasify as moving

        Returns:
        rule extracted for motion
        '''
        # 
        # Check for motion between frames (flexion, extension)
        dx,dy = previous_dist
        dx_curr,dy_curr = current_dist


        if current['y'] > previous['y']:
            return ["extension"]
        elif current['y'] < previous['y']:
            return ["flexion"]
        else:
            return ["stationary"]
