# Four Squares — Resume Instructions

State as of the last checkpoint:

    pages complete : 1539 of 1731  (88%)
    partial pages  : 0            (every page is all-four-blocks or none)
    cards on site  : 12248
    teasers banked : 1615
    remaining      : 192
    last full site verification: 1521 files, 0 failing (placement check included)

Wave 5 was launched for the final 363 pages. Agents 1, 3, 4, 6, 7 and 12
finished; six died on an API auth error ("Not logged in"), which is an
infrastructure failure, not a content problem. Nothing was left half-written —
the ledger shows 0 partial pages.

## To resume

1. Re-deal the remaining work. The ledger is the source of truth, so this is
   safe to run at any time and never re-does finished pages:

       cd ~/BGit/Bryan_git/charlie-kirk
       FSQ_BATCH=32 python3 prompts/four_squares/merge_wave.py resume --deal

   The tail is concentrated in Influencers and People. If most agents come back
   with tiny batches, re-run the lend-capacity dealer used for wave 5 (it is
   described in the run notes: give each agent its own remaining work first,
   then top up from the global pool, and tell each agent which extra areas it
   may edit that wave).

2. Launch 12 agents at high effort, one per batch file, using the wave-5 prompt
   text as the template. Each agent needs: its areas, its batch file, and the
   standing rules — all of which live in AGENT_BRIEF.md.

3. After every wave, in this order:

       python3 prompts/four_squares/harvest_teasers.py
       python3 prompts/four_squares/fix_broken_links.py --apply
       python3 prompts/four_squares/fix_double_escape.py --apply
       python3 prompts/four_squares/fix_escaped_anchors.py --apply
       python3 prompts/four_squares/relocate_blocks.py --apply
       ./prompts/four_squares/check_site.sh          # must end "0 failing"
       python3 prompts/four_squares/merge_wave.py <label>

   Only pass --deal when you are ready to start the NEXT wave; dealing during a
   wave changes batch files under running agents.

4. Regenerate routes.txt from the build whenever the site is rebuilt:

       python3 prompts/four_squares/build_routes.py

   Never let build_card_index.py own that file.

## Open items for a human

* site/docs/TPUSA/TPUSA.mdx is unreachable — the filename collides with the
  TPUSA/ directory, so the build serves no /TPUSA/TPUSA route. Rename, merge
  into /TPUSA/overview, or delete. Nothing links to it now.
* Panguitch_Timeline_Infographic.jpg keeps audit_image_publication.py red.
  images.yaml holds two entries for the same picture (9 MB original and a
  929 KB served copy, different shas), so the sha-keyed audit reports the
  original as unserved. It is on no page. Image-pipeline issue, not this pass.
