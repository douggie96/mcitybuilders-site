import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/* Every one of the 125 existing URLs maps to one of these collections.
   Migration is a data job, not 125 hand-rebuilds. */
const seo = {
  title: z.string().max(60),
  description: z.string().min(70).max(160),
  h1: z.string(),
  canonical: z.string().optional(),
  updated: z.coerce.date().optional(),
};

const services = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/services' }),
  schema: z.object({ ...seo, room: z.string().optional(), order: z.number().default(99) }),
});

const serviceAreas = defineCollection({          // 50 pages: service x town/region
  loader: glob({ pattern: '**/*.md', base: './src/content/service-areas' }),
  schema: z.object({ ...seo, service: z.string(), town: z.string(), county: z.string().optional(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).default([]) }),
});

const towns = defineCollection({                 // 16 pages: /areas-we-serve/*
  loader: glob({ pattern: '**/*.md', base: './src/content/towns' }),
  schema: z.object({ ...seo, town: z.string(), county: z.string(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).default([]) }),
});

const costGuides = defineCollection({            // 6 pages
  loader: glob({ pattern: '**/*.md', base: './src/content/cost-guides' }),
  schema: z.object({ ...seo, scope: z.string() }),
});

const articles = defineCollection({              // 31 pages: blog + top-level guides
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({ ...seo, published: z.coerce.date(), image: z.string().optional(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).default([]) }),
});

const legal = defineCollection({                 // 4 pages
  loader: glob({ pattern: '**/*.md', base: './src/content/legal' }),
  schema: z.object({ ...seo }),
});

const flooring = defineCollection({             // /flooring/* — one page per floor type
  loader: glob({ pattern: '[!_]*.md', base: './src/content/flooring' }),
  schema: z.object({ ...seo, order: z.number(), card: z.string().max(120),
                     image: z.string(), swatch: z.string(), imageAlt: z.string(), swatchAlt: z.string(),
                     costRange: z.string(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).length(5) }),
});
const flooringHub = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/flooring-hub' }),
  schema: z.object({ ...seo, intro: z.string(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).length(5) }),
});

const ideas = defineCollection({                 // /deck-building/*, /painting/*, /carpentry/* sub-service pages
  loader: glob({ pattern: '*/[!_]*.md', base: './src/content/ideas' }),
  schema: z.object({ ...seo, trade: z.enum(['decks', 'painting', 'carpentry']), order: z.number(),
                     card: z.string().max(120), image: z.string(), swatch: z.string(),
                     imageAlt: z.string(), swatchAlt: z.string(), costRange: z.string(),
                     faqs: z.array(z.object({ q: z.string(), a: z.string() })).length(5) }),
});

export const collections = { services, serviceAreas, towns, costGuides, articles, legal, flooring, flooringHub, ideas };
