import ImageButton from "../../shared/ImageButton"
import backImg from "../../assets/images/back.svg"
import StoreTable from "./ui/StoreTable"
import { useNavigate } from "react-router-dom"

import registerIcon from "../../assets/images/register.svg"
import Button from "shared/Button"


const Store = () => {
    const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }

    return (
        <>
            <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <div className="flex items-center justify-between gap-4 flex-wrap">
                <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
                    Store
                </h2>
                <Button type="button" buttonClasses="bodyBackground w-fit fade-bottom rounded-[15px] p-2.5 md:py-[26px] md:px-2 lg:px-8 flex justify-center items-center font-poppins font-semibold md:text-lg leading-normal gap-[18px] h-11 sm:h-14 md:h-[73px] text-white" >
                    <div className="sm:w-[21px] sm:h-[21px] w-4 h-4">
                        <img src={registerIcon} alt="date" className="w-full h-full" />
                    </div>
                    Add New Store
                </Button>

            </div>
            <StoreTable />
        </>
    )
}

export default Store