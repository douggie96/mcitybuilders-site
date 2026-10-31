/**
 * Service-area build matrix. 50-mile radius from Lancaster.
 *
 * Rule 3 was LIFTED by Douglas on 2026-09-11 — the six previously deferred
 * towns (Wayland, Weston, Natick, Sherborn, Wellesley, Dover) are now in scope.
 *
 * `mi` is computed from the Lancaster centroid (42.4556, -71.6731), not asserted.
 * No population figures: they would have to be invented, and invented numbers
 * produce confident bad plans.
 */
export type Ring = 1 | 2 | 3;

export interface Town {
  name: string;
  slug: string;
  county: string;
  mi: number;
  ring: Ring;
  /** true where a page already exists on the live site */
  live: boolean;
}

export const TOWNS: Town[] = [
  // ---- already live (16)
  { name: 'Lancaster',     slug: 'lancaster-ma',     county: 'Worcester',  mi: 0.0,  ring: 1, live: true },
  { name: 'Clinton',       slug: 'clinton-ma',       county: 'Worcester',  mi: 2.8,  ring: 1, live: true },
  { name: 'Bolton',        slug: 'bolton-ma',        county: 'Worcester',  mi: 3.8,  ring: 1, live: true },
  { name: 'Berlin',        slug: 'berlin-ma',        county: 'Worcester',  mi: 5.5,  ring: 1, live: true },
  { name: 'Sterling',      slug: 'sterling-ma',      county: 'Worcester',  mi: 4.8,  ring: 1, live: true },
  { name: 'Harvard',       slug: 'harvard-ma',       county: 'Worcester',  mi: 5.6,  ring: 1, live: true },
  { name: 'Stow',          slug: 'stow-ma',          county: 'Middlesex',  mi: 8.7,  ring: 1, live: true },
  { name: 'Boxborough',    slug: 'boxborough-ma',    county: 'Middlesex',  mi: 8.3,  ring: 1, live: true },
  { name: 'Leominster',    slug: 'leominster-ma',    county: 'Worcester',  mi: 6.5,  ring: 1, live: true },
  { name: 'Hudson',        slug: 'hudson-ma',        county: 'Middlesex',  mi: 7.6,  ring: 1, live: true },
  { name: 'Fitchburg',     slug: 'fitchburg-ma',     county: 'Worcester',  mi: 11.3, ring: 1, live: true },
  { name: 'Marlborough',   slug: 'marlborough-ma',   county: 'Middlesex',  mi: 9.7,  ring: 1, live: true },
  { name: 'Acton',         slug: 'acton-ma',         county: 'Middlesex',  mi: 12.5, ring: 1, live: true },
  { name: 'Sudbury',       slug: 'sudbury-ma',       county: 'Middlesex',  mi: 14.5, ring: 1, live: true },
  { name: 'Worcester',     slug: 'worcester-ma',     county: 'Worcester',  mi: 14.9, ring: 1, live: true },
  { name: 'Concord',       slug: 'concord-ma',       county: 'Middlesex',  mi: 16.5, ring: 2, live: true },

  // ---- Ring 1: under 15 miles, unclaimed (15)
  { name: 'Shirley',       slug: 'shirley-ma',       county: 'Middlesex',  mi: 6.1,  ring: 1, live: false },
  { name: 'Boylston',      slug: 'boylston-ma',      county: 'Worcester',  mi: 7.7,  ring: 1, live: false },
  { name: 'West Boylston', slug: 'west-boylston-ma', county: 'Worcester',  mi: 8.4,  ring: 1, live: false },
  { name: 'Ayer',          slug: 'ayer-ma',          county: 'Middlesex',  mi: 8.4,  ring: 1, live: false },
  { name: 'Northborough',  slug: 'northborough-ma',  county: 'Worcester',  mi: 9.5,  ring: 1, live: false },
  { name: 'Lunenburg',     slug: 'lunenburg-ma',     county: 'Worcester',  mi: 9.9,  ring: 1, live: false },
  { name: 'Princeton',     slug: 'princeton-ma',     county: 'Worcester',  mi: 10.5, ring: 1, live: false },
  { name: 'Shrewsbury',    slug: 'shrewsbury-ma',    county: 'Worcester',  mi: 11.2, ring: 1, live: false },
  { name: 'Littleton',     slug: 'littleton-ma',     county: 'Middlesex',  mi: 11.3, ring: 1, live: false },
  { name: 'Groton',        slug: 'groton-ma',        county: 'Middlesex',  mi: 11.9, ring: 1, live: false },
  { name: 'Holden',        slug: 'holden-ma',        county: 'Worcester',  mi: 12.0, ring: 1, live: false },
  { name: 'Southborough',  slug: 'southborough-ma',  county: 'Worcester',  mi: 12.9, ring: 1, live: false },
  { name: 'Westborough',   slug: 'westborough-ma',   county: 'Worcester',  mi: 13.2, ring: 1, live: false },
  { name: 'Townsend',      slug: 'townsend-ma',      county: 'Middlesex',  mi: 14.7, ring: 1, live: false },
  { name: 'Westford',      slug: 'westford-ma',      county: 'Middlesex',  mi: 14.7, ring: 1, live: false },

  // ---- Ring 2: 15-25 miles (33)
  { name: 'Pepperell',     slug: 'pepperell-ma',     county: 'Middlesex',  mi: 15.1, ring: 2, live: false },
  { name: 'Rutland',       slug: 'rutland-ma',       county: 'Worcester',  mi: 15.3, ring: 2, live: false },
  { name: 'Paxton',        slug: 'paxton-ma',        county: 'Worcester',  mi: 16.4, ring: 2, live: false },
  { name: 'Hubbardston',   slug: 'hubbardston-ma',   county: 'Worcester',  mi: 16.8, ring: 2, live: false },
  { name: 'Wayland',       slug: 'wayland-ma',       county: 'Middlesex',  mi: 17.2, ring: 2, live: false },
  { name: 'Ashland',       slug: 'ashland-ma',       county: 'Middlesex',  mi: 17.2, ring: 2, live: false },
  { name: 'Grafton',       slug: 'grafton-ma',       county: 'Worcester',  mi: 17.2, ring: 2, live: false },
  { name: 'Hopkinton',     slug: 'hopkinton-ma',     county: 'Middlesex',  mi: 17.5, ring: 2, live: false },
  { name: 'Framingham',    slug: 'framingham-ma',    county: 'Middlesex',  mi: 17.9, ring: 2, live: false },
  { name: 'Chelmsford',    slug: 'chelmsford-ma',    county: 'Middlesex',  mi: 18.5, ring: 2, live: false },
  { name: 'Gardner',       slug: 'gardner-ma',       county: 'Worcester',  mi: 18.5, ring: 2, live: false },
  { name: 'Millbury',      slug: 'millbury-ma',      county: 'Worcester',  mi: 18.6, ring: 2, live: false },
  { name: 'Leicester',     slug: 'leicester-ma',     county: 'Worcester',  mi: 18.8, ring: 2, live: false },
  { name: 'Lincoln',       slug: 'lincoln-ma',       county: 'Middlesex',  mi: 19.0, ring: 2, live: false },
  { name: 'Auburn',        slug: 'auburn-ma',        county: 'Worcester',  mi: 19.8, ring: 2, live: false },
  { name: 'Weston',        slug: 'weston-ma',        county: 'Middlesex',  mi: 19.8, ring: 2, live: false },
  { name: 'Natick',        slug: 'natick-ma',        county: 'Middlesex',  mi: 20.4, ring: 2, live: false },
  { name: 'Bedford',       slug: 'bedford-ma',       county: 'Middlesex',  mi: 20.4, ring: 2, live: false },
  { name: 'Northbridge',   slug: 'northbridge-ma',   county: 'Worcester',  mi: 21.0, ring: 2, live: false },
  { name: 'Sherborn',      slug: 'sherborn-ma',      county: 'Middlesex',  mi: 21.5, ring: 2, live: false },
  { name: 'Sutton',        slug: 'sutton-ma',        county: 'Worcester',  mi: 21.5, ring: 2, live: false },
  { name: 'Billerica',     slug: 'billerica-ma',     county: 'Middlesex',  mi: 21.8, ring: 2, live: false },
  { name: 'Holliston',     slug: 'holliston-ma',     county: 'Middlesex',  mi: 21.8, ring: 2, live: false },
  { name: 'Spencer',       slug: 'spencer-ma',       county: 'Worcester',  mi: 21.8, ring: 2, live: false },
  { name: 'Lowell',        slug: 'lowell-ma',        county: 'Middlesex',  mi: 21.9, ring: 2, live: false },
  { name: 'Barre',         slug: 'barre-ma',         county: 'Worcester',  mi: 22.1, ring: 2, live: false },
  { name: 'Wellesley',     slug: 'wellesley-ma',     county: 'Norfolk',    mi: 22.3, ring: 2, live: false },
  { name: 'Lexington',     slug: 'lexington-ma',     county: 'Middlesex',  mi: 22.7, ring: 2, live: false },
  { name: 'Waltham',       slug: 'waltham-ma',       county: 'Middlesex',  mi: 23.0, ring: 2, live: false },
  { name: 'Milford',       slug: 'milford-ma',       county: 'Worcester',  mi: 23.2, ring: 2, live: false },
  { name: 'Burlington',    slug: 'burlington-ma',    county: 'Middlesex',  mi: 24.6, ring: 2, live: false },
  { name: 'Dover',         slug: 'dover-ma',         county: 'Norfolk',    mi: 24.6, ring: 2, live: false },
  { name: 'Tewksbury',     slug: 'tewksbury-ma',     county: 'Middlesex',  mi: 24.8, ring: 2, live: false },

  // ---- Ring 3: 25-35 miles (10)
  { name: 'Newton',        slug: 'newton-ma',        county: 'Middlesex',  mi: 25.0, ring: 3, live: false },
  { name: 'Needham',       slug: 'needham-ma',       county: 'Norfolk',    mi: 25.3, ring: 3, live: false },
  { name: 'Oxford',        slug: 'oxford-ma',        county: 'Worcester',  mi: 25.3, ring: 3, live: false },
  { name: 'Medway',        slug: 'medway-ma',        county: 'Norfolk',    mi: 25.9, ring: 3, live: false },
  { name: 'Uxbridge',      slug: 'uxbridge-ma',      county: 'Worcester',  mi: 26.2, ring: 3, live: false },
  { name: 'Woburn',        slug: 'woburn-ma',        county: 'Middlesex',  mi: 26.6, ring: 3, live: false },
  { name: 'Bellingham',    slug: 'bellingham-ma',    county: 'Norfolk',    mi: 27.5, ring: 3, live: false },
  { name: 'Franklin',      slug: 'franklin-ma',      county: 'Norfolk',    mi: 29.3, ring: 3, live: false },
  { name: 'Athol',         slug: 'athol-ma',         county: 'Worcester',  mi: 29.9, ring: 3, live: false },
  { name: 'Andover',       slug: 'andover-ma',       county: 'Essex',      mi: 30.7, ring: 3, live: false },
];

/** Services that get a page per town. Roofing is absent and must stay absent. */
export const TOWN_SERVICES = [
  { slug: 'general-contractor',  label: 'General contractor',  priority: 1 },
  { slug: 'kitchen-remodeling',  label: 'Kitchen remodeling',  priority: 1 },
  { slug: 'bathroom-remodeling', label: 'Bathroom remodeling', priority: 1 },
  { slug: 'painting-contractor', label: 'Painting contractor', priority: 2 },
  { slug: 'deck-building',       label: 'Deck building',       priority: 2 },
  { slug: 'carpentry',           label: 'Carpentry',           priority: 3 },
] as const;

export const unclaimed = TOWNS.filter(t => !t.live);
export const ring1 = TOWNS.filter(t => t.ring === 1 && !t.live);
