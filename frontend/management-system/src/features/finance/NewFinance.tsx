import { useNavigate } from "react-router-dom"
import backImg from "../../assets/images/back.svg"
import ImageButton from "../../shared/ImageButton"
import Form from "./ui/Form"

const NewFinance = () => {
    const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }


    return (
        <>
            <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
               Create New Finance
            </h2>
            <Form />
        </>
    )
}

export default NewFinance