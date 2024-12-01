smoothCamGenerator v001

Date: 01/12/2024
Purpose: Generate a smoother motion path from your 3D camera in Nuke.
General Overview

The smoothCamGenerator Python script is designed to refine the motion of a tracked 3D camera in Nuke. By leveraging a self-contained Python button, this tool creates a new 3D camera with smoother motion while preserving the original direction and trajectory.

Upon execution, the script performs a sequence of operations to generate a new 3D camera linked to the original one. This new camera includes an additional "Smoothing" tab, providing the user with the following controls:
Main Controls

    Smooth: Adjusts the degree of smoothness applied to the camera's motion.
    Offset: Adds a positional offset to the new camera, allowing deviations from the original motion path while maintaining its overall direction.
    Bake: Unlinks the new camera from the original by baking the animation onto the new camera's knobs.

Usage Instructions

    Copy the SmoothCamGen.nk script to your .nk/Toolsets/ directory.
        (Optional) Create a subfolder for better organization.
    Restart your instance of Nuke.
    Access the group by:
        Pressing Tab and searching for "SmoothCamGen", or
        Browsing through the Toolset menu in the toolbar.
    Follow the instructions provided in the "Info" tab for setup and usage guidance.

Disclaimer

This tool has been tested on the following Nuke versions:

    12.1v1
    13.2v6
    14.0v1

While it is expected to work on other versions, compatibility cannot be guaranteed.
