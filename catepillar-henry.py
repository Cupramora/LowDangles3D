# catepillar-henry.py
# The Caterpillar Spine – PID-regulated modular pipeline controller
# Author: Dane (bioengineer) + Henry (the organism)

class PIDController:
    def __init__(self, kp=1.0, ki=0.1, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.previous_error = 0

    def correct(self, error):
        """Return a correction decision based on PID error."""
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        decision = {
            "retry": output < 3,
            "skip": 3 <= output < 6,
            "fail": output >= 6
        }
        return decision


class CaterpillarHenry:
    def __init__(self, input_file, mtl_file=None, material_params=None):
        self.input_file = input_file
        self.mtl_file = mtl_file
        self.material_params = material_params or {}
        self.state = "READY"
        self.segment_index = 0
        self.pid = PIDController()

        # Expected outputs for this job
        self.expected_outputs = {
            "clean_obj": False,
            "stl": False,
            "normal_map": False,
            "fbx": False,
            "glb": False,
            "wireframe": False,
            "broken_version": False,     # NEW
            "organized": False           # NEW
        }

        # Pipeline segments (Tier 1 + Tier 2 ports)
        self.pipeline_segments = [
            self.segment_import_and_clean,
            self.segment_generate_stl,
            self.segment_material_setup,
            self.segment_normal_bake,
            self.segment_export_fbx,
            self.segment_export_glb,
            self.segment_wireframe_render,

            # -------------------------
            # TIER 2 MODULE PORTS
            # -------------------------
            self.segment_generate_broken_version,   # NEW
            self.segment_organize_and_name,         # NEW

            self.segment_completion_check
        ]

    # ------------------------------
    # SPINE SEGMENTS (EMPTY SHELLS)
    # ------------------------------

    def segment_import_and_clean(self):
        return self.mock_result("clean_obj")

    def segment_generate_stl(self):
        return self.mock_result("stl")

    def segment_material_setup(self):
        return self.mock_result("material")

    def segment_normal_bake(self):
        return self.mock_result("normal_map")

    def segment_export_fbx(self):
        return self.mock_result("fbx")

    def segment_export_glb(self):
        return self.mock_result("glb")

    def segment_wireframe_render(self):
        return self.mock_result("wireframe")

    # ------------------------------
    # TIER 2 MODULE PORTS
    # ------------------------------

    def segment_generate_broken_version(self):
        """
        Placeholder for the broken-version generator.
        This will eventually:
            - fracture mesh
            - export broken OBJ/GLB
            - generate debris if needed
        """
        return self.mock_result("broken_version")

    def segment_organize_and_name(self):
        """
        Placeholder for the naming + folder organizing engine.
        This will eventually:
            - sanitize base name
            - generate consistent filenames
            - create product folder
            - move all outputs into folder
            - write metadata.json
        """
        return self.mock_result("organized")

    # ------------------------------
    # COMPLETION CHECK
    # ------------------------------

    def segment_completion_check(self):
        all_good = all(self.expected_outputs.values())
        return {"success": all_good, "error": 0 if all_good else 5}

    # ------------------------------
    # MOCK RESULT FOR NOW
    # ------------------------------

    def mock_result(self, key):
        if key in self.expected_outputs:
            self.expected_outputs[key] = True
        return {"success": True, "error": 0}

    # ------------------------------
    # THE CATERPILLAR SPINE LOOP
    # ------------------------------

    def run(self):
        print("Caterpillar-Henry: Starting pipeline…")

        while self.state != "COMPLETE":
            if self.segment_index >= len(self.pipeline_segments):
                self.state = "COMPLETE"
                break

            segment = self.pipeline_segments[self.segment_index]
            result = segment()

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


# ------------------------------
# EXAMPLE USAGE
# ------------------------------

if __name__ == "__main__":
    henry = CaterpillarHenry("input.obj", "input.mtl")
    henry.run()
