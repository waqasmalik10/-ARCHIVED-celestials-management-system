export interface EmployeeTableData {
  id?: number;
  name: string;
  status: string;
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
