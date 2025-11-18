import { useNavigate, useParams } from "react-router-dom"
import ImageButton from "../../../shared/ImageButton"
import backImg from "../../../assets/images/back.svg"
import { useFinance } from "../modal/FinanceContext";
import { useEffect } from "react";
import CategoryForm from "./CategoryForm";

const UpdateCategory = () => {
    const { financeCategoriesList, editCategoryData, editingCategory, setEditingCategory } = useFinance();
    const navigate = useNavigate()

    const backPgae = () => {
        navigate(-1)
    }
    const { categoryId } = useParams()
    useEffect(() => {
        if (financeCategoriesList.length > 0 && editingCategory === null) {
            const foundEmployee = financeCategoriesList.find((cate) => cate?.id === categoryId);
            console.log(foundEmployee, "Found")
            if (foundEmployee) {
                editCategoryData(foundEmployee);
            }
        }
        return () => {
            setEditingCategory(null);
        };
    }, [financeCategoriesList, categoryId])
    return (
        <>
            <ImageButton type="button" onClick={backPgae} className="mt-5">
                <img src={backImg} alt="back Image" />
            </ImageButton>
            <h2 className="mt-5 md:mt-[46px] text-[58px] font-semibold font-poppins leading-[140%] text-white">
                Update the Category
            </h2>
            <CategoryForm />
        </>
    )
}

export default UpdateCategory