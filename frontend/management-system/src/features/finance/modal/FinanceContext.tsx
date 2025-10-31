import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchFinanceTableData, fetchFinanceCategoriesData } from '../api/finance';

export interface FinanceTableData {
  FinanceId?: string,
  Date?: string,
  Description?: string,
  Amount?: number,
  TaxDeductions?: number,
  ChequeNumber?: string,
  CategoryID?: number,
  AddedBy?: string,
  CompanyID?: number
}

export interface FinanceCategoriesData {
  id?: number,
  name?: string,
  colorCode?: string,
  companyId?: number
}

interface FinanceContextType {
  financeList: FinanceTableData[];
  financeCategoriesList: FinanceCategoriesData[];
  setEditingFinance: (fin: FinanceTableData | null) => void;
  addFinance: (finance: FinanceTableData) => boolean;
  editingFinance: FinanceTableData | null;
  idExistError: string;
  clearError: () => void;
  successfullModal: boolean;
  setSuccessfullModal: (value: boolean) => void;
  updateFinance: (fin: FinanceTableData) => void;
  editFinanceData: (fin: FinanceTableData) => void;
  isDeleteModal: FinanceTableData | null
  setIsDeleteModal: (fin: FinanceTableData | null) => void
  handleFinanceDelete:(finance: FinanceTableData) => void;
}


const FinanceContext = createContext<FinanceContextType | undefined>(undefined);

export const useFinance = () => {
  const context = useContext(FinanceContext);
  if (!context) {
    throw new Error('Error');
  }
  return context;
};

interface FinanceProviderProps {
  children: ReactNode;
}

export const FinanceProvider: React.FC<FinanceProviderProps> = ({ children }) => {
  const [financeList, setFinanceList] = useState<FinanceTableData[]>([]);
  const [financeCategoriesList, setFinanceCategoriesList] = useState<FinanceCategoriesData[]>([])
  const [idExistError, setIdExistError] = useState("")
  const [editingFinance, setEditingFinance] = useState<FinanceTableData | null>(null);
  const [successfullModal, setSuccessfullModal] = useState<boolean>(false)
  const [isDeleteModal, setIsDeleteModal] = useState<FinanceTableData | null>(null);

  useEffect(() => {
    const loadFinance = async () => {
      try {
        const data = await fetchFinanceTableData();
        setFinanceList(data.financeAllList);
      } catch (error) {
        console.error(error);
      }
    };

    const loadFinanceCategories = async () => {
      try {
        const data = await fetchFinanceCategoriesData()
        setFinanceCategoriesList(data.financeCategories)
      } catch (error) {
        console.log(error)
      }
    }

    loadFinanceCategories()
    loadFinance();

  }, []);

  // const isDuplicateId = (id?: string) => {
  //   return id ? financeList.some((finance) => finance.FinanceId === id) : false;
  // }

  const addFinance = (finance: FinanceTableData) => {

    const updatedList = [...financeList, finance];
    console.log("added")
    setFinanceList(updatedList);
    setEditingFinance(null)
    setIdExistError("")
    setSuccessfullModal(true)
    window.scrollTo(0, 0);
    document.body.style.overflow = "hidden"
    return true

  };

  const editFinanceData = (finance: FinanceTableData) => {
    console.log(finance)
    setEditingFinance(finance);
    setSuccessfullModal(false);
    document.body.style.overflow = "auto";
    window.scrollTo(0, 0);
  };

  const updateFinance = (updatedFinance: FinanceTableData) => {

    const updatedList = financeList.map((fin) =>
      fin.FinanceId === updatedFinance.FinanceId ? updatedFinance : fin
    );
    console.log("updateList", updatedList)
    setFinanceList(updatedList);
    setSuccessfullModal(true);
    document.body.style.overflow = "hidden";
    window.scrollTo(0, 0);
    setIdExistError("");
  };

  const handleFinanceDelete = (finance: FinanceTableData) => {
    const updatingList = financeList.filter(i => i.FinanceId !== finance.FinanceId)
    setFinanceList(updatingList)
    setIsDeleteModal(null)
  }


  const clearError = () => setIdExistError("");


  return (
    <FinanceContext.Provider value={{ financeList, addFinance, clearError, idExistError, successfullModal, setSuccessfullModal, editingFinance, editFinanceData, updateFinance, setEditingFinance, isDeleteModal, setIsDeleteModal, handleFinanceDelete, financeCategoriesList }}>
      {children}
    </FinanceContext.Provider>
  );
};
