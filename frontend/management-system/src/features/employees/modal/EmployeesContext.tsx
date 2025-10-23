import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface EmployeeTableData {
  id?: number;
  name: string;
  status: string;
  date?: string;
  fullTimeJoinDate?: string;
  department?: string;
  employeeInformation?: string;
  email?: string;
  cnic?: string;
  designation?: string;
  team?: string;
  hobbies?: string;
  vehicleRegistrationNumber?: string;
  companyId?: string;
  dateOfBirth?: string;
  actualDateOfBirth?: string;
  bankName?: string;
  bankTitle?: string;
  bankAccountNumber?: string;
  bankIBAN?: string;
  bankBranchCode?: string;
  initialBaseSalary?: string;
  currentBaseSalary?: string;
  increamentAmount?: number;
  homeAddress?: string;
  image?: string;
}

interface EmployeesContextType {
  employeesList: EmployeeTableData[];
  addEmployee: (employee: EmployeeTableData) => boolean;
  clearError: () => void;
  idExistError: string;
  successfullModal: boolean;
  setSuccessfullModal: (value: boolean) => void;
  editEmployeeData: (emp: EmployeeTableData) => void;
  setEditingEmployee: (emp: EmployeeTableData | null) => void;
  updateEmployee: (emp: EmployeeTableData) => void;
  editingEmployee: EmployeeTableData | null;
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
  const [editingEmployee, setEditingEmployee] = useState<EmployeeTableData | null>(null);

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
    if (isDuplicateId(employee.id)) {
      setIdExistError("ID already exist");
      return false
    } else {
      const updatedList = [...employeesList, employee];
      console.log("added")
      setEmployeesList(updatedList);
      setEditingEmployee(null)
      setIdExistError("")
      setSuccessfullModal(true)
      window.scrollTo(0, 0);
      document.body.style.overflow = "hidden"
      return true
    }
  };

  const editEmployeeData = (employee: EmployeeTableData) => {
    setEditingEmployee(employee);
    setSuccessfullModal(false);
    document.body.style.overflow = "auto";
    window.scrollTo(0, 0);
  };

  const updateEmployee = (updatedEmployee: EmployeeTableData) => {
    if (
      isDuplicateId(updatedEmployee.id) &&
      updatedEmployee.id !== editingEmployee?.id
    ) {
      setIdExistError("Employee ID already exists. Please use a unique ID.");
      return;
    }
    const updatedList = employeesList.map((emp) =>
      emp.id === updatedEmployee.id ? updatedEmployee : emp
    );
    console.log("updateList", updatedList)
    setEmployeesList(updatedList);
    setSuccessfullModal(true);
    document.body.style.overflow = "hidden";
    window.scrollTo(0, 0);
    setIdExistError("");
  };


  const clearError = () => setIdExistError("");

  return (
    <EmployeesContext.Provider value={{ employeesList, addEmployee, idExistError, clearError, successfullModal, setSuccessfullModal, editEmployeeData, editingEmployee, updateEmployee, setEditingEmployee }}>
      {children}
    </EmployeesContext.Provider>
  );
};
