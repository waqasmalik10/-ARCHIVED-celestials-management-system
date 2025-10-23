import { Navigate, Route, Routes } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import RegisterEmployeesPage from "../pages/RegisterEmployeesPage";
import Setting from "../pages/Settings";
import EmployeesPage from "../pages/EmployeesPage";
import UpdateEmployeesPage from "pages/UpdateEmployeesPage";

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
