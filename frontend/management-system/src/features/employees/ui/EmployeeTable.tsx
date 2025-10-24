import { useEffect, useState } from "react"
import ProfileImage from "../../../assets/images/profileIcon.svg"
import { EmployeeTableData } from "../modal/EmployeesContext"
import Box from "../../../shared/Box";
import useIntersectionObserver from "../../../shared/UseIntersectionObserver";
import Button from "../../../shared/Button";
import { useEmployees } from "../modal/EmployeesContext";
import { useNavigate } from "react-router-dom";
import StatusModal from "./StatusModal";


const EmployeeTable = () => {
    const { employeesList, updateStatus } = useEmployees();
    const navigate = useNavigate();
    const [currentEmployee, setCurrentEmployee] = useState<EmployeeTableData | null>(null)


    const [ref, isVisible] = useIntersectionObserver({ threshold: 0.1 }) as [
        React.RefObject<HTMLDivElement>,
        boolean
    ];
    const [hasAnimated, setHasAnimated] = useState<boolean>(false);

    useEffect(() => {
        if (isVisible && !hasAnimated) {
            setHasAnimated(true);
        }
    }, [isVisible, hasAnimated]);



    const handleNameClick = (employee: EmployeeTableData) => {
        console.log(employee,)
        navigate(`/employees/update-employees/${employee.id}`);
    };

    const handleHistoryClick = (employee: EmployeeTableData) => {
        navigate(`/employees/increament-history/${employee.id}`)
    }

    const statusModalOpen = (employee: EmployeeTableData) => {
        setCurrentEmployee(employee)
         window.scrollTo(0, 0);
        document.body.style.overflow = "hidden"
    }

    const updateStatusText = (id: string, newStatus: string) => {
        updateStatus(id, newStatus)
        setCurrentEmployee(null)
         window.scrollTo(0, 0);
        document.body.style.overflow = "auto"
    }
    const closeStatusModal = () => {
        setCurrentEmployee(null)
        window.scrollTo(0, 0);
        document.body.style.overflow = "auto"
    }

    console.log(employeesList)

    return (
        <>
            <Box ref={ref}
                boxMainDivClasses={` mt-[30px] transition-all duration-500 delay-300 ${hasAnimated ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
                    }`}
            >
                <div className="w-full overflowXAuto">
                    <table className="w-full min-w-[1024px]">
                        <thead>
                            <tr className="">
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[40%] text-left pl-[109px]">
                                    Name
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Action
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Increament
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {employeesList.map((data: EmployeeTableData, index: number) => (
                                <tr key={index} className="border-t border-solid border-[#FFFFFF21]"
                                >
                                    <td className="py-3 md:py-[19px] pl-10 w-[40%] flex items-center gap-4 md:gap-[29px]">
                                        <img src={ProfileImage} alt="Profile" className="sm:w-10 sm:h-10 w-[30px] h-[30px]" />
                                        <button onClick={() => handleNameClick(data)} className="font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap hover:underline">
                                            {data.name}
                                        </button>
                                    </td>
                                    <td className="w-[30%] py-3 md:py-[19px]  pr-10 text-right">
                                        <button type="button" onClick={() => statusModalOpen(data)}
                                            className={`rounded-[15px] ml-auto px-[15px] h-6 md:h-[30px] text-xs md:text-[15px] md:leading-6 font-medium font-inter pt-px flex items-center w-fit ${data.status === "Active"
                                                ? "text-[#ADDC7B] bg-[#ADDC7B14]"
                                                : "text-[#FF8663] bg-[#FF866314]"
                                                }`}
                                        >
                                            {data.status}
                                        </button>
                                    </td>
                                    <td className="w-[30%] py-2.5 md:py-3.5  pr-10 text-right">
                                        <Button onClick={() => handleHistoryClick(data)} buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                                            History
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Box>
            {currentEmployee &&
                <StatusModal closeModal={closeStatusModal} employeeStatus={currentEmployee} onStatusUpdate={updateStatusText} />
            }
        </>
    )
}

export default EmployeeTable
