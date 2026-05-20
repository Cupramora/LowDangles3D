# catepillar-henry.py
# Pure Spine Version – all segments modular and external

class PIDController:
    def __init__(self, kp=1.0, ki=0.1, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.previous_error = 0

    def correct(self, error):
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        return {
            "retry": output < 3,
            "skip": 3 <= output < 6,
            "fail": output >= 6
        }


class CaterpillarHenry:
    def __init__(self, input_file, mtl_file=None, material_params=None, segments=None):
        self.input_file = input_file
        self.mtl_file = mtl_file
        self.material_params = material_params or {}
        self.state = "READY"
        self.segment_index = 0
        self.pid = PIDController()

        # External modular segments get plugged in here
        self.pipeline_segments = segments or []

        # Expected outputs (modules will update these)
        self.expected_outputs = {
            "imported": False,
            "cleaned": False,
            "clean_obj": False,
            "stl": False,
            "normal_map": False,
            "fbx": False,
            "glb": False,
            "wireframe": False,
            "broken_version": False,
            "organized": False
        }

    # ------------------------------
    # THE PURE SPINE LOOP
    # ------------------------------

    def run(self):
        print("Caterpillar-Henry: Starting modular pipeline…")

        while self.state != "COMPLETE":
            if self.segment_index >= len(self.pipeline_segments):
                self.state = "COMPLETE"
                break

            segment = self.pipeline_segments[self.segment_index]
            result = segment(self)  # pass Henry into the module

            if result["success"]:
                print(f"Segment {self.segment_index} completed.")
                self.segment_index += 1
                continue

            correction = self.pid.correct(result["error"])

            if correction["retry"]:
                print(f"Segment {self.segment_index} retrying…")
                continue

            if correction["skip"]:
                print(f"Segment {self.segment_index} skipped.")
                self.segment_index += 1
                continue

            if correction["fail"]:
                print(f"Segment {self.segment_index} failed. Pipeline aborted.")
                self.state = "FAILED"
                break

        print(f"Caterpillar-Henry: Pipeline {self.state}.")
        return self.state
