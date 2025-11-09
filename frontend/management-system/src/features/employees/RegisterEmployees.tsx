import Form from "./ui/Form"
import { useNavigate } from "react-router-dom"
import backImg from "../../assets/images/back.svg"
import ImageButton from "../../shared/ImageButton"

const RegisterEmployees = () => {
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
                Register the employee
            </h2>
            <Form />
        </>
    )
}

export default RegisterEmployees