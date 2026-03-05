import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Custom generateId so entry IDs match Starlight sidebar slugs (e.g. "welcome", "guide/recording", "features/click-circle")
const docs = defineCollection({
  loader: docsLoader({
    generateId: ({ entry }) => {
      const normalized = entry.replace(/\\/g, '/').replace(/\.(markdown|mdown|mkdn|mkd|mdwn|md|mdx)$/i, '');
      // index.md at any path → slug is the directory (e.g. features/click-circle/index → features/click-circle)
      return normalized.replace(/\/index$/i, '') || 'index';
    },
  }),
  schema: docsSchema(),
});

export const collections = {
  docs,
};
