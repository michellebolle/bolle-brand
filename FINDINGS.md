# Findings, bolle-brand

Short records of things that went wrong in this repo and what now stops them
recurring. One entry per finding, newest first. Opened 10 September 2026 because
BG-01 had nowhere to live.

---

## BG-01, 10 September 2026: a version bump changed the cover and not the footer

**What happened.** The guide carries its version number on 4 surfaces: the cover
meta, the footer line, the `meta name="description"` string and the `og:description`
string. The briefs for v2.3, v2.4, v2.5 and v2.6 each named the cover and the footer
explicitly. The brief for v2.7 named only the cover. It was followed literally, so
the cover went to v2.7 and the footer stayed at v2.6.

**How long it was live.** Shipped in `9576f12` at 2026-09-07 12:30 and corrected in
`dc57aba` at 2026-09-10 11:18, so just under 3 days. During that window the published
guide showed **Version 2.7 on the cover and v2.6 in the footer**, and the link had
been sent to 3 external designers.

**Why it matters more than a typo.** The guide's own confidentiality notice tells
those designers to "check the version on the cover against the live copy before you
rely on it". A document that disagrees with itself about its own version undermines
the instruction it gives for using it.

**Why no check caught it.** `build.py` derives the meta and og strings from the cover,
so those 3 can never drift from each other. That made the version look self consistent
in every automated output. The footer is authored by hand in `brand-guide.html` and
was the one surface nothing compared against anything.

**The fix.** A version bump names every surface carrying the number, not just the
cover. There are 4.

**The check.** `build.py` now reads all 4 version strings back out of the generated
`index.html` and refuses to write when they disagree. It reports the 4 values in the
failure so the odd one out is obvious. This runs on every build, so it cannot be
skipped before a push.

**Related.** The same shape as the stale source trap in `bolle-stockist`: a silent
failure that every existing check passed, because each check was looking at inputs
that agreed with each other rather than at the artefact.
