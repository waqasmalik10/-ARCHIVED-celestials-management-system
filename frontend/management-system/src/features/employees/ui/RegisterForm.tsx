import { useRef, useState } from "react";
import uploadImg from "../../../assets/images/uploadImg.svg";
import ImageButton from "../../../shared/ImageButton";
import FormInput from "../../../shared/FormInputs";
import Button from "../../../shared/Button";
import { EmployeeTableData } from "../api/employees"
import * as Yup from "yup";
import { useFormik } from "formik";
import { useEmployees } from "../modal/EmployeesContext";
import { useNavigate } from "react-router-dom";
import SuccessfullModal from "../../../shared/SuccessfullModal";


const formSchema = Yup.object().shape({
    name: Yup.string().required("Name is required"),
    employeeId: Yup.number().required("ID is required"),
    department: Yup.string().required("Department is required"),
    employeeInformation: Yup.string().required("Information is required"),
    date: Yup.string().required("Date is required"),
});

const Form = () => {
    const [file, setFile] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { addEmployee, clearError, idExistError, successfullModal, setSuccessfullModal } = useEmployees();
    const navigate = useNavigate();

    const labelStyles = "font-urbanist font-semibold text-[21px] leading-[180%] text-white"
    const inputBorder = "inputMainBorder mt-3.5 w-full rounded-[15px]"
    const inputStyles = "inputBox py-[21px] px-[29px] rounded-[15px] text-white"
    const errorClasses = "text-red-500 text-xs mt-1 absolute -bottom-6"

    const handleClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            const fileUrl = URL.createObjectURL(selectedFile);
            setFile(fileUrl);
            formik.setFieldValue('image', fileUrl);
        }
    };

    const handleSubmit = (values: {
        name?: string;
        image?: string;
        employeeId?: number;
        department?: string;
        date?: string | number | Date;
        employeeInformation?: string;
    }) => {
        const newEmployee: EmployeeTableData = {
            id: values.employeeId,
            name: values.name || '',
            status: 'Active',
        };
        const added = addEmployee(newEmployee);
        if (added) {
            formik.resetForm();
            setFile(null);
        }
        // navigate('/employees');
    }
    console.log(successfullModal)

    const successfullyAdded = () => {
        setSuccessfullModal(false)
        navigate('/employees')
        window.scrollTo(0, 0);
        document.body.style.overflow = "auto"
    }

    const formik = useFormik({
        initialValues: {
            name: "",
            date: "",
            image: "",
            employeeId: undefined,
            department: "",
            employeeInformation: "",
        },
        validationSchema: formSchema,
        onSubmit: handleSubmit,
    });
    return (
        <>
            <form onSubmit={formik.handleSubmit} noValidate className="mt-6 flex flex-col gap-[38px]">
                <div>
                    <p className="font-urbanist font-medium text-[21px] leading-[180%] text-[#FFFFFF99] mb-[38px]">
                        Image, Video, Audio, or 3D Model. File types supported: JPG, PNG, GIF, SVG, MP4, WEBM, MP3, WAV, OGG, GLB, GLTF. Max size: 100 MB
                    </p>
                    <div>
                        <label className={`${labelStyles}`}>Upload File</label>
                        <ImageButton type="button" onClick={handleClick} buttonClasses="mt-3.5 border border-dashed border-[#747681] w-full max-w-[484px] min-h-[484px] flex items-center justify-center">
                            {file ? (
                                <img
                                    src={file}
                                    alt="Uploaded preview"
                                    className="w-[145px] h-[145px] object-cover rounded-full"
                                />
                            ) : (
                                <img
                                    src={uploadImg}
                                    alt="profile"
                                    className="w-[145px] h-[145px] object-cover rounded-full"
                                />
                            )}

                            <input
                                type="file"
                                accept="image/*"
                                ref={fileInputRef}
                                style={{ display: "none" }}
                                onChange={handleFileChange}
                            />
                        </ImageButton>
                    </div>

                </div>
                <div className="relative">
                    <FormInput id="name"
                        name="name"
                        placeholder="Name"
                        onChange={formik.handleChange}
                        value={formik.values.name} label="Name" labelClassName={`${labelStyles}`} type="text" inputMainBorder={`${inputBorder}`} inputClassName={`${inputStyles}`} />

                    {formik.errors.name && formik.touched.name && (
                        <p className={`${errorClasses}`}>
                            {formik.errors.name}
                        </p>
                    )}
                </div>
                <div className="relative">
                    <FormInput label="Id"
                        type="number"
                        id="employeeId"
                        name="employeeId"
                        value={formik.values.employeeId}
                        onChange={(e) => {
                            formik.handleChange(e);
                            clearError();
                        }}
                        placeholder="Employee ID" labelClassName={`${labelStyles}`} inputMainBorder={`${inputBorder}`} inputClassName={`${inputStyles}`} />
                    {formik.errors.employeeId && formik.touched.employeeId && (
                        <p className={`${errorClasses}`}>
                            {formik.errors.employeeId}
                        </p>
                    )}
                    {idExistError && (
                        <p className={`${errorClasses}`}>
                            {idExistError}
                        </p>
                    )}
                </div>
                <div className="relative">
                    <FormInput label="Department" id="department" name="department" value={formik.values.department} onChange={formik.handleChange} placeholder="Department" labelClassName={`${labelStyles}`} type="text" inputMainBorder={`${inputBorder}`} inputClassName={`${inputStyles}`} />
                    {formik.errors.department && formik.touched.department && (
                        <p className={`${errorClasses}`}>
                            {formik.errors.department}
                        </p>
                    )}
                </div>
                <div className="relative">
                    <FormInput label="Date" id="date" name="date" value={formik.values.date} onChange={formik.handleChange} placeholder="Date" labelClassName={`${labelStyles}`} type="date" inputMainBorder={`${inputBorder}`} inputClassName={`${inputStyles}`} />
                    {formik.errors.date && formik.touched.date && (
                        <p className={`${errorClasses}`}>
                            {formik.errors.date}
                        </p>
                    )}
                </div>
                <div className="relative">
                    <label className={`${labelStyles}`}>Description</label>
                    <div className={`${inputBorder} h-[253px]`}>
                        <textarea id="employeeInformation" name="employeeInformation" value={formik.values.employeeInformation} onChange={formik.handleChange} placeholder="Employee Information..." className={`${inputStyles} h-full w-full outline-none`} />
                    </div>
                    {formik.errors.employeeInformation && formik.touched.employeeInformation && (
                        <p className={`${errorClasses}`}>
                            {formik.errors.employeeInformation}
                        </p>
                    )}
                </div>
                <Button type="submit" buttonClasses="border border-[#CDD6D7] border-solid bg-[#283573] py-5 px-[75px] rounded-[15px] mt-[58px] text-2xl font-semibold leading-[160%] font-urbanist text-white w-fit">
                    Register
                </Button>
            </form>
            {successfullModal &&
                <SuccessfullModal modalClassName="" modalMain="" successfullOk={successfullyAdded}>
                  Successfully Registered your Employee.
                </SuccessfullModal>
            }
        </>
    )
}

export default Form
