import { useContext, useRef, useState } from "react";
import profileIcon from "../../assets/images/profileIcon.svg";
import { ThemeContext } from "../../app/ThemeContext";
import Button from "../../shared/Button";

interface SettingBodyProps {
  superAdmin?: boolean;
  name?: string;
  email?: string;
}

export default function SettingBody({
  name,
  email,
}: SettingBodyProps) {
  const context = useContext(ThemeContext);
  const { theme, toggleTheme } = context;
  const [file, setFile] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
    }
  };

  return (
    <>
      <div className="flex flex-col gap-3 text-white">
        <p className="w-full p-7 bg-[#1E2C6D] dark:bg-[#383838]  text-3xl">Profile Image:</p>
        <div className="flex gap-10 flex-wrap items-center">
          {file ? (
            <img
              src={file}
              alt="Uploaded preview"
              className="mt-2 w-40 h-40 object-cover rounded-full"
            />
          ) : (
            <img
              src={profileIcon}
              alt="profile"
              className="mt-2 w-40 h-40 object-cover rounded-full"
            />
          )}

          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
          <div className="flex flex-wrap gap-2">
            <Button
              buttonClasses="buttonColor px-5 py-4 pb-5 rounded-[10px] text-white text-xl font-inter font-medium leading-[17px] text-center"
              onClick={handleClick}
            >
              Change Image
            </Button>
            <Button buttonClasses="buttonColor px-5 py-4 pb-5 rounded-[10px] text-white text-xl font-inter font-medium leading-[17px] text-center">
              Save
            </Button>
          </div>
        </div>
      </div>
      <div className="flex lg:flex-row flex-col gap-5 lg:gap-3 mt-6">
        <div className="w-full lg:w-1/2 flex flex-col gap-3 text-white">
          <p className="w-full p-7 bg-[#1E2C6D] dark:bg-[#383838]  text-3xl">Your Name:</p>
          <h1 className="text-2xl mt-4 px-7 capitalize">{name}</h1>
        </div>
        <div className="w-full lg:w-1/2 flex flex-col gap-3 text-white">
          <p className="w-full p-7 bg-[#1E2C6D] dark:bg-[#383838]  text-3xl">Your Email:</p>
          <h1 className="text-2xl mt-4 px-7">{email}</h1>
        </div>
      </div>
      <div className="mt-10">
        <Button
          buttonClasses="bg-[#1E2C6D] dark:bg-[#383838]  dark:bg-black  px-5 py-4 pt-4.5 rounded-[10px] text-white text-xl font-inter font-medium leading-[17px] text-center"
          onClick={toggleTheme}
        >
          {theme === "light" ? "Switch to Dark" : "Switch to Light"}
        </Button>
      </div>
    </>
  );
}
