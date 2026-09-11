/** Service definitions for the Ring 1 town pages.
 *  Kept in its own module because Astro's getStaticPaths() runs in an isolated
 *  scope and cannot close over consts declared in page frontmatter. */
export type Svc = 'general-contractor' | 'kitchen-remodeling' | 'bathroom-remodeling';

export const TOWN_SVC: Record<Svc, { label: string; img: string }> = {
  'general-contractor':  { label: 'General contractor',  img: '/rooms/exterior.jpg' },
  'kitchen-remodeling':  { label: 'Kitchen remodeling',  img: '/hero/K4_finished.jpg' },
  'bathroom-remodeling': { label: 'Bathroom remodeling', img: '/rooms/bathroom.jpg' },
};
export const SVC_KEYS = Object.keys(TOWN_SVC) as Svc[];
