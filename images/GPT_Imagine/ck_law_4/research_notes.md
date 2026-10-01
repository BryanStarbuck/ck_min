# Research Notes: Prompting GPT Image 2.0 for Law 4 Blog Header

Date: 2026-05-15

## What the model is

* GPT Image 2 (also "gpt-image-2") — OpenAI's flagship image gen model, released April 2026
* Native Thinking Mode (reasons through composition before pixels)
* 95-99% text rendering accuracy reported
* Native 4K output, up to 16 reference images on edit endpoint
* Knowledge cutoff: December 2025

## Recommended prompt LENGTH and STRUCTURE

* Natural English prose, not keyword soup — "write like you're describing a scene to a person"
* Consistent order: **background/scene → subject → key details → constraints**
* Include the intended USE up front ("editorial blog header image", "infographic", "ad") — this sets the "mode" and polish level
* For complex multi-element briefs, use short labeled segments / line breaks instead of one giant paragraph
* Six core building blocks: (1) structure + goal, (2) specificity + quality cues, (3) composition, (4) people + action, (5) constraints, (6) text rendering

## Scene + style ordering

* Scene-first is the OpenAI cookbook recommendation
* Style descriptor goes near the top alongside intended use, then revisited at the end as a quality cue ("editorial illustration", "matte digital painting", "photorealistic")
* For photorealism, the literal word "photorealistic" or phrases like "real photograph", "taken on a real camera" engage the right mode
* For editorial / journalism work, descriptors that worked in examples: "editorial illustration", "documentary photojournalism aesthetic", "high-contrast ink illustration", "muted desaturated palette", "stark and conceptual", "newspaper editorial aesthetic"

## Composition — left vs right, two subjects

* GPT Image 2 understands "left", "right", "behind", "overlapping" significantly better than DALL-E 3 or gpt-image-1
* Be explicit: "frame left", "frame right", "upper third", "centered with negative space on left"
* Split-screen / split-frame compositions are a documented working pattern
* Thinking Mode handles spatial requirements before generating

## In-image TEXT rendering

* Put the exact words in **double quotes** in the prompt
* Use **ALL CAPS** in the prompt to signal the words you want literally rendered
* Specify typography: "bold sans-serif, white, centered, high contrast"
* Short text (1-5 words) yields near-perfect rendering; longer text degrades but is much better than DALL-E 3
* Spell tricky words letter-by-letter if needed
* Demand "verbatim rendering (no extra characters)"
* For our use case: "NSA", "CIA", "MOSSAD", "DIA", and the caption "TRUSTED INVESTIGATORS" are all well within reliable range

## Dashed lines / diagram elements

* GPT Image 2 handles dashed connectors well — documented examples include "warm-copper dashed arcs", "dotted lines showing process steps", "subtle dotted lines or clean minimal arrows"
* Describe them like you would in an editorial illustration: "thin dashed white lines arcing from X to Y"
* Keep them subtle relative to subjects so the eye reads composition first

## Camera / framing language

* "Close-up", "medium shot", "wide", "three-quarter view", "eye-level", "low-angle" all work
* Lens hints ("35mm lens", "shallow depth of field") work for photoreal modes; less useful for illustration modes
* For two-subject split-frame: specify each subject's facing direction (e.g., "facing slightly right toward center")

## Lighting / mood

* Concrete descriptors: "warm natural daylight", "cool blue indoor low-key", "high-contrast", "golden hour", "overcast", "muted desaturated palette"
* Mood words work: "somber", "investigative", "determined", "serious"

## Aspect ratio and resolution

* gpt-image-2 supports 1:1, 16:9, 9:16, and intermediate ratios
* Native HD landscape: 1536x1024 (3:2)
* gpt-image-2-vip 2K tier: long edge fixed at 2048px → true 16:9 at 2K = **2048x1152**
* Engine constraints: max edge <3840px, both edges multiple of 16, max ratio 3:1, total pixels 655,360–8,294,400
* For our blog header, recommend specifying "16:9 aspect ratio, 2048x1152 resolution" — falls within engine limits and is the reliability sweet spot

## FAILURE MODES / refusals

* **Real public figures**: GPT Image 2 has tighter restrictions than DALL-E 3 on depicting real people. Editorial / news-adjacent prompts naming real political figures are likely to be refused.
  * Mitigation: describe the man on frame left as an unnamed archetype (clean-cut American man, early thirties, dark suit, microphone). Do NOT use the name "Charlie Kirk" in the prompt.
  * Same for the investigator on frame right — unnamed archetype only.
* **Real organization seals/logos**: Refusal risk for actual CIA/NSA/Mossad seals or trademarked imagery. Render as stylized monolithic plaques with quoted block-letter text instead.
* **Violence / weapons / gore**: Tighter than DALL-E 3. Already excluded in our spec — good.
* **Identity preservation**: For edits, use `input_fidelity="high"`. Not applicable for our initial generation, but useful for follow-up edits.
* **Knowledge cutoff Dec 2025**: Anything post-cutoff (recent events, new faces) won't render accurately without reference images via edit endpoint.

## Caption / typography count

* Three-word caption "TRUSTED INVESTIGATORS" is two words actually — well within reliable range
* Four agency labels (NSA, CIA, MOSSAD, DIA) all 3-6 letters each — well within range
* No need to drop to two words

## Decisions for the final prompt

* Style: editorial illustration with photographic compositing, NYT op-ed page / political-thriller poster aesthetic
* Ratio / size: 16:9, 2048x1152
* Subjects: unnamed archetypes (no real names)
* Agency labels: stylized monolithic dark plaques with quoted ALL-CAPS white block letters
* Caption: black rectangular bar under frame-right subject, white sans-serif "TRUSTED INVESTIGATORS"
* Structure: scene-first paragraph → composition (left / center / right) → typography block → palette + lighting → style descriptor → exclusions

## Sources

* OpenAI Cookbook — GPT Image Generation Models Prompting Guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
* OpenAI Cookbook — gpt-image-1.5 Prompting Guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide
* fal.ai — GPT Image 2 Prompting Guide and Examples: https://fal.ai/learn/tools/prompting-gpt-image-2
* PixVerse — GPT Image 2 Review: Prompt Guide and Use Cases in 2026: https://pixverse.ai/en/blog/gpt-image-2-review-and-prompt-guide
* Atlabs AI — The Ultimate GPT Image 2 Prompting Guide: https://www.atlabs.ai/blog/the-ultimate-gpt-image-2-prompting-guide-how-to-use-openai%E2%80%99s-best-image-model-2026
* Imagine.art — GPT Image 2 Prompt Guide + 70 Prompts: https://www.imagine.art/blogs/gpt-image-2-prompt-guide
* i-scoop — Prompting gpt-image-2 like a pro: https://www.i-scoop.eu/prompting-gpt-image-2-like-a-pro-guide/
* GenAIntel — GPT Image 2 Best New Features With Examples: https://www.genaintel.com/guides/openai-gpt-image-2-release-guide
* Tenorshare — ChatGPT Images 2.0 Infographic Prompts Tested 2026: https://www.tenorshare.ai/ai-tips/chatgpt-images-2-infographics-prompt.html
* Handy AI — Model Drop: GPT Image 2 (failure modes / refusals): https://handyai.substack.com/p/model-drop-gpt-image-2
* Apiyi — GPT-Image-2-VIP Size Complete Guide (resolutions): https://help.apiyi.com/en/gpt-image-2-vip-size-resolution-complete-guide-en.html
* Framia — GPT Image 2 Resolution: Native 2K Image Generation: https://framia.pro/page/en-US/news/gpt-image-2-resolution
