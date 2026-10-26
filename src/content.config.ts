import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		// heroBadge: the pill above the splash-page headline (see components/Hero.astro).
		schema: docsSchema({ extend: z.object({ heroBadge: z.string().optional() }) }),
	}),
};
