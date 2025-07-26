import '../styles/main.css'


export const metadata = {
  title: 'Synapse',
  description: 'A Graph-Based Search Engine',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
