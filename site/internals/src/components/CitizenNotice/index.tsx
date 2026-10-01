/**
 * CitizenNotice — the right-hand notice rail (the "right bar").
 *
 * Rendered once, as site chrome, by the `Root` swizzle at site/src/theme/Root.tsx.
 * It therefore appears on every page of the site. It is NOT page content, it is
 * NOT tied to any page list, and it does NOT replace, hide, move, or compete
 * with the table of contents — the TOC keeps its own column, untouched.
 *
 * THE WORDING DOES NOT LIVE HERE
 * ------------------------------
 * Every word on the rail comes from internals/src/data/right_bar.json, which is
 * generated from the master text file
 *
 *     ~/BGit/all/politics/charlie_kirk/ck/docusaurus/right_bar.txt
 *
 * by `python3 tools/sync_right_bar.py` (run from the repo root). To change the
 * rail, edit right_bar.txt and re-run the script. Do not type copy into this
 * component and do not hand-edit the JSON — the next sync overwrites it.
 *
 * THE SHAPE
 * ---------
 * Two halves split by a rule: the notice above (lead + body), the corrections
 * desk below (the call to action + the email). A reader who only reads the
 * bottom half still knows what to do. The email is always a mailto: link.
 *
 * The full right_bar.txt wording is taller than a laptop screen at 100px wide,
 * so on desktop the corrections half is pinned to the bottom of the rail and
 * only the notice half above it scrolls. The email is never below the fold.
 *
 * Width and placement live in the CK_CITIZEN_NOTICE block of
 * internals/src/css/custom.css, not here.
 */
import React from 'react';

import rightBar from '@site/internals/src/data/right_bar.json';

const MAILTO_SUBJECT = 'Correction to whoassassinatedcharliekirk.com';

export default function CitizenNotice(): JSX.Element {
  const {lead, body, action, email_label: emailLabel, email} = rightBar;
  const mailto = `mailto:${email}?subject=${encodeURIComponent(MAILTO_SUBJECT)}`;

  return (
    <aside
      className="ck-rail"
      role="complementary"
      aria-label="About the information on this site"
    >
      <div className="ck-rail__notice">
        <p className="ck-rail__lead">{lead}</p>

        {body.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </div>

      <div className="ck-rail__action">
        <p className="ck-rail__cta">{action}</p>

        {emailLabel && <p className="ck-rail__email-label">{emailLabel}</p>}

        <p className="ck-rail__email">
          <a href={mailto} aria-label={`Email ${email}`}>
            {email}
          </a>
        </p>
      </div>
    </aside>
  );
}
