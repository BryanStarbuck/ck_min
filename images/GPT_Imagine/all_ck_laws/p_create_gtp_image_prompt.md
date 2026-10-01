ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

LAWS_DIR dir is {ROOT_DIR}/laws

LAW_1_DIR dir is {LAWS_DIR}/1_DoJ_FBI
LAW_2_DIR dir is {LAWS_DIR}/2_US_Intel
LAW_3_DIR dir is {LAWS_DIR}/3_Require_to_Investigate
LAW_4_DIR dir is {LAWS_DIR}/4_Trusted_Investigations

LAWS_README is file {LAWS_DIR}/README.md

THIS_DIR dir is {ROOT_DIR}/images/GPT_Imagine/all_ck_laws

OUTPUT_FILE is file {THIS_DIR}/gpt_imagine_prompt.txt

RESEARCH_NOTES_FILE is file {THIS_DIR}/research_notes.md

IMAGE_TITLE is the string "Charlie Kirk Gov File - Four Forced Disclosure Laws"

IMAGE_USE is for blog posts and social media accompanying coverage of all four proposed federal laws (Law 1 FBI & DOJ Disclosure, Law 2 Intelligence Disclosure, Law 3 Mandate the Investigation, Law 4 Trusted Investigators) and the broader claim that intelligence services were behind the Charlie Kirk assassination and that these four laws together are the path to forced disclosure.

TARGET_GEN_AI is GPT Image 2.0 (OpenAI's image generation model, also referred to as "gpt-image-2", successor to gpt-image-1 / DALL-E line). When you see "Imagine" in the title, that refers to the same OpenAI image gen system.


==================== STAGE 1: Goal ====================

* Produce a single, hyper-detailed text prompt that, when pasted into GPT Image 2.0, will reliably produce a high-quality editorial / blog-header style image matching the visuals described in Appendix A.

* The final prompt text must be written in the exact prompt style and structure that OpenAI's GPT Image 2.0 responds to best. That is what the web research stage is for.

* Save the final prompt to {OUTPUT_FILE} as plain text — nothing else in that file but the prompt itself, ready to copy-paste into ChatGPT or the OpenAI image API.


==================== STAGE 2: Web Research ====================

* Run a Google web search (use WebSearch tool) on each of the queries below. For each query, read the top 3 to 5 results using WebFetch.

  * "GPT Image 2 prompt guide best practices"
  * "gpt-image-2 prompting tips OpenAI"
  * "OpenAI image generation prompt structure 2026"
  * "GPT Image 2 vs DALL-E 3 prompting differences"
  * "OpenAI gpt-image-1 prompt engineering style examples"
  * "GPT Image text rendering in image quality tips"
  * "GPT Image composition framing left right two subjects"
  * "GPT Image editorial illustration journalism style prompt"
  * "GPT Image rendering cartoon character mixed with photorealistic background"
  * "GPT Image Schoolhouse Rock I'm Just a Bill style cartoon prompt"
  * "GPT Image rendering US Capitol Building architecture prompt"

* Capture from the research:

  * The recommended prompt LENGTH (short vs long, token-style vs natural language).
  * The recommended prompt STRUCTURE (does GPT Image 2 prefer scene-first then style, or style-first then scene; how to handle multiple subjects; how to handle text rendering inside the image).
  * How to specify CAMERA / FRAMING terms (lens, focal length, angle, left/right composition, low-angle stair view) effectively.
  * How to specify LIGHTING and MOOD effectively.
  * How GPT Image 2 handles in-image typography (rendered words like "FBI", "CIA", "NSA", agency labels, bill titles).
  * How GPT Image 2 handles mixing a 1970s/1980s Saturday-morning cartoon character (Schoolhouse Rock "I'm Just a Bill" style — anthropomorphic rolled-up parchment scroll with arms, legs, eyes, sash) into an otherwise editorial / photorealistic composition.
  * Any documented FAILURE modes (e.g. avoid certain words, model refuses certain framings, text gets garbled past N words, faces of public figures get refused).
  * Aspect ratio guidance and resolution guidance for blog-header use (typically 16:9 or 1792x1024).

* Write a short summary of findings to {RESEARCH_NOTES_FILE}. Keep it under 80 lines. Cite source URLs.


==================== STAGE 3: Read Context ====================

* Skim each of the four law directories ({LAW_1_DIR}, {LAW_2_DIR}, {LAW_3_DIR}, {LAW_4_DIR}) for the short titles and one-line purpose of each law. Read {LAWS_README} for the strategic framing across all four laws.

* The four short titles to use are (4 words or less, as defined in the project CLAUDE.md):

  1. FBI & DOJ Disclosure
  2. Intelligence Disclosure
  3. Mandate the Investigation
  4. Trusted Investigators

* Read Appendix A below in this prompt file. Appendix A is the source of truth for what must appear in the image.


==================== STAGE 4: Handle Public Figures and Defamation ====================

* GPT Image 2 will likely REFUSE to render a recognizable likeness of Charlie Kirk as a real, identifiable person. Plan for this.

  * Default approach: describe the man on frame left as "a clean-cut American man in his early thirties, dark hair, light skin, wearing a dark suit and white shirt, holding a microphone, mid-speech at an outdoor university event" without naming him.

  * The viewer recognizes him from context (UVU courtyard background, suit + microphone, the blog post text). The image itself does not need to claim a likeness.

* For agency labels (FBI, CIA, NSA) — these are organizations, not people. Render them as labeled rectangular badges / blocks in the bottom-right corner of the frame (do NOT attempt the real seals — describe stylized stand-in graphics that read "FBI", "CIA", "NSA", in flat editorial style with white block-letter text on a dark fill). This avoids trademark issues and works better with GPT Image 2's text rendering.

* The four-law scroll labels need to be short enough for GPT Image 2 to render legibly (3 words max per scroll). Use the short titles listed in Stage 3.


==================== STAGE 5: Craft the Prompt ====================

* Combine the research findings from Stage 2 with the visual goals from Appendix A.

* The prompt should be one continuous block of natural English, hyper-detailed, in the order that the Stage 2 research determined works best for GPT Image 2.

* The prompt MUST cover:

  * Overall scene + composition (two-subject split frame: Charlie Kirk archetype on left, "I'm Just a Bill" cartoon character on right)
  * Frame left subject + frame left background (Charlie Kirk archetype with UVU campus courtyard behind him)
  * Frame right subject + frame right background (the Schoolhouse Rock "I'm Just a Bill" anthropomorphic scroll character with microphone, standing on the US Capitol Building's front steps, with the Capitol Building visible in the top third of the right side of the frame, camera zoomed in on the steps from a low angle)
  * The four labeled bills / scrolls representing the four laws — described so the viewer reads "four laws" at a glance (e.g. four small scrolls stacked or arranged around the Bill character, or the Bill character himself depicted as one of a quartet of identical bill characters lined up on the steps, each sash labeled with one of the four short law titles)
  * The three intelligence-agency / law-enforcement badges in the bottom-right corner of the frame: flat rectangular blocks with white sans-serif block-letter text reading exactly "FBI", "CIA", "NSA" — each on its own dark plaque
  * Color palette, lighting, mood
  * Art style (mixed-media: photorealistic / editorial backgrounds for the UVU campus and the Capitol exterior, combined with a clearly cartoon Schoolhouse Rock-style anthropomorphic scroll character on the right — pick the exact descriptor Stage 2 research says GPT Image 2 executes best for this mixed style)
  * Aspect ratio and resolution
  * Negative instructions (what should NOT appear — e.g. no real political figures, no gore, no weapons, no real government seals, no logos of real news organizations, no anime / chibi styling, no watermarks)

* Hyper-detail rule: every visual element in Appendix A must be named in the prompt. If you cannot name it, ask the user before writing the prompt.

* Save the finished prompt to {OUTPUT_FILE}.


==================== STAGE 6: Self-Review ====================

* Re-read {OUTPUT_FILE} against Appendix A.

* For each bullet in Appendix A, confirm the prompt contains a corresponding instruction.

* If any bullet is missing, add it and resave.

* Output to stdout a short summary in this format:

    ============================================================
    GPT Image 2.0 prompt for Four Laws image is ready.
    File: {OUTPUT_FILE}
    Research notes: {RESEARCH_NOTES_FILE}
    Appendix A coverage: N of N bullets covered
    ============================================================


==================== Appendix A: Visual Goals ====================

* Title / topic of the image: "Charlie Kirk Gov File - Four Forced Disclosure Laws". The image illustrates the thesis that intelligence services were behind the Charlie Kirk assassination, and that four proposed federal laws — taken together — are the mechanism that forces disclosure, mandates the investigation, and installs trusted investigators.

* Use case: blog post header image and social media share image. Editorial / investigative-journalism tone, with one intentional Saturday-morning-cartoon element (the "I'm Just a Bill" character) to evoke the civics-class memory of how a bill becomes a law. Serious but not gory, not pure cartoon.

* Aspect ratio: 16:9 landscape (blog header). Resolution: highest GPT Image 2.0 supports for that ratio (typically 1792x1024).

* Composition: two-subject split frame.

  * Frame LEFT: a clean-cut American man in his early thirties, dark hair, dark suit, white shirt, holding a black handheld microphone, mid-speech, three-quarter view facing slightly right. He is the speaker / victim figure (Charlie Kirk archetype). Do not name him in the prompt.

  * Frame RIGHT: a 1970s/1980s Schoolhouse Rock "I'm Just a Bill" style cartoon character. He is an anthropomorphic rolled-up parchment scroll: a vertical cylindrical rolled scroll forming the body, with cartoon arms and legs, a friendly cartoon face on the upper part of the scroll, a red sash diagonally across his "chest", and a small black handheld microphone in one hand as if he is talking to camera. He stands centered on the US Capitol Building's front marble steps. Classic Saturday-morning-cartoon 2D flat illustration style, clearly distinct from the photorealistic background.

* Background behind frame LEFT subject: the Utah Valley University (UVU) campus courtyard view — open paved plaza, modern university buildings, scattered students walking, daytime, clear sky, suggestive of an outdoor tabling event. Do not depict the shooting itself, do not depict any wound, do not depict the killer.

* Background behind frame RIGHT subject: the US Capitol Building exterior, viewed from a low angle on the front marble steps. The camera is zoomed in on the steps so the steps fill most of the right half of the frame, with the Bill cartoon character standing on those steps. Enough of the Capitol Building (the white facade, columns, and dome base) is visible in the top third of the frame to make the location unmistakable, but the Capitol does not dominate the frame — the steps and the cartoon character do.

* Four laws element: somewhere in the frame, the four laws must be readable at a glance. Pick whichever of these two layouts the Stage 2 research suggests GPT Image 2 will execute most cleanly:

  Option A (preferred): four small rolled-scroll "bill" props arranged on or around the Capitol steps near the Bill character — each scroll has a short label band reading one of the four short titles ("FBI & DOJ Disclosure", "Intelligence Disclosure", "Mandate the Investigation", "Trusted Investigators"). Three words max per visible label so GPT Image 2 renders text legibly — abbreviate if needed (e.g. "DOJ DISCLOSURE", "INTEL DISCLOSURE", "MANDATE INVESTIGATE", "TRUSTED INVESTIGATORS").

  Option B: four identical Schoolhouse Rock "I'm Just a Bill" characters standing in a row across the Capitol steps, each with a sash labeled with one of the four short titles. Only one of them holds the microphone.

  Pick one layout in Stage 5. Document the choice in {RESEARCH_NOTES_FILE}.

* Agency badges (FBI, CIA, NSA): three flat rectangular plaques stacked or arranged in a tight cluster in the BOTTOM-RIGHT corner of the frame. Each plaque has a solid dark background (near-black or very dark navy) with white sans-serif block-letter text reading exactly:

  * "FBI"
  * "CIA"
  * "NSA"

  These plaques are clearly inside the frame composition (overlaid on the lower-right area), not floating off the edge, and they do not obscure the Bill cartoon character.

* Lighting and color palette:

  * Frame left: warm, natural daylight, slightly desaturated, conveying an outdoor public event.
  * Frame right: clean midday daylight on the Capitol steps (white marble takes a slight cool cast), with the cartoon character rendered in bright Saturday-morning-cartoon colors (cream-yellow parchment body, red sash, classic black-line cartoon outlines) so he visually pops against the realistic background.
  * Agency badges (bottom right): high-contrast white-on-dark, flat editorial design.
  * Overall palette: muted realistic tones for backgrounds, with the cartoon character providing a single saturated focal accent on the right. Avoid any palette that reads as celebratory or upbeat.

* Mood: serious, investigative, somber but determined — with the cartoon Bill character providing a deliberate civics-class flavor (referencing how the law becomes a law). Style of New York Times opinion-section illustration or political-thriller film poster, with a clearly inserted retro 2D cartoon element on the right. NOT meme, NOT photorealistic news photo, NOT fully cartoon.

* Art style: editorial illustration / matte digital painting with photographic textures for the human figure and both backgrounds, combined with a flat 2D 1970s Saturday-morning cartoon style for the Bill character. The two styles are intentionally juxtaposed. Pick the exact style descriptor in Stage 5 based on Stage 2 research findings — choose the descriptors GPT Image 2 executes most reliably for mixed editorial / retro-cartoon compositions.

* Negative / exclusions: do NOT include:

  * Recognizable likenesses or names of any real living person (Charlie Kirk, Candace Owens, Tucker Carlson, etc.)
  * Real government seals or trademarked logos
  * Logos of real news organizations
  * Weapons, blood, gore, or depiction of violence
  * Any visible date, year, or other text beyond the in-image elements specified above
  * Anime / chibi styling for the cartoon character — it must be specifically 1970s/1980s American Saturday-morning Schoolhouse Rock style
  * Any text watermark
