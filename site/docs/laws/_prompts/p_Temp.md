 
ROOT_DIR dir is ~/BGit/Bryan_git/Charlie_Kirk_175_Critical_To_Expose

Under {ROOT_DIR} dir are 4 directories, which map to the 4 laws we want to pass:
        1_DoJ_FBI
        2_US_Intel
        3_Require_to_Investigate
        4_Trusted_Investigations


ORIGINAL_175_FILE is file {ROOT_DIR}/original/README.md

LAW_FOCUS_ON_NOW_DIR is law we focus on now and it's directory is in dir 1_DoJ_FBI

LAW_FOCUS_ON_NOW_FILE is law we focus on now and it's in the existing file {LAW_FOCUS_ON_NOW_DIR}/Law_{which law}.md

OUTPUT_FILE is file {ROOT_DIR}/other/people.md

* we are creating four laws. These are the Charlie Kirk Files Forced Disclosure laws
* They will include what we call the 175 list. These are a numbered list of areas that we need to make sure are fully disclosed. 

* The file LAW_FOCUS_ON_NOW_FILE already exists. Find the file that already exists. Never create a new file.

* This task only has permission to modify one file, and that file is {LAW_FOCUS_ON_NOW_FILE}

* Read all files into the context window that are in {ROOT_DIR}/other/

The Goal of this prompt:
* Find as many different categories of people that we want to include in this law.  See CURRENT_EXAMPLE below. It has too few categories. Find as many as possible.
* Output the results into OUTPUT_FILE.

CURRENT_EXAMPLE:
* "People involved" (PEOPLE_INVOLVED): This definition includes the following:
 a) All TPUSA employees, executives, board members, and donors of over $5 million. It includes TPUSA external contractors, such as the security team. It includes Erika Kirk.
   b) The following People in Utah (that were in Utah 9/10/2025 or 2 months before or after): It includes any US or foreign intelligence.  It includes any FBI that were doing anything or in knowledge of anything related to this case.  It includes anyone on UVU compus 9/10/2025.
   c) It includes any FBI, US or foreign intelligence, or anyone (in the USA or outside of the USA) discussing d.




Below explains how we list the "175 list": 
* Update {LAW_FOCUS_ON_NOW_FILE} so it has Schedule A at the bottom that has a numbered list 1 through 175.
* Those 1 thru 175 come from {ORIGINAL_175_FILE}
* The pattern in the output should match the example Example_175, but with real data put in.
* Titles should generally be 8 words or less.  More in rare cases.
* "{Describe what it includes}" It should full include what we want. It should end with another sentence that is a wide scope for anything else in that area.
   * Example: "Include all information about plans SU-TAA and SU-BND.  Also include information on all information about flights within 2 months before and 2 weeks after on anything related to Charlie Kirk investigation or anyone connected"
   * In the above example, the first sentence makes sure we get some specifics. BUt the second sentence broadens it up.



Example_175:
* #1: {Title}: {Describe what it includes}

* #2: {Title}: {Describe what it includes}

* #3: {Title}: {Describe what it includes}




Make sure the claude agent saved out the outputs to the correct one (or more) output files.
