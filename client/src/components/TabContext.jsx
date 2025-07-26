import React, { createContext } from 'react'


const TabContext = createContext();

function TabProvider({ children }) {
    const value = {
        tabs
    }

    return (
        <TabContext.Provider value={value}>{children}</TabContext.Provider>
    )
}

export default TabProvider