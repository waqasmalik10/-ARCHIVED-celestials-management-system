import { useNavigate, useParams } from "react-router-dom"
import backImg from "../../assets/images/back.svg"
import ImageButton from "../../shared/ImageButton"
import IncrementHistoryTable from "./ui/IncrementHistoryTable"
import { useEffect, useState } from "react"
import { useEmployees } from "./modal/EmployeesContext"
import Button from "../../shared/Button"
import IncrementModalForm from "./ui/IncreamentModalForm"

const IncreamentHistory = () => {
    const { employeesList, setEmployeeIncreamentList, addNewIncrement } = useEmployees();
    const [addIncreamentModalOpen, setAddIncreamentModalOpen] = useState(false)
    const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }
    const { employeeId } = useParams()
    useEffect(() => {
        console.log(employeesList, "Employee")
        if (employeesList.length > 0) {
            const foundEmployee = employeesList.find((emp) => emp?.id === employeeId);
            console.log(foundEmployee, "Found")
            setEmployeeIncreamentList(foundEmployee?.lastIncreament || [])
        }
        return () => {
            setEmployeeIncreamentList([]);
        };

    }, [employeesList, employeeId])

    const handleAddIncreamentModal = () => {
        setAddIncreamentModalOpen(!addIncreamentModalOpen)
        if (addIncreamentModalOpen) {
            window.scrollTo(0, 0);
            document.body.style.overflow = "auto"
        } else {
            window.scrollTo(0, 0);
            document.body.style.overflow = "hidden"
        }
    }

    return (
        <>
            <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
                Increament History
            </h2>
            <div className="flex justify-between items-center">
                <p className="text-[21px] font-medium font-urbanist leading-[180%] mt-6 text-[#FFFFFF99]">
                    Employee Id is <span className="font-semibold">{employeeId}</span>
                </p>
                <Button onClick={handleAddIncreamentModal} buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                    Add Increament
                </Button>
            </div>
            <IncrementHistoryTable />
            {addIncreamentModalOpen &&
                <IncrementModalForm addIncrement={addNewIncrement} closeModal={handleAddIncreamentModal} />
            }
        </>
    )
}

export default IncreamentHistory