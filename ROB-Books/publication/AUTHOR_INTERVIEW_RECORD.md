# Building R.O.B. — author interview record

This record separates Rodolfo Aramayo's firsthand recollection from facts independently supported by source, photographs, or the public website. It also records editorial transformations made to avoid turning memory, enthusiasm, or eight years of operation into an unsupported technical or safety claim.

## Responses received August 29, 2026

### Publication posture

The complete manual is a historical engineering reference and educational field manual. It should help readers understand ROB's evolution and reproduce its ideas, but it is not a dimensionally complete construction plan. ROB was built by hand, initially and substantially with wood, and the as-built CAD files do not exist. Reconstructing measured CAD is a future project. Eight years of iteration and operation are part of the history; they are not represented as a safety certification.

The changing prominence of humanoid robots is relevant context rather than a reason to erase the treaded platform. The book treats ROB as a record of one maker's decisions across the mobile, tracked, spatial-computing, and AI eras.

### Identity and origin

- ROB is a friendly name taken from “robot,” not an acronym.
- The project began after the author left Verizon Labs, where he worked as a systems software engineer on mobile VR/AR research technologies. He recalls building ROB in College Station, Texas, and dates the new treaded prototype to approximately 2016; no exact month is asserted.
- The 2017–2018 Cerebro serial controller belongs to ROB's initial physical prototype.
- Johnny 5 was personal inspiration for a friendly expressive robot in the era of mobile devices and 3D depth cameras. The books use no protected character art, logo, prop, or copied design.
- Cerebro is a playful model of a cognitive processing center or brain; it does not claim consciousness.
- “Rob Makina” was the author's Latin-sounding wordplay for “robot machine,” not another contributor.
- The v5 repository reset was a pragmatic attempt to leave behind accumulated Git history and artifacts. It imported an existing application; it did not begin Cerebro.

### Mission and software history

ROB began as an attempt to combine an expressive mobile robot with modern cameras, interfaces, and conversational software. The source confirms a CakeChat local neural-dialogue integration. Publication wording calls this an early pre-ChatGPT dialogue experiment; it does not claim that CakeChat was a technical ancestor of ChatGPT.

Today ROB is the most elaborate project of Rodolfo Aramayo's career and a continuing platform for exercising and teaching mobile development, spatial computing, robotics, perception, controls, and AI. The author's “most powerful mobile developer” wording is preserved as personal confidence and ambition, not printed as an objectively verified ranking.

### Builder and suppliers

Rodolfo Aramayo identifies himself as the sole builder, author, and principal software developer—the “me, myself, and Irene” comment was a joke about working alone. Suppliers are credited for the components they provided, without suggesting coauthorship, sponsorship, endorsement, or responsibility for ROB's integration:

- Apple — Mac mini computers;
- Arashi Vision / Insta360 — Insta360 Pro II panoramic camera;
- HengDrive — brushless motors;
- B-COMMAND — custom rotary/slip-ring interfaces;
- NETGEAR — Orbi networking equipment;
- AMBER Robotics — B1 arms and controller environment;
- SuperDroid Robots — LT2 tread system;
- Arduino — Mega 2560 controller platform;
- SLAMTEC / SLAMWARE — RPLIDAR and mapping stack;
- other suppliers only where a component record identifies them.

### Hardware eras and lessons

The author's first prototype combined a car battery, Power Wheels motors and wheels, scrap wood, an older Intel laptop, and an old robotic arm. The next major era used the SuperDroid Robots LT2 tracks and a third-wheel/flipper concept intended to improve turning and explore stair motion.

Early roughly 30 W brushless motors were underpowered at 12 V. Gear changes recovered torque but not the intended speed; a later 12-to-24 V boost stage made ROB stronger and faster while it remained a slow, high-torque machine. The drivetrain lesson is recorded as a design recollection, not a recommendation to over-volt an unidentified motor. The author would choose at least approximately 120 W per motor and about four times the speed in a future redesign, subject to a new full-system analysis.

Later eras added RPLIDAR, a stepper-driven torso, and hobby-servo arms and plastic grippers controlled by a 24-channel Maestro with recordable/replayable actions. Heavy AMBER B1 arms exposed the limits of the first single-arm controller environment and the author's then-limited Ubuntu/ROS experience. After years without the desired coordinated operation, the author purchased a dedicated dual-arm B1 setup for approximately $22,500. Recent AI-assisted work expanded secure controllers, Vision Pro H.264 video, camera and depth processing, machine vision, Gemini and Apple-model experiments, voice/video input, and the modern ROBController and Cerebro applications.

### Public history supported so far

- Maker Faire's official R.O.B. entry records the Bay Area 2019 exhibit on May 17--19; the official program locates that fair at the San Mateo County Event Center in San Mateo, California.
- Maker Faire's official 2023 yearbook records R.O.B. as a Bay Area project. The event ran October 13--15 and 20--22 at Mare Island Naval Shipyard in Vallejo, California.
- Maker Faire's official R.O.B. entry records the Bay Area 2024 exhibit on October 18--20 at Mare Island.
- Maker Faire's official R.O.B. entry records the Bay Area 2025 exhibit on September 26--28 at Mare Island.
- The 2026 Bay Area fair is scheduled for September 25--27, after this August 29 record. The book makes no claim that R.O.B. has appeared at that future event; a later accepted-project or post-event record can extend the ledger.

Primary records: [R.O.B. 2019](https://makerfaire.com/maker/entry/r-o-b-70608/), [2019 program guide](https://makerfaire.com/wp-content/uploads/2019/05/MF19BA_ProgramGuide_Small.pdf), [2023 project yearbook](https://makerfaire.com/yearbook/2023-projects/?_sfm_faire_information_faire_post=675781&_sft_mf-project-cat=engineering), [2023 event schedule and venue](https://makerfaire.com/bay-area-2023/sunday-october-22-2023/), [R.O.B. 2024](https://makerfaire.com/maker/entry/76120/), [R.O.B. 2025](https://makerfaire.com/maker/entry/r-o-b-78103/), and [2026 event schedule](https://makerfaire.com/bay-area/tickets/).

### Rights, reviewers, and audiences

The author confirms that he took every selected real photograph in the current book allowlist with his iPhone. He confirms that ROB and the visible components are his property and that the selected product/component photographs are his photographs of those owned components. There are no photographer exceptions or separately licensed product photographs in the closed allowlist. The selected assets contain no event, venue, bystander, or identifiable-person photograph, so venue and model-release questions are not applicable to this edition.

The author explicitly confirms Rodolfo Aramayo as author; OrbitusRobotics LLC as publisher/imprint and copyright owner; copyright year 2026; all-rights-reserved status for book text and artwork; repository-specific licensing for source code; and worldwide sales territory.

No external electrical, mechanical, educator/youth-safety, accessibility, privacy, or legal reviewer has been retained. The edition therefore cannot claim those approvals. Engineering construction claims that would require them are removed or reframed as history, evidence limits, conceptual lessons, and future documentation work. Automated validation supports but does not impersonate human approval.

The author approves the existing age bands: story 5–6; Volume 1 8–12; Volume 2 10–14; Volume 3 10–15; Volume 4 12–16; Volumes 5–8 and the complete manual for advanced readers.

## Resolved author questions

- [x] **Q01 — Start date and place.** “ROB was built in College Station, TX and the new treaded prototype was built around 2016ish.” Editorial treatment: College Station, Texas; approximately 2016 for the treaded prototype; exact month not asserted.
- [x] **Q03 — Photo exceptions.** “I took all the photos with my iPhone.” Editorial treatment: no photographer exception exists in the selected real-photo allowlist.
- [x] **Q04 — Publishing identity and territory.** “I confirm all the data about the copywrite.” This response was given to the complete stated list and records Rodolfo Aramayo as author; OrbitusRobotics LLC as publisher/imprint and copyright owner; 2026 copyright; all-rights-reserved book text/art; repository-specific source-code licenses; and worldwide sales territory.
- [x] **Q05 — Product-photo rights.** “Yes the robot is my own and the components are mine and the photos were taken by me.” Editorial treatment: all visible product/component photographs in the allowlist are the author's own photographs of components he owns; there are no exceptions.

The event-history question is resolved for the 2019, 2023, 2024, and 2025 editions by official Maker Faire records. The upcoming September 2026 fair is not treated as a completed appearance. Later final approvals—accessibility/device reading, printer proof, and final publisher sign-off—cannot be answered until those artifacts exist and are tracked in the main release gate rather than this interview.
