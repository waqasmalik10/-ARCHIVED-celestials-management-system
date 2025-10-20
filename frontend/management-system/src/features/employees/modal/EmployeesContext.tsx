import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface EmployeeTableData {
  id?: number;
  name: string;
  status: string;
}

interface EmployeesContextType {
  employeesList: EmployeeTableData[];
  addEmployee: (employee: EmployeeTableData) => boolean;
  clearError: () => void;
  idExistError: string;
  successfullModal: boolean;
  setSuccessfullModal: (value: boolean) => void;
}

const EmployeesContext = createContext<EmployeesContextType | undefined>(undefined);

export const useEmployees = () => {
  const context = useContext(EmployeesContext);
  if (!context) {
    throw new Error('Error');
  }
  return context;
};

interface EmployeesProviderProps {
  children: ReactNode;
}

export const EmployeesProvider: React.FC<EmployeesProviderProps> = ({ children }) => {
  const [employeesList, setEmployeesList] = useState<EmployeeTableData[]>([]);
  const [idExistError, setIdExistError] = useState("")
  const [successfullModal, setSuccessfullModal] = useState<boolean>(false)

  useEffect(() => {
    const loadEmployees = async () => {
      try {
        const response = await fetch('/dummy_json_data/employees_json_data/employeeslist.json');
        const data = await response.json();
        setEmployeesList(data.employeesList);
      } catch (error) {
        console.error(error);
      }
    };
    loadEmployees();
  }, []);

  const isDuplicateId = (id?: number) => {
    return id ? employeesList.some((employee) => employee.id === id) : false;
  }

  const addEmployee = (employee: EmployeeTableData) => {
    if(isDuplicateId(employee.id)) {
        setIdExistError("ID already exist");
        return false
    } else {
    setEmployeesList(prev => [...prev, employee]);
    setIdExistError("")
    setSuccessfullModal(true)
    window.scrollTo(0, 0);
    document.body.style.overflow = "hidden"
    return true
    }
  };

  
    const clearError = () => setIdExistError("");

  return (
    <EmployeesContext.Provider value={{ employeesList, addEmployee, idExistError, clearError, successfullModal, setSuccessfullModal }}>
      {children}
    </EmployeesContext.Provider>
  );
};
