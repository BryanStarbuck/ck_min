ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

LAW_DIR dir is {ROOT_DIR}/site/docs/laws/4_Trusted_Investigations

LAW_FILE is file {LAW_DIR}/Law_4_Trusted_Investigations.md

NOTES_FILE is file {LAW_DIR}/more/Notes_4_Trusted_Investigations.md

THIS_DIR dir is {ROOT_DIR}/images/GPT_Imagine/ck_law_4

OUTPUT_FILE is file {THIS_DIR}/gpt_imagine_prompt.txt

RESEARCH_NOTES_FILE is file {THIS_DIR}/research_notes.md

IMAGE_TITLE is the string "Charlie Kirk Gov File - Forced Disclosure Law #4 - Trusted Investigators"

IMAGE_USE is for blog posts and social media accompanying coverage of Law 4 (the Trusted Investigators Act) and the broader claim that an intelligence service was behind the Charlie Kirk assassination.

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
  * "GPT Image dashed connection lines diagram style prompt"

* Capture from the research:

  * The recommended prompt LENGTH (short vs long, token-style vs natural language).
  * The recommended prompt STRUCTURE (does GPT Image 2 prefer scene-first then style, or style-first then scene; how to handle multiple subjects; how to handle text rendering inside the image).
  * How to specify CAMERA / FRAMING terms (lens, focal length, angle, left/right composition) effectively.
  * How to specify LIGHTING and MOOD effectively.
  * How GPT Image 2 handles in-image typography (rendered words like "NSA", "CIA", caption boxes).
  * How GPT Image 2 handles symbolic / graphic-overlay elements like dashed lines, arrows, agency seals.
  * Any documented FAILURE modes (e.g. avoid certain words, model refuses certain framings, text gets garbled past N words, faces of public figures get refused).
  * Aspect ratio guidance and resolution guidance for blog-header use (typically 16:9 or 1792x1024).

* Write a short summary of findings to {RESEARCH_NOTES_FILE}. Keep it under 80 lines. Cite source URLs.


==================== STAGE 3: Read Context ====================

* Read {LAW_FILE} (it is the actual text of Law 4 — long file, skim the Purpose, Section 1 Definitions, and Section 0 Findings for the named entities and stated rationale).

* Read {NOTES_FILE} for the strategic framing of the law.

* Read Appendix A below in this prompt file. Appendix A is the source of truth for what must appear in the image.


==================== STAGE 4: Handle Public Figures and Defamation ====================

* GPT Image 2 will likely REFUSE to render a recognizable likeness of Charlie Kirk as a real, identifiable person. Plan for this.

  * Default approach: describe the man on frame left as "a clean-cut American man in his early thirties, dark hair, light skin, wearing a dark suit and white shirt, holding a microphone, mid-speech at an outdoor university event" without naming him.

  * The viewer recognizes him from context (UVU courtyard background, suit + microphone, the blog post text). The image itself does not need to claim a likeness.

* Same approach for the investigator on frame right — describe an archetype, not a specific named person. Example: "a serious-looking American investigative journalist in his forties, wearing a dark blazer, studying documents".

* For agency labels (NSA, CIA, etc.) — these are organizations, not people. Render them as labeled badges / monolithic logo-like blocks (do NOT attempt the real seals — describe stylized stand-in graphics that read "NSA", "CIA", etc., in flat editorial style). This avoids trademark issues and works better with GPT Image 2's text rendering.

* The black box caption under the investigator should contain placeholder text the prompt explicitly specifies, OR be left empty and added later in post. Recommend specifying short text the model can actually render (3 to 5 words max — GPT Image 2 still struggles past that).


==================== STAGE 5: Craft the Prompt ====================

* Combine the research findings from Stage 2 with the visual goals from Appendix A.

* The prompt should be one continuous block of natural English, hyper-detailed, in the order that the Stage 2 research determined works best for GPT Image 2.

* The prompt MUST cover:

  * Overall scene + composition (two-subject split: frame left vs frame right)
  * Frame left subject + frame left background (UVU campus courtyard view)
  * Frame right subject + frame right background (intelligence service assassination investigation imagery — evidence boards, redacted documents, surveillance photos, map pins)
  * The intelligence agency badges / blocks (NSA, CIA, Mossad, and any others from Appendix A) on the frame-left or center area
  * Dashed connection lines flowing from those agency badges across the frame to the investigator on frame right
  * The black caption bar with white text under the investigator (specify the exact text it should render)
  * Color palette, lighting, mood
  * Art style (editorial illustration / photo-realistic composite / political thriller poster — pick the one Stage 2 research says GPT Image 2 executes best for this kind of subject)
  * Aspect ratio and resolution
  * Negative instructions (what should NOT appear — e.g. no real political figures, no gore, no weapons, no logos of real news organizations)

* Hyper-detail rule: every visual element in Appendix A must be named in the prompt. If you cannot name it, ask the user before writing the prompt.

* Save the finished prompt to {OUTPUT_FILE}.


==================== STAGE 6: Self-Review ====================

* Re-read {OUTPUT_FILE} against Appendix A.

* For each bullet in Appendix A, confirm the prompt contains a corresponding instruction.

* If any bullet is missing, add it and resave.

* Output to stdout a short summary in this format:

    ============================================================
    GPT Image 2.0 prompt for Law 4 image is ready.
    File: {OUTPUT_FILE}
    Research notes: {RESEARCH_NOTES_FILE}
    Appendix A coverage: N of N bullets covered
    ============================================================


==================== Appendix A: Visual Goals ====================

* Title / topic of the image: "Charlie Kirk Gov File - Forced Disclosure Law #4 - Trusted Investigators". The image illustrates the thesis that an intelligence service was behind Charlie Kirk's assassination, and that Law 4 (the Trusted Investigators Act) is the mechanism to expose it.

* Use case: blog post header image and social media share image. Editorial / investigative-journalism tone. Serious, not gory, not cartoonish.

* Aspect ratio: 16:9 landscape (blog header). Resolution: highest GPT Image 2.0 supports for that ratio (typically 1792x1024).

* Composition: two-subject split frame.

  * Frame LEFT: a clean-cut American man in his early thirties, dark hair, dark suit, white shirt, holding a black handheld microphone, mid-speech, three-quarter view facing slightly right. He is the speaker / victim figure. Do not name him in the prompt.

  * Frame RIGHT: a serious investigator figure, American man in his forties, dark blazer, holding or examining documents / photographs, intent expression, three-quarter view facing slightly left. He represents one of the Trusted Investigators named in Law 4.

* Background behind frame LEFT subject: the Utah Valley University (UVU) campus courtyard view — open paved plaza, modern university buildings, scattered students walking, daytime, clear sky, suggestive of an outdoor tabling event. Do not depict the shooting itself, do not depict any wound, do not depict the killer.

* Background behind frame RIGHT subject: an intelligence-service assassination investigation workspace — wall of pinned photographs, redacted documents with black bars, surveillance images, a map with red pins, a corkboard with red string connecting items, an open laptop showing a flight path or radar trail. Dim, cool-toned, indoor lighting.

* Center / overhead: stylized monolithic agency badges representing intelligence services, arranged in a horizontal row in the upper third of the frame. Each badge is a flat, editorial-style rectangular plaque with white block-letter text on a dark background reading exactly:

  * "NSA"
  * "CIA"
  * "MOSSAD"
  * "DIA"
  * (Stage 2 research will tell you the maximum number of distinct in-image labels GPT Image 2 can render cleanly. Cap at four. Pick the four most important from this list in this order: NSA, CIA, MOSSAD, DIA.)

* Connection lines: from each agency badge, a dashed white line travels across the frame and converges on the investigator on frame right, suggesting that the investigator is the one tracing and exposing the agencies' role. The dashed lines should be clearly visible against the background but not so bold they overwhelm the subjects. Lines should NOT touch or originate from the man on frame left — he is the subject of the investigation, not the investigator.

* Caption bar: a solid black horizontal rectangle positioned directly below the investigator on frame right (NOT spanning the full image — only under the investigator). Inside, white sans-serif block text reads exactly: "TRUSTED INVESTIGATORS". Three words max so GPT Image 2 can render it cleanly. (If Stage 2 research shows GPT Image 2 cannot reliably render three words, drop to two: "INVESTIGATOR" — and note the change in {RESEARCH_NOTES_FILE}.)

* Lighting and color palette:

  * Frame left: warm, natural daylight, slightly desaturated, conveying an outdoor public event.
  * Frame right: cool, blue-tinted, low-key indoor lighting, conveying investigative workspace.
  * Center agency badges: neutral, flat, high-contrast white-on-black or white-on-dark-navy.
  * Overall palette: muted with red accents on the map pins and corkboard string. Avoid any palette that reads as celebratory or upbeat.

* Mood: serious, investigative, somber but determined. Style of New York Times opinion-section illustration or political-thriller film poster, NOT cartoon, NOT meme, NOT photorealistic news photo.

* Art style: editorial illustration / matte digital painting with photographic textures. Pick the exact style descriptor in Stage 5 based on Stage 2 research findings — choose the descriptor GPT Image 2 executes most reliably for editorial-investigative compositions.

* Negative / exclusions: do NOT include:

  * Recognizable likenesses or names of any real living person (Charlie Kirk, Candace Owens, Tucker Carlson, etc.)
  * Real government seals or trademarked logos
  * Logos of real news organizations
  * Weapons, blood, gore, or depiction of violence
  * Any visible date, year, or other text beyond the in-image elements specified above
  * Cartoonish / chibi / anime styling
  * Any text Watermark
