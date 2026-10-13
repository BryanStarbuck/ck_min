---
title: "Body Tour Research: Where the Transmitter Sat, and the Angles"
draft: true
---

{/* Research record for the 3D Body Tour (site/internals/static/scorecard/exhibit/).
    draft: true keeps it off the production site; it shows only on the local dev server. */}

# Body Tour Research: Where the Transmitter Sat, and the Angles

Started 2026-10-13. This file records everything behind two numbers in the 3D Body Tour: **where the RØDE transmitter sat on Charlie Kirk's chest**, and **the angles** (the State's bullet path, and the line from the transmitter up to the neck wound). It holds Bryan's instructions, the research text he supplied, the video work, the measurements, and what the diagrams now show. Update it whenever new evidence moves either number.

## Summary

* **Where the transmitter sat (measured from video):** on the **upper right chest**, about **4.7 cm (about 2 in) below the T-shirt neckline** and **5 to 7 cm (2 to 3 in) right of center**, just under the right collarbone. This is where its magnetic clip shows on the front camera in every frame where the clip can be seen, from earlier in the event right up to the frames just before he was hit.
* **That is higher than the written accounts, not lower.** The supplied research text quotes observers who put it "near" or "under the right nipple". A man's nipple sits roughly 15 to 20 cm below the neckline, about 4 to 6 inches lower than the clip. No frame we found shows the clip or the bulge that low. Bryan's sense that it sat lower than the nipple is not supported by the footage we hold.
* **The diagrams now show:** the transmitter at the measured spot. The dashed "could have sat" outline runs from there down to nipple level, so it covers the written accounts too.
* **The line from the transmitter to the wound:** about **14 cm (5.5 in)** long. It rises about **45 degrees** above level and leans about 40 degrees across his body toward his left. If the transmitter had been at the nipple, the line would be about 26 cm (10 in) long and rise about 59 degrees.
* **The State's bullet angle:** drawn at the **sworn 9 degrees** (415 ft to the tent, 410 ft flat, 68 ft drop, prelim Day 4). The **published range of 4 to 10 degrees** is shaded around it, with a thin line at the commonly cited 6 degrees. At any angle in that range, the path meets the spine at about C6 and C7, not C2.

## What the diagrams use (code)

All in `site/internals/static/scorecard/exhibit/body_tour_assets/anatomy.js`. The model is in centimetres; +x is the patient's left; y = 0 is the sternal notch.

| Constant | Value | Meaning |
|---|---|---|
| `DEVICE_XY` | (-6.0, -4.2) | Centre of the 44 x 45.3 x 18.5 mm housing: 6 cm right of center, 4.2 cm below the sternal notch (the T-shirt neckline sits about 1 cm above the notch) |
| `DEVICE_ZONE` | centre (-8.0, -10.4), radii 4.2 x 7.6 | Dashed outline from the measured spot down to just under the right nipple |
| `NIPPLE_R` | (-10.0, -14.5) | Right nipple in the model, used only for the "some accounts" label |
| `BULLET_ANGLE` | sworn 9, estimate 6, range 4 to 10 | Degrees below level; the path is drawn at 9, the range is shaded |
| `JET_ANGLE` | about 44 | Computed: the transmitter-to-wound line's rise above level |

The page text that states these numbers is on neck.html (charge steps 1 and 2), spine.html (bullet step 3, charge step 1), lungs.html (charge step 1), heart.html (charge intro and step 1) and body_tour.html (the two boxes).

## The video research

### What was searched

* `videos.csv` (55 rows) and `videos/videos.yaml` (477 video entries, with titles and descriptions where they exist).
* Every video file on this machine: 501 in the repo's `videos/` folder (gitignored) and 333 under `~/_Mirror/Politics/Charlie_Kirk_Mi/`. Each was probed for resolution, frame rate and length.
* Ranked by: resolution, a camera angle that shows the front of his chest, and how much of the frame his head-to-waist takes up at the moment he was hit.

### The clips that matter

| Clip | Size | What it shows | Use |
|---|---|---|---|
| `~/_Mirror/.../Assassination/CK_Assassination.mp4` | 1920 x 1080, 30 fps, 55 s | The front broadcast-style camera. From about 29 s, a tight shot from head to lap, square to his chest | **Primary.** The clip is visible at 29.5, 30.5, 33.0 and 33.5 s (just before impact) and 44.5 s; hidden by the bunched shirt at 36.5 to 37.5 s |
| `~/_Mirror/.../video/Blake Bednarz - Reward ... [1978863594709082112].mp4` | 3240 x 2160, 60 fps, 164 s | Side by side: left panel is the same front camera, sharper, earlier in the event while he holds the microphone | **Confirms.** Clip in the same place at 88 s |
| `videos/2084153118317568321.mp4` (Project Constitution, "High-Resolution Source Clip of the Shooting Moment") | 2160 x 2420, 60 fps, 105 s | Close, from his right side and slightly behind, seated, head to lap, through the impact (about 34.8 s) | Highest resolution at impact, but it sees his right shoulder and back, not the front of his chest. **Cannot place the transmitter** |
| `~/_Mirror/.../Mic/US_did_ 911 - @jonaaronbray ... [2027171669668683777].mp4` | 3840 x 2160 | Jon Bray's own zoomed analysis of the front camera | His red arrow points at the same clip, just below the collar on the right |
| `~/_Mirror/.../video/Muppet Masher - It comes from under his shirt ... [2066468514530283520].mp4` (same footage as the "Marissa" post) | 1702 x 2254, 30 fps, 25 s | Phone video from the crowd, head to lap, through the impact | **Mirrored left to right** (the "PROVE ME WRONG" banner reads backwards). Never judge left or right from it without flipping it. Too soft to place the clip |

Evidence frames (gridded, with pixel coordinates) are saved outside the repo in `~/T/_body_tour_evidence/`.

### The measurements

The clip's own size is the ruler: the RØDE MagClip GO is **35.1 x 19.7 mm**. The shoulder silhouette, about 51 cm for a man his size, is the cross-check.

| Frame | Neckline centre (px) | Clip centre (px) | Scale | Clip below neckline | Clip right of centre |
|---|---|---|---|---|---|
| CK_Assassination.mp4, 29.5 s (1920 x 1080) | (1016, 516) | (902, 580) | clip length 59 px gives 0.060 cm/px; shoulders 772 px give 0.066 cm/px | 64 px = **4.0 to 4.6 cm** (the higher figure allows for his forward lean) | 114 px = **7.1 cm** |
| Bednarz composite, 88 s, left panel (3240 x 2160) | (746, 676) | (681, 738) | clip length 48 px gives 0.073 cm/px; shoulders 658 px give 0.078 cm/px | 62 px = **4.7 cm** | 65 px = **4.9 cm** (his torso is turned slightly) |

The "FREEDOM" print sits about 11 to 12 cm below the neckline in both frames. The clip sits well above it, close to the collar. Taken together: about **4.5 to 5 cm below the neckline and 5 to 7 cm right of center**. The two frames are about a minute apart and agree, so the clip did not slide down during the event.

What the video cannot settle: exactly where the 44 x 45 mm housing sat behind the 35 x 20 mm clip. The housing could extend up to about 2 cm beyond the clip in any direction. The diagram centres it on the clip.

## The angles

### The State's bullet path

* **Sworn record:** prelim Day 4 (July 9, 2026), a State crime-scene sergeant: about 415 ft from perch to tent, 410 ft measured flat, a drop of about 68 ft. That gives arctan(68 / 410), about **9.4 degrees** ([The Angle Is Wrong](/scorecard/Not_A_Rifle_Wound/Wrong_Angle)).
* **Supplied research text** (below): about **6 degrees**, range about 4 to 10, using about 430 ft and about 46 ft. With 60 ft of drop it gives about 8 degrees.
* **Prosecutors' words:** "front to back, slightly left to right, and downward" (State's bindover brief, page 2, outside the quotation marks; not the examiner's words).
* **Drawn:** the path at 9 degrees; a shaded fan from 4 to 10 degrees; a thin line at 6. The entry is low on the front-left of the neck, between the voice box and windpipe ([Wound Trajectory and Angle](/Gun_Bullet/Wound_Trajectory_Angle)). From there, every angle in the range meets the spine at about C6 and C7.
* **The C4 to C5 entry claim** in the supplied text ("a detailed forensic/ballistics analysis", unnamed): if the entry were that high, a downward path would meet the spine at about C5, still about 5 cm (2 in) below C2. spine.html now says this.

### The line from the transmitter to the wound

* From the measured transmitter spot to the entry: about 14 cm (5.5 in), rising about 45 degrees and leaning about 40 degrees toward his left. Drawn as a straight line (`fx.jet` in stage.js).
* For comparison, from the nipple-level placement used in the first update of 2026-10-13: about 26 cm (10 in) at about 59 degrees. That version was replaced once the video measurement was in.

## Bryan's instructions (this research, 2026-10-13)

> Re-update things based on this. We want the angle to be correct.
>
> [first supplied text, below]
>
> There are videos we have of when the shot occurred. Have one where the video has as much of Charlie shown as right when he's shot, where we can see him all the way down to his waistline or his lap or whatever. We want to go through videos that are like that. I think we have videos.csv. I think we have pages.csv. You can go work on finding those.
>
> Even though the text below up here says it was right under the right nipple, I thought it was a little bit lower than that. Use the above information to initially update the files, as far as the HTML files in here, the visual, and all that. After you've done that and saved that off, go back to the videos. Try to find the highest resolution where the part of the frame from head to waist is generally the biggest percentage of the frame. Using it from the right when it happened and the start of the mic, you want to find as low as it had been.
>
> If we can find from the videos that it was far lower than the text above saying right under the right nipple, then we want to get that information. Update locations.md in this directory with all your research and all information I provided here so far and any prior prompts. We want to have this stuff documented.
>
> When you're done, update the diagrams again based on whatever you found, if you found it was lower than the information provided here from the videos and
>
> [second supplied text, below]

What was done, in that order:

1. Moved the transmitter to the right pectoral, near or just under the nipple, as the first supplied text describes. Added the 4 to 10 degree range for the bullet. Saved.
2. Searched the videos (above). Found the clip measurably **higher**: about 2 in below the neckline, not at or below the nipple.
3. Wrote this file.
4. Updated the diagrams again to the measured position, keeping the nipple-level accounts inside the dashed outline.

## Earlier instructions that shaped the Body Tour (same day)

* **Build request:** a contents page (`body_tour.html`, almost a menu of body parts) and one page per body part (neck, brain, heart, lungs, spine), each with a back button, the part name at top left, and two tabs: **"If Bullet"** and **"Shaped Charge Explosion"**. 3D views with a see-through mesh body and the important organs inside. Text appears as you scroll, with lines pointing at what each card talks about. A medical examiner explaining to a jury in plain terms, technically accurate.
* **Stance:** the State's brief is the prosecution's advocacy document, heavily one-sided; don't take it as the truth. The site's investigation concludes, close to conclusively, that it was a shaped charge explosion; don't discount or underweight it.
* **Charge geometry as first described:** a very small, powerful shaped charge blasting into his chest, "at a little bit of an angle across his body, across the torso, from his front right stomach area or below one pack, but probably across the body". The video now places it higher than that: upper right chest.
* **Bullet geometry as first described:** came in through the left neck, going back, "kind of horizontal to the ground, not down".
* **Buttons:** a third button, "Body Tour (3D)", on `/scorecard/overview` and `/scorecard/Not_A_Rifle_Wound/Side_To_Side`, after Exhibit 11 and the Analysis.
* **Upkeep:** the prompt `p_update_medical_diagrams.md` refreshes the tour or adds a body part; the menus come from `parts.js`.

## The research text Bryan supplied (as given, unedited)

This is a research summary pasted into the conversation. Its sources are mostly X posts, described rather than linked, and nothing in it has been checked against the original posts. It is **not** the site's position. In particular, the site's investigators conclude Charlie Kirk was killed by a charge at the microphone; where this text calls those posts unsupported, that is the text's own view. Naming the person who placed the microphone records where it was put, nothing more. Nothing indicates anyone on the security team, the AV crew or TPUSA staff knew of any device.

### Supplied text 1: where the transmitter sat

> **Upper right chest area (roughly the right pectoral region / near or under the right nipple), not down at the stomach.**
>
> Detailed analyses and X posts consistently place the bulkier RØDE Wireless PRO transmitter (the part under the shirt) on the **upper right chest**, creating a visible rectangular bulge under the white "FREEDOM" T-shirt. The MagClip GO magnetic clasp sat on the outside of the fabric; the transmitter housing (approx. 44 × 45.3 × 18.5 mm) was inside. This matches standard magnetic lavalier setups and pre-event footage of Kirk being mic'd.
>
> **Key quotes and descriptions from X/Twitter and related sources**
>
> * **Jon Bray** (detailed physical-evidence post on the RØDE Wireless PRO): "Before the event, multiple cameras captured a clearly visible rectangular bulge on the **upper right chest** — the 18.5mm-deep housing pushing the fabric outward, creating a deformation. The MagClip clasp is visible as a small dark rectangle on the shirt surface." After the event the bulge was gone while the clasp remained.
> * Another post: "Charlie Kirk was wearing a mic on his shirt (**black rectangle on his right upper tee shirt**) with a battery pack directly behind it."
> * Placement description: "Philip Goldsberry secured it under Charlie's shirt next to the necklace" (initial clipping; the bulk then sat lower/right of the collar area).
> * Observer notes on the right side: "more on his right side of his chest **near under his nipple**"; "marks under his **right nipple**"; "RODE Microphone that was placed on the **right side**"; "right side, under his nipple."
> * Broader references: "rectangular bulge on the upper chest area under his T-shirt"; "device fixed to Kirk's upper chest."
>
> These point to the transmitter sitting on the **right side of the chest**, roughly in the lower-to-mid right pectoral region (near or under the right nipple / lower right pec), lateral to the midline. It is **not** centered on the stomach, not low on the abdomen, and not "down toward his stomach." The visible bulge was higher—upper right chest rather than mid/lower abdomen.
>
> **Approximate position (best public approximations; no half-inch survey exists)**
>
> * **Horizontally**: Right of the sternum/centerline, on the right pec (roughly under or just below the right nipple area according to multiple observers looking at stills and video).
> * **Vertically**: Upper chest / right pectoral level—well above the center of the stomach (which would be lower abdomen). Descriptions cluster around "upper right chest," "right upper tee shirt," and "under the right nipple," not "stomach" or "abdomen."
> * The MagClip itself was the small external rectangle; the larger transmitter housing created the fabric deformation underneath.
>
> Mainstream reporting and fact-checks (e.g., AAP FactCheck and others) confirm the visible bulge was the magnetic microphone pack Kirk commonly used with his handheld mic, not a blood bag or other device. Conspiracy-oriented posts frequently discuss the same upper-right-chest bulge in the context of alternative theories, but the location descriptions align with the analyses above.
>
> No public source provides a precise half-inch measurement or proportional measurement from the nipple/pec bottom/stomach center. The consistent consensus from the most detailed posts is **upper right chest / right pectoral region (near under the right nipple)**.

### Supplied text 2: the bullet angle and the vessel hit

> **Approximately 6 degrees down from the horizontal (range of estimates roughly 4–10° depending on precise measurements).**
>
> Charlie Kirk was shot once in the neck on September 10, 2025, while speaking under a tent at Utah Valley University in Orem, Utah. The shot came from a prone position on the roof of the Losee Center (a multi-story student services/administration building), roughly 130–143 yards / ~430 feet horizontally away (New York Times cited ~430 feet; other reports ~130–142 yards / 130 m). Vertical elevation difference estimates for the rooftop relative to Kirk's seated position are typically in the ~45–60 ft range (consistent with a building of several stories on slightly higher ground; one early observer noted ~60 vertical feet).
>
> The depression angle from horizontal is θ = arctan(Δh / d). Using ~430 ft horizontal and ~46 ft vertical drop gives ~6.1°. Other calculations with ~60 ft vertical yield ~8°. Independent analyses and ballistics discussions commonly cite ~6° (with a range of about 4–8° or up to ~6–10°). The downward angle is shallow; at that distance with a scoped .30-06-class bolt-action rifle it is a straightforward shot once the elevation is accounted for (Rifleman's Rule reduces apparent bullet drop at an angle). Court-related materials and reconstructions confirm a clear line of sight with the shooter prone near the roof edge.
>
> **The left carotid artery (common carotid, in the anterior neck/zone where it branches), with damage on the left side of the neck.**
>
> Multiple eyewitness and reporter accounts (including Deseret News journalists present) describe the bullet striking the left side of Kirk's neck, with immediate heavy bleeding from that side (blood described as gushing/spurting onto his left shoulder/pec area). Field responders identified arterial neck hemorrhage consistent with the carotid ("it's a carotid artery, so you can't put a tourniquet on it"). Medical commentators, ER physicians, and medical examiners reviewing the available video and clinical presentation concluded the round hit the carotid artery and jugular vein territory, producing catastrophic hemorrhage plus neurological effects (including immediate decorticate posturing consistent with high cervical cord/brainstem disruption).
>
> A detailed forensic/ballistics analysis places the entry on the left lateral neck near the C4–C5 level, with catastrophic disruption of the left carotid artery and left jugular vein, bone contact, fragmentation, and no exit wound (fragment recovered at autopsy). Official public information confirms the cause of death as a gunshot wound to the neck (homicide); the full autopsy is part of court records but not released in detail for privacy reasons, so the precise named vessel and full trajectory path remain based on the combination of eyewitness, clinical, and reconstructive evidence rather than a single published ME narrative. Consensus across available sources is left-sided carotid (common carotid) injury rather than right side.
>
> **Relevant X/Twitter-style posts and details (as of recent searches):**
> Users have referenced a "downward ~6–9 degree trajectory to the lower left neck" and discussed the ballistics of a .30-06 at that angle/distance. Other posts note the left-side neck wound "where the main artery is," "carotid artery blown out," and left-sided bleeding. One example: discussion of a single .30-06 round to the lower left neck from under ~150 yards at a slight downward 6–9° angle. Broader posts simply reference the neck shot and arterial bleeding without finer anatomic precision. These align with the left-side carotid descriptions above; conspiracy-oriented posts exist but are not supported by the physical evidence (rooftop position, distance, audio, and wound location).
>
> In short: shallow ~6° downward shot from the Losee Center roof to the left side of the neck, disrupting the left carotid artery (and associated vessels). Official detailed public medical reports remain limited, so the above synthesizes contemporaneous reporting, eyewitness accounts, medical expert commentary, and available forensic analyses.

### How the supplied text was used

* **The vessel:** the left common carotid and left jugular veins match State's Exhibit 11 as quoted ("left common carotid and left internal and external jugular veins"). No change was needed.
* **The 6 degree angle:** added as the shaded 4 to 10 degree range beside the sworn 9 degrees. The sworn figure stays the drawn path, because it is the court record.
* **The C4 to C5 entry:** noted on spine.html. Even that high, the path meets the spine about 2 inches below C2.
* **"Under the right nipple":** shown as the bottom of the dashed outline, labelled "Some accounts: as low as the nipple". The measured position is drawn as the transmitter.

## Open questions

* **Release of the full report:** the sealed report's photographs would show the bulge and the clip directly, and any mark on the skin under them.
* **Raw camera files:** the uncompressed front-camera file would sharpen the clip measurement to within a few millimetres.
* **Other close angles:** any phone video taken from in front, close enough to see the shirt between the collar and the chest print, would cross-check the front camera.
