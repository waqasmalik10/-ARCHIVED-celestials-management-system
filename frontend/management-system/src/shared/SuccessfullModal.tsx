// src/components/SuccessfullModal.tsx

import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';

interface SuccessfullModalModalProps {
  modalClassName?: string;
  children: React.ReactNode;
  modalMain?: string;
  onClick?: () => void;
  successfullOk?: () => void;
}

const SuccessfullModal = React.forwardRef<HTMLDivElement, SuccessfullModalModalProps>(({
  modalClassName,
  modalMain,
  children,
  onClick,
  successfullOk,
  ...props
}, ref) => {
  const modalRoot = document.getElementById('modal-root');

  const [show, setShow] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShow(true), 600);
    return () => clearTimeout(timer);
  }, []);

  if (!modalRoot) return null;

  return ReactDOM.createPortal(
    <div
      onClick={onClick}
      className={`h-screen flex justify-center items-center bg-[#5558948f] px-4 bg-cover z-[999999] fixed top-0 left-0 w-full backdrop-blur-[7px] ${modalMain}`}
      {...props}
    >
      <div
        ref={ref}
        className={`min-w-[500px] relative rounded-[15px] modal-sketch-wrapper ${modalClassName}`}
      >
        <svg className="modal-sketch-svg" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
          <rect x="0" y="0" width="100%" height="100%" rx="15" ry="15" />
        </svg>

        <div className="modal-sketch-content">
          <h1 className="text-2xl font-semibold leading-normal text-center font-poppins text-white sketch-content-title">
            {children}
          </h1>

          <button
            type="button"
            onClick={successfullOk}
            className="py-2.5 px-4 bg-[#259DA8] rounded-[12px] h-12 w-full font-inter font-medium text-base leading-7 text-white mt-8"
            style={{ animation: show ? 'modalContentFadeIn 0.6s ease forwards' : 'none', animationDelay: '0.4s' }}
          >
            OK
          </button>
        </div>
      </div>
    </div>,
    modalRoot
  );
});

export default SuccessfullModal;
