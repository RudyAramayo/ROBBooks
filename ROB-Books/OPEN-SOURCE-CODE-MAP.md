# R.O.B. source-code map

This map tells book readers exactly where to begin. All paths are relative to the workspace root used for this edition:

```text
/Users/rob/dev
```

On another computer, replace that prefix with the directory where the repositories were checked out. For example:

```bash
cd /path/to/dev
sed -n '1,220p' ROBArduino/ROBOT_CEREBELLULAR_BASE_APP/ROBOT_CEREBELLULAR_BASE_APP.ino
rg -n "ROBControl" Cerebro ROBController ROBControllerVision
```

## A necessary licensing distinction

“The source is visible in this workspace” and “the project is open source” are not automatically the same statement. `ORobotics/LICENSE` is the explicit top-level license found during this review. Several other repositories expose readable source locally but do not have a top-level license file in the inspected snapshot. Without a license grant, readers may study the code but should not assume permission to redistribute or create derivative releases. The AMBER V2 API has its own license file inside its API directory. The captured `amber_core` executables are binaries and are not open source in this snapshot.

Before publishing the whole collection, add an intentional license to every repository the owner wishes to release and preserve third-party notices.

## Firmware

Repository: `ROBArduino`

| Role | File analyzed | Status |
|---|---|---|
| current Base controller | `ROBArduino/ROBOT_CEREBELLULAR_BASE_APP/ROBOT_CEREBELLULAR_BASE_APP.ino` | Present firmware reference for serial parsing, treads, flipper, actuator, IR, IMU, and heartbeat |
| retired Torso controller | `ROBArduino/ROBOT_CEREBELLULAR_TORSO_APP/ROBOT_CEREBELLULAR_TORSO_APP.ino` | Historical three-Arduino architecture |
| retired Head controller | `ROBArduino/ROBOT_CEREBELLULAR_HEAD_APP/ROBOT_CEREBELLULAR_HEAD_APP.ino` | Historical experiment |

Volume 2 analyzes these most closely. Volumes 1, 3, 4, and the field manual use the Base sketch where firmware affects their lesson.

## Cerebro: the Ubuntu-facing Mac coordinator

Repository: `Cerebro`

| Topic | Start with this file |
|---|---|
| main coordination | `Cerebro/Cerebro/ROBMainViewController.mm` |
| Arduino serial output and helpers | `Cerebro/Cerebro/ROBSerialBox.m` |
| camera and bounded frame delivery | `Cerebro/Cerebro/CameraManager.swift` |
| controller protocol and server-side authentication | `Cerebro/Cerebro/AutoNet/AutoNetShared/AutoNetDataTransferProtocol.swift` |
| autonomy state machine | `Cerebro/Cerebro/ROBAutonomyCoordinator.swift` |
| optional AI path | `Cerebro/Cerebro/ROBAI.swift` |
| typed model action schema | `Cerebro/Cerebro/GeminiRoboticsProtocol.swift` |
| animation persistence | `Cerebro/Cerebro/KeyframeAnimationManager.swift` |
| AMBER high-level client | `Cerebro/Amber-PythonAPI/Amber V2 API/amber_api/amber_robot.py` |
| AMBER wire structures | `Cerebro/Amber-PythonAPI/Amber V2 API/amber_api/basic_cmd/` |

Volumes 4 and 5 analyze Cerebro's software architecture. Volume 6 analyzes the AMBER API and its boundary with the Ubuntu core.

## iPhone and Watch controller

Repository: `ROBController`

| Topic | Start with this file |
|---|---|
| iPhone/iPad control UI | `ROBController/Consciousness/ConsciousViewController.mm` |
| network client | `ROBController/Consciousness/AutoNetClient/AutoNetClient.swift` |
| client wire contract | `ROBController/Consciousness/AutoNetClient/AutoNetDataTransferProtocol.swift` |
| Watch relay | `ROBController/Consciousness/AutoNetClient/ROBWatchRelay.swift` |
| Watch UI | `ROBController/Consciousness-Watch Watch App/ContentView.swift` |
| robot-action proposal schema | `ROBController/Consciousness/ROBRobotActionProtocol.swift` |
| transport security fixtures | `ROBController/Tests/ROBControlTransportSecurityFixtureTests.swift` |

Always compare the client contract with Cerebro's matching file. A protocol is a relationship between implementations, not a fact owned by one file.

## Vision Pro controller

Repository: `ROBControllerVision`

| Topic | Start with this file |
|---|---|
| spatial cockpit layout | `ROBControllerVision/ROBControllerVision/App/ContentView.swift` |
| control surfaces | `ROBControllerVision/ROBControllerVision/Features/Control/ControlPanel.swift` |
| speech control | `ROBControllerVision/ROBControllerVision/Features/Control/OperatorSpeechPanel.swift` |
| camera presentation | `ROBControllerVision/ROBControllerVision/Features/Video/VideoPanel.swift` |
| telemetry | `ROBControllerVision/ROBControllerVision/Features/Telemetry/TelemetryPanel.swift` |
| pairing | `ROBControllerVision/ROBControllerVision/Features/Connection/CerebroPairingSheet.swift` |
| reusable wire protocol | `ROBControllerVision/Packages/ROBControlCore/Sources/ROBCerebroTransport/Control/ROBControlWire.swift` |
| reusable client state machine | `ROBControllerVision/Packages/ROBControlCore/Sources/ROBCerebroTransport/Control/ROBControlClient.swift` |

Volume 5 analyzes the spatial control and speech features. Volume 4 introduces the role of this repository.

Volume 7 is the implementation-level ROBControllerVision book. Its recommended reading order begins with `Package.swift`, domain protocols and `RobotSession`, continues through `RobotViewModel`, controller/head/speech inputs, then follows the control and video transports down to H.264 validation and AVFoundation presentation. Every chapter prints the file being analyzed.

Volume 8 is the implementation-level Cerebro companion. It begins with the mixed Objective-C/Swift application boundary, dissects `ROBSerialBox.h/.m`, then follows AVFoundation and DepthAI RGB-D frames through Vision, SceneKit, `SceneSnapshot`, MLX LLM/VLM inference, Gemini Live, the stage-show coordinator, saber choreography, and the robot side of the Volume 7 control/video protocols. It also identifies the Kinect/OpenNI/PCL files as historical artifacts from the repository's initial import rather than presenting them as the current camera path.

## AMBER arm sources and captured Ubuntu runtime

| Evidence | Exact path | Publication status |
|---|---|---|
| readable V2 Python API | `Cerebro/Amber-PythonAPI/Amber V2 API/` | Has a directory-local `LICENSE`; read it before reuse |
| single-arm robot description | `Amber URDF/amber_b1.urdf` | Readable model; confirm its licensing and mesh rights before redistribution |
| dual-arm robot descriptions | `AmberHomeFolder/amber/amber_core/urdf/dual_b1/` | Captured files; licensing not established by this book |
| LCM schema source | `AmberHomeFolder/amber/sin_wave/rawLcm/` | Readable message definitions; licensing not established by this book |
| left launch configuration | `AmberHomeFolder/amber/L-10/launch.json` | Machine-specific captured configuration |
| right launch configuration | `AmberHomeFolder/amber/R-11/launch.json` | Machine-specific captured configuration |
| CAN discovery script | `AmberHomeFolder/amber/amber_core/init/initCan.sh` | Historical script requiring review |
| left/right core | `AmberHomeFolder/amber/L-10/amber_core_L`, `AmberHomeFolder/amber/R-11/amber_core_R` | Captured, byte-identical binaries; not source code |

Volume 6 clearly labels which of these files it is analyzing at each chapter. Do not copy `.ssh`, histories, logs, caches, virtual environments, or USB serial inventories from the captured home folder.

## Website and learning games

Repository: `ORobotics`

The project contains the explicit top-level `ORobotics/LICENSE`. Hugo content, layouts, data, and static assets live under the conventional project directories visible at its root. Find the USB-splicing and robot-lab lessons with:

```bash
rg -n -i "usb|splice|5v|robot lab|game" ORobotics/content ORobotics/layouts ORobotics/static ORobotics/assets
```

Repository: `ROBTrainingGames`

This companion contains native training-game source. Consult its project files and local documentation for build targets; verify or add a license before calling it open source publicly.

## Book sources themselves

Repository: `Presentation`

| Material | Location |
|---|---|
| editable manuscripts | `Presentation/ROB-Books/source/` |
| shared book style and source-trail boxes | `Presentation/ROB-Books/source/robbook.sty` |
| generated PDFs | `Presentation/ROB-Books/output/pdf/` |
| build script | `Presentation/ROB-Books/tools/build_books.sh` |
| validation script | `Presentation/ROB-Books/tools/validate_books.sh` |
| evidence hashes | `Presentation/ROB-Books/SOURCE_SNAPSHOT.md` |

Generated PDFs are outputs. Make editorial changes in the manuscript or shared style, rebuild, and validate rather than editing a PDF.

## If a path changes

Use the symbol or filename to rediscover it:

```bash
rg --files Cerebro ROBController ROBControllerVision ROBArduino | rg 'CameraManager|AutoNetDataTransferProtocol|BASE_APP'
rg -n "struct ROBControlFrameHeader|class ROBSerialBox|ROBAutonomyCoordinator" Cerebro ROBController ROBControllerVision
```

Then update both the book's `SOURCE TRAIL — ANALYZING NOW` box and this map. Record the repository commit and file hash in `SOURCE_SNAPSHOT.md` for a publication release.
