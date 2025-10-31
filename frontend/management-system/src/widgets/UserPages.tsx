import { Navigate, Route, Routes } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import RegisterEmployeesPage from "../pages/RegisterEmployeesPage";
import Setting from "../pages/Settings";
import EmployeesPage from "../pages/EmployeesPage";
import UpdateEmployeesPage from "../pages/UpdateEmployeesPage";
import IncreamentHistoryPage from "../pages/IncreamentHistoryPage";
import FinancePage from "../pages/FinancePage";
import NewFinancePage from "../pages/NewFinancePage";
import UpdateFinancePage from "../pages/UpdateFinancePage";
import CategoryListsPage from "../pages/CategoryListsPage";
import NewCategoryPage from "../pages/NewCategoryPage";

interface UserPageProps {
  name: string;
  superAdmin: boolean;
}

export default function UserPage({ superAdmin }: UserPageProps) {
  return (
    <>
      <Routes>
        {/* {!superAdmin && (
          <>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/" element={<Dashboard />} />
          </>
        )} */}
        <Route path="/" element={<Dashboard />} />
        <Route path="/employees" element={<EmployeesPage />} /> 
        <Route path="/employees/register-employees" element={<RegisterEmployeesPage />} />
        <Route path="/employees/update-employees/:employeeId" element={<UpdateEmployeesPage />} />
        <Route path="/employees/increament-history/:employeeId" element={<IncreamentHistoryPage />} />
        <Route path="/finance" element={<FinancePage />} />
        <Route path="/finance/new-finance" element={<NewFinancePage />} />
        <Route path="/finance/update-finance/:financeId" element={<UpdateFinancePage />} />
        <Route path="/finance/category-lists" element={<CategoryListsPage />} />
        <Route path="/finance/category-lists/new-category" element={<NewCategoryPage />} />
        <Route path="/settings" element={<Setting />} />
      </Routes>

      {/* {superAdmin ? (
        <>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </>
      ) : null} */}
    </>
  );
}
