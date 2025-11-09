import Box from "../../../shared/Box"
import Button from "../../../shared/Button"
import { useState } from "react"
import { useFinance, FinanceCategoriesData } from "../modal/FinanceContext"

const CategoryTable = () => {
    const { financeCategoriesList } = useFinance()
    const tableDataClassName = "py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-white w-[17.5%] pl-3 pr-10 text-right truncate"
    const tableHeadingClassName = "whitespace-nowrap py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[17.5%] pl-3 pr-10 text-right"


    return (
        <>
            <Box
                boxMainDivClasses={` mt-[30px] transition-all duration-500 delay-300`}
            >
                <div className="w-full overflowXAuto">
                    <table className="w-full min-w-[1024px]">
                        <thead>
                            <tr className="">
                                <th className={`${tableHeadingClassName} !w-[30%] !text-left !pl-10 !pr-3`}>
                                    Category Id
                                </th>
                                <th className={`${tableHeadingClassName}`}>
                                    Category Name
                                </th>
                                <th className={`${tableHeadingClassName}`}>
                                    Color Code
                                </th>
                                <th className={`${tableHeadingClassName}`}>
                                    Company Id
                                </th>
                                <th className={`${tableHeadingClassName}`}>
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {financeCategoriesList.map((data: FinanceCategoriesData, index: number) => (
                                <tr key={index}>
                                    <td className={`${tableDataClassName} !w-[30%] !text-left !pl-10 !pr-3`}>
                                        {data.id}
                                    </td>

                                    <td className={`${tableDataClassName}`}>
                                        {data.name}
                                    </td>
                                    <td className={`${tableDataClassName}`}>
                                        {data.colorCode}
                                    </td>
                                    <td className={`${tableDataClassName}`}>
                                        {data.companyId}
                                    </td>
                                    <td className={`${tableDataClassName}`}>
                                        <div className="flex items-center h-full w-full justify-end gap-4">
                                            <Button type="button" buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                                                Update
                                            </Button>
                                            <Button type="button" buttonClasses="bodyBackground px-4 py-3 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                                                Delete
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Box>
        </>
    )
}

export default CategoryTable