import type { TownExtra } from './town-extra';

/**
 * Ring 2 second layer — access, services, price drivers and first checks.
 *
 * This is what keeps 99 same-service pages from converging into one page
 * repeated 33 times. Without it the build fails its own uniqueness floor.
 */
export const EXTRA2: Record<string, TownExtra> = {
  'pepperell-ma': {
    access: 'Rural and open, with room to work at most properties. Supplier runs are long from here, so we stage materials rather than making trips.',
    systems: 'Largely well and septic. Septic capacity is the first question on any project that adds a fixture, and it gets answered before a layout is drawn.',
    priceContext: 'In the riverside village housing, damp and sill deterioration are the items most likely to move a quote. We look at the base of the walls before we price the finishes.',
    firstCheck: 'the basement and the sills — in Pepperell the low ground near the river has a long history of putting water where it should not be',
  },
  'rutland-ma': {
    access: 'Long driveways and real winter access considerations on the higher ground. Exterior work here is planned around the season rather than promised through it.',
    systems: 'Predominantly well and septic, with watershed land affecting some parcels. Any fixture addition starts with what the existing system can take.',
    priceContext: 'Elevation drives exterior cost. Envelope work runs larger here than the same house would in the valley, so we budget for finding more rather than less.',
    firstCheck: 'the weather elevations — at this height the west and north faces tell you the real condition of the envelope',
  },
  'paxton-ma': {
    access: 'Comfortable at most properties, with some longer wooded driveways. Nothing that changes the approach.',
    systems: 'Watershed protection land constrains septic work on some parcels here more than in the surrounding towns, and that is worth establishing for your specific address before design.',
    priceContext: 'In the mid-century stock the cost driver is how much of the list you do at once. Kitchen, bath, panel and windows tend to come due together, and one mobilisation beats four.',
    firstCheck: 'whether the wall you want removed is load-bearing, because in a Paxton ranch it usually is',
  },
  'hubbardston-ma': {
    access: 'The most remote town in Ring 2. Long private driveways, long supplier runs, and winter access that genuinely affects scheduling. We stage materials on site rather than running back and forth.',
    systems: 'Universally well and septic. Capacity governs any project that adds fixtures and is established before anything is designed.',
    priceContext: 'Distance carries real hours here, and we itemise it rather than hiding it in the trade lines. On antique stock, what we find in the rear ells is the other variable.',
    firstCheck: 'the structure of any rear ell — on a Hubbardston farmhouse these were built later and to a lower standard than the house in front of them',
  },
  'wayland-ma': {
    access: 'Large wooded lots with long driveways. Protection of existing landscape and finishes is a genuine line in the scope, not a courtesy.',
    systems: 'Town water in parts, septic common on the larger lots. Conservation land near the Sudbury River affects some parcels and is worth establishing early.',
    priceContext: 'Mid-century modern houses cost more to renovate correctly, and the reason is detailing rather than material. Flat and low-slope construction, large glazed walls and exposed structure do not tolerate a conventional approach.',
    firstCheck: 'whether the house is a conventional frame or a post-and-beam modern, because everything about the approach follows from that',
  },
  'ashland-ma': {
    access: 'Straightforward suburban access through the newer developments, tighter near the centre and the rail line.',
    systems: 'Municipal water and sewer across most of the developed town, which keeps bathroom work uncomplicated in the newer stock.',
    priceContext: 'The age spread is the variable. A number quoted for a 1990s colonial tells you nothing about a house near the old centre, and we will not pretend otherwise.',
    firstCheck: 'the age of the house, because in Ashland it determines the entire approach',
  },
  'grafton-ma': {
    access: 'Easy in the newer developments. The mill villages are close-set with limited side access, so staging and dumpster placement are planned in advance.',
    systems: 'Municipal services in the villages and developed areas. Older mill housing sometimes still has original waste runs worth inspecting before a bathroom is moved.',
    priceContext: 'In multi-family village properties the code scope — separation, egress, smoke and CO — is part of the quote rather than an afterthought. That is a real cost and it belongs on the page.',
    firstCheck: 'whether the property is single or multi-family, because the code requirements and therefore the price change completely',
  },
  'hopkinton-ma': {
    access: 'Large lots with proper driveways. Straightforward, with the usual care needed on newer landscaping and finished basements below the work.',
    systems: 'Septic is common on the larger lots. Where present, any added fixture is checked against capacity before design.',
    priceContext: 'Finish standard drives the number. The existing work is usually decent, so the case for replacement has to be real, and the replacement has to be visibly better.',
    firstCheck: 'the quality of what is already there — in Hopkinton it is often good enough that the honest answer is a smaller job',
  },
  'framingham-ma': {
    access: 'Varies enormously. Suburban neighbourhoods are easy; the downtown multi-family stock has limited access, contested parking and staging that has to be planned before day one.',
    systems: 'Municipal water and sewer throughout the developed city, which makes bathroom additions realistic wherever the structure allows.',
    priceContext: 'Multi-family work carries code scope that single-family work does not, and it is the single biggest reason two Framingham quotes can look nothing alike.',
    firstCheck: 'the occupancy — single-family, two-family or three-family changes the code requirements, the scope and the price',
  },
  'chelmsford-ma': {
    access: 'Comfortable throughout. Suburban lots with driveways that take a truck and a dumpster.',
    systems: 'Municipal services across most of the town, so second-floor bath additions in the cape stock come down to where the stack runs.',
    priceContext: 'Sequencing rather than unit price is the real question here. When the kitchen, bath, panel and windows are all due, the cost-effective plan avoids opening the same wall twice.',
    firstCheck: 'the electrical panel and its capacity, because in this stock it frequently limits what the kitchen can have',
  },
  'gardner-ma': {
    access: 'Constrained in the older city neighbourhoods — close-set lots, limited side access, on-street parking. Planned before we start.',
    systems: 'Municipal water and sewer through the developed city. Older waste runs are worth surveying before a bathroom is rearranged around them.',
    priceContext: 'On two- and three-family properties the code scope is a real line item. On the older single-families, what the previous retrofits left behind is the variable.',
    firstCheck: 'what previous work has already been done and whether it was permitted, because in this stock there is usually a layer of it',
  },
  'millbury-ma': {
    access: 'Straightforward away from the river. The mill-village streets near the water are tighter and need staging planned.',
    systems: 'Municipal services in the developed areas, septic at the edges. Older houses often carry waste runs from several different eras.',
    priceContext: 'Damp and sill work on the low riverside ground is the item most likely to change the number. Finishes over an unrepaired sill are money wasted.',
    firstCheck: 'the basement and the base of the exterior walls — the Blackstone valley ground here holds water',
  },
  'leicester-ma': {
    access: 'Generally comfortable, with longer driveways and more grade on the higher ground.',
    systems: 'Mixed, and it varies by village rather than following one town-wide rule. Which services a parcel actually has is established before a bathroom is designed.',
    priceContext: 'Elevation on the higher ground means exterior envelope work runs larger than the same house lower down. That is a real difference, not a contingency.',
    firstCheck: 'whether the parcel is on town sewer or septic, because in Leicester that genuinely varies street to street',
  },
  'lincoln-ma': {
    access: 'Long wooded driveways on large lots. Conservation land affects many parcels and access routes, and protecting existing landscape is part of the scope.',
    systems: 'Septic is common given the lot sizes and land-use protection. Capacity and siting are established early rather than assumed.',
    priceContext: 'The mid-century modern stock is where cost diverges from expectation. Flat and low-slope construction, glazed walls and exposed structure need an approach, and a conventional renovation instinct produces the wrong answer expensively.',
    firstCheck: 'the building form and the structure type, because in Lincoln that decides whether this is a conventional job or not',
  },
  'auburn-ma': {
    access: 'Easy. Suburban lots with real driveways throughout.',
    systems: 'Municipal services across most of the town, which makes adding an upstairs bath in the cape stock realistic where the stack allows.',
    priceContext: 'In a cape the price turns on the stack. If it sits where an upstairs bath can tie in, the job is reasonable. If not, you are opening walls across the house.',
    firstCheck: 'where the waste stack runs, and what headroom the knee-wall space upstairs actually gives you',
  },
  'weston-ma': {
    access: 'Long private driveways on very large lots. The route from road to work area can be long enough to affect material handling, and protection of existing finishes and landscape is a real cost line.',
    systems: 'Private services are common on the larger properties, so any fixture addition is checked against them before design.',
    priceContext: 'Finish standard is the whole cost story. Tighter carpentry tolerances, better tile layout, more time in the detailing. We itemise that rather than bury it, so you can see what you are paying for.',
    firstCheck: 'the standard of the existing work, because in Weston it is usually good and the case for replacing it needs to be genuine',
  },
  'natick-ma': {
    access: 'Easy in the suburban neighbourhoods, tighter downtown and on some lake-side roads with narrow access.',
    systems: 'Municipal water and sewer through most of the developed town. Some lake-side properties have origins that complicate the picture and are checked individually.',
    priceContext: 'The spread of house ages means Natick quotes vary more than the surrounding towns. A downtown Victorian, a post-war cape and a 1990s colonial are three different jobs.',
    firstCheck: 'the age and origin of the house — particularly whether a lake-side property started life as a seasonal building',
  },
  'bedford-ma': {
    access: 'Comfortable suburban access throughout.',
    systems: 'Municipal services across the developed town, so bathroom work is structurally rather than system limited.',
    priceContext: 'Many of these houses have had one previous renovation. Its quality and whether it was permitted are the variables, and we check rather than build on top of an assumption.',
    firstCheck: 'what has already been done to the house and whether it was done properly',
  },
  'northbridge-ma': {
    access: 'The mill-village rows in Whitinsville are the tightest access in Ring 2 after Lowell — shared drives, no side yard, and staging that has to be agreed before work starts.',
    systems: 'Municipal services in the villages. Original waste runs in the mill housing are worth surveying before any layout change.',
    priceContext: 'Access and staging carry real hours in the village housing. Some of it also has historic significance that affects what can be done to the exterior.',
    firstCheck: 'how we get materials in and waste out, because in the Whitinsville rows that is a genuine constraint on the schedule',
  },
  'sherborn-ma': {
    access: 'Long private driveways on large lots. Straightforward once on site, with care needed on landscape and existing finishes.',
    systems: 'Almost entirely well and septic on large lots. Capacity governs any added fixture and there is usually room for a solution — but it is established before design.',
    priceContext: 'Period houses at a high finish expectation. The cost is time rather than material: matching trim profiles and working around framing that is neither square nor plumb.',
    firstCheck: 'the septic system and its capacity, before a single fixture is chosen',
  },
  'sutton-ma': {
    access: 'Rural and open with generous room at most properties. Longer supplier runs than the towns closer to Worcester.',
    systems: 'Predominantly well and septic. Capacity is the governing constraint on adding fixtures.',
    priceContext: 'On antique stock the honest position is that the assessment matters more than the estimate. We say which parts of the quote are firm and which are provisional.',
    firstCheck: 'sills and floor structure, both of which have usually been repaired at least once already in a house this age',
  },
  'billerica-ma': {
    access: 'Easy throughout. Suburban lots with driveways that take a truck and a dumpster.',
    systems: 'Municipal services across most of the town, so bathroom additions come down to the stack and the structure.',
    priceContext: 'Previous owner-completed work is the recurring variable here. We check what is behind it and whether it was permitted before quoting anything that builds on it.',
    firstCheck: 'the permitting history and the quality of any previous addition or finished basement',
  },
  'holliston-ma': {
    access: 'Comfortable across most of the town, with some longer wooded driveways.',
    systems: 'Mixed municipal and private depending on the part of town, so services are established for your specific parcel before a bathroom is designed.',
    priceContext: 'The split between older centre housing and newer colonial stock means two very different scopes, and the quote reflects which one you have rather than a town average.',
    firstCheck: 'which services the parcel actually has, because in Holliston it varies',
  },
  'spencer-ma': {
    access: 'Open and rural away from the centre, tighter in the older village housing. Supplier runs are long.',
    systems: 'Largely well and septic outside the centre. Capacity is the first question on any added fixture.',
    priceContext: 'Distance and the age of the stock are both real. On multi-family centre properties, code scope is a further line item.',
    firstCheck: 'the sills and the structure, on housing that is both old and further from services than most of the region',
  },
  'lowell-ma': {
    access: 'The most constrained work in the whole 50-mile radius. Triple-deckers with no side access, contested street parking, and historic district requirements in parts of the city. Staging, delivery timing and dumpster permits are planned before day one, not improvised.',
    systems: 'Municipal water and sewer throughout. In multi-family buildings the stack is shared, which governs what can be moved and when the water can be shut off.',
    priceContext: 'Access and multi-family code scope are the two things that make Lowell quotes look different from suburban ones. Both are real hours and both belong in the price.',
    firstCheck: 'the building occupancy and the shared stack, because in a triple-decker those decide what is even possible',
  },
  'barre-ma': {
    access: 'Rural, open and distant. Long supplier runs and real winter access considerations. We stage materials rather than making trips.',
    systems: 'Well and septic throughout. Capacity governs any project that adds fixtures.',
    priceContext: 'Distance and elevation both carry hours, and the antique stock means the assessment is worth more than the estimate until something is opened up.',
    firstCheck: 'the sills and the frame, on housing that is genuinely old and takes real weather',
  },
  'wellesley-ma': {
    access: 'Mature neighbourhoods with established landscape and finished interiors either side of the work. Protection and dust control are a real part of the scope here.',
    systems: 'Municipal services throughout, so the constraints are structural and architectural rather than system capacity.',
    priceContext: 'Matching period detail is where the money goes. Trim profiles, plaster work and window proportion in this stock are specific, and getting them wrong is immediately visible from the street.',
    firstCheck: 'the original trim and plaster detail, because matching it is most of the skill and most of the cost',
  },
  'lexington-ma': {
    access: 'Comfortable suburban access in most neighbourhoods. Properties near the historic centre need more care and may carry review requirements on exterior work.',
    systems: 'Municipal services throughout. System capacity is rarely the constraint here.',
    priceContext: 'Two different cost stories in one town: historic fabric near the centre where matching detail drives the number, and mid-century modern where the structure does.',
    firstCheck: 'whether the property sits in a historic district, which is much easier to know before design than after',
  },
  'waltham-ma': {
    access: 'Constrained in the dense centre — limited side access, contested parking, and neighbours close on both sides. Planned before we start.',
    systems: 'Municipal services throughout. Shared stacks in multi-family buildings govern what can move and when water can be off.',
    priceContext: 'Multi-family code scope and access are the two real cost differences from suburban work. Both are itemised rather than absorbed.',
    firstCheck: 'the occupancy and the stack, because in a Waltham two- or three-family those set the boundaries of the job',
  },
  'milford-ma': {
    access: 'Tighter than the Ring 2 average in the centre — close-set lots and limited side access. Easy in the newer development at the edges.',
    systems: 'Municipal water and sewer through the developed town. Older waste runs warrant a survey before a layout change.',
    priceContext: 'Centre-of-town access and any multi-family code scope are the variables. The newer stock prices conventionally.',
    firstCheck: 'the occupancy and the access, both of which vary sharply between the centre and the edges of town',
  },
  'burlington-ma': {
    access: 'Easy. A uniform suburban stock with proper driveways throughout.',
    systems: 'Municipal services throughout, so bathroom work is limited by structure rather than by capacity.',
    priceContext: 'Because the stock is so uniform, quoting here is predictable and the schedule can be reliable. The structural work in splits and raised ranches is the main swing.',
    firstCheck: 'the load path through a split or raised ranch, which rarely lands where people assume',
  },
  'dover-ma': {
    access: 'Very long private driveways on large lots. Material handling and landscape protection both carry real hours here.',
    systems: 'Well and septic on large lots. Capacity is established before anything is designed — there is usually room for a solution, but it is not assumed.',
    priceContext: 'Period fabric at an exacting finish standard, plus the access. The cost is time and care rather than material.',
    firstCheck: 'the septic and the access route, before the design conversation starts',
  },
  'tewksbury-ma': {
    access: 'Comfortable suburban access throughout.',
    systems: 'Municipal services across most of the town, with septic on some outlying parcels.',
    priceContext: 'Previous additions and owner-completed work are the recurring variable. We check the permitting history before quoting anything built on top of them.',
    firstCheck: 'what has already been added to the house, and whether it was permitted and done properly',
  },
};
