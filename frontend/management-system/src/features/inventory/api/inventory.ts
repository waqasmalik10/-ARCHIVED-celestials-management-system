export interface StoreTableData {
 id: number,
 name: string,
 uniqueIdentifier: string,
 description: string,
 companyId: number
}

export interface StoreListData {
    storeAllList: StoreTableData[]
}

export const fetchStoreTableData = async (): Promise<StoreListData> => {
  try {
    const response = await fetch(
      "/dummy_json_data/inventory_json_data/storeTable.json"
    );
    if (!response.ok) {
      throw new Error(`${response.status}`);
    }
    const data = await response.json();
    return { storeAllList: data.storeTable };
  } catch (error) {
    console.error(error);
    throw error;
  }
};
