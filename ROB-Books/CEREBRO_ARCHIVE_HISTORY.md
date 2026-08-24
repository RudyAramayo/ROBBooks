# Cerebro before the fresh v5 repository

The current public Cerebro Git history begins on 5 August 2025 with commit
`4c4f1d4`, whose subject calls itself an “initial commit with v5 changes and a
fresh repo.” That commit is a repository boundary, not the birth of Cerebro.
Five preserved archive folders recover the application's earlier workshop
history. Together they show ROB-specific Mac software by 2017-2018, a first
Git history beginning on 1 January 2018, years of perception and control
experiments, and a 2025 migration into the fresh v5 repository.

This record distinguishes three kinds of evidence:

- **upstream ancestry**, where an older example supplied starting code;
- **ROB-specific work**, identified by project names, code, file headers, and
  commits; and
- **repository migration**, where existing code entered a new Git history.

The folders are preserved under the archive labels `Cerebro v1` through
`Cerebro v5`. Those labels are useful evidence coordinates, but they should not
be read as proof that each folder was a formal public release.

## Corrected chronology

| Archive evidence | Date range established by the evidence | What it preserves |
|---|---|---|
| `Cerebro v1` | upstream sample dated 2009; ROB-specific additions dated 2017-2018 | A Cocoa serial console adapted into a ROB command station, including 250000-baud serial I/O, the seven-field text frame, motion actions, keyboard input, and early peer-network scaffolding. |
| `Cerebro v2` | 2018-01-01 to 2018-05-17 | Cerebro's first surviving Git history: speech, separate Base/Head/Torso serial roles, Mac UI composition, SceneKit, multipeer communication, Kinect/OpenNI/NiTE/PCL attempts, a named consciousness bridge, and Leap Motion. |
| `Cerebro v3` | shared 2018 root; master through 2022-04-09 | Controller arbitration, autonomy permission, multilingual speech, Maestro servos, ReSpeaker and RealSense processes, human/head tracking, RTSP, T265, performance work, AutoNet, and the decision to split RPLidar into another repository. |
| `Cerebro v4` | shared 2018 root; master through 2025-07-02 | A branch of the older history carried through Apple-silicon migration, USB/text-output hardening, Google LLM responses, singleton-process work, continuous speech experiments, and Apple Foundation Models work. |
| `Cerebro v5` archive | independent root on 2025-08-05 | A fresh repository importing the already substantial robot program, followed by the modern Gemini, OAK, AMBER, animation, perception, and 2026 safety/architecture work documented elsewhere in the series. |

## The v1 seed: a serial example becomes ROB's Mac command station

The oldest folder is a pre-Git working archive. Its Cocoa shell retains the
header “Arduino Serial Example” and credits Gabe Ghearing with a 30 June 2009
creation date. That is the ancestry of the starting example, not evidence that
Cerebro or ROB began in 2009.

ROB-specific evidence appears later. `KeyboardInputView.m` credits Rob Makina
on 18 September 2017, `SerialDebug.m` credits Rob Makina on 1 January 2018, and
the Xcode product is named Cerebro. The adapted `SerialExample.m` opens a
specific USB modem device at 250000 baud and provides forward, backward,
turning, flipper, and linear-actuator actions. `BotCommands` records the same
seven signed fields later documented throughout the ROB stack: three brake and
motor pairs followed by the linear actuator command. `MCManager` and the
keyboard view show that local buttons were already beginning to grow into
multiple control inputs.

This is Cerebro's first surviving software root: not yet the broad robot mind
of later years, but a practical Mac-to-machine nervous system. It could format
ROB's command language, open the serial link, display traffic, and give the
builder direct controls while the hardware protocol was still being learned.

## v2: the command station grows a voice, senses, and a body map

`Cerebro v2` contains eleven commits. The root, `0141a646`, was committed by
Rob Makina on 1 January 2018. The next day, commit `6824552` completed a
SpeechBox, `1ddd815` added working serial paths for Base, Head, and Torso while
binding controls and windows, and `1aef23a` added multipeer and SceneKit
controllers.

The surviving main controller composes serial, speech, keyboard, SceneKit,
multipeer, NiTE, Leap Motion, chat, and a class named `ROBConsciousness`. That
name records the intended architectural role, not proof that the early bridge
was a completed autonomous intelligence. Likewise, the SceneKit controller's
sample scene is UI scaffolding rather than evidence of a calibrated digital
twin.

The January perception commits are unusually candid evidence. They record
OpenNI and PCL integration, celebrate point-cloud data appearing in Cerebro,
attempt NiTE user tracking, and then label one integration a failure. In May,
the history records further libfreenect/NiTE work and ends at `c278298`, a Leap
Motion integration. Successes and failed integrations belong in the history
together: this was the period when Cerebro expanded from issuing commands to
experimenting with voice, people, hands, point clouds, and multiple robot
subsystems.

## v3: control arbitration and the perception laboratory

The v3 archive retains the 2018 root and fifty commits across all surviving
branches; its master branch contains forty-six. Commits after the v2 endpoint
add advanced controller commands and follow tracking. By May 2019,
`892cd08` explicitly requires a master controller identity to prevent
conflicting input and requires permission for autonomous mode. That is an
early form of the authority boundary that later ROBControl designs formalize.

The 2019 history then reads like a robotics laboratory notebook: Maestro servo
control and electrical noise, volume and mood controls, multilingual input and
output, wireless joining, head tracking, NiTE and VTK iterations, ReSpeaker
and RealSense task processes, visual recognition, human tracking tied to torso
camera movement, RTSP work, Intel T265 tracking, headless-performance fixes,
an elbow degree of freedom, and repaired Google speech/chat behavior. Separate
branches preserve NiTE2, libfreenect, ROB2, and T265 experiments.

The v3 master ends at `00fbf6b` on 9 April 2022. That commit records a cleanup,
the installation of AutoNet, the decision to move RPLidar into a separate
repository, and controller binding from the iPad. Cerebro was already a
distributed, mixed-language robot coordinator years before the v5 Git reset.

## v4: migration without severing the old history

The v4 archive shares the 2018 root and the historical experiment branches,
but its master follows a line that diverged from the later v3 master after the
9 November 2019 T265/perception checkpoint `b676ced`. It carries the
application through an M1 checkpoint in July 2023, memory-safe text-output and
USB-network changes, and a September 2023 demo with Google LLM responses.

Two commits on 2 July 2025 make the transition explicit. `cc87f3e` records
singleton-process checking, a continuous-speech beta, and the intention to
create the next v5 release. `1a3c779` records working Apple Foundation Models
AI alongside an XPC crash that still needed investigation. This is continuity
with unresolved engineering work, not a blank new application.

## v5: a new Git root around an old machine

The v5 archive has a different root commit: `4c4f1d4` on 5 August 2025. The
commit has no parent and its own subject says it contains v5 changes in a fresh
repository. Its imported tree already includes the macOS storyboard, speech,
serial control, camera management, AutoNet, lidar, Kinect/RealSense-era
components, Leap Motion, RTSP, task launchers, Core ML assets, and mixed
Objective-C/Swift code.

The correct reading is therefore:

```text
upstream Cocoa serial example (2009)
        |
ROB-specific Cerebro seed (2017-2018)
        |
first surviving Cerebro Git root (2018)
        |
v2 / v3 / v4 workshop histories (2018-2025)
        |
fresh v5 Git repository imports the existing system (2025)
        |
current public development (2025-present)
```

The fresh repository made the modern history easier to work with, but it also
hid the commit-level ancestry from an ordinary `git log`. The archive restores
that missing context.

## Evidence boundaries and preservation notes

- The v1 folder has no Git metadata. File headers, project settings, source,
  and SHA-256 fingerprints establish the surviving state, but not every edit's
  exact date or author.
- The 2009 attribution belongs to the upstream Arduino serial example. The
  books do not claim that ROB or Cerebro began in 2009.
- The archived Git author labels include Rob Makina, Rodolfo Aramayo, Orbitus,
  and a placeholder `you@example.com` identity. Commit labels are evidence
  coordinates, not a complete contributor biography.
- The folders contain third-party examples, libraries, models, and SDK
  material. Their presence does not transfer authorship or publication rights.
- Some preserved working copies contain uncommitted changes or iCloud
  placeholders. Historical claims in the books use committed objects when Git
  exists and identify the pre-Git v1 evidence separately.
- Preserve the archive folders read-only. If they are ever migrated, retain
  original `.git` directories, hashes, file timestamps, notices, and an
  integrity manifest before normalizing or cleaning anything.

## Reproducible evidence coordinates

| Item | Fingerprint or Git coordinate |
|---|---|
| v1 `SerialExample.m` | SHA-256 `0ebe93d9045a90b08df01cf34218361b391e8343877171a1ab115c5f2440e728` |
| v1 `KeyboardInputView.m` | SHA-256 `e3b16998585e5dbc88a90aaa5b61d35d25abc8776d008015dbff1a01ebb437eb` |
| v1 `SerialDebug.m` | SHA-256 `c1de40a9361dc6881f749ccf20145c86738ecde58f743dbf60f7f562a9e36d5c` |
| v1 `BotCommands` | SHA-256 `8f4368a4ed19406bf0948e67791ae998f88378e15a58092d2ef44afb50d66ee6` |
| v1 Xcode project | SHA-256 `fe4e6ce0c549c45a483b4947e2c7f6ca1dd6067ecddc66a645555a6853221d05` |
| v2 Git range | `0141a6461303302e53941c398ebeda4f60c1a1c7` through `c27829851b9252310a7ee14337ec7c773ca52813` |
| v3 master | `00fbf6bdc4ec9c62df9173253bfe3b7e4ab1c2db` |
| v4 master | `1a3c7799bdb4b60d0d4917f5de4ad0a95d88e96e` |
| v5 fresh root | `4c4f1d454253e39798c23aed4522716068aadd98` |

The full inspection snapshot, including branch counts and working-tree cautions,
is recorded in `SOURCE_SNAPSHOT.md`.
