// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';

export default defineConfig({
	site: 'https://docs.perms.io',
	integrations: [
		starlight({
			title: 'Permio docs',
			description:
				'Documentation for Permio (perms.io), permissions as a service with resource-level RBAC. Quickstart, concepts, SDKs (TypeScript, Go, Python, Rust, Java) and API reference.',
			logo: { src: './src/assets/logo.svg', replacesTitle: true, alt: 'Permio' },
			favicon: '/favicon.svg',
			// Fails the build on broken internal links and anchors. llms.txt is only written at deploy.
			plugins: [starlightLinksValidator({ exclude: ['/llms.txt'] })],
			customCss: ['./src/styles/theme.css'],
			head: [
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' } },
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' } },
				{
					tag: 'link',
					attrs: {
						rel: 'stylesheet',
						href: 'https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap',
					},
				},
				{ tag: 'meta', attrs: { name: 'theme-color', content: '#111827' } },
			],
			components: {
				Header: './src/components/Header.astro',
				Footer: './src/components/Footer.astro',
				// The brand is dark-only, like perms.io and the dashboard.
				ThemeProvider: './src/components/ThemeProvider.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
			},
			expressiveCode: {
				themes: ['github-dark-default'],
				styleOverrides: {
					borderRadius: '0.75rem',
					borderColor: '#1f2937',
					codeBackground: '#0b1120',
					codeFontFamily: "'JetBrains Mono', ui-monospace, monospace",
					codeFontSize: '0.85rem',
					uiFontFamily: "'Nunito', ui-sans-serif, system-ui, sans-serif",
					frames: {
						editorTabBarBackground: '#111827',
						editorActiveTabBackground: '#0b1120',
						editorActiveTabIndicatorTopColor: '#29e8c6',
						editorActiveTabIndicatorBottomColor: 'transparent',
						terminalTitlebarBackground: '#111827',
						terminalBackground: '#0b1120',
						frameBoxShadowCssValue: '0 18px 40px -18px rgb(0 0 0 / 0.6)',
					},
				},
			},
			sidebar: [
				{
					label: 'Start here',
					items: [
						{ label: 'Overview', link: '/' },
						{ label: 'Quickstart', slug: 'quickstart' },
					],
				},
				{
					label: 'Concepts',
					items: [
						{ label: 'How it works', slug: 'how-it-works' },
						{ label: 'Resources and inheritance', slug: 'concepts/resources' },
						{ label: 'Groups', slug: 'concepts/groups' },
						{ label: 'API keys', slug: 'concepts/api-keys' },
						{ label: 'Plans and limits', slug: 'concepts/plans-and-limits' },
						{ label: 'IAM fundamentals', slug: 'iam-basics' },
					],
				},
				{
					label: 'Guides',
					items: [
						{ label: 'Filtering lists and share dialogs', slug: 'guides/filtering-and-sharing' },
						{ label: 'MCP server', slug: 'guides/mcp' },
					],
				},
				{
					label: 'SDKs',
					items: [
						{ label: 'TypeScript', slug: 'sdk/typescript' },
						{ label: 'Go', slug: 'sdk/go' },
						{ label: 'Python', slug: 'sdk/python' },
						{ label: 'Rust', slug: 'sdk/rust' },
						{ label: 'Java', slug: 'sdk/java' },
					],
				},
				{
					label: 'API reference',
					items: [
						{ label: 'Overview', slug: 'api-reference' },
						{ label: 'Permissions & Roles', slug: 'api-reference/permissions' },
						{ label: 'Organisations & Projects', slug: 'api-reference/organizations' },
						{ label: 'Pagination', slug: 'api-reference/pagination' },
					],
				},
			],
		}),
	],
});
