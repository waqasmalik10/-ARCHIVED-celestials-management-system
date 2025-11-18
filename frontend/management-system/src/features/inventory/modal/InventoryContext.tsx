import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchStoreTableData } from '../api/inventory';

export interface StoreTableData {
    id?: number,
    name?: string,
    uniqueIdentifier?: string,
    description?: string,
    companyId?: number
}

interface InventoryContextType {
    storeList: StoreTableData[];
}


const InventoryContext = createContext<InventoryContextType | undefined>(undefined);

export const useInventory = () => {
    const context = useContext(InventoryContext);
    if (!context) {
        throw new Error('Error');
    }
    return context;
};

interface InventoryProviderProps {
    children: ReactNode;
}

export const InventoryProvider: React.FC<InventoryProviderProps> = ({ children }) => {
    const [storeList, setStoreList] = useState<StoreTableData[]>([]);


    useEffect(() => {
        const loadStore = async () => {
            try {
                const data = await fetchStoreTableData();
                setStoreList(data.storeAllList);
            } catch (error) {
                console.error(error);
            }
        };

        loadStore()

    }, []);




    return (
        <InventoryContext.Provider value={{ storeList }}>
            {children}
        </InventoryContext.Provider>
    );
};
