import { React,StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/main.css'
import AppRouter from './router.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
      <AppRouter />
  </StrictMode>,
)
