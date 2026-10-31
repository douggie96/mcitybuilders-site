/**
 * Single source of truth for NAP and site-wide facts.
 * NOTHING here may be invented. Every value is carried from the live site,
 * CANONICAL_NAP.md, or the Google Business Profile.
 * Values marked VERIFY must be re-read on the day of publication.
 */
export const SITE = {
  name: 'Maverick City Builders',
  legalName: 'Maverick City Builders',
  url: 'https://mcitybuilders.com',
  phone: '(508) 656-7436',
  phoneHref: 'tel:+15086567436',
  email: 'douglas@mcitybuilders.com',
  address: {
    street: '1171 Main St',
    locality: 'Lancaster',
    region: 'MA',
    postalCode: '01523',
    country: 'US',
  },
  addressNote: 'Office visits by appointment',
  geo: { lat: 42.4556, lng: -71.6731 },
  owner: 'Douglas Mourao',
  // Douglas's standing rule: the HIC/CSL registration number is never published.
  // Massachusetts HIC advertising rules require the registration number to appear
  // wherever registration is claimed, so with the number withheld NO licensing or
  // insurance claim may appear anywhere on the site. This string is the footer
  // line and must stay free of any such claim.
  licensing: 'Lancaster, Massachusetts',
  social: {
    facebook: 'https://www.facebook.com/mcitybuilders',
    instagram: 'https://www.instagram.com/mcitybuilders',
  },
  crm: {
    endpoint: 'https://backend.leadconnectorhq.com/external-tracking/events',
    locationId: 'b5lmCvdlpVkhC4JOVBjd',
    trackingId: 'tk_e76468050a3e42e0b65b2fa5b3c87a7f',
  },
  analytics: { ga4: 'G-7HXJQJL5Q2', metaPixel: '1750236342810025' },
} as const;

/**
 * Claims that must be verified against a primary source before they appear on
 * any published page. Until verified they render as null and the component
 * that would use them omits the whole block.
 */
export const UNVERIFIED = {
  projectCount: null,     // VERIFY — "60+ projects" was never substantiated
  rating: null,           // VERIFY — read from live GBP on publication day
  reviewCount: null,      // VERIFY — same
  yearsInBusiness: null,  // VERIFY
  crewSize: null,         // VERIFY
} as const;

/** SERVICES. Roofing is deliberately absent and must never be added. */
export const SERVICES = [
  { slug: 'kitchen-remodeling',   title: 'Kitchen remodeling',   room: 'Kitchen',
    blurb: 'Layout changes, cabinetry, counters, tile and the electrical and plumbing behind them.', img: '/hero/K4_finished.jpg', real: false },
  { slug: 'bathroom-remodeling',  title: 'Bathroom remodeling',  room: 'Bathroom',
    blurb: 'Full gut renovations, walk-in showers, tile, vanities and ventilation done properly.', img: '/rooms/bathroom.jpg', real: false },
  { slug: 'general-renovations',  title: 'General renovations',  room: 'Living room',
    blurb: 'Whole-home and multi-room work, from opening up a floor plan to finishing a basement.', img: '/rooms/basement.jpg', real: false },
  { slug: 'carpentry',            title: 'Carpentry',            room: 'Staircase',
    blurb: 'Finish carpentry, built-ins, trim, stairs and the framing that sits behind them.', img: '/rooms/stairs.jpg', real: false },
  { slug: 'deck-building',        title: 'Deck building',        room: 'Deck',
    blurb: 'Composite and wood decks, railings, stairs and structural repair of existing decks.', img: '/rooms/deck.jpg', real: false },
  { slug: 'interior-painting',    title: 'Interior painting',    room: 'Interior',
    blurb: 'Prep-first interior painting: patching, priming and a finish that holds up.', img: '/rooms/living.jpg', real: false },
  { slug: 'exterior-painting',    title: 'Exterior painting',    room: 'Exterior',
    blurb: 'Scraping, priming and painting exteriors on a Massachusetts weather schedule.', img: '/rooms/exterior.jpg', real: false },
  { slug: 'building-restoration', title: 'Building restoration', room: 'Structure',
    blurb: 'Rot repair, sill and structural work, sheathing and envelope repairs on older homes.', img: '/work/worcester-ma-rot-repair-dormer-opened-up-800.webp', real: true },
  { slug: 'water-damage-restoration', title: 'Water damage restoration', room: 'Structure',
    blurb: 'Locating the source, removing what is compromised and rebuilding it correctly.', img: '/work/worcester-ma-rot-repair-new-sheathing-flashing-800.webp', real: true },
] as const;

/** The four-step Maverick Process. */
export const PROCESS = [
  { n: '01', title: 'We come and look',
    body: 'A real site visit, not a phone quote. Measurements, existing conditions, photographs, and an honest conversation about what the work actually involves.' },
  { n: '02', title: 'You get a written scope',
    body: 'A line-by-line scope and price. What is included, what is not, and what we would flag as a risk before anyone signs anything.' },
  { n: '03', title: 'We build it',
    body: 'Permits pulled where they are required. A crew that shows up, protects the rest of your house, and tells you when something changes.' },
  { n: '04', title: 'We finish it',
    body: 'Punch list closed out, site cleaned, and a walkthrough before we call it done. If something is wrong afterwards, you call us.' },
] as const;
