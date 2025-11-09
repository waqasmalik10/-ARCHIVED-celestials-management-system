import ImageButton from "../../shared/ImageButton"
import backImg from "../../assets/images/back.svg"
import { useNavigate } from "react-router-dom"
import CategoryTable from "./ui/CategoryTable"
import Button from "shared/Button"

const CategoryLists = () => {
    const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }

    const handleNewCategory = () => {
        navigate("new-category")
    }

    return (
        <>
            <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
                Create New Finance
            </h2>
            <Button type="button" onClick={handleNewCategory} buttonClasses=" mt-4 bodyBackground px-4 py-6 font-inter font-medium text-base sm:text-lg md:text-xl leading-normal text-white whitespace-nowrap rounded-[15px]">
                Add Category
            </Button>
            <CategoryTable />
        </>
    )
}

export default CategoryLists