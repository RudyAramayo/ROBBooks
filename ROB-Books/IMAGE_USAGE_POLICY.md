# Image distinctness policy

The eight numbered *Building R.O.B.* volumes should feel like different visual journeys, not reshuffled copies of one photo deck.

## Visual ownership

- Volume 1 owns early history, ROB portraits, and the systems-feedback plate.
- Volume 2 owns circuits, wiring, power, and the circuits/signals plate.
- Volume 3 owns drivetrain, fabrication, actuators, and the mechanics plate.
- Volume 4 owns computing, cameras, architecture slides, and software/autonomy plates.
- Volume 5 owns its AI-era cover and source-history presentation.
- Volume 6 owns the dual-AMBER-arm feedback illustration.
- Volume 7 owns the controller-system cutaway and code-centered presentation.
- Volume 8 owns the Cerebro perception-and-control plate and robot-side software presentation.

A generated illustration must be captioned as conceptual. A photograph used to support a physical or historical claim may not be replaced merely for variety unless the replacement supports the same claim and its caption is rewritten.

## Intentional numbered-volume exception

`2022-chassis-wiring-overhead.jpg` appears in Volumes 1 and 2. Volume 1 uses it once as dated timeline evidence. Volume 2 analyzes its electrical routing. This is the only allowed cross-volume image in the current numbered series.

## Complete field manual

The *Complete Builder's Field Manual* is the deliberate visual index and consolidation layer for the series. It repeats selected evidence photographs from the numbered volumes because its claims must remain reviewable without requiring eight books open at once. This exception applies only to the manual and only to evidence photographs or historical slides; it is not permission to reuse decorative chapter art casually.

The audit reports manual overlap separately so editors can reduce it as new, publication-safe as-built photographs and measured diagrams become available.

## Editorial rule

Before adding or replacing an image:

1. run `bash tools/audit_image_reuse.sh`;
2. identify the volume that owns the topic;
3. prefer an unused prepared asset or that volume's conceptual plate;
4. rewrite the caption to describe exactly what the image shows;
5. never convert conceptual art into engineering evidence;
6. add a cross-volume exception only with a written evidence reason;
7. rebuild and run the full PDF validator.
