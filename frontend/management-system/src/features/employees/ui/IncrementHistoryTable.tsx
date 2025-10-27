import { useState } from "react";
import Box from "../../../shared/Box";
import Button from "../../../shared/Button";
import { useEmployees } from "../modal/EmployeesContext";
import IncrementModalForm from "./IncreamentModalForm";


const IncrementHistoryTable = () => {
    const { employeeIncreamentList, editIncreamentList, editingIncreamentList, updateIncrement } = useEmployees();
    const [updateModal, setUpdateModal] = useState<null | { increamentAmount: number; increamentDate: string }>(null);

    const updateModalOpen = (incrementData: { increamentAmount: number; increamentDate: string }) => {
        editIncreamentList(incrementData);
        setUpdateModal(incrementData);
        window.scrollTo(0, 0);
        document.body.style.overflow = "hidden"
    };

    const updateModalClose = () => {
        setUpdateModal(null);
        window.scrollTo(0, 0);
        document.body.style.overflow = "auto"
    };

    return (
        <>
            <Box
                boxMainDivClasses={` mt-[30px] transition-all duration-500 delay-300`}
            >
                <div className="w-full overflowXAuto">
                    <table className="w-full min-w-[1024px]">
                        <thead>
                            <tr className="">
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[40%] text-left pl-[109px]">
                                    Increment Amount
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Increment Date
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {employeeIncreamentList && employeeIncreamentList.length > 0 && (
                                employeeIncreamentList.map((data, index) => (
                                    <tr key={index}>
                                        <td className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-white w-[40%] text-left pl-[109px]">
                                            {data.increamentAmount}
                                        </td>
                                        <td className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-white w-[30%] pl-3 pr-10 text-right">
                                            {data.increamentDate}
                                        </td>
                                        <td className="py-0 w-[30%] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-white pl-3 pr-10 text-right">
                                            <div className="flex items-center h-full w-full justify-end gap-4">
                                                <Button onClick={() => updateModalOpen(data)} buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                                                    Update
                                                </Button>
                                                <Button buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                                                    Delete
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </Box>
            {
                updateModal &&
                <IncrementModalForm incrementFieldsData={editingIncreamentList || undefined} updatedIncrement={updateIncrement} closeModal={updateModalClose} />
            }

        </>
    )
}

export default IncrementHistoryTable
