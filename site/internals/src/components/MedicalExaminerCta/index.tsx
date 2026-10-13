import React from 'react';

// "Medical Examiner" call-to-action: the way into the 3D Body Tour of State's
// Exhibit 11 (the sealed medical examiner report), at the top of the home page.
//
//   <MedicalExaminerCta />
//
// The tour is static HTML under internals/static/scorecard/exhibit/ (copied from
// the charlie-kirk repo by tools/sync_exhibit.py), not a Docusaurus route. So this
// is a plain <a>, never <Link>: React Router would treat the .html path as an app
// route and show the 404 page. Styles: CK_ME_CTA block in internals/src/css/custom.css.

export const BODY_TOUR_URL = '/scorecard/exhibit/body_tour.html';

// A microphone at the centre of a blast.
function MicBlastIcon(): JSX.Element {
  return (
    <svg className="ck-me-cta__icon" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
      <defs>
        <radialGradient id="ckMeBlast" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fff3b0" />
          <stop offset="45%" stopColor="#ffb703" />
          <stop offset="80%" stopColor="#fb5607" />
          <stop offset="100%" stopColor="#d00000" />
        </radialGradient>
      </defs>
      <polygon
        fill="url(#ckMeBlast)"
        points="35.8,1.2 39.3,13.9 48.2,10.4 47.4,20.0 60.5,19.9 51.3,29.3 58.8,35.3 50.1,39.3 56.8,50.7 44.0,47.4 42.5,56.9 34.7,51.3 28.2,62.8 24.7,50.1 15.8,53.6 16.6,44.0 3.5,44.1 12.7,34.7 5.2,28.7 13.9,24.7 7.2,13.3 20.0,16.6 21.5,7.1 29.3,12.7"
      />
      <g transform="rotate(-28 32 32)" stroke="#1b1b1f" strokeWidth="2" strokeLinejoin="round">
        <rect x="25" y="13" width="14" height="20" rx="7" fill="#f4f4f6" />
        <path d="M26 20h12M26 25h12" fill="none" strokeWidth="1.4" />
        <path d="M21 27v1a11 11 0 0 0 22 0v-1" fill="none" strokeLinecap="round" />
        <path d="M32 39v8M26 48h12" fill="none" strokeLinecap="round" />
      </g>
    </svg>
  );
}

export default function MedicalExaminerCta(): JSX.Element {
  return (
    <div className="ck-me-cta">
      <a className="ck-me-cta__btn" href={BODY_TOUR_URL}>
        <MicBlastIcon />
        <span className="ck-me-cta__text">
          <span className="ck-me-cta__label">Medical Examiner</span>
          <span className="ck-me-cta__sub">Exhibit 11's injuries in 3D: a bullet, or a blast at the mic?</span>
        </span>
        <svg className="ck-me-cta__arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </a>
    </div>
  );
}
