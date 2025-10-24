import { useNavigate, useParams } from "react-router-dom"
import backImg from "../../assets/images/back.svg"
import ImageButton from "../../shared/ImageButton"
import IncreamentHistoryTable from "./ui/IncreamentHistoryTable"

const IncreamentHistory = () => {
     const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }
    const { employeeId } = useParams()
    return (
        <>
        <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
                Increament History
            </h2>
            <p className="text-[21px] font-medium font-urbanist leading-[180%] mt-6 text-[#FFFFFF99]">
                Employee Id is <span className="font-semibold">{employeeId}</span>
            </p>
            <IncreamentHistoryTable />
        </>
    )
}

export default IncreamentHistory