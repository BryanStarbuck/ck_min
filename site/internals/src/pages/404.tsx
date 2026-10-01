import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";

// Custom 404 page. Docusaurus will route any unmatched URL here.
// Includes useful internal links so visitors who hit a stale or mistyped URL
// can recover quickly and so search engines can crawl onward from the page.
export default function NotFound(): React.ReactElement {
  return (
    <Layout
      title="Page Not Found"
      description="The page you requested could not be found on the Who Assassinated Charlie Kirk investigation site. Browse the main sections to continue.">
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h1>Page Not Found</h1>
            <p>
              The page you requested could not be found. It may have moved or
              the link may be out of date.
            </p>
            <h2>Main sections</h2>
            <ul>
              <li>
                <Link to="/">Home — Who Assassinated Charlie Kirk</Link>
              </li>
              <li>
                <Link to="/Fix/overview">Fix Laws</Link>
              </li>
              <li>
                <Link to="/Your_Actions_Fix_It/overview">
                  Your Actions Fix It
                </Link>
              </li>
              <li>
                <Link to="/Timeline/overview">Timeline</Link>
              </li>
              <li>
                <Link to="/Cause_of_Death/overview">Cause of Death</Link>
              </li>
              <li>
                <Link to="/Mic/overview">The Microphone</Link>
              </li>
              <li>
                <Link to="/court/overview">Court &amp; Trial</Link>
              </li>
            </ul>
          </div>
        </div>
      </main>
    </Layout>
  );
}
