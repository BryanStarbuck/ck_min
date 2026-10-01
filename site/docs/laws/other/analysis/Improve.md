# Attorney Analysis: Improvements for the Four Charlie Kirk Disclosure Laws

**Analyst Role:** Attorney reviewing proposed federal legislation for enforceability, constitutional vulnerability, scope issues, and improvements
**Scope:** All four laws (Law 1 DoJ/FBI, Law 2 US Intel, Law 3 Mandatory Investigation, Law 4 Trusted Investigators) and the Discovery document
**Date:** March 19, 2026

---

## CRITICAL IMPROVEMENTS (Highest Priority)

### 1. Schedule A Item Count Inconsistency Across Laws — Creates Ambiguity and Enforcement Risk

**Problem:** The four laws reference different Schedule A item counts: Law 1 references "213 Critical Disclosure Items," Law 2 references "214 Critical Disclosure Items," Law 3 references "208 Critical Disclosure Items," and Law 4 references "208 Critical Disclosure Items." The actual Schedule A content in each law file also varies. This inconsistency creates a serious ambiguity that agencies will exploit. An agency could argue it complied with Law 3's 208 items while ignoring the additional items in Law 1's 213 or Law 2's 214.

**Why it matters:** Any agency defending non-compliance will point to the discrepancy and argue the statute is ambiguous about what is actually required, invoking the rule of lenity (ambiguity in criminal statutes resolved in favor of the defendant). This could gut the criminal enforcement provisions.

**Fix:** Harmonize all four laws to reference the same Schedule A with the same item count. Use a single canonical version maintained at the GitHub repository. All four laws should reference the same number. If items were added to some laws but not others, those additions must be propagated to all four.

---

### 2. Appointments Clause Vulnerability for Law 4's Designated Trusted Investigators

**Problem:** Law 4 names 17 private citizens as Designated Trusted Investigators with authority to issue subpoenas, compel testimony, administer oaths, conduct depositions, and exercise powers equivalent to federal officers. This almost certainly violates the Appointments Clause (Article II, Section 2). Under *Lucia v. SEC* (2018) and *Buckley v. Valeo* (1976), any officer exercising "significant authority pursuant to the laws of the United States" must be appointed through constitutionally prescribed channels (nomination by the President and confirmation by the Senate for principal officers, or appointment by the President, courts, or department heads for inferior officers). Congress cannot directly appoint officers who exercise executive power.

**Why it matters:** This is the single most likely basis for a facial constitutional challenge that could invalidate all of Law 4. The law already addresses this for government-employee investigators (Section 1(a-1)) but does not address the core constitutional problem: Congress is directly naming private citizens to exercise coercive government authority.

**Fix:** Restructure Law 4 so that the 17 named individuals are nominated by the President and confirmed by the Senate (or appointed by a court), rather than directly named by statute. Alternatively, structure them as congressional agents exercising legislative oversight authority (analogous to the GAO or CBO), rather than executive investigative authority. A third option: have the independent review board (appointed by constitutionally proper methods) designate these individuals, using the statutory list as a mandatory short-list from which the board must select. Any of these fixes preserves the intent while avoiding the Appointments Clause problem.

---

### 3. Automatic Budget Reductions May Violate Appropriations Clause

**Problem:** Laws 1, 2, 3, and 4 all impose automatic, self-executing budget reductions (25% per month in Laws 1/2, 10% per month in Law 4) upon certification of non-compliance. The Constitution vests the power of the purse exclusively in Congress (Article I, Section 9, Clause 7). While Congress can prospectively condition appropriations, delegating the power to trigger budget cuts to a review board (which is not Congress itself) raises serious constitutional questions. The Supreme Court in *Clinton v. City of New York* (1998) struck down the Line Item Veto Act precisely because it gave the President unilateral power to cancel appropriations. Similarly, delegating budget-cut authority to a review board may be struck down as an unconstitutional delegation of the appropriations power to a non-congressional body.

**Why it matters:** If the budget reduction provisions are struck down, the laws lose their most powerful enforcement mechanism beyond criminal prosecution (which requires DOJ cooperation — the very entity being compelled).

**Fix:** Restructure the budget reductions as congressionally self-executing sequester-style reductions triggered by calendar deadlines (similar to the Budget Control Act of 2011 sequester), rather than reductions triggered by a review board certification. Alternatively, have the review board certification trigger a mandatory congressional vote within 14 days (similar to the War Powers Resolution mechanism), with the reduction taking effect automatically if Congress does not affirmatively vote to override. This keeps the power in Congress's hands while creating a strong default toward enforcement.

---

### 4. No Exhumation Authority for Independent Forensic Examination

**Problem:** The investigation notes indicate no autopsy was performed on Charlie Kirk despite Utah Code 26B-8-205 requiring it for gun violence deaths. Law 3 (Section 3A) mandates investigation of the autopsy failure but does not provide explicit statutory authority to exhume and conduct a full independent autopsy. Without this, investigation teams can only investigate the failure to autopsy — they cannot actually perform the autopsy.

**Why it matters:** The autopsy is potentially the single most important piece of evidence in the entire investigation. Without the actual forensic examination, many of the Schedule A items (exploding microphone theory, alternative caliber, wound trajectory, explosive residue) cannot be definitively resolved. The investigation would be investigating an absence rather than creating new evidence.

**Fix:** Add explicit exhumation authority to Laws 3 and 4, authorizing investigation teams and Designated Trusted Investigators to petition a federal court for an order authorizing exhumation and independent forensic examination by pathologists selected by the investigation teams (not by any covered agency). Include provisions for: (a) the family to be notified and given opportunity to be heard but not to veto; (b) chain of custody requirements; (c) multiple independent pathologists from different institutions; (d) all findings to be publicly disclosed.

---

### 5. Statute of Limitations for Criminal Penalties Is Excessive and Vulnerable

**Problem:** Laws 1 and 2 set a 45-year statute of limitations for criminal offenses under the Act. While the intent is to prevent running out the clock, a 45-year statute of limitations is unprecedented for disclosure offenses and may be challenged as violating due process (inability to mount a defense after decades) or as arbitrary and capricious. By comparison, the general federal statute of limitations is 5 years (18 U.S.C. 3282), and even for the most serious non-capital offenses the longest is typically 10 years.

**Why it matters:** A court might strike the 45-year provision as unreasonable, which would leave the criminal penalties with no specified limitations period — defaulting to the 5-year general federal statute. This is worse than having a reasonable but extended period.

**Fix:** Reduce to 10-15 years from the date of discovery (not from the date of the offense), with a tolling provision that suspends the limitations period during any period of active concealment. This is legally defensible — many fraud statutes use discovery-based limitations with tolling. It achieves the same anti-running-the-clock purpose without the constitutional vulnerability.

---

## HIGH PRIORITY IMPROVEMENTS

### 6. Section Numbering Gap in Law 1 — Missing Section 1

**Problem:** Law 1 jumps from "Section 0: Congressional Findings" to "Section 2: Broad Mandatory Disclosure" — there is no Section 1. The Definitions section (which should logically be Section 1) appears after Section 12K near the end of the document. This is structurally unusual for legislation and will cause confusion. Moreover, the definitions appear in two places (once as "Section 1" near the end, and separately as "Supplemental Definitions" further below), creating potential inconsistency.

**Why it matters:** Courts interpreting statutes look at structure. Having definitions at the end rather than near the beginning, with duplicative supplemental definitions, invites arguments that a term used early in the statute was not defined at the point of use, or that the supplemental definition (which controls in case of conflict per its own terms) was added as an afterthought and should be given less weight.

**Fix:** Move Section 1 (Definitions) to its proper position between Section 0 and Section 2. Merge the Supplemental Definitions into Section 1. Eliminate all duplicative definitions — one definition per term, in one location.

---

### 7. Private Right of Action Notice Period Inconsistency

**Problem:** Law 1 requires 14 days' written notice before a citizen can bring suit to compel compliance (Section 9(a)). Laws 2 and 4 require 60 days' notice (Law 2 Section 10(a); Law 4 Section 10C(a)). Law 3 does not appear to have a private right of action at all.

**Why it matters:** The inconsistency in notice periods is exploitable. A 60-day notice period in Laws 2 and 4 is excessive for a disclosure statute with a 30-day compliance deadline — by the time the notice period expires, the agency has been non-compliant for 90 days total. The absence of a private right of action in Law 3 means citizens have no judicial remedy if the mandated investigations are not conducted.

**Fix:** (a) Harmonize all four laws to a 14-day notice period, consistent with Law 1. (b) Add an explicit private right of action to Law 3 allowing citizens to compel the mandated investigations. (c) For all laws, retain the emergency injunction provision (Law 1 Section 9(a-1)) that allows suit without notice when evidence destruction is imminent.

---

### 8. Overly Broad Scope for Private Entity Compliance — Due Process Risk

**Problem:** Law 1 Section 2(e) requires covered agencies to issue subpoenas to private entities for all Schedule A records, with $100,000/day penalties for non-compliance. The scope is enormous — it covers "rental car companies, hotels, Accurate Energetic Systems (AES), banks, telecommunications providers, and any other entity in possession of relevant records." Many of these entities (e.g., every hotel within 20 miles of UVU, every rental car company in Utah) are not parties to the investigation and may not have any relevant records. Requiring them to prove a negative (that they have no responsive records) under threat of $100,000/day penalties raises due process concerns.

**Why it matters:** A small hotel or rental car franchise could face ruinous penalties for failing to produce records it never had. This is a taking without due process and will generate sympathy in court. A judge is more likely to enjoin the entire private entity compliance framework if it appears to impose unreasonable burdens on innocent third parties.

**Fix:** (a) Add a good-faith compliance safe harbor for private entities: if a private entity certifies under oath that it has conducted a reasonable search and possesses no responsive records, it is deemed compliant unless the review board has specific evidence to the contrary. (b) Scale penalties to entity size — $100,000/day for major corporations (banks, telecoms), lower amounts for small businesses. (c) Provide that private entities may petition the review board for an extension of the 30-day deadline upon showing good cause, such as the volume of records to be searched.

---

### 9. Review Board Appointment Structure — Political Imbalance in Law 2

**Problem:** Law 2's review board (Section 9(a)) is appointed: 2 by the Speaker, 2 by the Senate Majority Leader, and 1 by the Senate Minority Leader. This is a 4-1 partisan split favoring the majority party. By contrast, Law 1's review board (Section 8(a)) includes appointments by the Chief Justice and the Comptroller General, providing structural independence from partisan politics.

**Why it matters:** A 4-1 partisan review board undermines the credibility of the oversight mechanism and invites challenges that the board is a political tool rather than an independent oversight body. It also makes the law vulnerable to the argument that it is designed for partisan political purposes rather than genuine transparency.

**Fix:** Adopt Law 1's appointment structure for Law 2 as well: include appointments by the Chief Justice and Comptroller General to ensure non-partisan representation. All four laws should use the same board appointment mechanism, or reference a single unified review board.

---

### 10. Redundant Review Boards Across Laws Create Coordination Chaos

**Problem:** Laws 1 and 2 each establish their own independent review board. Law 3 establishes an "external independent oversight board." Law 4 has Designated Trusted Investigators plus references to the Law 1 review board. This creates potentially four separate oversight bodies, all with subpoena power, all demanding records from the same agencies, with no clear coordination mechanism and potentially conflicting directives.

**Why it matters:** Agencies will exploit the confusion. If the Law 1 review board orders disclosure of a record and the Law 2 review board orders it withheld pending classification review, the agency can claim it is caught between conflicting commands and produce nothing. The administrative burden of responding to four separate oversight bodies also provides a plausible excuse for delay.

**Fix:** Consolidate to a single unified review board referenced by all four laws. If separate boards are truly needed (e.g., to reflect different expertise for law enforcement vs. intelligence oversight), establish a clear hierarchy and coordination protocol, including: (a) which board's order controls in case of conflict; (b) a joint meeting requirement at least monthly; (c) a unified records request portal so agencies receive one consolidated demand rather than four separate ones.

---

### 11. Whistleblower Protection — "Directly to the Public" Disclosure Has No Limits

**Problem:** All four laws authorize whistleblowers to disclose covered information "directly to the public" with full immunity from criminal prosecution, including immunity from the Espionage Act. While protecting whistleblowers is essential, blanket immunity for any public disclosure of classified information — with no requirement of exhausting internal channels first — goes further than any existing whistleblower statute and will face intense opposition. It also creates a national security argument that the law authorizes indiscriminate disclosure of sources and methods.

**Why it matters:** This provision will be the target of a presidential veto, DOJ opposition, and aggressive litigation. If a court strikes the "directly to the public" provision as unconstitutional (implicating the President's Article II authority over classified information), it could drag down the more defensible whistleblower protections with it.

**Fix:** Restructure the whistleblower provisions to require disclosure first to a listed recipient (review board, investigation team, congressional committee) before authorizing direct public disclosure. Add a 14-day waiting period: if the listed recipient fails to act on the disclosure within 14 days, the whistleblower may then disclose to the public with full immunity. This preserves the safety valve while providing a more defensible structure.

---

### 12. Law 3 Cross-Agency Investigation Structure Has a Circular Problem

**Problem:** Law 3 Section 3B assigns cross-agency investigation responsibilities: FBI investigates CIA, CIA investigates FBI, NSA investigates DIA/NRO/NGA, and the IC team investigates NSA. But if the evidence points to collusion between multiple agencies, the entire cross-investigation framework collapses — you cannot have CIA investigate FBI if both are implicated. The conflict-of-interest trigger (Section 4(c)) transfers authority to a special commission, but only after a written certification and 14-day congressional action period.

**Why it matters:** In a scenario where multiple agencies are implicated (which the underlying investigation theory suggests), the cross-agency framework fails immediately and everything depends on the fallback special commission mechanism, which requires 14 days of congressional action. During those 14 days, implicated agencies could destroy evidence.

**Fix:** Add an emergency provision: if two or more agencies are simultaneously implicated, authority transfers immediately (not after 14 days) to a court-appointed Special Master or to the Designated Trusted Investigators under Law 4. Remove the 14-day congressional action period for multi-agency implication scenarios — make the transfer automatic and self-executing, with Congress appointing a permanent commission within 30 days to supersede the interim arrangement.

---

### 13. Discovery Document Uses "Possible" Language That Weakens Legal Force

**Problem:** The Discovery document (Discovery/README.md) extensively uses framing like "(Possible) Linkage #1," "(Possible) Linkage #2," etc. While the disclaimer language is appropriate for defamation protection, the word "possible" in what is intended to be a legal discovery request weakens the document's force. A court or agency receiving a discovery request framed as "possible" linkages may treat them as speculative rather than as legitimate investigative leads requiring response.

**Why it matters:** In formal discovery practice, requests are stated as demands, not as possibilities. A defense attorney would not write "it is possible that the prosecution has exculpatory evidence" — they would write "produce all exculpatory evidence." The "possible" framing gives agencies an easy basis to characterize the entire discovery request as speculative.

**Fix:** Reframe the Discovery document's linkage section to state factual predicates without the "possible" qualifier. For example, instead of "(Possible) Linkage #1: Chain of custody for the rifle shows allegedly potential evidence planting," write: "Linkage #1: The chain of custody for the rifle must be disclosed because it bears on whether evidence was planted." The disclaimer at the top of the document already protects against defamation — the individual items do not need additional hedging.

---

### 14. No Mandatory Exculpatory Disclosure to Defense Counsel for Robinson

**Problem:** While Law 1 Section 12K and Law 2 Section 12I establish statutory Brady obligations, and Law 1 requires disclosure to defense counsel within 5 days, Law 2 requires disclosure within 14 days. Neither Law 3 nor Law 4 contain any Brady codification at all. Moreover, Laws 3 and 4 establish investigation teams that may generate significant new exculpatory evidence through their investigations, but there is no mechanism requiring those investigation teams to share exculpatory findings with Robinson's defense counsel.

**Why it matters:** If a Law 3 or Law 4 investigation team discovers exculpatory evidence (e.g., evidence that another party committed the assassination), and that evidence is not shared with Robinson's defense counsel, it could result in a wrongful conviction. The constitutional Brady obligation applies to prosecutors, not to congressional investigation teams — so there must be an explicit statutory requirement.

**Fix:** Add a mandatory exculpatory disclosure provision to Laws 3 and 4 requiring all investigation teams and Designated Trusted Investigators to share any exculpatory, impeachment, or mitigating evidence with Tyler Robinson's defense counsel within 48 hours of discovery. Harmonize the disclosure timeline across all four laws to 48 hours (not 5 days in Law 1 and 14 days in Law 2).

---

### 15. Foreign Sovereign Immunity Limits on Disclosure

**Problem:** Multiple Schedule A items demand records from or about foreign governments (Egypt, Israel, France) and their intelligence services. The laws override the Third Party Rule and direct MLAT requests, but they do not address the Foreign Sovereign Immunities Act (FSIA, 28 U.S.C. 1602-1611), which generally shields foreign states from jurisdiction. If a foreign government refuses to comply with MLAT requests, there is no enforcement mechanism beyond public shaming (reporting the refusal to Congress).

**Why it matters:** The MLAT process is voluntary — a foreign government can simply refuse. The laws have no mechanism to compel foreign government cooperation, and the FSIA would prevent U.S. courts from issuing orders against foreign governments.

**Fix:** (a) Add a provision authorizing the President to impose diplomatic consequences (e.g., aid reduction, visa restrictions) on foreign governments that refuse to cooperate, with mandatory reporting to Congress. (b) Add a provision that foreign government refusal to cooperate creates an adverse inference that the foreign government possesses evidence of its involvement. (c) Direct the intelligence community to use all lawful intelligence collection methods to obtain the information refused by foreign partners. (d) Consider provisions similar to the Magnitsky Act that authorize sanctions on specific foreign officials who obstruct cooperation.

---

## MODERATE PRIORITY IMPROVEMENTS

### 16. Law 4 Performance Bonus of Up to $1,000,000 Per Person — Excessive and Exploitable

**Problem:** Law 4 Section 3(e)(3) authorizes Designated Trusted Investigators to award mandatory performance bonuses of up to $1,000,000 per individual for "significant investigative breakthroughs," with the Designated Trusted Investigator having "sole discretion." This creates an obvious conflict of interest: a Designated Trusted Investigator could award million-dollar bonuses to team members who produce findings supporting the investigator's preferred narrative, creating a financial incentive for biased investigation.

**Why it matters:** This provision will be used to attack the credibility of the entire investigation. Opponents will argue that investigation findings were purchased rather than discovered. It also creates a risk of fraud — a Designated Trusted Investigator could award bonuses to associates for minimal contributions.

**Fix:** (a) Cap performance bonuses at $50,000 per individual (still generous by government standards). (b) Require approval by the review board, not sole discretion of the Designated Trusted Investigator. (c) Require public disclosure of all bonus recipients, amounts, and the specific findings that justified the bonus.

---

### 17. 30-Day Disclosure Deadline Is Probably Unachievable — Creates an Easy Compliance Defense

**Problem:** All four laws require production of all covered records within 30 days. Given the scope — potentially millions of records across dozens of agencies, some classified, some in legacy systems — full compliance in 30 days is operationally impossible. Agencies will argue in good faith that they tried but could not physically locate, review, and produce all records in 30 days.

**Why it matters:** If the deadline is so unrealistic that no agency can meet it, the automatic penalty provisions kick in universally, which a court may find disproportionate. A court could issue a system-wide stay of penalties, effectively neutering enforcement. This is exactly what happened with the Epstein Files Transparency Act — DOJ produced only a fraction by the deadline and faced no consequences.

**Fix:** The interim milestone structure (7/14/21/30 days) is a good start but should include a "substantial compliance" safe harbor: an agency that has produced 80% of known responsive records by the 30-day deadline and is making good-faith efforts on the remainder receives a 30-day extension before penalties kick in. This preserves the urgency while making the standard legally defensible. The key is that "substantial compliance" must be certified by the review board, not self-certified by the agency.

---

### 18. No Anti-Mootness Provision for the Pending Criminal Case

**Problem:** All four laws reference the pending criminal case *State of Utah v. Tyler Alexander Robinson*. If Robinson pleads guilty, is convicted, or the case is otherwise resolved before the laws are enacted or fully implemented, agencies may argue that the legislative purpose (supporting the defense) is moot. The Brady codification provisions would lose their immediate application.

**Why it matters:** A plea deal or conviction could be used as a basis to argue reduced urgency for disclosure, potentially allowing courts to stay or slow enforcement. The criminal case resolution does not eliminate the need for disclosure, but it weakens the most legally compelling argument (Robinson's Sixth Amendment rights).

**Fix:** Add a provision stating explicitly that the disclosure and investigation mandates of all four laws are independent of and survive the resolution of the Robinson criminal case by any means (plea, conviction, acquittal, dismissal). State that the legislative purpose extends beyond the criminal case to the public's right to know the full truth about the death of a public figure, and that disclosure obligations continue regardless of case outcome.

---

### 19. Repeated Disclaimers in Operative Text — Still Unfixed

**Problem:** All four laws still contain disclaimer paragraphs embedded within operative statutory text at multiple locations. In actual federal legislation, a single disclaimer in the Congressional Findings suffices. Repeated disclaimers create an internal contradiction: the statute demands disclosure of evidence suggesting wrongdoing while simultaneously disclaiming that any wrongdoing occurred.

**Why it matters:** An opposing DOJ counsel will quote the disclaimer back at the statute's drafters: "Congress itself acknowledged these are merely questions, not allegations — therefore there is no compelling interest justifying these extraordinary disclosure requirements." The disclaimers also add length to already-long statutes.

**Fix:** Consolidate all disclaimers to a single location in Section 0 (Congressional Findings) of each law. Remove all other instances from operative text. The single disclaimer should state that the law mandates investigation and disclosure, not that Congress has reached conclusions.

---

### 20. Constitutional Vulnerabilities in No-Presidential-Override Provisions — Partially Fixed

**Problem:** Laws 1 and 2 use an absolute prohibition approach ("The President may not...") without the procedural judicial review mechanism that Law 3 implemented. The Supreme Court has recognized that the President has some inherent Article II authority over executive branch information, particularly classified national security information. An absolute statutory bar with no judicial review mechanism is more vulnerable than a procedural framework that channels presidential assertions through judicial review with a presumption against privilege.

**Why it matters:** If a court strikes the no-override provision in Laws 1 or 2, the President could then unilaterally delay or block disclosure indefinitely — exactly the JFK Records Act failure these laws are designed to prevent.

**Fix:** Adopt Law 3's approach across all four laws: presidential assertions of privilege must be submitted to a three-judge panel within 14 days, with a presumption against privilege, burden of proof on the President (clear and convincing evidence standard), and no delay beyond 30 days without court approval.

---

### 21. Law 3 Lacks Explicit Standalone Operation Clause — Still Unfixed

**Problem:** Laws 1, 2, and 4 contain explicit standalone operation clauses stating they are fully enforceable regardless of whether companion legislation is enacted. Law 3 does not contain such a clause. If Laws 1 and 2 are not enacted, Law 3 references disclosure mechanisms and review boards from those companion statutes without clear fallback authority.

**Why it matters:** If only Law 3 passes, agencies could argue that the investigation mandates are inoperative because the disclosure infrastructure referenced in the law does not exist.

**Fix:** Add a standalone operation clause to Law 3 identical in structure to Law 2 Section 12F(b), stating that Law 3 is fully operative regardless of whether any companion law is enacted, and that any reference to companion law structures vests equivalent authority in Law 3's own external oversight board.

---

### 22. Defense Counsel Pressure Investigation Gap

**Problem:** The investigation notes reference concerns about whether Tyler Robinson's defense attorneys may be pressured by government agencies. None of the four laws address the possibility of agency pressure on defense counsel — e.g., to limit discovery requests or accept plea deals that foreclose investigation.

**Why it matters:** If defense counsel were under such pressure, Brady material may never be used effectively for the defendant or disclosed to the public.

**Fix:** Add a provision in Law 3 or Law 4 authorizing Designated Trusted Investigators or the review board to investigate whether defense counsel in the Robinson case has been subject to government pressure, direction, or influence. If such pressure is found, authorize the court to appoint independent amicus counsel to review all Brady material and make independent disclosure decisions.

---

### 23. No Provision for Grand Jury Proceedings

**Problem:** None of the four laws authorize or require the empaneling of a federal grand jury to investigate the death of Charlie Kirk. The laws focus on disclosure and investigation by executive branch teams, but do not provide a mechanism for criminal accountability through the normal criminal justice process.

**Why it matters:** Without grand jury authority, the investigation teams can produce findings and reports, but cannot bring indictments. The criminal penalties in the laws apply to obstruction of the disclosure/investigation process, but not to the underlying criminal conduct related to the death itself. If the investigation reveals that foreign intelligence operatives or U.S. government officials participated in the assassination, there is no mechanism in these laws to prosecute them for the assassination.

**Fix:** Add a provision in Law 3 authorizing any investigation team or the external oversight board to petition the Attorney General (or, if the AG is recused, the Special Master or independent counsel) to empanel a federal grand jury. If the AG declines within 30 days, authorize the oversight board to appoint independent counsel with grand jury authority.

---

### 24. Gag Order Override May Violate Separation of Powers

**Problem:** Laws 1, 2, and 4 contain provisions overriding state court gag orders in the Robinson criminal case (Law 1 Section 12J, Law 2 Section 12H, Law 4 Section 10B-1). While the Supremacy Clause supports federal preemption of state law, a federal statute that specifically targets a named pending state court case and overrides specific judicial orders in that case raises concerns about congressional interference with judicial proceedings. The Supreme Court in *Plaut v. Spendthrift Farm* (1995) held that Congress cannot retroactively reopen final judgments, and the principles underlying that decision counsel against Congress legislatively overriding specific judicial orders in identified pending cases.

**Why it matters:** A court might hold that the gag order override provisions are unconstitutional as applied — which would leave the gag order in place and prevent the disclosure of some of the most important evidence (witness statements, defense arguments) to the investigation teams.

**Fix:** Rather than legislatively overriding specific judicial orders, create a mechanism for investigation teams to petition the state court (or a federal court on removal) to modify the gag order as it applies to production of records to congressionally authorized investigation teams. Frame it as requesting an accommodation rather than commanding an override. Alternatively, include a general preemption provision (not naming a specific case) stating that state court orders may not restrict production of records to entities operating under federal legislative authority.

---

### 25. Schedule B "People Listed" Definition Is Overly Broad — 4th Amendment Risk

**Problem:** Schedule B (P35) includes "any other person with relevant information" as a catch-all, which combined with the disclosure requirements effectively authorizes the government to investigate any person in connection with the Charlie Kirk case. Category P4 includes "all persons physically present on the Utah Valley University campus on September 10, 2025" — potentially thousands of students and faculty who simply attended class that day. Category P26 includes all persons affiliated with AIPAC, ADL, Heritage Foundation, etc., which could encompass hundreds of thousands of people based solely on political affiliation.

**Why it matters:** Requiring disclosure of records about persons based solely on their physical presence at a university campus or their membership in political organizations raises serious First and Fourth Amendment concerns. A court could strike the entire Schedule B definition as overbroad, taking the whole disclosure framework down with it.

**Fix:** (a) Add a nexus requirement: for categories P4 (all UVU campus persons) and P26 (lobbying organizations), disclosure is required only for persons for whom there is specific, articulable evidence connecting them to the investigation (not merely their presence or affiliation). (b) Remove the catch-all P35 category or narrow it to "any other person for whom a covered agency possesses specific evidence of involvement." (c) Add a privacy protection: for individuals swept in solely by physical presence (P4), only aggregate data (cell tower dumps) should be publicly disclosed; personally identifying information should be disclosed only to investigation teams under seal.

---

### 26. Personal Device Forensic Imaging Requirement — 4th Amendment Problem

**Problem:** Law 1 Section 5(f) requires forensic imaging of "personal cell phones, personal email accounts, personal cloud storage, and encrypted messaging applications" of any person who worked on the investigation. This is essentially a warrantless search of personal devices based solely on employment status. Under *Riley v. California* (2014), law enforcement must obtain a warrant to search a cell phone. A federal statute cannot authorize warrantless forensic imaging of personal devices without meeting Fourth Amendment requirements.

**Why it matters:** This provision will be immediately challenged and likely enjoined, potentially generating an injunction that delays the entire records preservation framework.

**Fix:** Restructure Section 5(f) to require forensic imaging through a judicial order (not a warrantless seizure). Have the review board petition a federal magistrate for imaging orders based on a showing that the person had access to covered records and that imaging is necessary to verify preservation. This preserves the investigative purpose while meeting Fourth Amendment requirements.

---

### 27. No Witness Protection Provisions

**Problem:** The laws extensively address whistleblower protections (retaliation against employees who disclose information) but do not address physical protection of witnesses. The investigation notes describe witness intimidation including threats ("You're the next target"), and the laws themselves allege a pattern of witness suppression. Yet none of the four laws establish a witness protection program or authorize protective measures for witnesses who cooperate.

**Why it matters:** Without witness protection, the elaborate disclosure and investigation framework may produce no new witnesses. People who fear for their safety will not cooperate even with the strongest whistleblower protections if their physical security is not addressed.

**Fix:** Add a provision establishing a witness protection fund (separate from the investigation budget) administered by the U.S. Marshals Service (which already runs WITSEC). Authorize investigation teams to recommend witnesses for protective measures. Include provisions for temporary relocation, identity protection, and security details for cooperating witnesses.

---

### 28. Caliber Error in Law 2 Item #169 — ".386-caliber"

**Problem:** Law 2 Schedule A Item #169 (Unusual Autopsy Findings) references "a .386-caliber bullet." This is not a standard ammunition caliber. The weapon in the government's account is a .30-06 caliber Mauser Model 98 (citizen investigators conclude an [explosive at the microphone](/Mic/overview) killed Charlie, not that rifle). The number ".386" does not correspond to any known cartridge designation. This appears to be a typographical error.

**Why it matters:** In a statute, a factual error in a specific forensic reference undermines credibility and provides a basis for agencies to argue that the drafters lacked technical expertise, calling into question whether other specific claims are similarly erroneous.

**Fix:** Correct to ".30-06 caliber" or, if the intent was to reference a different caliber for comparison purposes, specify the correct caliber designation.

---

## PREVIOUSLY IDENTIFIED ITEMS — STATUS UPDATE

### 29. Constitutional Vulnerabilities (Presidential Override) — PARTIALLY FIXED (from prior analysis)

Laws 1 and 2 still use an absolute prohibition approach. See Item 20 above for the full analysis and fix.

### 30. Repeated Disclaimers — NOT FIXED (from prior analysis)

See Item 19 above.

### 31. Partial Passage Risk (Standalone Fallback) — PARTIALLY FIXED (from prior analysis)

Law 3 still lacks an explicit standalone operation clause. See Item 21 above.

---

## SUMMARY

The most urgent fixes, ranked by importance to the laws surviving constitutional challenge and achieving their intended purpose:

1. **Appointments Clause fix for Law 4** (Item 2) — without this, Law 4 is almost certainly unconstitutional
2. **Schedule A harmonization** (Item 1) — without this, agencies will exploit ambiguity across all four laws
3. **Automatic budget reduction restructuring** (Item 3) — high risk of being struck down, taking the primary enforcement mechanism with it
4. **Exhumation authority** (Item 4) — without this, the most critical forensic evidence cannot be obtained
5. **Statute of limitations reduction** (Item 5) — 45 years is indefensible; 10-15 with tolling achieves the same goal
6. **Schedule B overbreadth narrowing** (Item 25) — 4th Amendment challenge could take down the entire disclosure framework
7. **Unified review board** (Item 10) — coordination chaos among four oversight bodies will paralyze implementation
8. **Whistleblower "directly to public" restructuring** (Item 11) — most likely target for presidential veto
9. **Private right of action harmonization and addition to Law 3** (Item 7)
10. **Anti-mootness provision for criminal case resolution** (Item 18)


## Citizen Investigator Claims on X (Forced Disclosure Discourse)

*(Attributed public commentary about transparency demands — does not rewrite statutory text above.)*

Citizen investigators and legislative advocates on X argue that ordinary FOIA and criminal discovery will not force full production in the Charlie Kirk case, citing **JFK Records Act failures** (agencies missing decades of deadlines; reports of large unreviewed FBI caches) and the **Epstein Files Transparency Act** pattern of partial dumps without a Special Master with teeth. Accounts such as **@HolonCitizen** have promoted a four-law package (FBI/DOJ disclosure, IC disclosure, mandatory investigation, trusted civilian investigators) and named figures including Candace Owens, Dave Smith, Tucker Carlson, Ian Carroll, and others as proposed **trusted investigators** under Law 4-style designs — a **policy proposal**, not an enacted statute.

Parallel media clips recirculated by accounts such as **@FurkanGozukara** claim **Candace Owens** has criticized federal handling of discovery (FBI/ATF files). Counter-posts argue the Robinson case already has DNA, video, and confession-note material unlike JFK and therefore needs no special act. Investigators answer that none of that material shows how Charlie died: the ATF could not tie the autopsy fragment to the rifle, and the physical evidence points to [an explosive at his microphone](/Mic/overview), not the government's .30-06 account. This page records both the **demand for forced disclosure** and the **official-narrative pushback** so readers can judge whether Schedule A-style lists (FBI 302s, cell data, aircraft, drones, ballistics, AV SD cards) match what X investigators say remains withheld.

Related public pages: [Fix overview](/Fix/overview), [laws landing](/laws), Discovery, [explain all four laws](/laws/explain/all/overview).

{/* CK_INTERESTING_HERE_START */}

## Interesting In This Area

* Four bills, four different Schedule A counts: 213, 214, 208 and [208](/laws/other/List_Of_Laws).
* Naming seventeen private citizens in [Law 4](/laws/Trusted_Investigations/Law_4_Trusted_Investigations) invites an Appointments Clause challenge.
* No draft yet authorises exhumation, which [Law 3](/laws/Require_to_Investigate/Law_3_Require_to_Investigate) would need for the medical questions.
* [The fixed file](/laws/other/analysis/Fixed/Improve) records what earlier reviews already closed.

{/* CK_INTERESTING_HERE_END */}

{/* CK_INTERESTING_OTHER_START */}

## Interesting In Other Areas

* [Search-trend spikes](/GoogleSearches/overview) reportedly preceded the event by weeks.
* [The timeline](/Timeline/overview) puts suspect photos out after custody, not before.
* [Legal investigation](/legal_investigation/overview) tracks what the docket shows and what it omits.

{/* CK_INTERESTING_OTHER_END */}

{/* CK_4SQ_SECTION_START */}

## Other Pages In This Section

<div className="ck-4sq">

<div className="ck-4sq-card ck-4sq-stack">
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="/laws/other/analysis/Laws_Not_Complying">Laws Not Complying with Charter (List_Of_Laws.md) -- Comprehensive Analysis</a></p>
    <p className="ck-4sq-text">Every place the four drafts drift from their own charter, item by item: counts that do not match, a Definitions section buried behind Schedule A, and a required disclaimer Law 1 never carries. A charter is only worth something if somebody audits against it.</p>
    <a className="ck-4sq-btn" href="/laws/other/analysis/Laws_Not_Complying">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>
<div className="ck-4sq-card ck-4sq-side">
  <a className="ck-4sq-thumb" href="/laws/other/old/Require_to_Investigate/more/Human_Requirements"><img src="/img/evidence/14f90a40f5d68c452073308d5374fd2d50adcd3ffe0dcbe70a39c967191e9b8e.jpg" data-cid="QmdhWqrdvZMxknDa6fUm4yw5AJQbovKdxoweEwaRGNWcj1" alt="This is a high-resolution photograph or digital scan of a printed document featuring four paragraphs of English text on a white page." loading="lazy" /></a>
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="/laws/other/old/Require_to_Investigate/more/Human_Requirements">Human Requirements: Law 3 - Require Investigation</a></p>
    <p className="ck-4sq-text">The plain-English demand behind Law 3 as first written: disclosure alone is not enough, because an agency can hand over files and still decline to investigate. This is the archived version; <a href="/laws/Require_to_Investigate/more/Human_Requirements">the current one is here</a>.</p>
    <a className="ck-4sq-btn" href="/laws/other/old/Require_to_Investigate/more/Human_Requirements">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>
<div className="ck-4sq-card ck-4sq-stack">
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="/laws/other/old/Trusted_Investigations/more/Output_Analysis">Output Analysis: Law 4 - Trusted Investigations</a></p>
    <p className="ck-4sq-text">The original requirement-by-requirement audit of Law 4, every line marked MET with the section that meets it. Read it beside <a href="/laws/Trusted_Investigations/more/Output_Analysis">the current audit</a> to see what the redraft added.</p>
    <a className="ck-4sq-btn" href="/laws/other/old/Trusted_Investigations/more/Output_Analysis">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>
<div className="ck-4sq-card ck-4sq-stack">
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="/laws/DoJ_FBI/Law_1_DoJ_FBI">Law 1: Charlie Kirk Investigation - DoJ/FBI Forced Disclosure Act</a></p>
    <p className="ck-4sq-text">The full statutory text of the DoJ and FBI disclosure law, modelled on the Epstein Files Act. This is the live draft the <a href="/Fix/overview">Fix section</a> summarises.</p>
    <a className="ck-4sq-btn" href="/laws/DoJ_FBI/Law_1_DoJ_FBI">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>

</div>

{/* CK_4SQ_SECTION_END */}

{/* CK_4SQ_SITEWIDE_START */}

## Elsewhere In The Investigation

<div className="ck-4sq">

<div className="ck-4sq-card ck-4sq-stack">
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="/Legal/FBI-Witness-Intimidation">FBI Witness Intimidation (Claims)</a></p>
    <p className="ck-4sq-text">A witness says he sent the FBI his close-range footage and was then asked to delete it, with a follow-up call to confirm. A second thread concerns free trauma counselling offered to UVU witnesses. Both are recorded as unverified allegations.</p>
    <a className="ck-4sq-btn" href="/Legal/FBI-Witness-Intimidation">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>

</div>

{/* CK_4SQ_SITEWIDE_END */}

{/* CK_AUTHOR_CREDIT */}

*This website's author is [@HolonCitizen](https://x.com/HolonCitizen) on X and [YouTube/@HolonCitizen](https://www.youtube.com/@HolonCitizen). Follow me there.*

## Interesting

* The disclosure list grew to include [Item #182 on a security detail background](/laws/other/analysis/Fixed/Any_more_to_Add), plus witness-intimidation items.
* Research notes flag [memorial domain searches from Arizona and Israel](/Media/Vance-Mission-Continuation) before the killing.
* The world's default account of the case is [a single edited Wikipedia page](/Media/Wikipedia-Coverage), with forensic disputes quarantined.

## Related Areas

<div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0.5rem 2rem',
marginTop:'0.5rem'}}>
<div>

* [Fix the Charlie Kirk Situation](/Fix/overview)
* (Possible) Cover‑up
* Government Evidence

</div>
<div>

* Proof Intel Services
* [Legal Investigation](/legal_investigation/overview)
* FBI

</div>
</div>

## Related

<div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0.5rem 2rem',
marginTop:'0.5rem'}}>
<div>

* [Factual Challenges — REMAINING UNFIXED ITEMS](/laws/other/analysis/Challenges)

</div>
<div>

* [Laws Not Complying with Charter (List_Of_Laws.md) -- Comprehe…](/laws/other/analysis/Laws_Not_Complying)
* [Attorney Analysis: Improvements for Law 1 (DoJ/FBI Forced Dis…](/laws/other/analysis/Fixed/Improve)
* [Charlie Kirk Files Forced Disclosure -- Threat Analysis & Rec…](/laws/other/Worries_By_Each_4_Laws)

</div>
</div>
