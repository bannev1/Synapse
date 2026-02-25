import '../styles/main.css'

import { TabProvider } from '@/components/contexts/TabContext'


export const metadata = {
	title: 'Synapse',
	description: 'A Graph-Based Search Engine',
}

export default function RootLayout({ children }) {
	return (
		<html lang="en">
			<body>
				<TabProvider>
					{children}
				</TabProvider>
			</body>
		</html>
	)
}
