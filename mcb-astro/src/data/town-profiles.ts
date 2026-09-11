/**
 * Ring 1 town profiles — the substance that makes each page genuinely local
 * rather than a template with the name swapped.
 *
 * RULE: everything here is either geography, publicly-known town character, or
 * housing-stock description. NO invented permit fees, NO invented statistics,
 * NO invented project counts, NO claimed past jobs. If MCB has not done work in
 * a town, the page says what we would expect to find there, not what we did.
 */
export interface TownProfile {
  slug: string;
  name: string;
  county: 'Worcester' | 'Middlesex' | 'Norfolk' | 'Essex';
  mi: number;
  /** One line placing the town. Geography and character only. */
  setting: string;
  /** What the housing stock is actually like — drives the renovation angle. */
  stock: string;
  /** The specific renovation problem this town's houses tend to present. */
  challenge: string;
  /** Kitchens: what the rooms are typically like and what people ask for. */
  kitchen: string;
  /** Bathrooms: same. */
  bath: string;
  /** Neighbouring towns for the internal-link triangle. */
  neighbours: string[];
}

export const RING1: TownProfile[] = [
  {
    slug: 'shirley-ma', name: 'Shirley', county: 'Middlesex', mi: 6.1,
    setting: 'a small rural town in the Nashua River valley, just over the line from Lancaster and bordering the former Fort Devens land',
    stock: 'antique farmhouses and capes along the older roads, a cluster of nineteenth-century mill-village housing around Shirley Village, and pockets of later ranches and colonials on larger rural lots',
    challenge: 'the antique housing here tends to have been added to more than once. Kitchens and bathrooms are often in ells and rear additions that were built to a lower standard than the original house, with shallow foundations, undersized framing and floors that have moved',
    kitchen: 'original kitchens in the farmhouses are usually small rear rooms with a single window and a door to the yard. The common project is opening the wall between that room and an adjacent pantry or dining room, which almost always means dealing with a bearing wall and the plumbing stack',
    bath: 'many of the older houses have a single full bath carved out of a bedroom upstairs, with waste running through framing that was never designed for it. Adding a first-floor bath is the more frequent request',
    neighbours: ['Lancaster', 'Ayer', 'Groton', 'Lunenburg'],
  },
  {
    slug: 'boylston-ma', name: 'Boylston', county: 'Worcester', mi: 7.7,
    setting: 'a small town on the eastern shore of the Wachusett Reservoir, between Lancaster and Worcester',
    stock: 'a mix of antique centre-of-town colonials, mid-century ranches and capes, and newer colonial-style construction on larger lots away from the reservoir land',
    challenge: 'a substantial share of the town is watershed protection land, which constrains what can be built and where. On the practical side, the mid-century housing here is at the age where original kitchens, baths, windows and electrical panels are all reaching end of life at once',
    kitchen: 'the ranches and capes have compact galley or L-shaped kitchens closed off from the living space. Opening them to the dining or family room is the dominant project, and in a ranch that usually means a structural header across a long span',
    bath: 'one-and-a-half baths is the common starting point in the mid-century stock. Either the hall bath gets reworked properly, or an underused closet and a corner of a bedroom become a second full bath',
    neighbours: ['West Boylston', 'Berlin', 'Sterling', 'Northborough'],
  },
  {
    slug: 'west-boylston-ma', name: 'West Boylston', county: 'Worcester', mi: 8.4,
    setting: 'a town on the Wachusett Reservoir whose original centre was flooded when the reservoir was built in the 1890s, leaving the surviving village rebuilt on higher ground',
    stock: 'late-nineteenth and early-twentieth century houses on the rebuilt village streets, a strong band of mid-century ranches and capes, and newer construction toward the town edges',
    challenge: 'the older village housing sits on original fieldstone and early poured foundations, and sill and rim rot from decades of grade and gutter problems is common. That work has to be dealt with before any finish work is worth paying for',
    kitchen: 'village houses have small kitchens at the back with a pantry alongside. Absorbing the pantry into the kitchen is the natural move and gives real counter run without an addition',
    bath: 'upstairs baths in the older stock are often over the kitchen, so any layout change interacts with the ceiling and the venting below. Worth planning both rooms together if both are on the list',
    neighbours: ['Boylston', 'Sterling', 'Holden', 'Worcester'],
  },
  {
    slug: 'ayer-ma', name: 'Ayer', county: 'Middlesex', mi: 8.4,
    setting: 'a compact railroad town at a historic junction, bordering the redeveloped Devens area',
    stock: 'dense late-nineteenth and early-twentieth century housing near the centre and the rail line, including two- and three-family properties, with post-war and newer single-family construction further out',
    challenge: 'the older centre housing is close-set, often with limited side access, which changes how exterior work and material handling have to be staged. Multi-family properties also bring code requirements that single-family work does not',
    kitchen: 'centre-of-town houses have narrow kitchens with the sink on an exterior wall and little natural light. The useful projects here are usually about light and circulation as much as cabinetry',
    bath: 'original baths in this stock are small and were often fitted into former closets or hall ends. Gaining usable space generally means taking it from an adjacent room rather than rearranging within the existing footprint',
    neighbours: ['Shirley', 'Littleton', 'Groton', 'Harvard'],
  },
  {
    slug: 'northborough-ma', name: 'Northborough', county: 'Worcester', mi: 9.5,
    setting: 'a town on the Assabet River between Worcester and the Route 495 corridor, with a historic centre and substantial later residential growth',
    stock: 'antique houses around the old centre, a large body of post-war capes, ranches and split-levels, and considerable colonial-style development from the 1980s onward',
    challenge: 'the split-levels and raised ranches here present the most awkward renovation geometry in the region — half-flights, short bearing walls and ducting in exactly the places you want to open up',
    kitchen: 'in the splits and raised ranches the kitchen sits at the top of the entry stairs, cut off from everything. Opening it to the dining and living space is the single most requested change and needs the structure worked out properly rather than guessed at',
    bath: 'the 1980s colonials are now at the age where the original primary bath needs a full rebuild — fibreglass surrounds, builder-grade vanities and tile set on substrates that have had thirty years of water',
    neighbours: ['Boylston', 'Westborough', 'Southborough', 'Marlborough'],
  },
  {
    slug: 'lunenburg-ma', name: 'Lunenburg', county: 'Worcester', mi: 9.9,
    setting: 'a largely rural town northeast of Fitchburg, with Lake Whalom on its eastern side',
    stock: 'antique farmhouses on the country roads, a concentration of former seasonal cottages around the lake that have been converted to year-round use, and newer single-family construction',
    challenge: 'the converted lake cottages are the defining local problem. Many were built as summer camps — minimal foundations, no insulation to speak of, undersized framing, and plumbing and electrical added incrementally over decades. Renovating one is usually a bigger structural job than it looks from inside',
    kitchen: 'cottage kitchens are small and often on an uninsulated exterior wall. Doing a kitchen here properly usually means opening the wall, insulating and correcting framing before a single cabinet is ordered',
    bath: 'seasonal-origin plumbing is the recurring issue — waste lines with poor fall, supply lines run where they can freeze, and vents that were never properly tied in. That gets corrected as part of the work, not around it',
    neighbours: ['Fitchburg', 'Leominster', 'Shirley', 'Townsend'],
  },
  {
    slug: 'princeton-ma', name: 'Princeton', county: 'Worcester', mi: 10.5,
    setting: 'a hilltown on the slopes of Wachusett Mountain, rural, with large lots and significant elevation',
    stock: 'antique farmhouses and capes, a number of substantial period houses around the town centre, contemporary and post-and-beam homes built to take advantage of the views, and newer custom houses on acreage',
    challenge: 'elevation and exposure. Houses here take harder weather than those in the valley towns — more wind-driven rain, more snow load, more freeze-thaw on exteriors. Exterior envelope and rot problems show up earlier and more severely than they do ten miles away',
    kitchen: 'the contemporary and post-and-beam houses often have open kitchens with cathedral ceilings, where the constraint is running services rather than moving walls. The antique farmhouses present the opposite problem',
    bath: 'larger lots mean well and septic rather than town services on much of the housing stock, so adding a bathroom is a system question before it is a layout question. That gets checked before anything is designed',
    neighbours: ['Sterling', 'Holden', 'Rutland', 'West Boylston'],
  },
  {
    slug: 'shrewsbury-ma', name: 'Shrewsbury', county: 'Worcester', mi: 11.2,
    setting: 'a large suburban town on the eastern edge of Worcester, running down to Lake Quinsigamond',
    stock: 'one of the densest and most varied stocks in the area — pre-war housing near the Worcester line, a very large body of post-war capes and ranches, 1960s and 70s colonials and splits, and continuing newer development',
    challenge: 'the post-war capes are the signature Shrewsbury project. Small footprint, knee walls upstairs, low headroom, and a kitchen and bath that were both minimal when built. Getting real space out of one takes planning rather than just better finishes',
    kitchen: 'cape and ranch kitchens here are typically eight by ten feet with a doorway on every wall. The gain usually comes from taking a dining room or a rear entry into the kitchen footprint, not from rearranging within it',
    bath: 'the classic cape has one bath on the first floor and none upstairs. Putting a bath into the upstairs knee-wall space is common, feasible, and entirely dependent on where the existing stack runs',
    neighbours: ['Worcester', 'Boylston', 'Northborough', 'West Boylston'],
  },
  {
    slug: 'littleton-ma', name: 'Littleton', county: 'Middlesex', mi: 11.3,
    setting: 'a town on the Route 495 corridor with Long Lake at its centre and orchard land on its higher ground',
    stock: 'antique houses along the older roads, former lake cottages converted to year-round homes, substantial post-1980 colonial development, and newer construction near the commuter rail',
    challenge: 'as with the other lake towns, converted cottages carry structural and insulation deficits from their seasonal origins. The newer colonial stock has the opposite issue — it is now old enough that original kitchens, baths and mechanicals are all due at once',
    kitchen: 'the 1980s and 90s colonials have closed kitchens with a peninsula and a separate formal dining room nobody uses. Removing the wall between them is the most common single project in this stock',
    bath: 'primary baths in that same colonial stock were built with a corner tub, a fibreglass shower and a long low vanity. Replacing the tub with a proper walk-in shower is the usual brief',
    neighbours: ['Ayer', 'Boxborough', 'Westford', 'Harvard'],
  },
  {
    slug: 'groton-ma', name: 'Groton', county: 'Middlesex', mi: 11.9,
    setting: 'a historic, largely rural town on the Nashua River, with a long main street and significant conservation and school land',
    stock: 'an unusually strong concentration of eighteenth and nineteenth century houses along Main Street and the older roads, together with later colonial development and custom homes on acreage',
    challenge: 'genuinely old houses, many with historic significance and some within local historic district oversight. Work on the visible exterior of these houses can carry review requirements, and the interiors need an approach that respects original fabric rather than stripping it out',
    kitchen: 'period houses here often have the kitchen in a rear ell added in a later century. The good projects keep the original rooms intact and do the modern work in the ell, which is usually also where the structure most needs attention',
    bath: 'fitting modern baths into a period house without damaging what makes it worth owning is the whole job. Chases, stack routes and floor structure all need to be worked out before anything is opened up',
    neighbours: ['Ayer', 'Shirley', 'Townsend', 'Pepperell'],
  },
  {
    slug: 'holden-ma', name: 'Holden', county: 'Worcester', mi: 12.0,
    setting: 'a large residential town directly north of Worcester, suburban toward the city and rural at its northern end',
    stock: 'a substantial body of post-war capes and ranches on the Worcester side, 1960s through 1980s colonials and splits through the middle of town, and rural antique and newer housing to the north',
    challenge: 'the volume of mid-century housing at the same stage of life. Original kitchens, single baths, undersized electrical panels and aging windows tend to arrive as a list rather than a single project, which makes sequencing and budgeting the real skill',
    kitchen: 'closed-off kitchens with a doorway to a formal dining room are the standard condition. Whether the wall between them is bearing is the first question, and in the ranches it very often is',
    bath: 'one full bath plus a half is typical. The most valuable move is usually converting that half bath into a full, which depends entirely on what is available for waste and vent in the wall it sits on',
    neighbours: ['Worcester', 'West Boylston', 'Princeton', 'Paxton'],
  },
  {
    slug: 'southborough-ma', name: 'Southborough', county: 'Worcester', mi: 12.9,
    setting: 'an affluent town between the Route 9 and Route 495 corridors, with a historic centre, reservoir land and large residential lots',
    stock: 'period houses around the centre, substantial estate-scale properties, and a large body of high-specification colonial construction from the 1980s onward',
    challenge: 'expectation. The finish standard in this stock is high, which means the carpentry, tile and paint have to be genuinely good rather than merely complete. It also means the existing work being replaced was often decent, so the case for the change has to be real',
    kitchen: 'kitchens here are usually already large. The projects are about layout quality and materials rather than square footage — reworking an island that does not function, correcting a work triangle, upgrading cabinetry and stone',
    bath: 'primary suites in the 1980s and 90s stock have oversized corner tubs and dated tile. Converting to a large walk-in shower with proper waterproofing and a well-executed tile layout is the dominant project',
    neighbours: ['Westborough', 'Northborough', 'Marlborough', 'Hopkinton'],
  },
  {
    slug: 'westborough-ma', name: 'Westborough', county: 'Worcester', mi: 13.2,
    setting: 'a town at the junction of the Route 9 and Route 495 corridors, with a historic centre and substantial commercial and residential development',
    stock: 'antique and Victorian housing near the centre, post-war capes and ranches, and a large volume of colonial and townhouse development from the 1980s onward',
    challenge: 'a wide spread of house ages in a small area, which means there is no single Westborough project. A downtown Victorian and a 1990s colonial two miles apart need completely different approaches, and the assessment matters more than usual',
    kitchen: 'the Victorian and antique stock near the centre has small, compartmented kitchens with pantries and back stairs. The colonial stock has the standard closed kitchen and unused formal dining room. Different problems, different solutions',
    bath: 'in the older centre housing, baths were retrofitted into houses built without them and the plumbing shows it. In the newer stock it is straightforward replacement of builder-grade fittings',
    neighbours: ['Northborough', 'Southborough', 'Shrewsbury', 'Grafton'],
  },
  {
    slug: 'townsend-ma', name: 'Townsend', county: 'Middlesex', mi: 14.7,
    setting: 'a rural town on the Squannacook River near the New Hampshire line, with three distinct village centres',
    stock: 'antique farmhouses and capes, nineteenth-century village housing around the centres, and newer single-family homes on rural lots',
    challenge: 'distance from services and genuinely old building stock. Much of the housing is on well and septic, and the antique houses have the full set of period issues — sill rot, settled framing, retrofitted systems and additions built to varying standards',
    kitchen: 'farmhouse kitchens here are rear rooms with low ceilings and small windows. Raising the perceived space usually means addressing ceiling height or borrowing from an adjacent room, both of which are structural questions',
    bath: 'adding a bath to an antique farmhouse on septic is a system question first. Capacity and layout of the existing system get checked before a fixture is chosen',
    neighbours: ['Lunenburg', 'Groton', 'Pepperell', 'Shirley'],
  },
  {
    slug: 'westford-ma', name: 'Westford', county: 'Middlesex', mi: 14.7,
    setting: 'a town in the Nashoba Valley on the Route 495 corridor, with orchard land, a historic centre and substantial modern residential growth',
    stock: 'antique houses and farmsteads on the older roads, a moderate body of post-war housing, and a very large volume of colonial development from the 1980s through the 2000s',
    challenge: 'the dominant stock is late-eighties to early-2000s colonials now hitting their first real renovation cycle. Everything in them was builder-grade and everything is due at the same time, so the work is about getting the sequencing and the budget allocation right',
    kitchen: 'these houses have a closed kitchen with a peninsula, a breakfast nook, and a formal dining room across the hall. Removing the wall to the dining room or family room is the standard project and the structure is usually straightforward',
    bath: 'the original primary bath in this stock — corner soaking tub, small fibreglass shower, double vanity in a laminate top — is the most-replaced room in the region. The usual brief is losing the tub for a proper tiled walk-in shower',
    neighbours: ['Littleton', 'Chelmsford', 'Groton', 'Acton'],
  },
];
