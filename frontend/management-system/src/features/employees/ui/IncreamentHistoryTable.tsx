import Box from "shared/Box"

const IncreamentHistoryTable = () => {
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
                                    Increament AMount
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Increament Date
                                </th>
                                <th className="py-3 md:py-[19px] text-base md:text-lg font-inter font-medium leading-normal md:leading-[30px] text-[#FFFFFF7A] w-[30%] pl-3 pr-10 text-right">
                                    Action
                                </th>
                            </tr>
                        </thead>
                    </table>
                </div>
            </Box>
        </>
    )
}

export default IncreamentHistoryTable