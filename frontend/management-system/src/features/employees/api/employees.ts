export interface EmployeeTableData {
  id?: number;
  name: string;
  status: string;
  date?: string;
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

export interface EmployeeListData {
  employeesList: EmployeeTableData[]
}


export const fetchEmploeeTableData = async (): Promise<EmployeeListData> => {
  try {
    const response = await fetch(
      "/dummy_json_data/employees_json_data/employeeslist.json"
    );
    if (!response.ok) {
      throw new Error(`${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
