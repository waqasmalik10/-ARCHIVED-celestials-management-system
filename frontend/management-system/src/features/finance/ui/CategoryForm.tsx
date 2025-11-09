import FormInput from "../../../shared/FormInputs"
import * as Yup from "yup";
import { useFormik } from "formik";
import { v4 as uuidv4 } from "uuid";

const formSchema = Yup.object().shape({


});
const CategoryForm = () => {

    const labelStyles = "font-urbanist font-semibold text-[21px] leading-[180%] text-white"
    const inputBorder = "inputMainBorder mt-3.5 w-full rounded-[8px]"
    const inputStyles = "inputBox py-[21px] px-[29px] rounded-[15px] text-white placeholder-[#747681]"
    const errorClasses = "text-red-500 text-xs mt-1 absolute -bottom-6"

    const handleSubmit = (values: any) => {

    }


    const formik = useFormik({
        initialValues: {
            id: "",
        },
        validationSchema: formSchema,
        onSubmit: handleSubmit,
        enableReinitialize: true,
    });

    return (
        <>
            <form onSubmit={formik.handleSubmit} noValidate>
                <div className="grid md:grid-cols-2 gap-[38px]">
                    <div className="relative">
                        <FormInput label="Id"
                            type="text"
                            id="id"
                            name="id"
                            value={formik.values.id}

                            readOnly
                            placeholder="Category ID" labelClassName={`${labelStyles}`} inputMainBorder={`${inputBorder}`} inputClassName={`${inputStyles}`} />

                    </div>
                </div>

            </form>
        </>
    )
}

export default CategoryForm