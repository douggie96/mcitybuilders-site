/**
 * Second layer of town-specific substance.
 *
 * The first build failed its own uniqueness check at 98% similarity between
 * same-service pages — exactly the "template with the name swapped" failure
 * Rule 3 warns about. These fields exist to carry real, differing content into
 * the sections that were previously shared boilerplate.
 *
 * Everything here is geography, publicly-known town character, or infrastructure
 * that follows from it. No invented permit fees, no invented statistics.
 */
export interface TownExtra {
  /** Site access and logistics — genuinely different town to town. */
  access: string;
  /** Water and waste: town services vs well and septic. Drives bathroom scope. */
  systems: string;
  /** What moves the price in this town specifically. */
  priceContext: string;
  /** The first thing we check on a house here. */
  firstCheck: string;
}

export const EXTRA: Record<string, TownExtra> = {
  'shirley-ma': {
    access: 'Most of Shirley is easy to work in — rural roads, generous driveways and room for a dumpster and a materials drop without blocking anyone. The tighter exception is the older village housing, where houses sit closer to the road and staging has to be planned rather than assumed.',
    systems: 'Much of the town is on private well and septic. For any project adding a bathroom or a second kitchen sink, septic capacity is the first question and it gets answered before a layout is drawn.',
    priceContext: 'On the antique stock, the variable that moves the number most is what we find in the rear ells. Those additions were often built cheaply and have the shallowest foundations and the most rot. We open one up and price from what is actually there.',
    firstCheck: 'the sills and the rim where a rear ell meets the original house — the most reliable place in a Shirley farmhouse to find rot that nobody knew about',
  },
  'boylston-ma': {
    access: 'Straightforward almost everywhere. Boylston lots are generous and driveways take a truck and a dumpster without difficulty. The reservoir-side roads can be narrow but the houses themselves sit back.',
    systems: 'A mix. Parts of town are on municipal water, and septic is common. Given the watershed land, any work touching a septic system here warrants checking what applies to that particular parcel before it is designed.',
    priceContext: 'In the mid-century ranches and capes, the cost driver is how much of the list you do at once. Original kitchen, single bath, old panel and aging windows tend to come due together, and doing them in one mobilisation is meaningfully cheaper than four separate visits.',
    firstCheck: 'whether the wall you want to remove is load-bearing — in a Boylston ranch it very often is, and the header spec changes the budget',
  },
  'west-boylston-ma': {
    access: 'The rebuilt village streets are close-set with modest side yards, so material staging and dumpster placement need planning. Away from the centre there is plenty of room.',
    systems: 'Municipal services through much of the developed area, with septic on the outskirts. Older village houses sometimes still have original waste lines that are worth inspecting before a bathroom is rearranged around them.',
    priceContext: 'Sill and rim repair is the item most likely to change a West Boylston quote. Decades of grade and gutter problems against the older village houses have done predictable damage, and finish work over an unrepaired sill is money wasted.',
    firstCheck: 'the base of the exterior walls and the grade around them — the village housing here has a consistent history of water sitting where it should not',
  },
  'ayer-ma': {
    access: 'The most constrained town in Ring 1. Centre-of-town houses are close together with limited side access and on-street parking pressure. We plan staging, dumpster placement and delivery timing before we start rather than working it out on day one.',
    systems: 'Municipal water and sewer through the developed centre, which simplifies bathroom additions considerably compared with the septic towns nearby.',
    priceContext: 'For multi-family properties the code requirements — separation, egress, smoke and CO — are part of the scope, not an afterthought, and they belong in the quote. For single-family work in the centre, access and staging carry real hours.',
    firstCheck: 'how we are going to get materials in and waste out, because in central Ayer that genuinely affects the schedule and the price',
  },
  'northborough-ma': {
    access: 'Good. Suburban lots with real driveways throughout most of the town. The Route 20 corridor properties can have awkward turning but nothing that changes the approach.',
    systems: 'Municipal water and sewer across most of the developed town, with septic on some outlying parcels. Adding a bathroom is usually a structural and layout question here rather than a system-capacity one.',
    priceContext: 'On split-levels and raised ranches the structural work is the swing factor. Opening a kitchen in a split often means a header, and sometimes a post and footing below it, because the load path runs somewhere inconvenient. That gets worked out and priced before we commit to a layout.',
    firstCheck: 'the load path through a split-level — where the structural loads actually land, which is rarely where people assume',
  },
  'lunenburg-ma': {
    access: 'Easy on the rural roads and at the newer houses. The lake-side properties are the exception: narrow access roads, steep short driveways and tight lots, all of which affect how work is staged and what equipment can reach the house.',
    systems: 'Predominantly well and septic. On converted cottages this is critical — many were sized for seasonal use, and adding a bathroom or a dishwasher to a system built for summer weekends is a system question first.',
    priceContext: 'Converted cottages are where quotes move most. What looks like a kitchen job frequently turns out to include insulation, framing correction and sometimes foundation work. We open up before we commit, and we tell you what we find the day we find it.',
    firstCheck: 'whether the structure under a converted cottage was ever built for year-round loading — piers, frost depth and framing size',
  },
  'princeton-ma': {
    access: 'Long rural driveways, significant grade, and winter access that genuinely matters. A steep Princeton driveway in February changes the schedule, and we plan exterior work around the season rather than promising through it.',
    systems: 'Almost entirely well and septic. Any project adding fixtures starts with what the existing system can take. On the larger lots there is usually room for a solution, but it has to be established before design.',
    priceContext: 'Exposure is the local cost driver. Houses on the mountain slopes take harder weather, so exterior envelope work runs larger here than the same house would ten miles down in the valley. Budget for finding more, not less.',
    firstCheck: 'the weather side of the house — on a Princeton hillside the west and north elevations tell you the real condition of the envelope',
  },
  'shrewsbury-ma': {
    access: 'Mostly straightforward suburban access. The denser pre-war streets near the Worcester line and some of the lakeside roads are tighter and need staging planned in advance.',
    systems: 'Municipal water and sewer across the great majority of the town. That removes the main constraint on adding bathrooms and makes second-floor bath additions in the cape stock realistic.',
    priceContext: 'In a cape, the price turns on the stack. If the existing waste stack is positioned so an upstairs bath can tie into it, the job is reasonable. If it is not, you are opening walls and floors across the house, and that is a different number. We establish which before quoting.',
    firstCheck: 'where the waste stack runs and what the knee-wall space upstairs actually gives you in headroom',
  },
  'littleton-ma': {
    access: 'Good across the newer developments. The lake roads and some of the older orchard-area properties are narrower, with a few long shared driveways that need coordinating.',
    systems: 'Mixed. Municipal water in parts, septic common, particularly on the older and lake-side properties. Converted cottages carry the same seasonal-system issue as Lunenburg.',
    priceContext: 'On the post-1980 colonials the scope is usually predictable and the pricing is stable. On a converted cottage it is not, and we will say so up front rather than giving you a comfortable number we would have to revise.',
    firstCheck: 'in the colonials, whether the wall between kitchen and dining is bearing; in the cottages, the foundation and the insulation',
  },
  'groton-ma': {
    access: 'Rural and generally generous, with the notable exception of the Main Street houses, where the buildings sit close to a busy road and staging has to account for both traffic and appearance.',
    systems: 'Largely well and septic outside the centre. On antique houses the existing waste runs are often a patchwork of several eras and worth surveying properly before a bathroom is moved.',
    priceContext: 'Period houses cost more to renovate well, and the reason is time rather than material. Matching existing trim profiles, working around original fabric and dealing with framing that is not square or plumb all take hours that a new-build kitchen does not. We quote the hours honestly.',
    firstCheck: 'whether the house sits in a local historic district, because that can affect exterior work and it is much easier to know before design than after',
  },
  'holden-ma': {
    access: 'Comfortable throughout. Suburban lots with driveways that take a truck and a dumpster. The rural north end has long drives but no real constraint.',
    systems: 'Municipal water and sewer across the developed southern and central parts of town, septic to the north. For most Holden projects the services are not the limiting factor.',
    priceContext: 'The realistic question in Holden is sequencing rather than unit price. When the kitchen, the bath, the panel and the windows are all due, the cost-effective plan is a phased order that avoids tearing into the same wall twice. We will lay that out even where it means less work for us this year.',
    firstCheck: 'the electrical panel and its capacity — in this stock it frequently needs attention and it affects what the kitchen can have',
  },
  'southborough-ma': {
    access: 'Large lots and long driveways, generally easy, though on estate properties the route from the road to the work area can be long enough to affect material handling. Protection of existing landscape and finishes is a real part of the job here.',
    systems: 'Mixed municipal and private services depending on the part of town. On the larger properties, private systems are common and any fixture addition is checked against them first.',
    priceContext: 'The finish standard is what drives cost. Tighter tolerances on carpentry, better tile layout, better materials and more time in the detailing. That is a legitimate cost and we will itemise it rather than bury it, so you can see what you are paying for.',
    firstCheck: 'the quality of what is already there — in Southborough the existing work is often decent, and the case for replacing it needs to be genuine',
  },
  'westborough-ma': {
    access: 'Varies with the part of town. The 1980s-onward developments are easy. The older centre streets are tighter, with less side yard and more parking pressure.',
    systems: 'Municipal water and sewer across most of the developed town, which keeps bathroom work uncomplicated in the newer stock.',
    priceContext: 'Because the housing spans such a range of ages in a small area, Westborough quotes vary more than in the surrounding towns. A downtown Victorian and a 1990s colonial two miles apart are not comparable jobs, and a number quoted for one tells you nothing about the other.',
    firstCheck: 'the age of the house first, because it determines everything else about the approach',
  },
  'townsend-ma': {
    access: 'Rural and open, with generous room to work at most properties. The trade-off is distance — supplier runs are longer from here, which we plan around by staging materials rather than making trips.',
    systems: 'Predominantly well and septic. Septic capacity is the governing constraint on any project that adds fixtures, and we establish it before design rather than after.',
    priceContext: 'On antique farmhouses the honest position is that the assessment matters more than the estimate. Until a wall or a floor is opened, a number is partly a guess. We say which parts of a Townsend quote are firm and which are provisional, rather than presenting all of it as certain.',
    firstCheck: 'floor structure and sills — in a house of this age and this far out, both have usually been repaired at least once already',
  },
  'westford-ma': {
    access: 'Good. The modern developments have proper driveways and room to work. Some of the older orchard-area properties have longer and rougher access.',
    systems: 'Mixed, with municipal services in the developed areas and septic on outlying and older properties. Most of the late-eighties-onward stock is straightforward for bathroom work.',
    priceContext: 'In the dominant colonial stock the scope is predictable, which means the quote can be firm and the schedule can be reliable. The variable is how much you do at once — these houses tend to need the kitchen, the primary bath and the windows in the same few years.',
    firstCheck: 'whether the kitchen-to-dining wall is bearing, and where the HVAC trunk runs, because in this stock the ductwork is more often the obstacle than the framing',
  },
};
