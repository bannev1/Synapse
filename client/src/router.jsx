import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// Pages for public / non-authenticated users
import SignInPage from './pages/SignIn';
import RegisterPage from './pages/Register';

// Components for authenticated pages
import RequireAuth from './components/RequireAuth';
import MasterLayout from './components/MasterLayout';

// Pages for authenticated users
import ProfilePage from './pages/Profile';
import WorkshopsPage from './pages/Workshops';
import XpPage from './pages/Xp';

const router = createBrowserRouter([
    // Public pages
    {
        path: "/signIn",
        element: <SignInPage/>,
    },
    {
        path: "/register",
        element: <RegisterPage/>,
    },
    // Authenticated pages
    {
        element: <RequireAuth/>,
        children: [{
            element: <MasterLayout />,
            children: [
                { path: '/profile', element: <ProfilePage /> },
                { path: '/workshops', element: <WorkshopsPage /> },
                { path: '/xp', element: <XpPage /> },
            ]
        }]
    },
    // Fail-safe route, go to signin page
    {
        path: "*",
        element: <SignInPage />
    }
]);

export default function AppRouter() {
    return <RouterProvider router={router} />;
}
