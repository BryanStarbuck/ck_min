findings_for_hierarchy.md — VIDEO PIPELINE FINDINGS

Written by videos_planning/p_update_video_hierarchy.md, run 2026-07-23.
This is the human work list. Everything here is something a person has to
decide or do; nothing in it is fixed by re-running the pipeline.

==========================================================================
1. THE CENSUS IN THE PROMPT IS WRONG BY 8x — READ THIS FIRST
==========================================================================

p_update_video_hierarchy.md's KNOWLEDGE section says the corpus is 'on the
order of 55-65 video entries' and warns that 'if the rebuilt YAML has
hundreds of video entries, something is wrong'. It is 400, and nothing is
wrong. The census counted the repo corpus and skipped the mirror.

  ~/_Mirror/Politics/Charlie_Kirk_Mi   325 video files, 20.3 GB, across 71
                                       concept-filed directories
  ALL 325 are fully processed: 325 .transcription, 322 .ai_description,
  325 .ocr. Not one is missing a sidecar.

The mirror is the LARGEST and BEST-DOCUMENTED part of the video corpus, and
its directory names are years of hand filing by concept — the strongest
clustering signal this pipeline has. The prompt's own Stage 2 lists it as
source 5, so it was included. Update the census section of the prompt so the
next run does not treat 400 entries as a bug.

Other census corrections measured on disk:
  * videos/ holds 49 .mp4, not 46.
  * 4 disk files have no manifest record, not 1: 2026310419405504514.mp4,
    2038934507307343872.mp4, _QwGo0LyZ3I.mp4, kirk-parents-hearing-3006.mp4.
  * The 18 manifest-records-with-no-disk-file figure is exactly right.

==========================================================================
2. videos/manifest.yaml WAS NOT VALID YAML — FIXED
==========================================================================

Line 402 read:
    description: 'Erika Kirk takes the torch after Charlie's assassination'
An apostrophe inside a single-quoted YAML scalar must be doubled. The file
would not parse at all, so no stage that reads the manifest could run. It is
now:
    description: 'Erika Kirk takes the torch after Charlie''s assassination'
This is the only edit this run made outside videos.yaml and this directory.
Whatever writes manifest.yaml (the /ck_add_text skill) should quote-escape.

==========================================================================
3. THE .ocr FORMAT, RECORDED (Stage 1 asked for this)
==========================================================================

An .ocr sidecar is a YAML document, NOT bare text. Keys observed on all 327:
  source, status, engine, level, generated, kind, language, stride_seconds,
  frames_sampled, truncated, text, blocks
`text` is a block scalar holding every sampled frame's glyphs concatenated.
`blocks` is a list of {text, confidence, start, end} with per-frame timing —
so OCR carries TIMESTAMPS, which the prompt did not know. For a screen-
recorded post, blocks[].start/end is a second source of timing alongside the
ai_description shot list. Worth harvesting on a later pass.

Two ai_description formats also differ from the prompt's description:
  * The twelve ## sections are NOT always in the documented order.
    Parse by header name, never by position.
  * Some sidecars open with a preamble line before ## Overview
    ('Certainly! Here is a hyper-detailed factual description...').
    A parser that takes everything before the first ## as the overview gets
    the preamble instead.
  * Shot-list bullets use both '* **00:00 - 00:10**' and '- **00:00**:'.

==========================================================================
4. TRANSCRIPTION WORK LIST — 34 videos with no transcription of any kind
==========================================================================

Neither the video nor an audio sibling has a .transcription. Until these are
run through Large File Bridge they cannot be clustered or placed on evidence,
and this run placed them structurally or not at all.

  * 1965869689755812061                                                none
  * 1965871960702828885                                                none
  * 1965884012565766172                                                none
  * 1965890646746513821                                                none
  * 1965892000185725129                                                none
  * 1965913654840406034                                                none
  * 1966235480732873149                                                none
  * 1966293765158560167                                                none
  * 1969832388823003519                                                none
  * 2026310419405504514.mp4                                            video
  * 2038934507307343872.mp4                                            video
  * 2069185145555255370_source                                         none
  * 2075691199575265757                                                none
  * 2076465128329846991                                                none
  * 2079560806690324910.mp4                                            video
  * 2079684519762993659.mp4                                            video
  * kirk-parents-hearing-3006.mp4                                      video
  * site/QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R                none
  * yt/0pvEGO4W85k                                                     none
  * yt/0ykbt_WGOZE                                                     none
  * yt/1RbDMiEReys                                                     none
  * yt/1xTpQ9RHkvk                                                     none
  * yt/2exo7iJ-qdc                                                     none
  * yt/8HkNMTNHsa8                                                     none
  * yt/J2DKRfwSt94                                                     none
  * yt/PLnZT7Gz_VSN520UilgmZqikvi3n1MsuZR                              none
  * yt/PLuXXbBFpPc0lhc6PfJae8Rav-gMNpmeuL                              none
  * yt/X8UKjN5cjvw                                                     none
  * yt/ccRNaLGavf8                                                     none
  * yt/qpGPZHdil1E                                                     none
  * yt/v6yrnyo                                                         none
  * yt/v705uyi                                                         none
  * yt/w-ng95XlQb4                                                     none
  * yt/wcD2khO3rOA                                                     none

PARTIAL TRANSCRIPTS — 38 videos. The ASR stopped before the end of the media
(the header's '✓ full' marker is absent), so transcript_complete is false.
These are the dangerous ones: a page written from one of them confidently
describes a video it only heard part of. Re-run them.

  * 2046416264562921472.mp3
  * 2070615710003589174.mp4
  * 2071072788132118610.mp4
  * 2077277163053564059.mp4
  * 2077951056697331723.mp4
  * 2077994177216827578_1.mp4
  * AES_Interview.mp4
  * AES_Interview_compressed.mp4
  * Blue_Side.mp4
  * Candace Owens - 🚨BREAKING NEWS!🚨 On September 10th, after Charlie’s assasi
  * Damin Toell - oh no [2036081362869030912].mp4
  * Darth Powell - If you think Charlie Kirk was shot with a 30-06  You're a f
  * Diligent Denizen 🇺🇸 - ‼️🇺🇸： Google Trend searches for TYLER JAMES ROBINSON
  * Drone_Shot_South.mp4
  * French Legionaire.mp4
  * Funneral.mp4
  * HustleBitch - 🚨 THEY WERE MUCH CLOSER THAN YOU THINK - WATCH AND PAY ATTEN
  * Jason Cain - I believe I have found the #CharlieKirk #Sniper shooting loca
  * Jason Cain - I believe I have found the #CharlieKirk #Sniper shooting loca
  * MJTruthUltra - UPDATE： Charlie Kirk  Candace Owens latest finding about th
  * MJTruthUltra - UPDATE： Charlie Kirk  Candace Owens latest finding about th
  * Marissa - Absolute proof he was not shot! [2075401619152539648].mp4
  * Mr Commonsense - @shaunmmaguire Newly Discovered Crowd Video Of A Man CELE
  * Muppet Masher - It comes from under his shirt. I don't know what else to s
  * Project Constitution - 🚨ALERT： BREAKING Down The MYSTERY FLIGHT BEFORE CHA
  * Project Constitution - 🚨Breaking： Newly Uncovered Footage Appears to Show 
  * RAW_CIA_Drones.mp4
  * SU_BBT.mp4
  * Shaun Maguire - Of all the videos of people celebrating the assassination 
  * South_Side.mp4
  * South_Side_Stairs.mp4
  * Tyler_Running.mp4
  * US_did_ 911 - @jonaaronbray Okay, the official narrative is BS. That has b
  * YREFY Laine Schoneberger.mp4
  * _MvCUbhcVsUi8L9G [_MvCUbhcVsUi8L9G].mp4
  * https%3A%2F%2Fx.com%2FProjectConstitu%2Fstatus%2F1999947478901088281.mp4
  * roofshooter3.ia.mp4
  * roofshooter3.mp4

NO AI DESCRIPTION — 44 videos.

  * 1965869689755812061
  * 1965871960702828885
  * 1965884012565766172
  * 1965890646746513821
  * 1965892000185725129
  * 1965913654840406034
  * 1966235480732873149
  * 1966293765158560167
  * 1969832388823003519
  * 2026310419405504514.mp4
  * 2038934507307343872.mp4
  * 2046414464447287296.mp3
  * 2046416264562921472.mp3
  * 2046416264567140352.mp3
  * 2068463186668605858.mp3
  * 2069185145555255370.mp3
  * 2069185145555255370_source
  * 2071736376215920842_extracted.mp3
  * 2072814926133866634.mp3
  * 2075691199575265757
  * 2076465128329846991
  * 2079560806690324910.mp4
  * 2079684519762993659.mp4
  * Project Constitution - 🚨 BREAKING： UNDENIABLE PROOF OF MULTIPLE SHOOTERS I
  * Teacher_Lounge_Shooter.mp4
  * Yes, Still MORE DISTURBING Searches from before Charlie Kirk Passed [tA7GE
  * kirk-parents-hearing-3006.mp4
  * site/QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R
  * yt/0pvEGO4W85k
  * yt/0ykbt_WGOZE
  * yt/1RbDMiEReys
  * yt/1xTpQ9RHkvk
  * yt/2exo7iJ-qdc
  * yt/8HkNMTNHsa8
  * yt/J2DKRfwSt94
  * yt/PLnZT7Gz_VSN520UilgmZqikvi3n1MsuZR
  * yt/PLuXXbBFpPc0lhc6PfJae8Rav-gMNpmeuL
  * yt/X8UKjN5cjvw
  * yt/ccRNaLGavf8
  * yt/qpGPZHdil1E
  * yt/v6yrnyo
  * yt/v705uyi
  * yt/w-ng95XlQb4
  * yt/wcD2khO3rOA
==========================================================================
5. IPFS: 337 of 395 CIDs ARE NOT PINNED — EVERY ONE PUBLISHES AS A DEAD PLAYER
==========================================================================

This is the single biggest obstacle to publishing the video hierarchy at all.
The site plays video from public IPFS gateways; an unpinned CID is served by
no gateway. It plays perfectly on this machine because the local node has the
blocks, and an IPFS Companion browser extension will make it look fine here
too — and it is dead for every visitor.

  pinned:      58  (essentially just the videos/ corpus from manifest.yaml)
  NOT pinned:  337  (essentially the entire mirror)

NOTHING WAS PINNED BY THIS RUN, deliberately. Pinning announces content to
the public IPFS network and is irreversible in practice. Pinning the mirror
would publish 20 GB of material that has never been reviewed for what it
contains — bystander faces, uninvolved voices, private captures. That review
is the prerequisite, and videos_planning/exclude_videos.txt is where its
output goes. Any pinning job MUST filter every entry in that file first.

17 entries have no CID at all and cannot be published with a player:
  * 2071736376215920842_extracted.mp3                            x
  * yt/0pvEGO4W85k                                               youtube
  * yt/0ykbt_WGOZE                                               youtube
  * yt/1RbDMiEReys                                               youtube
  * yt/1xTpQ9RHkvk                                               youtube
  * yt/2exo7iJ-qdc                                               youtube
  * yt/8HkNMTNHsa8                                               youtube
  * yt/J2DKRfwSt94                                               youtube
  * yt/PLnZT7Gz_VSN520UilgmZqikvi3n1MsuZR                        youtube
  * yt/PLuXXbBFpPc0lhc6PfJae8Rav-gMNpmeuL                        youtube
  * yt/X8UKjN5cjvw                                               youtube
  * yt/ccRNaLGavf8                                               youtube
  * yt/qpGPZHdil1E                                               youtube
  * yt/v6yrnyo                                                   rumble
  * yt/v705uyi                                                   rumble
  * yt/w-ng95XlQb4                                               youtube
  * yt/wcD2khO3rOA                                               youtube

==========================================================================
6. WHERE THE INVESTIGATION HAS NO VIDEO COVERAGE AT ALL
==========================================================================

The tree mirrors the whole site on purpose, so the empty nodes are a real
research output: they are the parts of the investigation with no footage.
1,389 of 1,559 nodes are empty and carry publishable: false.

THESE LEVEL 2 SECTIONS HAVE ZERO VIDEO IN THE ENTIRE CORPUS:

  * After Events                                 After
  * Analysis and Documentation                   analysis_documentation
  * Campus and University                        campus_university
  * Companies & Organizations                    Companies_Organizations
  * Electrocution — The B-Field Resonant Cascade Electrocution
  * Government Evidence                          gov
  * Government Organizations                     government_organizations
  * Key Individuals                              key_individuals
  * Legal                                        Legal
  * Legal Investigation                          legal_investigation
  * Motive                                       Motive
  * Narrative                                    Narrative
  * New Laws (Fix)                               Fix
  * Organizations and Groups                     organizations_groups
  * Political Context                            political_context
  * Proof Intel Services                         Proof_Intel_Services
  * Proof Not Tyler                              Proof_Not_Tyler
  * Property & Locations                         Locations
  * Security and Law Enforcement                 security_law_enforcement
  * Social Media Analysis                        social_media_analysis
  * Suspicious                                   Suspicious
  * Technology and Surveillance                  technology_surveillance
  * The Laws                                     laws
  * Tyler Robinson Not Assassin                  Tyler_Robinson_Not_Assassin
  * Vote                                         Vote
  * Your Actions Fix It                          Your_Actions_Fix_It

publishable: false MUST BE HONOURED by p_yaml_to_site.md and
p_level2_update.md. Generating a page per node would add ~1,389 empty
'Videos -> FBI -> Search Warrants' pages that say nothing and hand a visitor
arriving from a topic page a dead end where they expected footage.

==========================================================================
7. should_be_on_pages FAILS TWO OF THE FOUR ACCEPTANCE TARGETS — READ WHY
==========================================================================

  measured                       target            result
  should_be_on_pages == []       5%-25%            33%   FAIL (too many empty)
  >= 1 page                      >= 75%            66%   FAIL (too few placed)
  >= 2 pages                     >= 20%            44%   PASS
  on_pages == [] for all         must not be 100%   no    PASS

THIS WAS NOT TUNED TOWARD THE BAND, AND SHOULD NOT BE. Hand audits of ten
randomly sampled proposals were run against four successive configurations:

  config                                          hand-audited precision
  lexical scoring, images-pipeline rules                 4/10
  + distinctive-token gate, evidence floor               (same misses)
  + claim-vs-scene token split                           2/10
  + two-distinctive-title-tokens, cluster binding        5/10   <- shipped

Loosening the gates to reach 75% coverage puts the precision back at 2-4/10,
i.e. it manufactures publishing instructions that a human then has to undo on
live pages. The prompt itself says a weak topical match is worse than none.
So the shipped configuration is the precise one, and the coverage gap is
reported here as work rather than hidden by relaxing a threshold.

WHY VIDEO SCORES WORSE THAN THE IMAGES PIPELINE (which hand-audited 65-70%):

  Roughly half this corpus is RAW EVENT FOOTAGE, not commentary. A clip of
  the UVU crowd has a long transcript — hundreds of words of ambient chatter,
  'Whoo! USA! USA!' — which is high-volume and topically empty. Against 1,495
  pages that are all about the same event, that noise always finds something
  to match. An image never had this failure mode: a photo with nothing in it
  produced a short description and scored low, whereas ambient audio produces
  a LONG transcript and scores high.

  The fix that worked was to stop trusting per-video text and trust the
  CLUSTER instead. The cluster map in build_tree.py was authored by hand from
  the mirror's own concept directories, and a cluster name states what its
  footage is about far more reliably than one clip's transcript. 36 of 126
  corpus clusters bound to a specific site page this way; the remaining 90
  are the top of the work list below.

HOW TO ACTUALLY RAISE COVERAGE — three things, in order of value:

  a) BIND THE REMAINING 90 CORPUS CLUSTERS TO SITE PAGES BY HAND. This is
     ~90 decisions, each covering several videos, and each far more reliable
     than a per-video guess. Add them as an explicit table in
     generator/plan_should_be.py next to CLUSTER_PAGE.
  b) CREATE THE MISSING PAGES. 429 assignments were dropped because their
     target page already held six videos. A page over the cap is a page that
     wants a child page — see section 8.
  c) TRANSCRIBE THE 33. Section 4.
==========================================================================
8. WANTED PAGES THAT DO NOT EXIST (pages over the six-video load)
==========================================================================

429 planned placements were dropped because the target page was already
carrying six videos. Each of these is a concept with more footage than one
page should hold — i.e. a page that wants child pages under it. Creating them
is the cleanest way to raise video coverage on the site.

Ranked by how much footage is queued behind them (overflow count):

    9 videos  site/docs/Narrative/Shot_in_the_heart.mdx
    6 videos  site/docs/People/donald-trump.mdx
    6 videos  site/docs/Suspects/Black_Clothing_Suspect.mdx
    6 videos  site/docs/Suspicious/UVU_9_10/all-black-construction-worker.mdx
    6 videos  site/docs/FBI/Kash_Patel_Briefings.mdx
    6 videos  site/docs/Israel_Main_Suspect/charlie-said-israel-would-kill-him.mdx
    6 videos  site/docs/People/hunter-kozak.mdx
    6 videos  site/docs/distraction_people/George_Zinn.mdx
    6 videos  site/docs/Influencers/podcasts-megyn-kelly.mdx
    6 videos  site/docs/People/blake-bednarz.mdx
    6 videos  site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx
    6 videos  site/docs/Suspicious/Cause_of_Death/shirt-before-blood.mdx
    6 videos  site/docs/UVU/CIA-UVU-Profiles.mdx
    6 videos  site/docs/US_Intelligence/cia.mdx
    6 videos  site/docs/TPUSA/TPUSA_Opposite_Charlie.mdx
    6 videos  site/docs/Censorship/Censorship_Investigation_Index.mdx
    6 videos  site/docs/Influencers/podcasts-project-constitution.mdx
    6 videos  site/docs/Influencers/x/project-constitution.mdx
    6 videos  site/docs/Suspicious/UVU_9_10/rick-cutler-hand-device.mdx
    6 videos  site/docs/Suspicious/Defense_Attorneys/parents-declined-attorneys.mdx
    6 videos  site/docs/Tent/Platform_Water_Bottles.mdx
    6 videos  site/docs/Drones/Butler_PA_Drone_Parallel.mdx
    6 videos  site/docs/Influencers/podcasts-dave-smith.mdx
    6 videos  site/docs/Suspicious/UVU_9_10/stairs-guy-backpack.mdx
    6 videos  site/docs/Security_Team/next-event-no-plan.mdx
    6 videos  site/docs/Gov_Mind_Control/mkultra-program.mdx
    6 videos  site/docs/Mic/rode-wireless-mic.mdx
    6 videos  site/docs/distraction_people/Pellet_Gun_Man.mdx
    6 videos  site/docs/Killer/Close_Range_Theories.mdx
    6 videos  site/docs/Planes/N1098L/overview.mdx
    6 videos  site/docs/Suspicious/TPUSA_Peripheral/schoneberger-yrefy-sponsor.mdx
    6 videos  site/docs/Influencers/podcasts-patrick-bet-david.mdx
    5 videos  site/docs/Locations/Washington_County_Sheriff.mdx
    5 videos  site/docs/Suspicious/FBI/patel-shut-down-kent-probe.mdx
    5 videos  site/docs/court/mirandize/baron-coleman-early-turn-in.mdx
    5 videos  site/docs/Timeline/rental-cars-vehicle-movements-timeline.mdx
    5 videos  site/docs/distraction_people/Hunter_Kozak.mdx
    5 videos  site/docs/Israel/threat-to-western-politicians-iran-war.mdx
    5 videos  site/docs/Fix/Churches.mdx
    5 videos  site/docs/Suspicious/Trial_Legal/uncalled-roof-eyewitness.mdx

==========================================================================
9. BYTE-IDENTICAL DUPLICATE FILES IN THE MIRROR
==========================================================================

12 files are byte-for-byte copies of another file already in the corpus —
same CID, different name ('Jesse_ON_FIRE', '... copy', '... copy 2'). They
are one video, not several, so the duplicate is folded into its twin and its
path recorded in the surviving entry's duplicate_paths. Nothing was deleted
from disk. Worth cleaning up in the mirror itself:

  keep  1965892000185725129
    dup 1965913654840406034
  keep  Double_Shot.mp4
    dup Front_Left_Camera.mp4
  keep  FINAL_CIA_Drones.mp4
    dup v3 New CIA Video.mp4
  keep  Jesse_ON_FIRE.mp4
    dup Jesse_ON_FIRE copy.mp4
    dup Jesse_ON_FIRE copy 2.mp4
  keep  10_Drones.mp4
    dup Crowdsource The Truth - These unknown flying objects were record
  keep  Project Constitution - TPUSA's Tyler Bowyer DOUBLY EXPOSED – Birth
    dup Project Constitution - 🚨 BREAKING： NEW DRONE FOOTAGE  From The T
  keep  James Li - 🚨 Meet Skyler Baird — he is the “eyewitness” who： - app
    dup James Li - 🚨 Meet Skyler Baird — he is the “eyewitness” who： - a
  keep  10_Pellet_Gun.mp4
    dup War Reporter - 🚨 BREAKING： The alleged shooter of Charlie Kirk h
  keep  SU_BBT.mp4
    dup Candace Owens - 🚨BREAKING NEWS!🚨 On September 10th, after Charli
  keep  12.ia.mp4
    dup 13.ia.mp4
  keep  4k_60fps_from_South.mp4
    dup 4K_South_High_Res_Close_60fps.mp4

==========================================================================
10. SCHEMA ADDITIONS THIS RUN MADE
==========================================================================

Beyond the expanded schema the prompt specifies, one optional property was
added because the corpus needed it:

  duplicate_paths   list of other files on this machine whose bytes are
                    identical to this entry's. [] when there are none. See
                    section 9. Without it, folding a duplicate would lose the
                    record that the second file exists.

_key MINTING NOTE. The prompt says to prefer a site section's page_key from
pages.csv 'when it is free'. None are free — pages.csv already uses every one
of them for the site page the node MIRRORS. So every node key in videos.yaml
carries a Vid_ prefix (Vid_FBI, Vid_Exploding_Microphone, ...). That keeps
_keys unique file-wide AND collision-free against pages.csv when the video
pages are eventually added to it. The node records the page it mirrors in
site_page / site_level_2, which is what Stage 9's merge actually needs.

==========================================================================
11. on_pages SUBTRACTIONS (recorded, per the union rule)
==========================================================================

should_be_on_pages is a SUPERSET of on_pages. 10 observed placements were
deliberately NOT carried into the plan, each with its reason:

  * 1965869689755812061                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_5.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1965871960702828885                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_3.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1965884012565766172                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_8.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1965890646746513821                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_2.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1965913654840406034                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_7.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1966235480732873149                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_4.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1966293765158560167                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_6.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 1969832388823003519                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_9.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * 2076465128329846991                          -> site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/Img_Photo_Narrative_Shot_in_the_Heart_1.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target
  * site/QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFb -> site/docs/Photos/Mic/Img_Photo_448e0d.mdx
      reason: the page is under site/docs/Photos — the images pipeline's output, which Stage 13 may not target

Note what those subtractions reveal: the IMAGES pipeline has placed VIDEO
CIDs on pages under site/docs/Photos. Those are videos filed as images. Worth
a look from the images side — this pipeline may not touch /Photos.

==========================================================================
12. STAGE 12 IS CORRECTLY EMPTY
==========================================================================

video_page is "" on all 400 entries. site/docs/Videos holds only overview.mdx
and buckley-carlson-kash-patel-valhalla.mdx, neither of which carries the
ck_video_cid frontmatter the binding matches on. Both are PROTECTED hand-
written pages and were not guessed at by filename. video_page fills in once
p_yaml_to_site.md generates the Level 5 pages and stamps them.

==========================================================================
13. WHAT THE NEXT RUN SHOULD DO FIRST
==========================================================================

  1. Fix the census section of p_update_video_hierarchy.md (section 1 here).
  2. Review the mirror for publishability, fill exclude_videos.txt, and only
     then consider pinning. 337 unpinned CIDs is the gate on the whole
     hierarchy going live.
  3. Hand-bind the 90 unbound corpus clusters to site pages (section 7a).
  4. Transcribe the 33, re-run the 38 partials (section 4).
  5. Harvest blocks[].start/end timing out of the .ocr sidecars (section 3).

## Stage 3 write-up findings

### agent_06

* Vid_4k_Full_56bSKCp - transcript AND ai_description both describe a Michigan House Election Integrity Committee hearing (Lansing, HOUSE TV stamp 06/03/25), not UVU footage. Entry is unverifiable as filed; media needs opening.
* Vid_Ryne_Simmons_bPUC272 - ai_description identifies the event footage as the July 2024 Butler PA rally; its own on-screen text list reads "THE AMERICAN COMEBACK TOUR" (UVU, Sept 10 2025).
* Vid_Short_Video_Clip_Captures_qzHCQmC, Vid_Short_Video_Clip_Captures_s4Sc3Ex, Vid_Video_Captures_Live_Outdoor_qNoKV2w, Vid_Video_Captures_Chaotic_Scene_2GZEXPr - ai_descriptions name the seated Prove Me Wrong speaker as Steven Crowder; it is Charlie Kirk.
* Vid_Short_Raw_Documentary_Style_VNHn6qz - ai_description places the event at University of Washington, Seattle; it is UVU.
* Vid_4k_60fps_South_5duWBzw - ai_description guesses Denver, Colorado and reads the post-shot scramble as security tackling a disruptor; neither is supported.
* Vid_3_Drones_PfsVmL5 - filed in the drone cluster but no aerial object appears; ai_description also guesses Phoenix, Arizona.
* Vid_5_No_Drones_Ae575Xv - filed in the drone cluster; filename and footage both confirm no drone. Kept as a control angle.
* Vid_12_Short_Drone_Video_AV87bDo and Vid_Crowdsource_Truth_Do_Any_1966510 - same underlying 16s clip (identical timecode 00;13;11;07, watermark, audio, magnifier loop) held as two entries.
* Vid_Ryan_1_k6rkFas and Vid_Jammles_ShadowofEzra_Says_Photos_1982156 - Vid_Ryan_1 embeds the whole of the Jammles clip behind 67s of commentary; overlapping content in one cluster.
* Vid_Censorship_Ld3J1DY - filed under "Censorship of the Investigation" but contains no suppression claim; it is Gov. Cox broadcast material on social media harms. Fits as official-speech, not suppression.
* Vid_David_Nino_Rodriguez_Man_1982164 - ai_description guesses Las Vegas, Nevada with nothing on screen supporting it.
* Vid_Bechedith_Re_Baroncoleman_VLuvMully_2076295 - ai_description reads the booking-sheet arrest date as 09/11/2021; the document is 2025.
* Vid_FaithDrivUr_Narrator_Says_Police_2078917 - the courtroom exhibit monitor timecode reads 9/10/2021 9:24:48 AM; camera clock year error, footage is Sept 10 2025.
* Vid_MarioNawfal_Erika_Kirk_Takes_6L9661F - no media file, no transcript, no ai_description; only archived post text exists. Page written without a player.

### agent_01

* Vid_TBD_mwSLnKH - State Farm Stadium (Glendale, AZ) memorial footage filed in the "South Side Shot Analysis" ballistics cluster; own frames contradict the filing.
* Vid_Funneral_dKD6hNm - same misfiling (Glendale memorial pan). Also the file has NO audio stream at all, contradicting the ai_description's account of ambient crowd noise.
* Vid_South_Side_ZXD4iw6 - ai_description places the clip at the AGR building, Butler PA; it is the UVU courtyard (matching interior appears in Vid_Inside_Vents_R8NRStG).
* Vid_South_Side_Stairs_KuQuRkf - ai_description guesses Washington DC; it is UVU. Transcript is completely empty (music-only edit).
* Vid_Mile_Kovacevic_HustleBitch_Between_1971989 - ai_description places it at Mt. San Antonio College, Walnut CA; it is UVU.
* Vid_Project_Constitution_MIND_BLOWING_1978201 - ai_description guesses Salt Lake City; it is Orem/UVU.
* Vid_Short_Video_Clip_Captures_xrYHJoc - ai_description reads the instant of the shot as a man tackling the questioner to the ground; the audio is the final Q&A exchange and every other angle shows a mass startle drop. Automated "tackle" reading is wrong.
* Vid_Thomas_Perera_Am_JohnCullen_1977744_3 - ai_description reads the SAME instant as a "sucker punch" and places it in Seattle WA; both wrong. Two independent automated misreads of the same second.
* Vid_Thomas_Perera_Am_JohnCullen_1977744 - ai_description says Butler PA / Trump rally; the transcript says "Charlie's sitting there" and the banner reads PROVE ME WRONG. It is UVU.
* Vid_Thomas_Perera_Am_JohnCullen_1977744_2 - ai_description says Butler PA with Trump at the podium, yet records YREFY/YREFY.COM banners behind the podium and UVU stage audio. It is UVU.
* Vid_14_Visible_Ia_VinKu55 vs Vid_14_Visible_d1k73u7 - same footage, two audio passes; the machine transcripts contradict each other on the key line ("There's NO shot fired right now" vs "He's been shot"). Neither is quotable as testimony.
* Vid_Wendy7839570959_Witness_Camera_Saying_2079042 - ai_description of the inset footage reads it as a white substance splashed on a man's face; the inset audio is the pre-shot stage exchange, so that reading does not fit.
* Vid_Sword_Truth_Hey_Troofevades_2016609 - the clip is an AI-generated illustration (poster says he asked Grok to imagine it); the aerial background is a generic red-brick quad, not UVU, and "0.4mm Algorithm Precision" is not physically meaningful. Transcript is boilerplate artefact text.
* Vid_Conman_Please_Share_Video_1977286_3 - transcript is noise only ("Thank you. You"); the clip has no speech, so the drone claim exists only in the post text.
* Vid_Inside_Vents_R8NRStG - transcript is the lyrics of the backing song, not speech; risks being read as narration or testimony.
* Vid_Shiloheffort_Media_Orig_SH4D0W_2077994_2 - the poster framing archived in Charlie_Kirk.txt describes a question about HAND movements; the held edit marks hair-touching. Archived claim and held artefact do not match.
* Vid_Side_Shot_rjArE7Q and Vid_Side_Shot_2_EB6QBt1 - the same presentation held twice (6:53 short cut, 13:08 full cut) as two separate cluster entries.
* Vid_Yard_1_EpS4n6m and the Vid_14_Visible pair - the name "Isaac" is called in both; possibly the same filming party, worth checking before treating them as independent captures.
* Vid_Aducarrabh_Slow_Motion_Object_8MBbCYs, Vid_Dr_Speaker_Heart_Shot_M4NUARg, Vid_Bizarro_Videos_Vest_Ricochet_HS3Fpz7, Vid_Cashloren_Glenn_Beck_Tells_wvJ1rfZ - no media, no transcript, no ai_description; written from archived post text (and, for two of them, transcripts preserved in Charlie_Kirk.txt).
* PUBLICATION RISK - Vid_Side_Shot_rjArE7Q / Vid_Side_Shot_2_EB6QBt1 name no one but point on screen at two identifiable private bystanders and assert they shot Charlie Kirk. Both are currently "pending"/unpinned. They should not be pinned and made playable without a review.
* PUBLICATION RISK - Vid_Shiloheffort_Media_Orig_SH4D0W_2077994 and _2 are already pinned and playable, and the short edit puts a named living private individual on screen with the caption "Actor?". Counterpoints are carried in the write-ups, but the embeds themselves carry the accusation.

### agent_03

* Vid_John_Cullen_BenSwann_Thought_1969719, Vid_John_Cullen_SharylAttkisson_4_1969372, Vid_Charo_BlakeBednarz_Grok_Attached_1978846 - whisper transcripts contain only the filler token "you" repeated; all three videos are genuinely silent, so the sidecar is correct but useless. Lean on ai_description.
* Vid_Spy_Plane_Analysis_oW3EvAi and Vid_Blake_Bednarz_Original_Post_1978553 - identical recording held twice; transcripts match word for word. One is credited to Bednarz, one filed untitled.
* Vid_Alley_Files_Oh_Wow_2032224 and Vid_Red_Pill_Dispenser_Official_2038934 - same broadcast segment; the Red Pill copy is a phone pointed at a monitor and adds ~20s of preamble, the Alley Files copy runs longer and is cleaner.
* Vid_Charo_BlakeBednarz_Grok_Attached_1978846 - content is a chatbot output asserting the low passes were routine drone-retrieval training, i.e. exculpatory; filed inside the spy-plane cluster where it reads as supporting evidence. Also names a crew roster that conflicts with a second roster in CK_FILE.
* Vid_Alley_Files_Another_Video_2033665 - ai_description reads the post-shot close-protection response as a spectator vaulting the barrier and tackling the speaker, and names the seated man as Steven Crowder. Both wrong; potential libel source if copied into prose.
* Vid_Alley_Files_Heres_Short_2044122 - ai_description again names the speaker Steven Crowder.
* Vid_Blood_Hands_Black_Shirt_t7yTCYe and Vid_Blood_Hands_Black_Shirt_UESJx2U - filenames promise a black-shirted person with blood on their hands; neither ai_description records blood or such a person. Clip 1 is an older man being carried from the plaza by officers; clip 2 is 10s of crowd on the stairs.
* Vid_Blood_Hands_Black_Shirt_t7yTCYe - ai_description places the location in Longmont, Colorado; it is the UVU plaza.
* Vid_Blood_Hands_Black_Shirt_UESJx2U - ai_description guesses Fort Collins, Colorado; tent text ("AMERICAN...", "PROVE ME WRONG") fixes it as UVU.
* Vid_Project_Constitution_URGENT_CALL_1981171 - ai_description guesses Butler, Pennsylvania; American Comeback / Prove Me Wrong branding fixes it as UVU.
* Vid_Muppet_Masher_Comes_Under_2066468 - post caption asserts something comes from under the subject's shirt; ai_description describes the opening body movement as laughter and records no shirt, blood or injury. Needs a human frame-by-frame before it is used as evidence.
* Vid_Meidas_Charise_Lee_MONEY_2029848 - dates its own source (a "February 2026 Epstein ledger") after the events it purports to explain, names entities that do not match the documented TPUSA corporate structure, and accuses several named living people. Unusable as evidence.
* Vid_Rubber_Duck_TM_REMEMBER_2032172 - archival 2012 CNN Sandy Hook footage with a hoax-framing caption, no connection to this investigation. Recommend removal from the public hierarchy.
* Vid_Sword_Truth_Https_T_2033545 - 8:23 anonymous monologue accusing a named living widow of complicity and guilt with zero documentation, plus abusive language. Recommend removal from the public hierarchy.
* Vid_Teacher_Lounge_Shooter_4uXg3De - no ai_description sidecar at all (transcript only). Filed under the Teachers Lounge cluster but is a George Webb livestream about shot geometry, not that room. Back half contains sustained unverified allegations against a named serving federal official plus speculation about private individuals' identities; only the front section is publishable.
* Vid_Project_Constitution_ALERT_BREAKING_1986565 - filed under the Piper N59906 cluster but is almost entirely about low-altitude drones and security jurisdiction; the fixed-wing aircraft is not its subject.
* Vid_Project_Constitution_ALERT_BREAKING_1986847 - whisper transcript is empty (music-only clip). Also: the graphics half and the aerial-imagery half are never joined by anything on screen, and the tail number is never shown.
* Vid_ProjectConstitu_FBI_Ignored_Eyewitnesses_2045871 / _2 - the two entries are the two clips of one X post; _2 (the shorter) is a CNN broadcast segment, _1 (the longer) is a studio commentary monologue. Neither title reflects that.
* Vid_Project_Constitution_Breaking_Newly_1979071 - ai_description identifies the walking subject as "likely Dylan Rounds," a person from an unrelated Utah missing-person case; wholly wrong and it also seeded the page description.
* Vid_Project_Constitution_Breaking_Newly_1979071 - transcript is ASR filler over a silent clip ("I'm not sure. Okay." repeating). Not a transcript.
* Vid_Troofevades_Demonstration_Real_Shaped_2071072 - same ASR-filler-over-silence failure; qwen3-asr output is unusable.
* Vid_Tyler_Running_xJyU633 - filed and named as Tyler running; the six seconds show an interior pan across the UVU Hall of Flags with staff at tables. Nobody is running and nobody is identifiable.
* Vid_0HOUR_Hey_Jimmy_Rustlin_1965902 - filed under Tyler Robinson Footage; the frames show a small white object crossing the sky, not a person. Belongs nearer the drones/airborne-object cluster.
* Vid_Clothing_Change_qHbnd8p and Vid_Clothing_Change_Copy_YMV1Zzv - duplicates of the same Gov. Cox press-conference answer (22s vs 23s subtitled). Two cluster slots for one artefact.
* Vid_Blake_Bednarz_UVU_Reviews_1981078 and _1981078_2 - near-duplicate pair from the same post (#1 and #2), both 31s. Same issue.
* Vid_Blake_Bednarz_UVU_Reviews_1981078 - transcript mishears "gang violence" as "gang buttons"; the companion capture renders it correctly.
* Vid_Blake_Bednarz_Reward_Current_1978863 - transcript is the same half-sentence looping ~6 times, which is accurate to the file but reads as a broken transcript.
* Vid_Virginia_Tech_Sept_4_BJ8f2PK - file name carries a September 4 date but the speech is plainly post-assassination (Kelly speaks of Kirk in the past tense and of the courage of attending "given what happened"). Stored date is wrong.
* Vid_SAS_July_11_PrD4MBV - ai_description shot list ends at 22:26 with the outro card, against a stated 32:27 runtime; capture appears to include trailing material.
* Vid_Megyn_Kelly_Charlie_Kirk_YWSyzDK - is a 2:14 excerpt of Vid_SAS_July_11_PrD4MBV (same July 11 SAS conversation). Both are held as separate cluster entries; the relationship is now stated on both pages.
* Vid_Realhonestash_Source_Clip_UFaZsYm - no transcript, no ai_description, no local file, no sha256; only a CID and a source URL shared with Vid_Realhonestash_Candace_Owens_Covers_2069185. Page written honestly as "not established".
* Vid_Realhonestash_Candace_Owens_Covers_2069185 - archive copy is an .mp3 audio extraction, so no visual description can exist; "What The Footage Shows" says so rather than guessing.
* Vid_Realstewpeters_Stew_Peters_Explains_2069997 - transcript renders "Elbit Systems of America" phonetically as "Albert Systems of America" throughout (Charlie_Kirk.txt already carries the bracketed correction), and "McEwen, Tennessee" as "Macau"/"McCowan".
* Vid_Muppet_Masher_TommyLaRussoLLC_2075684 and Vid_Project_Constitution_Breaking_Newly_1979071 - appear to be the same Wyze porch camera on the same morning (stamps 08:22:50 and 08:22:30), filed as unrelated entries by different posters.
* PUBLICATION CAUTION - Vid_Blake_Bednarz_Who_Guy_1985423 is a crowdsourced "who is this guy?" request that isolates and zooms on an unnamed young event volunteer who is doing nothing but handling merchandise. Currently pending/unpinned. It should not be pinned and made playable without a review; the write-up names no one and states no conduct is alleged.
* PUBLICATION CAUTION - Vid_Project_Constitution_BREAKING_CHARLIE_1976506 points on screen at an unidentified person running during the evacuation and asserts in text that he is the shooter, while simultaneously running a "DO YOU KNOW THIS PERSON?" appeal. Pending/unpinned; same review recommendation.
* Vid_High_Res_Table_Item_jY48QtB - ai_description labels the clip as Butler PA, July 13 2024, with Benny Johnson at the desk; the signage it itself lists (TURNING POINT USA, YREFY.COM, AMERICAN COMEBACK) is UVU on Sept 10 2025.
* Vid_Vide_353_3mwXTjc - ai_description names the man at the table as Steven Crowder and calls the event his tour; it is the TPUSA Prove Me Wrong table at UVU.
* Vid_DguzChVxdJ3Fq5m2_mqMvtwW - same Steven Crowder misattribution on a second file; the machine pass makes this error repeatedly across the corpus.
* Vid_In2ThinAir_WATCH_Charlie_Kirks_1972341 - ai_description reads the footage as three men praying and then a medical episode; it is the seconds after the shot at the table, per the post's own caption and the folder it sits in.
* Vid_Project_Constitution_EXCLUSIVE_BRAND_1977138 - ai_description states the questioner "physically attacks a security guard" and calls him argumentative and the instigator of a fight. No attack is on the recording; the audio at that instant is the last Q&A line. This is the most harmful automated misread found in this batch and it was retracted explicitly on the page.
* Vid_Erika_Evil_Doors_XsWAQXY - ai_description does not identify the speaker at all (calls her an unnamed blonde presenter delivering a PBS news segment) and reads the memorial placard as "a sign for a boy named Charlie". The 17 minutes are Erika Kirk's address; the PBS card is only the broadcaster's end slate.
* Vid_ProjectConstitu_Project_Constitution_Video_2002152 - ai_description calls the montage a memorial slideshow commemorating the life of Bobby Harpole. The site's own profile records him as living; the funeral-home item relates to the family's funeral-services background.
* Vid_MvCUbhcVsUi8L9G_YPH91X5 vs Vid_RyanMatta_BlakeBednarz_RealCandaceO_IanCarrollShow_1968566 - two passes over near-identical UVU exterior camera footage stamped 9/10/2025 12:23:35 disagree on the subject: one reads a long-barrelled rifle in both hands, the other a backpack and no carried object.
* Vid_Vide_35_kKkV3NJ appears to be a subset of Vid_XBHHgwl_EZFACOKB_ptfhcUv (same LDS exchange audio, same angle) but the two are filed in different clusters - Vid_Table_Charlie and Vid_Raw_Shooting_860c. Worth deduplicating or cross-referencing.
* CLUSTER FILING - Vid_RyanMatta_FBI_Needs_Immediately_1984001, _1984014 and Vid_Project_Constitution_NEW_AndrewKolvet_1975655 are filed under Vid_UVU_Venue / Citizen Analysis of the Footage (Part 5). None of the three is analysis of UVU footage: two are studio commentary about Egyptian flight records, one is a Charlie Kirk Show segment about a text chain. Same problem in Part 3 with Vid_Censored_Humans_Charlie_Kirk_2019832 (studio Epstein monologue) and Vid_Final_Cut_Tile_Why_2033216 (AmericaFest stage debate).
* Empty or unusable transcripts in this batch: Vid_High_Res_Table_Item_jY48QtB, Vid_In2ThinAir_WATCH_Charlie_Kirks_1972341, Vid_RyanMatta_BlakeBednarz_RealCandaceO_IanCarrollShow_1968566 (all silence filler); Vid_10_Full_Video_46HJJFb ("Yes"); Vid_Hand_Off_pANvLdZ (one garbled line); Vid_FeelingThePain_HolonCitizen_Stelzner_N1150_2027989 (two syllables); Vid_MvCUbhcVsUi8L9G_YPH91X5 (recogniser hallucination over silence); Vid_French_Legionaire_F1TACDV (no audio stream at all); Vid_ProjectConstitu_Project_Constitution_Video_2002152 (music only); Vid_Vide_222_9tmMm9G (distant PA, unattributable).
* PRIVACY - ai_descriptions for Vid_Public_Bureau_Investigation_Realjesseonfire_2039944 and Vid_Tate_Helmuth_BlakeBednarz_Here_1981181 record vehicle licence plate characters; Vid_ProjectConstitu_Project_Constitution_Video_2002152 names a young family member on a scholarship certificate. All three suppressed on the published pages; they should be scrubbed from videos.yaml too.
* PUBLICATION CAUTION - Vid_French_Legionaire_F1TACDV is a slideshow that pairs a young private individual's souvenir cap with French Foreign Legion imagery and asserts he stood inside a restricted zone. It names nobody but shows his face from six angles. It is currently unpinned; pinning it would publish a face-based identification resting on a tourist cap.

### Agent 02 (Stage 3 write-up)

* Vid_Short_Video_Clip_Captures_R4BRD75 - ai_description says the speaker is "hit in the neck by a thrown object" and the audience "cheers"; the frames are the moment of the shooting.
* Vid_11_Minutes_Full_GvwBe3W - ai_description reads 10:15 as an agitator running on stage to throw liquid; it is the shooting and its aftermath.
* Vid_10_Visible_Skip_19_i65NBCJ - ai_description attributes the booth to Steven Crowder; it is the TPUSA American Comeback Tour event. Shot-by-shot also stops at ~23 min of a 70-min file, omitting the entire post-shooting section.
* Vid_10_1_Min_30_DupLVw1 - ai_description calls the bag contents "handguns and ammunition magazines"; siblings covering the identical seconds call them green tubes/canisters or blue clothing. Resolution cannot settle it.
* Vid_Video_X_DDyfNFA and Vid_Sarah_Fields_JfbNuSX - same recording twice (TikTok @rynestimetwo, "In the tunnel right after!"); footage is a political-rally tunnel evacuation with a protective-detail SUV, one ai_description identifies it as Butler PA 2024-07-13. Misfiled under Vid_Truck_Behind_Tent (a UVU cluster).
* Vid_Sarah_Fields_JfbNuSX - filename attaches a person's name that nothing in the footage supports.
* Vid_George_Zinn_XLeQjpa - filed in the George Zinn cluster; footage is a distant crowd stampede screen-recording in which no individual is resolvable. He is not visible.
* Vid_HustleBitch_WATCH_George_Zinn_1971065 - caption asserts a named living person "appears to set something down"; the highlighted figure is a few dozen pixels and no object is resolvable.
* Vid_DiligentDenizen_George_Zinn_TPUSA_2078878 - YAML title cites "Hull testimony on Robinson"; no such passage exists in the audio, which is the jail call only.
* Vid_FINAL_CIA_Drones_a74hWXT and Vid_Original_Fixed_High_Q_n4m8oYt - byte-identical transcripts; one recording held as two nodes. Both ai_descriptions describe the assassination as a "speculative or fictional" event.
* Vid_BlakeBednarz_Blake_Bednarz_Asks_2078118 - ai_description reads the podium seal as "Providence Police Department"; it is the Utah briefing.
* Vid_Video_Captures_Sudden_Panic_UGrq9XY - transcript after the reports is degraded crowd garble that yields plausible-looking phrases ("good job", "he shot him") nobody demonstrably said. Should not be quoted as speech anywhere.
* Vid_Pellet_Gun_9f8a - all nine leaf videos are variants of one street-detention capture (differing crop, length, overlay, watermark). Cluster count of 9 overstates the evidence to 1 recording.
* Vid_Wtshesaid72_Animated_B_Field_2077277 - node title claims a "B-field resonant cascade"; the clip's own overlays only describe pressure compression/expansion. Title and content belong to different arguments.
* Vid_Big_Great_Truck_Back_8C1NKW1 and Vid_Project_Constitution_BREAKING_NEWS_1976730 - both make murder accusations against unnamed private bystanders (camera operators, an audience member with a phone) from magnified low-resolution frames. Written up strictly as reported claims; recommend a human review of whether these belong on the public site at all.

### Agent 08 (Stage 3 write-up)

* Vid_HustleBitch_LISTEN_CLOSELY_CONSTRUCTION_1979029 - filed under the Brown Shirt Figure cluster; its content is the all-black construction-worker witness account (a different figure entirely). Belongs with Suspicious/UVU_9_10/all-black-construction-worker.
* Vid_HustleBitch_LISTEN_CLOSELY_CONSTRUCTION_1979029 - ai_description places the events in Butler, Pennsylvania; they are Orem, Utah.
* Vid_Full_Brown_Shirt_1_pkfYYrG, Vid_Full_Brown_Shirt_2_NN4AW8o, Vid_Val_VenisTM_Big_ValbowskiTM_1978346 - all three ai_descriptions locate the UVU footage at the July 2024 Butler PA Trump rally. Wrong event, wrong state.
* Vid_Brown_Shirt_6zZKqK6 - ai_description locates the event in West Palm Beach, Florida; it is UVU, Orem, Utah.
* Vid_Val_VenisTM_Big_ValbowskiTM_1978346 - ai_description reads the white streak as passing near the man's head; CK_FILE records the same poster's claim as the streak leaving his hand. The two readings point in opposite directions and the clip cannot support either.
* Vid_Project_Constitution_BREAKING_UNDENIABLE_1977953 - no ai_description exists for this 2:19:04 file; the visual account had to be reconstructed from the participants narrating their own screen shares.
* Vid_Yes_Still_MORE_DISTURBING_ubpia1E - no ai_description exists for this 2:03:22 file. Same reconstruction problem.
* Vid_Diligent_Denizen_Google_Trend_1979286 - transcript is empty. Correct: the clip is music-only with no voice-over.
* Vid_Sam_Parker_MORE_CHARLIE_1977027 - ai_description names the on-camera presenter "Baron" while the post is carried under the Sam Parker account. The segment is an excerpt of the same stream as Vid_Project_Constitution_ISRAELI_IP_1977626, whose description also names "Baron". Presenter identity unresolved in the YAML.
* Vid_Project_Constitution_ISRAELI_IP_1977626 - ai_description records the aircraft registration on the John Cullen screenshot as N109BL; the audio clearly says N1098L.
* Vid_Rob_Hild_Shaner_Brodderick_mKrPjEP - ai_description characterises the FBI Salt Lake City post as a "fake tweet" and the whole scenario as "a fictional satirical scenario". It is neither.
* Vid_Rob_Hild_Shaner_Brodderick_mKrPjEP, _cvpYPjX, _xtQwBdj and Vid_Ryan_Matta_1/_2 - filed under Vid_Raw_Shooting_b200 ("Raw Shooting Footage Part 2"); none of the five is raw shooting footage. They are a podcast segment, pre-event crowd footage with a metadata read-out, a recorded phone call over a campus walkthrough, an arrival clip, and a pre-event TikTok. Cluster is mis-scoped.
* Vid_Ryan_Matta_1_KRScixh - ai_description names the seated speaker under the American Comeback Tour tent as Steven Crowder; the framing is consistent with Charlie Kirk. Same misidentification agent 02 logged on Vid_10_Visible_Skip_19_i65NBCJ.
* Vid_SU_BBT_mffHmBd - transcript is a hallucination. The file has no audio; the ASR engine emitted a sentence about US military spending that appears nowhere in the video. Should be blanked in the YAML.
* Vid_MJTruthUltra_UPDATE_Charlie_Kirk_1990936 - silent fixed-camera car-park footage with two yellow arrows added. Nothing on screen ties the arrowed vehicles to the rental-car claim it was posted alongside; no plate, no timestamp, no location.
* PRIVACY - Vid_MJTruthUltra_UPDATE_Charlie_Kirk_1990575 reads out and displays four vehicle registration plates attributed to people who have been accused of nothing. Plates deliberately NOT reproduced on the published page; they should be scrubbed from the ai_description in videos.yaml.
* PRIVACY - Vid_Ryan_Matta_2_2yFNVp1 ai_description records a vehicle licence plate. Suppressed on the page; scrub from the YAML.
* Vid_John_Basham_BREAKING_Newly_1966008 and Vid_Mr_Commonsense_Shaunmmaguire_Newly_1966324 - both are short music-backed re-cuts of the footage in Vid_Shaun_Maguire_All_Videos_1965967 with the surrounding ducking crowd edited out. Gemini reads both as "promotional/triumphant highlight clips" precisely because the context is gone. Three nodes, one recording.
* PUBLICATION CAUTION - the Vid_Celebrating_Man cluster attaches an accusation of celebrating a murder to an unidentified private individual on the basis of a few seconds of body language filmed off a TV screen. Written up as presence-only per the site's Curly_Hair_Man page; recommend human review before any of the three is pinned.
* Vid_IanCarrollShow_Ian_Carroll_7_2076529 - the middle of the monologue moves from criticism of a state and a lobby into sweeping dehumanising generalisations about a religious and ethnic group. Recorded as present on the page but not quoted or paraphrased. Flagging so no later pass mines the transcript for quotes.

* Vid_Roof_q354FHR - ai_description is a hallucinated loop: the same handful of sentences repeat with timestamps running past 03:11:00 on a 01:09:43 file. Unusable; page written from the transcription only. Re-run the describer.
* Vid_Roofshooter2_wWrqZub - filed under Roof and Runner Clips but the footage is a 6-second indoor pan across a multicultural info table looking out a window. No rooftop and no rooftop figure anywhere in frame.
* Vid_Roofshooter1_C58bMEh - ai_description places the clip at Butler Community College, El Dorado, Kansas and reads a sign as "SPARKS AUTOMOTIVE". Neither appears anywhere in Charlie_Kirk.txt, and the identical audio track is published elsewhere as UVU shooting-position analysis. Location unresolved.
* Vid_Roofshooter1_C58bMEh and Vid_Jason_Cain_Believe_Have_1965910 - same underlying capture, word-for-word identical audio, two nodes with two different CIDs. Cross-linked on both pages; consider merging.
* Vid_Roofshooter3_Ia_zjRsfyL and Vid_Roofshooter3_ggvQD8N - near-duplicate copies of the same 1:40 surveillance composite (one an Internet Archive pull). Kept as separate pages deliberately since the trimming argument benefits from independent copies, but flagging the duplication.
* Vid_Running1_nCFPcKn - ai_description guesses the crowd scene "resembles a flash mob" or "possibly a promotional giveaway". Contradicted by the sibling clip's audio ("it's a gunshot, I think"). Not used on the page.
* Vid_Project_Constitution_BREAKING_High_1970986 - transcript for a 3:50 file returns one sentence, identical to the audio on Vid_Conman_Please_Share_Video_1977286_2. Either the reel is genuinely near-silent or the transcript is mis-paired; needs re-processing.
* Vid_Conman_Please_Share_Video_1977286 and _1977286_2 - both published under a caption promising "video and pictures of the drone suspected of assassinating". Neither clip contains any airborne object at all. Clip 2's audio also places it AFTER the shot.
* Vid_Mario_Nawfal_DRONE_FOOTAGE_1965990 - media does not match the title. The file shows a bystander catching a dropped bottle at a Prove Me Wrong table, not drone crime-scene footage. Likely a wrong-attachment-index download; re-pull the source post.
* Vid_Jason_Cain_Believe_Have_1965910_2 - ai_description reads a banner as "BYU" while also reading "A PLACE FOR YOU", a UVU slogan seen on banners in several other clips. Almost certainly a misread of UVU; also note the street imagery is dated Nov 2023, two years before the event.
* Vid_CK_Assassination_Lvvoqkb - ai_description characterises the moment of the killing as "a short comedic meme edit" in which the subject is "comically blown up". Badly wrong and offensive; discarded. Re-run the describer.
* Vid_Assass_South_FPRyVZf - filed under The Moment of the Shot with a filename asserting a south-angle argument. Footage is a stage-rush tackle at a Prove Me Wrong event, looped to music, plus one inserted still of a red arrow at Kirk's ear. No shooting, no angle analysis, no acoustics.
* Vid_ZREIKMIESTER_Slow_Motion_Mic_2077921 - titled as a slow-motion mic/LiPO-battery explosion diagram video. The file is a 14-second reaction loop with no diagram, no annotation and no slow motion. Its real value is an unusually clean close view of the lavalier as worn; page written that way.
* PUBLICATION CAUTION - Vid_Project_Constitution_EXPOSED_Charlie_2032617 is not Charlie Kirk material at all. It is 2012 news footage of an unrelated private person with no connection to this case, filed under a sensational headline. It carries no evidentiary value here and should be removed from the public hierarchy.
* PUBLICATION CAUTION - Vid_TPV_Sean_Iranian_Hackers_2039399 sources its entire case to an anonymous "Iranian operative" transmission of hacked emails that are never shown, and from that base makes specific criminal accusations against several named living people, alongside paid ad reads for a VPN and for unproven cancer treatments. Page reports the segment's character and sourcing and deliberately does NOT restate the accusations or name their targets. Recommend human review of whether this belongs on the public site.
* Vid_After2_6arfsun - ai_description identifies the escorted figure as Donald Trump and the location as Milwaukee, Wisconsin. The clip is filed with Sept 10 2025 UVU material and its gravel slope, barricade line and SUV fleet match the other captures in the cluster. Identification not adopted on the page.
* Vid_After2_6arfsun - transcript is an ASR hallucination over crowd noise: invented English fragments followed by the same city name repeated sixteen times. Nothing on the soundtrack corresponds. Should be blanked in the YAML.
* Vid_After5_hAtoSPH - transcript header reports covering 00:00:21 of audio against a 00:00:03 source, and returns only the fragment "I don't". Unusable; blank it.
* Vid_After5_hAtoSPH - ai_description reads the crowd as "cheering", "excited" and calls the clip "fan or event coverage". Three seconds cannot distinguish a cheering crowd from a surging one; the clip is filed with the aftermath on filename alone and nothing in its frames timestamps it.
* Vid_After4_d3MzSj5 - ai_description reads the event tent lettering as "AMERICAN CONSPIRACY". It is the American Comeback Tour canopy.
* Vid_Afternongraphic8_hg8SeRn vs Vid_Afternongraphic8_Ia_bYZmob2 - same nine-minute news pool reel, identical runtime and transcript. Two nodes, one recording. The two description passes disagree on the tripod equipment (camera vs 3D scanner), on the officer name tape (L. LESSLEY vs E. LEGGEY) and on the number of barricaded classrooms. Neither reading is authoritative.
* Vid_Ryan_Matta_3_dP3Mhi4 - filed under "Raw Shooting Footage (Part 3)" but the footage ends before the shot; it is sixteen minutes of the event running normally, closing on a TikTok end card. Also not Ryan Matta's footage: the end card credits creator @caseyjpbryson.
* Vid_Ryan_Matta_3_dP3Mhi4 - transcript is badly degraded word salad over open-air crowd audio. Subject matter (a Q&A about the Church of Jesus Christ of Latter-day Saints) is recoverable; no line in it can carry a quotation.
* Vid_Ryan_Matta_4_gUPPw9v - not raw shooting footage either; it is a talking-head reaction clip relaying a Candace Owens post and a Sam Parker post. Cluster Vid_Raw_Shooting_ce59 is mis-scoped, same defect agent 02 logged for Vid_Raw_Shooting_b200.
* Vid_Timing_qBFKKR8 - ai_description places the venue in South Jordan, Utah. It is UVU, Orem. The split-screen synchronisation is the editor's work and no sync method is shown; treated on the page as a proposed reconstruction, not a verified timestamp.
* Vid_HustleBitch_WALK_THROUGH_UVU_1971954 - transcript returns five isolated stray words. Correct: the walk-through has no narration. Blank it rather than leave the noise.
* Vid_VLuvMully_Cowboy_S_Smokehouse_2077951 - transcript is empty and the header reports no coverage. Correct: twelve silent seconds of a receipt.
* Vid_Project_Constitution_BREAKING_Physics_1980724 - ai_description reads the analysed frames as showing a man in a red cap resembling Donald Trump; the transcript describes them as successive frames of Kirk at the table. Unresolved, and it matters because the whole colour analysis rests on which source images were used.
* Vid_Project_Constitution_BREAKING_Physics_1980724 - should_be_on_pages lists Israel_Main_Suspect/charlie-said-israel-would-kill-him, Planes/SU-BND and CoverUp/Antisemitism_Branding. None of the three bears on a trajectory analysis; only Suspicious/Cause_of_Death/energy-mismatch fits.
* Vid_2071736376215920842_Extracted_x - audio-only extraction of Vid_CatQuestionsAll_Benny_Johnson_Says_2071736, no CID, identical transcript. Two nodes, one recording.
* Vid_ProjectConstitu_Joshua_Peterson_TPUSA_2070467 is a two-minute cut of the same statement held at 2:44 as Vid_M0ssad_Recruit_Emp_1_JR6nHX2. The short cut ends on the alleged admission and drops Peterson's own qualification that he did not know what the organisation understood. Both nodes kept; the difference is flagged on both pages.
* PUBLICATION CAUTION - Vid_FurkanGozukara_Stew_Peters_Segment_2055445 closes with the speaker's stated opinion that a living family member had foreknowledge of, and involvement in, the killing. Not reproduced or paraphrased on the published page. Flagging so no later pass mines the transcript for quotes.
* PUBLICATION CAUTION - Vid_SECURITY_TEAM_W4LpzMV is fourteen minutes of an anonymous narrator speculating about unnamed members of the close-protection detail from slowed-down wide shots. Recommend removal from the public hierarchy.
* Vid_Candace_Myron_kezPsbX - the primary source for the "they are going to kill me" text claim. Nothing is shown on camera: no screenshot, no document, no third party. Owens says "I showed the messages" referring to material outside this excerpt. Worth capturing that longer segment if it can be found.
* Vid_Illuminatibot_VOICE_SKULL_TECHNOLOGY_2033659, Vid_Matrixbot_Professor_Demonstrates_How_2054260 and Vid_Professor_Example_nUPwPTC are ONE recording (Naval Postgraduate School physics lecture demo, transcripts differ only in ASR errors). A fourth copy is already embedded on /Gov_Mind_Control/frey-effect-v2k as @UAPLuigi's "Project Pandora" clip. Four nodes, one demo - consider collapsing.
* Vid_FINAL_CIA_Drones_3L2xrQM and Vid_Full_Drone_2025_Oct_hoQ1YxX have byte-identical transcripts and the same 14:14 runtime. One presentation, two nodes. Vid_RAW_CIA_Drones_GtdgM4K is a single still frame extracted from the same argument.
* Vid_Mrredpillz_Jokaqarmy_Direct_Energy_2010844 - caption overlay claims "Direct Energy Weapons were used in Venezuela"; Venezuela is never mentioned in the congressional testimony the clip actually contains. Caption contradicts content.
* Vid_Voice_God_33DXeAg and Vid_Illuminatibot_VOICE_SKULL_TECHNOLOGY_2033659 - both filed as "voice to skull" but their footage is airborne ultrasonic/LRAD hardware, a different mechanism from microwave hearing. Cluster label is broader than the evidence.
* Vid_Drone_Shot_South_g1FoVJ3 - filename asserts a drone; the two seconds of footage and its ai_description record only crowd, building and sky. No aerial object present. Mis-named, not mis-filed.
* Vid_GoPro_Ring_Radiates_Upward_KFXry5h - ai_description is wrong about the event (calls it Steven Crowder's tour; the branding in frame is TPUSA's American Comeback Tour at UVU) and records no ring artefact anywhere in the 27 seconds. Transcript is ASR hallucination over wind/crowd noise - unusable. Filename claim unverified.
* Vid_FqnNxEdIKfPXgAlj_CCtKidN - ai_description characterises the moment of the shooting as "a physical altercation" and "a scuffle" breaking out behind the tent. The transcript is unambiguous that it is a gunshot. Anyone working from the machine description alone would be badly misled.
* Vid_Kirk_Rifle_Roof_iFybgaD - security-feed timestamp rendered as "2:23:49 PM"; the shot is at 12:23:30 MT, so this is probably a cropped "12:23:49". Needs checking against the original released file, not this phone-of-a-TV capture.
* Vid_GTG_Trinity_Fast_Moving_1986786 - the voiceover is a scripted dramatic monologue about "the cabal", unrelated to Utah or to this case, laid over UVU footage as a soundtrack. Reads as testimony on a skim; it is not. should_be_on_pages for this node lists body-transport-burial, laws/explain/all and Fix/disabled/Law1 - none relevant.
* Vid_Project_Constitution_ICYMI_CIA_1979657 - should_be_on_pages lists /Suspicious/Law_Enforcement/gun-drop-and-search-sequence; the clip is about Utah State University's intelligence centre and has no bearing on that page.
* Vid_2038934507307343872_2038934 - no transcription and no ai_description sidecar exists. Page written from manifest provenance plus the existing write-up on /People/tyler-robinson, which embeds the same CID. Sidecars should be generated.
* PUBLICATION CAUTION - Vid_TPV_Sean_TPUSA_Insider_1982809. Seventeen minutes of allegations about a named living woman's conduct and her family, sourced entirely to an unnamed "whistleblower", with no document, no recording of the source and no corroboration anywhere in the video. Includes a trafficking-adjacent claim about her family. None of it reproduced or paraphrased on the published page. The generated H1 still carries the accusatory X headline verbatim (the node title in videos.yaml) - frontmatter title/sidebar/description were retitled but the H1 cannot be changed from Stage 3. Recommend retitling the node in videos.yaml and human review before this page is pinned or indexed.
* PUBLICATION CAUTION - Vid_Blue_Side_nN7ZYX2. An @DO_NOT_COMPLY edit circling three unidentified private individuals near the stage and asserting via text cards that they exchanged tactical signals and that one concealed and then hid an object at the moment of the shooting. Written up strictly as the poster's claim with the pixel-level and body-language objections stated; no one named, nothing adopted. Recommend human review.
* PUBLICATION CAUTION - Vid_Project_Constitution_TYLER_ROBINSON_1982459. Substantial personal material (mental state, substance use, living conditions, relationship) about a living private individual who has not been charged, sourced to one anonymous acquaintance via a pseudonymous Substack, presented as screenshots rather than verifiable exports. Not reproduced on the published page. The presenter did seek comment three times and received none.
* PUBLICATION CAUTION - Vid_QwGo0LyZ3I_gAQoxPs (Wolves and Finance, TPUSA finances). Presenter states on camera that he has received a cease and desist from Turning Point. Contains a non-expert handwriting inference about a sitting president used to build an interference argument. Written up as allegation throughout, with Robert Barnes's flat on-camera denial carried at equal length per the pairing rule.
* Vid_Redacted_Havana_Syndrome_Real_2035096 - the episode carries two full scripted ad reads (a supplement, and a paid "remove graphene oxide from your body" service the host links twice) and promotes the guests' forthcoming film. Commercial interest is on the face of the broadcast and is noted on the page. Its satellite-plus-cell-tower delivery model also directly contradicts the portable-device congressional testimony in Vid_Mrredpillz_Jokaqarmy_Direct_Energy_2010844, filed in the same cluster.
* Vid_Microphone_Footage_Embedded_Mic_tWFFbU4 - the stored CID QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R is a STILL IMAGE, not a video: /Mic/overview serves it inside an img tag at 1920x1016 and it is also the image on the Photos side. The actual video in that embed block is QmQK5HHckHYVhKPBPAQpHNo9KbYgJSW1ziKLHF9k6WA3a7. The generated page wraps a picture in a video player. Repoint or drop the node.
* Vid_AES_Interview_X2RjiJm and Vid_AES_Interview_Compressed_fb9ndmt - both copies have NO AUDIO STREAM ("[No audio stream - nothing to transcribe]"). The artefact is a six-minute interview whose entire value is the account; it is unrecoverable from either file. Both are also filed under The Microphone Footage while the content is the AES Tennessee plant explosion - they belong with the AES thread.
* Vid_Master_Chief_John_James_1985431 - ai_description is materially wrong and would be offensive if published: it reads the slowed frames as a comic/suggestive gesture and calls the clip satirical. The transcript ("Not counting gang violence") plus the Yrefy/TPUSA backdrop place these frames at UVU at or immediately before the moment of injury. Regenerate the description; do not reuse it.
* Vid_Marissa_Absolute_Proof_Shot_2075401 - ai_description places the scene in West Palm Beach, Florida. The AMERICAN COMEBACK table banner, the 47 caps and the reversed PROVE ME WRONG tent valance are the UVU setup in Orem, Utah. Same error class in Vid_Y4iVm588Tf4kJH3A_T6tf2Sp (Florida, palm trees) and Vid_US_Did_911_Jonaaronbray_2027171.
* Vid_Project_Constitution_MYSTERY_SOLVED_2039801, Vid_Y4iVm588Tf4kJH3A_T6tf2Sp - transcripts are ASR hallucinations over music-only tracks ("Thank you for watching", "Subscribe and join my YouTube agency"). Treat as empty. Both clips are silent annotation reels.
* Vid_Https_3A_2F_2Fx_ENsJFh8 - a ten-second abstract motion-graphic loop, no audio, no people, no location, generated entirely in software. It is a stray asset saved alongside an X post, not evidence, and it is sitting in a citizen-analysis cluster. Candidate for exclude_videos.txt.
* Vid_Conspiracybot_Youre_Seeing_Im_2031633 - filed under Citizen Analysis of the Footage; it is a c.2011 high-school-gym clip of Charlie Kirk and belongs under Vid_Charlie_His_Own.
* Vid_Force_ViKu1111_MrsErikaKirk_Legend_2031298 - filed under Citizen Analysis of the Footage; it is a Max Blumenthal split-screen political compilation containing no UVU footage and nothing forensic.
* Vid_Ryan_2_mc1Jnym - filed under Court Hearing Footage; it contains no court footage at all. It is a driving vlog about a YouTube channel removal. Vid_Ryan_1_ZCvMUxA in the same cluster does carry genuine courtroom video (Jeffrey Nyman for the Kirk family).
* Vid_Kirk_Parents_Hearing_3006_VNvFbTs - no transcription or ai_description sidecar, but videos.md records it as a trim/re-encode of Ryan_1.mp4, whose sidecars exist. Sidecars can be inherited rather than regenerated.
* Vid_ArtifexMemor_Video_Juliandorey_Julian_2079560 - no transcription and no ai_description sidecar, on one of the highest-value items in the corpus (Joe Kent, named former NCTC director, first person). A full transcript already exists on site/docs/intelligence/Joe_Kent_Dorey_Interview.mdx and was used for the write-up. Generate the sidecars.
* Vid_MJTruthUltra_2046414, Vid_MJTruthUltra_2046416, Vid_MJTruthUltra_2046416_2 - file_path points at .mp3 audio extractions while the published CIDs on /Locations/Valhalla and /Locations/Goat_Island serve video/mp4. None of the three has an ai_description. Vid_MJTruthUltra_2046416_2 has a one-word transcript ("Okay") for 25 seconds and needs a visual description generated from the video, since it is the location-analysis clip.
* Vid_MJTruthUltra_2046414 is a shorter cut of the same Tucker Carlson conversation as Vid_FurkanGozukara_Buckley_Carlson_Dismantles_2046380, which is also already published as a standalone page at /Videos/buckley-carlson-kash-patel-valhalla. Three nodes, one conversation.
* Vid_Steve_Cameron_What_Ever_2060792 - /People/olivia-bishop describes her as a private individual named only in unverified online speculation and withholds detail. This clip is a local TV news package in which she gives a named, on-the-record witness interview about passing a man on a residential street. The profile is incomplete and should record the broadcast as a primary, separate basis. Nothing in the footage implies wrongdoing by her.
* Vid_Did_Know_Charlie_Kirk_p7Xm3eS and Vid_Did_Know_Charlie_Kirk_SPmC52p are the same 1:13 reaction edit (MP4 copy and YouTube WebM copy, N9phYmyKE9w). Both are excerpts of Vid_Charlie_Bonhoeffer_uZaC186, the full 32-minute Wallnau broadcast, which is the primary source and should be cited instead.
* PUBLICATION CAUTION - Vid_Whistle_Blower_Patrick_Howley_avKAyVy. A 1:30 silhouetted, hooded "whistleblower" interview making specific unverified allegations about a named living woman, her parents and foreign intelligence. No source, no document, no date, and the closing card sequence is entertainment-channel branding (spider logos, a Wu-Tang-themed Instagram handle), which reads as dramatised rather than recorded testimony. None of the allegations reproduced or paraphrased on the published page. Recommend exclusion review before pinning.
* PUBLICATION CAUTION - Vid_Matrixbot_BOMBSHELL_LEAKED_AUDIO_2036510. Unauthenticated "leaked audio" (black screen, waveform, Stew Peters Show logo) in which the speaker enumerates individuals by ethnicity and asserts foreign control over named living commentators. Unverified provenance, no chain of custody, 83-second excerpt of a longer conversation. Content described but deliberately not reproduced. Recommend exclusion review.
* PUBLICATION CAUTION - Vid_Plan_Martyr_Charlie_Kirk_AT4TRXr. A 57-minute monologue (David Vose, episode 2186) whose Bonhoeffer biography is largely accurate but which is interleaved with an extended ethnic-conspiracy historical theory and unverified assertions about named living people including Masonic-oath claims and an Antichrist identification. Summarised at high level only; no passages quoted. Recommend human review before pinning.
* PUBLICATION CAUTION - Vid_Honest_Ash_Just_Keeps_2075689. A 21-second phone clip of a jogger crossing a desert resort plaza (giant daisy sculptures, glass railings, arid hills - not UVU), carrying chyron-styled overlay text asserting it shows "Charlie Kirk's real shooter escaping", plus two meme-account watermarks. It labels an unidentified private individual as a killer. Written up as a debunk with no one named. Recommend exclusion review.
* Vid_Y4iVm588Tf4kJH3A_T6tf2Sp - the edit places the caption "These are the Assassins" over unidentified members of the crowd and circles the back pocket of an unnamed man in a plaid shirt. Labels not adopted and no one identified on the published page. Flagging so no later pass mines these frames for names.

* Vid_Double_Shot_x3fP97V — ai_description names the seated speaker as a different commentator (Steven Crowder); UVU Review watermark + American Comeback/Prove Me Wrong/yrefy branding say otherwise. Identification unresolved.
* Vid_Short_Video_Captured_Political_RRcZpiS — same misidentification (Steven Crowder) in the ai_description for video/16.mp4; also asserts a questioner line ("Right, not counting") absent from the transcript, and reads the questioner as female.
* Vid_Brief_Handheld_Video_Capturing_jcLZwDJ — ai_description for video/2.mp4 repeatedly calls the footage a "simulated" active-shooter drill, and claims the speaker was tackled and put into a minivan. Both false/unsupported; the ai_description of the identical file 2.ia.mp4 describes neither.
* Vid_Video_Captures_Dramatic_High_UBNwyKh / Vid_Brief_Handheld_Video_Capturing_jcLZwDJ — video/2.ia.mp4 and video/2.mp4 are the same 37s capture (identical transcripts) catalogued as two entries with two contradictory descriptions.
* Vid_2026310419405504514_2026310 / Vid_Darth_Powell_Think_Charlie_2026310 — same X post 2026310419405504514, same 26s footage, ingested twice (repo videos/ and _Mirror) with different sha256/CID. Duplicate pair.
* Vid_MuppetMasher_Compilation_Camera_Witness_2069350 — ai_description says the interviewee identifies "the suspected shooter"; she says twice she is NOT saying he was the shooter. Baseline also carried a private campaign email address and a list of accusatory overlay names; both removed from the page.
* Vid_ZEayucmsJ3z5W_GU_oY392Xa — baseline labelled an unidentified private man in the crowd "(The Suspect)" and reproduced his clothing description on a public page. Removed. Clip accuses him of causing the death and offers a reward to identify him.
* Vid_Project_Constitution_EYEWITNESS_DROPS_1977638 — poster's headline claims "SHOT POINT-BLANK"; the witness never says it and says he saw no one near a shooter. Headline contradicts the clip.
* Vid_Short_Video_Captures_Moment_utQE41v — ai_description guesses the venue as Phoenix, Arizona; it is UVU, Orem.
* Vid_AMeadowInquiry_Cabot_Phillips_Alibi_2011947 — ai_description guesses Los Angeles; the carpet-comparison claim asserts Fort Huachuca. Neither is established; interior finishes are generic.
* Vid_Blake_Frank_FT_Call_2062655 — ai_description labels the man on stage "Frank"; Frank Turek is the man holding the phone in the audience area. Who-is-who is wrong.
* Vid_Blake_Bednarz_Source_1984320 — ai_description assigns the clip to a differently named debate series and describes clothing that does not match Sept 10, 2025.
* Vid_TRILLION_Tried_Animate_Bullet_1999703, Vid_Darth_Powell_Think_Charlie_2026310, Vid_2026310419405504514_2026310 — transcripts are single stray tokens; these clips have no speech at all, so "empty transcript" here is correct rather than a failure.
* Vid_VigilantFox_Eyewitness_One_Pop_ttYzPo9, Vid_TND_Eyewitness_Like_Direct_9uxwgCE, Vid_Charlie_Ward77_TV_News_1AbVTQN, Vid_Maxwell1995Vjjo_TV_Witness_Re_hfCTmz6, Vid_AmericaOnly76_Video_Realstewpeters_Stew_2079684 — no transcription or ai_description sidecar exists at all; quotes had to be recovered from host pages and Charlie_Kirk.txt.
* Vid_15_Very_End_MdNUL81 — 10:16 transcript is heavily garbled through the theology section (proper nouns and scripture references defeat the recogniser); re-transcribe with a stronger engine.

============================================================
FINDINGS — p_level2_update.md run (2026-07-23, navigation rework)
============================================================

Rewrote gen_videos_pages.py cluster/L2 emission to match the Photos Level 2
model (two-column flex TOC at top, prose after, Related Areas with written-record
cross-link + up-link + peer clusters). Read-only wrt videos.yaml. Items for
p_update_video_hierarchy.md, not fixed here:

* YAML bloat: 1,395 of 1,559 cluster nodes are empty (0 videos in their whole
  subtree) — inherited mirror-directory skeleton. They are correctly skipped at
  publish time (no page, no TOC entry), but they inflate the tree and slow every
  walk. Consider pruning empty nodes in the hierarchy build.
* CID→JPEG mismatch: Vid_Microphone_Footage_Embedded_Mic_tWFFbU4
  (cid QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R) resolves to a JPEG, not
  video. Player correctly withheld; the entry should be re-checked in the YAML.
* Media pending (11): 9 no-media, 1 no-cid, 1 not-video — rendered with honest
  "media pending" notes, no dead players.
* Large nodes to review for needs_split: Vid_UVU_Venue (99 own / 103 recursive).

================================================================
p_next_buttons.md RUN — 2026-07-23
================================================================

Carried out videos_planning/p_next_buttons.md. Precondition gate PASSED
(0 image file_paths, 0 "This image" prose, 383/400 = 95% CID coverage).

WHAT WAS DONE
  * Extended generator/gen_videos_pages.py to (a) compute one global
    document-pre-order "Next Video" chain over the 369 published video pages,
    looping last->first, and (b) render a dark-navy (#0d2b6b) "Next Video" pill
    with white label + white right chevron directly under each player, styled by
    a new ck-video-next rule inside the CK_VIDEO_LAYOUT block of custom.css.
  * Added generator/set_next_video.py — surgically writes next_video into
    videos/videos.yaml from the generator's manifest (generated_pages.json).
    Diff confined to next_video lines only (0 non-next_video lines changed);
    357 shot_timeline block scalars left byte-identical.
  * Build PASSED. Traversal via the actual rendered hrefs is a single cycle of
    length 369 covering every page and returning to start. Cluster-boundary,
    wrap, and media-pending cases all verified. Nothing pinned as a side effect.

FINDINGS FOR A LATER HIERARCHY / SITE PASS
  1. video_page DRIFT (bookkeeping, not a page problem). Every one of the 400
     YAML entries currently carries video_page: "" even though 369 Level 5 pages
     exist on disk and are correct. bind_video_pages.py (Stage 12) + the emit
     step that copies video_page.json into the YAML have not been re-run since
     the last hierarchy rebuild blanked it. This prompt therefore took the
     page->video mapping from the generator's own manifest (the authority that
     mints the pages), not from video_page. ACTION: run p_yaml_to_site.md /
     bind_video_pages so video_page is repopulated; next_video already points at
     the right pages regardless.
  2. One S video has NO cid and NO sha256 — Vid_2071736376215920842_Extracted_x
     (an audio-only .mp3 extraction, file_path
     ~/BGit/Bryan_git/charlie-kirk/videos/2071736376215920842_extracted.mp3).
     next_video was bound to it by file_path fallback. Consider assigning it a
     CID/sha on a later corpus pass.
  3. 11 media-pending pages (no-media 9, no-cid 1, not-video 1): each keeps its
     honest "media pending" note and STILL carries a working Next Video button.
     They are real destinations in the loop.
  4. 1 CID whose bytes are a JPEG, player correctly withheld:
     Vid_Microphone_Footage_Embedded_Mic — CID
     QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R resolves to image/jpeg. Page
     is media-pending "not-video". Needs a correct video CID on a later pass.
  5. The old CK_NEXT_BUTTON_START/END marker wrapper (from an earlier button
     design) was retired: the button is now an integral part of the full page
     the generator rewrites each run, matching how the player and back button
     are emitted. No page carries the stale markers and none has a double button.
  6. A concurrent external repo process ("Bryan 26 Tower") was editing many
     unrelated pages (adding {/* CK_AUTHOR_CREDIT */} author-credit blocks under
     Photos/, After/, Topics3/, etc.) DURING this run. Those edits are not from
     this pipeline; this run only wrote videos.yaml (next_video), site/docs/Videos/**,
     the CK_VIDEO_LAYOUT block of custom.css, video_posters, the Videos
     overview TOC, and pages.csv video rows.
