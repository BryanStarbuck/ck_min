 
ROOT_DIR dir is ~/BGit/Bryan_git/Charlie_Kirk_175_Critical_To_Expose

Under {ROOT_DIR} dir are 4 directories, which map to the 4 laws we want to pass:
        1_DoJ_FBI
        2_US_Intel
        3_Require_to_Investigate
        4_Trusted_Investigations


ORIGINAL_175_FILE is file {ROOT_DIR}/original/README.md

INPUT_INVESTIGATION_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)

OUTPUT_FILE is file {ROOT_DIR}/other/Slides/Slides.yaml

Your instructions are:
* Read all of this into the context window: INPUT_INVESTIGATION_FILE
* Read all files in {ROOT_DIR}/Discovery/ and {ROOT_DIR}/1_DoJ_FBI/ into the context window.
* Only file to modify or grow is OUTPUT_FILE.

Read the MD file of the law in the first law directory. Read the Charlie_Kirk.txt investigation file, that input_investigation_file. Read those in the context. Come up with this output_file. Grow the contents of that to be a slide deck of what would the contents be of the slides to have this as a video walking through the slides to go introduce this to everybody. Make it 40 slides.

For each slide, include the title text, the points you'll make on there. They don't have to be a bullet list; they could have graphics. You could have three panels; it could have whatever. Output it as a YAML file, hierarchical. There's a top hierarchy, and the second level would be an array of slides underneath there. Have all the properties mapped out that include the title slide, that means the content is structured on slide YAML properties, YAML hierarchy. Have what the speaker speaks through verbally to go with the slide. 





Make sure the claude agent saved out the outputs to the correct one (or more) output files.
