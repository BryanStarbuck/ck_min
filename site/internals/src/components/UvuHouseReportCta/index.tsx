import React from 'react';

// Entry point into /UVU/UVU_House_Report ("Critical Request: UVU House Report").
// Placed on ~50 pages. The animated GIF is stored ONCE in
// internals/static/img/uvu_house_report/ and every page reuses that one URL.
//
//   <UvuHouseReportCta />             button + three sentences
//   <UvuHouseReportCta gif={85} />    + the animated slide GIF at 85% width (Level 2 pages)
//   <UvuHouseReportCta gif={50} />    + the GIF at 50% width (topic pages)

export const UVU_HOUSE_REPORT_URL = '/UVU/UVU_House_Report';
export const UVU_HOUSE_REPORT_GIF = '/img/uvu_house_report/uvu_house_report_animated.gif';

type Props = {gif?: number};

export default function UvuHouseReportCta({gif}: Props): JSX.Element {
  return (
    <div
      className="ck-uvu-house-cta"
      style={{
        clear: 'both',
        margin: '1.8rem 0',
        padding: '1.2rem 1.4rem',
        border: '3px solid #d62828',
        borderRadius: '10px',
        background: 'rgba(214,40,40,0.07)',
      }}>
      <a
        href={UVU_HOUSE_REPORT_URL}
        style={{
          display: 'inline-block',
          padding: '0.95rem 1.8rem',
          background: '#d62828',
          color: '#fff',
          borderRadius: '8px',
          fontSize: '1.25rem',
          fontWeight: 800,
          letterSpacing: '0.02em',
          textDecoration: 'none',
          boxShadow: '0 3px 10px rgba(0,0,0,.3)',
        }}>
        🚨 Critical Request: UVU House Report →
      </a>
      <p style={{margin: '0.9rem 0 0', fontSize: '1.05rem', lineHeight: 1.55}}>
        UVU's 158-page After-Action Report never once mentions the house UVU owns on the hill
        above the construction site, <strong>691 W 925 S</strong>, even though the rooftop man's
        exit path ran right beside it and the rifle was found at the base of that hill. Who was
        in that house on September 10, and whose vehicles were parked in front, may be the single
        fastest way to crack open who really carried out Charlie Kirk's assassination. UVU holds
        the keys, the approvals, and the records, so we all need to ask UVU to release a{' '}
        <a href={UVU_HOUSE_REPORT_URL}>
          <strong>"UVU House / Charlie Kirk Report"</strong>
        </a>
        .
      </p>
      {gif ? (
        <a href={UVU_HOUSE_REPORT_URL} style={{display: 'block', marginTop: '1rem'}}>
          <img
            src={UVU_HOUSE_REPORT_GIF}
            alt="Animated slides: the UVU-owned house at 691 W 925 S, the vehicles parked in front on September 10, 2025, the rooftop man's exit path, and where the gun was found. HolonCitizen asks UVU to release a UVU House / Charlie Kirk Report."
            loading="lazy"
            style={{
              width: `${gif}%`,
              maxWidth: '100%',
              height: 'auto',
              display: 'block',
              borderRadius: '6px',
              boxShadow: '0 3px 12px rgba(0,0,0,.3)',
            }}
          />
        </a>
      ) : null}
    </div>
  );
}
