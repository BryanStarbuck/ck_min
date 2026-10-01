#!/bin/sh
# IPFS evidence files for the Charlie Kirk investigation.
# Run on any machine with IPFS installed and the daemon running.
#
# ipfs pin add <CID>
#   Fetches the content from the IPFS network into your local node
#   and pins it so it is never garbage-collected. Pinned nodes
#   rebroadcast the content to other peers — keeping the evidence live.
#
# If you also want the file written to disk as a regular file:
#   ipfs get -o <path> <CID>

# Blake Bednarz UVU original Metadata Report from my file.txt
ipfs pin add QmaXvzn9BSV44J9bLgvi9ZTz7uKNPmyqzErZgR4gEiaApL

# Blake Bednarz UVU video_forensic_information_sheet.pdf
ipfs pin add QmUT8ZdgWfDsk38NPBytTWsshbwwcnwNEqoDo4HCUXWjTJ

# Video files go one level deeper into the videos/ subdirectory.
# To write the video to disk: ipfs get -o videos/ <CID>
# Blake Bednarz UVU original.MP4  (~3 GB)
ipfs pin add QmP2eKb15evsp4wWAJZaLXxq8wtXrLNEvoRSTzvm3sWYBc

# 2045200557531435037.mp4 — @RealCandaceO · 2026-04-17
# Candace Owens explains Tyler Robinson hearing; demands FBI release discovery documents
ipfs pin add QmeC1zcPBzgp9REfTbH7Hz1kyoL6P2kyQcYxoYTbMbLvGq
