#!/usr/bin/env python3
"""
replay_from_capture.py

Automated script for replaying captured robot commands using the official PyNiryo API.
Generated automatically from network traffic captures.

WARNING: This script will execute captured movements on the robot.
Ensure the workspace is clear of obstacles before execution.

Dependencies:
  source .venv/bin/activate
  pip install pyniryo python-dotenv

Usage:
  python3 replay_from_capture.py

Research Context:
  This tool demonstrates the lack of authentication and authorization in industrial
  robot control protocols, enabling replay attacks from captured network traffic.
"""
import sys
import time
import os
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    # Load .env from project root
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    print("✓ Environment variables loaded")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠ Using default values (if any)")

ROBOT_IP = os.getenv("ROBOT_IP", "192.168.0.100")

print("="*60)
print("REPLAY SCRIPT FROM CAPTURED TRAFFIC")
print("="*60)
print(f"Target robot IP: {ROBOT_IP}")
print("="*60)
print()

try:
    from pyniryo import NiryoRobot, PoseObject
    print("✓ pyniryo imported successfully")
except ImportError as e:
    print("✗ ERROR: pyniryo not installed")
    print("Install with: pip install pyniryo")
    sys.exit(1)

def replay_commands():
    """Esegue la sequenza di comandi catturati."""
    print(f"\nConnecting to robot at {ROBOT_IP}...")
    
    try:
        robot = NiryoRobot(ROBOT_IP)
        print("✓ Connected successfully\n")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)
    
    try:

        # Command 1: CALIBRATE (captured at 2026-01-07 11:22:38)
        print("Executing: CALIBRATE")
        robot.calibrate_auto()
        print("✓ Calibration completed")
        time.sleep(0.5)  # Small delay between commands

        # Command 2: CALIBRATE (captured at 2026-01-07 11:22:38)
        print("Executing: CALIBRATE")
        time.sleep(0.5)  # Small delay between commands

        # Command 3: UPDATE_TOOL (captured at 2026-01-07 11:22:38)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 4: UPDATE_TOOL (captured at 2026-01-07 11:22:40)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 5: GET_CONNECTED_CONVEYORS_ID (captured at 2026-01-07 11:22:40)
        print("Executing: GET_CONNECTED_CONVEYORS_ID")
        conveyors = robot.get_connected_conveyors_id()
        print(f"✓ Conveyors: {conveyors}")
        time.sleep(0.5)  # Small delay between commands

        # Command 6: UPDATE_TOOL (captured at 2026-01-07 11:22:40)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 7: UPDATE_TOOL (captured at 2026-01-07 11:22:40)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 8: UPDATE_TOOL (captured at 2026-01-07 11:22:40)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 9: GET_CURRENT_TOOL_ID (captured at 2026-01-07 11:22:40)
        print("Executing: GET_CURRENT_TOOL_ID")
        tool_id = robot.get_current_tool_id()
        print(f"✓ Current tool: {tool_id}")
        time.sleep(0.5)  # Small delay between commands

        # Command 10: GET_HARDWARE_STATUS (captured at 2026-01-07 11:22:40)
        print("Executing: GET_HARDWARE_STATUS")
        hw_status = robot.get_hardware_status()
        print(f"✓ Hardware status: {hw_status.connection_up}")
        time.sleep(0.5)  # Small delay between commands

        # Command 11: GET_DIGITAL_IO_STATE (captured at 2026-01-07 11:22:40)
        print("Executing: GET_DIGITAL_IO_STATE")
        io_state = robot.get_digital_io_state()
        print(f"✓ Digital I/O retrieved ({len(io_state)} pins)")
        time.sleep(0.5)  # Small delay between commands

        # Command 12: SET_IMAGE_BRIGHTNESS (captured at 2026-01-07 11:22:40)
        print("Executing: SET_IMAGE_BRIGHTNESS")
        robot.set_brightness(70)
        print("✓ Brightness set to 70")
        time.sleep(0.5)  # Small delay between commands

        # Command 13: SET_IMAGE_BRIGHTNESS (captured at 2026-01-07 11:22:40)
        print("Executing: SET_IMAGE_BRIGHTNESS")
        time.sleep(0.5)  # Small delay between commands

        # Command 14: SET_IMAGE_CONTRAST (captured at 2026-01-07 11:22:40)
        print("Executing: SET_IMAGE_CONTRAST")
        robot.set_contrast(60)
        print("✓ Contrast set to 60")
        time.sleep(0.5)  # Small delay between commands

        # Command 15: SET_IMAGE_CONTRAST (captured at 2026-01-07 11:22:40)
        print("Executing: SET_IMAGE_CONTRAST")
        robot.set_contrast(60)
        print("✓ Contrast set to 60")
        time.sleep(0.5)  # Small delay between commands

        # Command 16: SET_IMAGE_CONTRAST (captured at 2026-01-07 11:22:42)
        print("Executing: SET_IMAGE_CONTRAST")
        time.sleep(0.5)  # Small delay between commands

        # Command 17: SET_IMAGE_SATURATION (captured at 2026-01-07 11:22:42)
        print("Executing: SET_IMAGE_SATURATION")
        robot.set_saturation(100)
        print("✓ Saturation set to 100")
        time.sleep(0.5)  # Small delay between commands

        # Command 18: SET_IMAGE_SATURATION (captured at 2026-01-07 11:22:42)
        print("Executing: SET_IMAGE_SATURATION")
        time.sleep(0.5)  # Small delay between commands

        # Command 19: MOVE (captured at 2026-01-07 11:22:42)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 20: MOVE (captured at 2026-01-07 11:22:47)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 21: MOVE (captured at 2026-01-07 11:22:47)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 22: MOVE (captured at 2026-01-07 11:22:51)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 23: MOVE (captured at 2026-01-07 11:22:55)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 24: MOVE (captured at 2026-01-07 11:22:59)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 25: MOVE (captured at 2026-01-07 11:22:59)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 26: MOVE (captured at 2026-01-07 11:22:59)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 27: MOVE (captured at 2026-01-07 11:22:59)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 28: MOVE (captured at 2026-01-07 11:23:03)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 29: MOVE (captured at 2026-01-07 11:23:07)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 30: MOVE (captured at 2026-01-07 11:23:11)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 31: MOVE (captured at 2026-01-07 11:23:11)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 32: MOVE (captured at 2026-01-07 11:23:11)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 33: MOVE (captured at 2026-01-07 11:23:11)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 34: MOVE (captured at 2026-01-07 11:23:12)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 35: MOVE (captured at 2026-01-07 11:23:12)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 36: MOVE (captured at 2026-01-07 11:23:12)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 37: MOVE (captured at 2026-01-07 11:23:15)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 38: MOVE (captured at 2026-01-07 11:23:26)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 39: MOVE (captured at 2026-01-07 11:23:30)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 40: MOVE (captured at 2026-01-07 11:23:30)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 41: MOVE (captured at 2026-01-07 11:23:33)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 42: CALIBRATE (captured at 2026-01-07 11:25:54)
        print("Executing: CALIBRATE")
        robot.calibrate_auto()
        print("✓ Calibration completed")
        time.sleep(0.5)  # Small delay between commands

        # Command 43: CALIBRATE (captured at 2026-01-07 11:25:54)
        print("Executing: CALIBRATE")
        time.sleep(0.5)  # Small delay between commands

        # Command 44: UPDATE_TOOL (captured at 2026-01-07 11:25:54)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 45: UPDATE_TOOL (captured at 2026-01-07 11:25:55)
        print("Executing: UPDATE_TOOL")
        robot.update_tool()
        print("✓ Tool updated")
        time.sleep(0.5)  # Small delay between commands

        # Command 46: SET_IMAGE_BRIGHTNESS (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_BRIGHTNESS")
        robot.set_brightness(70)
        print("✓ Brightness set to 70")
        time.sleep(0.5)  # Small delay between commands

        # Command 47: SET_IMAGE_BRIGHTNESS (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_BRIGHTNESS")
        time.sleep(0.5)  # Small delay between commands

        # Command 48: SET_IMAGE_CONTRAST (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_CONTRAST")
        robot.set_contrast(60)
        print("✓ Contrast set to 60")
        time.sleep(0.5)  # Small delay between commands

        # Command 49: SET_IMAGE_CONTRAST (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_CONTRAST")
        time.sleep(0.5)  # Small delay between commands

        # Command 50: SET_IMAGE_SATURATION (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_SATURATION")
        robot.set_saturation(100)
        print("✓ Saturation set to 100")
        time.sleep(0.5)  # Small delay between commands

        # Command 51: SET_IMAGE_SATURATION (captured at 2026-01-07 11:25:55)
        print("Executing: SET_IMAGE_SATURATION")
        time.sleep(0.5)  # Small delay between commands

        # Command 52: MOVE (captured at 2026-01-07 11:25:55)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 53: MOVE (captured at 2026-01-07 11:25:58)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 54: MOVE (captured at 2026-01-07 11:25:58)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 55: MOVE (captured at 2026-01-07 11:26:02)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 56: MOVE (captured at 2026-01-07 11:26:07)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 57: MOVE (captured at 2026-01-07 11:26:10)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 58: MOVE (captured at 2026-01-07 11:26:10)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 59: MOVE (captured at 2026-01-07 11:26:11)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 60: MOVE (captured at 2026-01-07 11:26:11)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 61: MOVE (captured at 2026-01-07 11:26:14)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 62: MOVE (captured at 2026-01-07 11:26:18)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 63: MOVE (captured at 2026-01-07 11:26:22)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 64: MOVE (captured at 2026-01-07 11:26:22)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 65: MOVE (captured at 2026-01-07 11:26:22)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 66: MOVE (captured at 2026-01-07 11:26:23)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 67: MOVE (captured at 2026-01-07 11:26:23)
        print("Executing: MOVE")
        pose = PoseObject(x=-0.009, y=0.196, z=0.3, roll=2.393, pitch=1.116, yaw=-1.726)
        robot.move_pose(pose)
        print("✓ Moved to position (-0.009, 0.196, 0.300)")
        time.sleep(0.5)  # Small delay between commands

        # Command 68: MOVE (captured at 2026-01-07 11:26:26)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 69: MOVE (captured at 2026-01-07 11:26:30)
        print("Executing: MOVE")
        pose = PoseObject(x=0.195, y=-0.072, z=0.398, roll=-1.466, pitch=1.457, yaw=-0.338)
        robot.move_pose(pose)
        print("✓ Moved to position (0.195, -0.072, 0.398)")
        time.sleep(0.5)  # Small delay between commands

        # Command 70: MOVE (captured at 2026-01-07 11:26:34)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 71: MOVE (captured at 2026-01-07 11:26:34)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        # Command 72: MOVE (captured at 2026-01-07 11:26:36)
        print("Executing: MOVE")
        time.sleep(0.5)  # Small delay between commands

        print("\n" + "="*60)
        print("REPLAY COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ ERROR during replay: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            robot.close()
            print("\n✓ Robot connection closed")
        except:
            pass

if __name__ == '__main__':
    print("\n⚠️  WARNING: This script will move the robot!")
    print("Make sure the workspace is clear of obstacles.\n")
    
    response = input("Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        sys.exit(0)
    
    replay_commands()
